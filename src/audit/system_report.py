"""P4c — system-level (per domain / agent role / handoff edge) stability aggregate, label-free.

Usage: python -m src.audit.system_report [--percentile 10]  -> audit/system_report.{md,json}
"""
from __future__ import annotations

import argparse
import csv
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path

from .report import _load, _pct

AUDIT = Path("audit")
WRAPPERS = {"policy_checker", "db_agent", "solver", "verifier"}


def build(percentile: int = 10) -> dict:
    d1, d3, d7, d3a = (_load(f) for f in ("d1.jsonl", "d3.jsonl", "d7.jsonl", "d3_args.jsonl"))
    q = 1 - percentile / 100
    index = {}
    if Path("runs/index.csv").exists():
        for row in csv.DictReader(open("runs/index.csv")):
            index[row["run_id"]] = row
    domains = sorted({r["domain"] for r in d1} | {r["domain"] for r in d3})
    out: dict = {"percentile": percentile, "domains": {}}
    for dom in domains:
        D1 = [r for r in d1 if r["domain"] == dom]
        D3A = [r for r in d3a if r["domain"] == dom]
        D3 = [r for r in d3 if r["domain"] == dom]
        D7 = [r for r in d7 if r["domain"] == dom]
        runs = sorted({r["run_id"] for r in D1 + D3})
        succ = [index[r]["success"] == "True" for r in runs if r in index and index[r]["status"] == "ok"]
        dom_out = {"n_runs": len(runs), "success_rate*": (sum(succ) / len(succ)) if succ else None, "agents": {}, "handoff_edges": {}, "hotspots": [], "confidence_curve": {}}
        agents = sorted({r["agent"] for r in D1} | {r["agent"] for r in D3 if r["kind"] == "tool_call"})
        thr_d1 = {role: _pct([1 - r["confidence"] for r in D1 if r["role"] == role], q) for role in ("planner", "subagent")}
        thr_h = _pct([r["layer2"]["H2"] for r in D1 if r["role"] == "planner"], q)
        for ag in agents:
            a1 = [r for r in D1 if r["agent"] == ag]
            a2 = [r for r in D3A if r["agent"] == ag]
            a3 = [r for r in D3 if r["agent"] == ag and r["kind"] == "tool_call"]
            role = "planner" if ag == "planner" else "subagent"
            t = thr_d1.get(role)
            checks = Counter()
            for r in a3:
                for k, v in r["checks"].items():
                    checks[k] += int(v)
            dom_out["agents"][ag] = {
                "decisions": len(a1),
                "low_confidence_ratio": (sum(1 for r in a1 if t is not None and 1 - r["confidence"] >= t) / len(a1)) if a1 else None,
                "mean_confidence": statistics.fmean(r["confidence"] for r in a1) if a1 else None,
                "handoff_layer_low_ratio": (sum(1 for r in a1 if thr_h is not None and r["layer2"]["H2"] >= thr_h and r["layer2"]["H2"] > 0) / len(a1)) if (a1 and role == "planner") else None,
                "ungrounded_arg_ratio": (sum(1 for r in a2 if r["n_ungrounded"] > 0) / len(a2)) if a2 else None,
                "tool_calls": len(a3),
                "tool_check_ratios": {k: (checks[k] / len(a3)) if a3 else None for k in ("error", "empty", "repeat", "schema", "ignored")},
            }
        edges = defaultdict(list)
        for r in D7:
            edges[(r["wrapper"], r["direction"])].append(r)
        for (w, d), rows in edges.items():
            fids = [r["fidelity"] for r in rows if r.get("fidelity") is not None]
            miss = Counter(k for r in rows for k in r.get("missing", []))
            alt = Counter(k for r in rows for k in (r.get("altered") or {}))
            dom_out["handoff_edges"][f"{w}:{d}"] = {"n": len(rows), "mean_fidelity": statistics.fmean(fids) if fids else None,
                                                    "low_fidelity_ratio(<0.8)": (sum(1 for f in fids if f < 0.8) / len(fids)) if fids else None,
                                                    "top_missing_keys": miss.most_common(3), "top_altered_keys": alt.most_common(3)}
        hot = Counter()
        for r in D3:
            if r["kind"] == "tool_call":
                for k, v in r["checks"].items():
                    if v:
                        hot[f"{r['agent']}: {r['tool']} {k}"] += 1
            elif not r["satisfied"]:
                for m in r["missing"]:
                    hot[f"{r['agent']}: claim {m['type']} without tool evidence"] += 1
        for (w, d), rows in edges.items():
            for r in rows:
                for k in (r.get("altered") or {}):
                    hot[f"{w} {d}: '{k}' altered"] += 1
        dom_out["hotspots"] = hot.most_common(5)
        # confidence by decision index (per run), averaged
        by_idx = defaultdict(list)
        per_run = defaultdict(list)
        for r in sorted(D1, key=lambda r: (r["run_id"], r["step_id"])):
            per_run[r["run_id"]].append(r["confidence"])
        for vals in per_run.values():
            for i, c in enumerate(vals):
                by_idx[min(i // 5, 5)].append(c)
        dom_out["confidence_curve"] = {f"decisions {k*5}-{k*5+4}" if k < 5 else "decisions 25+": statistics.fmean(v) for k, v in sorted(by_idx.items())}
        out["domains"][dom] = dom_out
    return out


def to_md(rep: dict) -> str:
    L = ["# System stability report (label-free)", "", f"Flag thresholds = top {rep['percentile']}% of each item's own distribution (per role). `success_rate*` uses ground truth and is shown for reference only.", ""]
    for dom, d in rep["domains"].items():
        L += [f"## {dom} — {d['n_runs']} runs, success_rate* = {d['success_rate*']}", "", "### Agents", "",
              "| agent | decisions | mean conf | low-conf ratio | handoff-layer low | ungrounded-arg ratio | tool calls | error | empty | repeat | schema | ignored |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for ag, a in d["agents"].items():
            f = lambda x: "-" if x is None else f"{x:.2f}"
            tc = a["tool_check_ratios"]
            L.append(f"| {ag} | {a['decisions']} | {f(a['mean_confidence'])} | {f(a['low_confidence_ratio'])} | {f(a['handoff_layer_low_ratio'])} | {f(a['ungrounded_arg_ratio'])} | {a['tool_calls']} | {f(tc['error'])} | {f(tc['empty'])} | {f(tc['repeat'])} | {f(tc['schema'])} | {f(tc['ignored'])} |")
        L += ["", "### Handoff edges", "", "| edge | n | mean fidelity | low(<0.8) ratio | top missing | top altered |", "|---|---|---|---|---|---|"]
        for e, v in d["handoff_edges"].items():
            f = lambda x: "-" if x is None else f"{x:.2f}"
            L.append(f"| {e} | {v['n']} | {f(v['mean_fidelity'])} | {f(v['low_fidelity_ratio(<0.8)'])} | {v['top_missing_keys']} | {v['top_altered_keys']} |")
        L += ["", "### Hotspots (top 5)", ""] + [f"- {h[0]} — {h[1]}" for h in d["hotspots"]] + ["", "### Confidence by decision index", "", json.dumps(d["confidence_curve"], indent=1)]
        L.append("")
    return "\n".join(L)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--percentile", type=int, default=10)
    a = ap.parse_args()
    rep = build(a.percentile)
    (AUDIT / "system_report.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    (AUDIT / "system_report.md").write_text(to_md(rep), encoding="utf-8")
    print("system report written for domains:", list(rep["domains"]))


if __name__ == "__main__":
    main()
