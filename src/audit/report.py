"""P4b — per-trace audit report: audit/report/<run_id>.json and .md (flags per item with evidence; no fused score).

Usage: python -m src.audit.report [--runs runs] [--percentile 10]
Thresholds for *flagging* are label-free percentiles of each item's own score distribution (per role) across all
scored steps; the report lists every flag with the evidence pointer produced by the module.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

AUDIT = Path("audit")
AUX = {"user_sim", "summarizer"}


def _load(name: str) -> list[dict]:
    p = AUDIT / name
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def _pct(values: list[float], q: float) -> float | None:
    if not values:
        return None
    v = sorted(values)
    k = min(len(v) - 1, max(0, int(round(q * (len(v) - 1)))))
    return v[k]


def build(percentile: int = 10) -> dict[str, dict]:
    d1, d3, d7, d3a = (_load(f) for f in ("d1.jsonl", "d3.jsonl", "d7.jsonl", "d3_args.jsonl"))
    q = 1 - percentile / 100
    # label-free thresholds per role
    thr_d1 = {role: _pct([1 - r["confidence"] for r in d1 if r["role"] == role], q) for role in ("planner", "subagent")}
    thr_d1_h = _pct([r["layer2"]["H2"] for r in d1 if r["role"] == "planner"], q)
    thr_d7 = _pct([1 - r["fidelity"] for r in d7 if r.get("fidelity") is not None], q)

    reports: dict[str, dict] = defaultdict(lambda: {"flags": [], "per_module_summary": {}, "coverage": {}})
    for r in d1:
        rep = reports[r["run_id"]]
        rep["per_module_summary"].setdefault("D1", {"n_scored": 0, "method": r["method"]})["n_scored"] += 1
        inst = 1 - r["confidence"]
        t = thr_d1.get(r["role"])
        if t is not None and inst >= t:
            top = sorted(r["dist"].items(), key=lambda kv: -kv[1])[:3]
            rep["flags"].append({"step": r["step_id"], "agent": r["agent"], "module": "D1", "layer": "tool",
                                 "signal": {"confidence": round(r["confidence"], 3), "p_actual": round(r["p_actual"], 3), "margin": round(r["margin"], 3)},
                                 "evidence": "action distribution: " + ", ".join(f"{a} {p:.2f}" for a, p in top) + f" (actual: {r['actual']})"})
        if r["role"] == "planner" and thr_d1_h is not None and r["layer2"]["H2"] >= thr_d1_h and r["layer2"]["H2"] > 0:
            rep["flags"].append({"step": r["step_id"], "agent": r["agent"], "module": "D1", "layer": "handoff",
                                 "signal": {"p_delegate": round(r["layer2"]["p_delegate"], 3), "H2": round(r["layer2"]["H2"], 3)},
                                 "evidence": f"delegate-vs-not split p_delegate={r['layer2']['p_delegate']:.2f}"})
    for r in d3:
        rep = reports[r["run_id"]]
        s = rep["per_module_summary"].setdefault("D3", {"tool_calls": 0, "utterances": 0, "checks": defaultdict(int)})
        if r["kind"] == "tool_call":
            s["tool_calls"] += 1
            fired = [k for k, v in r["checks"].items() if v]
            for k in fired:
                s["checks"][k] += 1
            if fired:
                rep["flags"].append({"step": r["step_id"], "agent": r["agent"], "module": "D3", "signal": {"checks": fired, "tool": r["tool"]},
                                     "evidence": f"tool {r['tool']} call #{r['call_id']}: " + ", ".join(fired) + (f"; schema: {r['schema_errors']}" if r.get("schema_errors") else "")})
        else:
            s["utterances"] += 1
            if not r["satisfied"]:
                rep["flags"].append({"step": r["step_id"], "agent": r["agent"], "module": "D3", "signal": {"satisfied": False},
                                     "evidence": "claims without prior tool evidence: " + ", ".join(f"{m['type']}={m['value']}" for m in r["missing"][:5])})
    for r in d7:
        rep = reports[r["run_id"]]
        s = rep["per_module_summary"].setdefault("D7", {"n_handoffs": 0})
        s["n_handoffs"] += 1
        if r.get("fidelity") is not None and thr_d7 is not None and (1 - r["fidelity"]) >= thr_d7 and r["fidelity"] < 1:
            rep["flags"].append({"step": r["planner_step_id"], "agent": "planner", "module": "D7", "direction": r["direction"],
                                 "signal": {"fidelity": r["fidelity"], "missing": r["missing"][:5], "altered": r["altered"]},
                                 "evidence": f"{r['wrapper']} {r['direction']}: missing {r['missing'][:3]} altered {list(r['altered'])[:3]}"})
    for r in d3a:  # D3 rule 3: fabricated identifier-like tool-call arguments
        rep = reports[r["run_id"]]
        s = rep["per_module_summary"].setdefault("D3_args", {"n_steps": 0, "n_values": 0, "n_ungrounded": 0})
        s["n_steps"] += 1; s["n_values"] += r["n_values"]; s["n_ungrounded"] += r["n_ungrounded"]
        if r["n_ungrounded"] > 0:
            rep["flags"].append({"step": r["step_id"], "agent": r["agent"], "module": "D3", "layer": "arguments",
                                 "signal": {"ungrounded_ratio": round(r["ungrounded_ratio"], 3)},
                                 "evidence": "argument values never given to the agent: " + ", ".join(f"{u['tool']}.{u['kind']}={u['value']}" for u in r["ungrounded"][:5])})
    for rid, rep in reports.items():
        rep["run_id"] = rid
        rep["flags"].sort(key=lambda f: (f["step"], f["module"]))
        rep["thresholds"] = {"percentile": percentile, "D1": thr_d1, "D1_handoff": thr_d1_h, "D7": thr_d7, "D3_args": "any ungrounded value"}
        for k, v in rep["per_module_summary"].items():
            if isinstance(v, dict) and "checks" in v:
                v["checks"] = dict(v["checks"])
    return reports


def to_md(rep: dict) -> str:
    lines = [f"# Audit report — {rep['run_id']}", "", "| step | agent | module | signal | evidence |", "|---|---|---|---|---|"]
    for f in rep["flags"]:
        lines.append(f"| {f['step']} | {f['agent']} | {f['module']}{'/' + f['layer'] if f.get('layer') else ''}{'/' + f['direction'] if f.get('direction') else ''} | {json.dumps(f['signal'], ensure_ascii=False)} | {f['evidence']} |")
    lines += ["", "## Per-module summary", "```", json.dumps(rep["per_module_summary"], ensure_ascii=False, indent=1), "```",
              "", f"Thresholds (label-free, top {rep['thresholds']['percentile']}% per item): `{json.dumps(rep['thresholds'], default=str)}`"]
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--percentile", type=int, default=10)
    a = ap.parse_args()
    out = AUDIT / "report"
    out.mkdir(parents=True, exist_ok=True)
    reps = build(a.percentile)
    for rid, rep in reps.items():
        (out / f"{rid}.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
        (out / f"{rid}.md").write_text(to_md(rep), encoding="utf-8")
    print(f"reports: {len(reps)} -> {out}/ ; total flags = {sum(len(r['flags']) for r in reps.values())}")


if __name__ == "__main__":
    main()
