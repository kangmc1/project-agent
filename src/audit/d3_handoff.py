"""D3 — handoff 정보 손실 (information loss across a handoff boundary), judged by an LLM comparing the two texts directly.

User decision (2026-09-09 11:10): the adopted D3 is the LLM-only version. Against a 60-item information-loss gold
(labels/d3_loss/), direct LLM comparison tracked the gold at least as well as every code route (8B fact extraction + set diff,
raw-text value-token recall) and was better at flagging MATERIAL losses, which are mostly reframings ("parameter error" ->
"system issue", "recorded" -> "processed") that value sets cannot see. Default judge: gpt-oss-20b (best on the gold and not the
executing model's own family). The 8B-extraction route lives on as a comparator in src/audit/comparators/d3_factset.py.

For every handoff (planner wrapper call -> subagent), two boundaries:
  instruction->premise : A = planner's instruction, B = subagent's first message
  report->planner      : A = subagent's final report, B = planner's next message + next tool-call arguments
The judge lists A's concrete facts and marks each preserved / missing / altered in B, then reports fidelity = preserved / facts.
Score used downstream = 1 - fidelity (loss rate). Disk-cached per (model, prompt). Env: LLM_JUDGE_BASE/MODEL/TAG (llm_only.py).
Output: audit/d3_handoff.jsonl (+ d3_handoff_stats.json with --stats)   Usage: python -m src.audit.d3_handoff [--runs runs] [--stats]
"""
from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path

from .extract import map_parallel
from .comparators.d3_factset import _load_run, _load_text, _dedupe_wrapper_rows, _planner_wrapper_calls, _find_planner_step_id
from . import llm_only as L

AUDIT = Path("audit")


def handoff_tasks(run: Path) -> list[dict]:
    steps, calls, meta = _load_run(run)
    domain = meta.get("domain", run.name.split("_")[0])
    pcalls = _planner_wrapper_calls(steps)
    planner_steps = [s for s in steps if s["agent"] == "planner"]
    out = []
    for row in _dedupe_wrapper_rows(calls):
        try:
            args = json.loads(row["args_json"])
        except Exception:
            args = None
        pstep = _find_planner_step_id(pcalls, row["tool"], args, row["step_id"])
        if pstep is None:
            continue
        instruction = (args or {}).get("instruction", "") if isinstance(args, dict) else _load_text(row["args_json"])
        first = next((s for s in steps if s["agent"] == row["tool"] and s["step_id"] > pstep), None)
        premise = (first["response"].get("content") or "") if first else ""
        report = _load_text(row["result_json"])
        nxt = next((s for s in planner_steps if s["step_id"] > row["step_id"]), None)
        b1 = ""
        if nxt is not None:
            b1 = (nxt["response"].get("content") or "") + "\n" + "\n".join(tc["function"].get("arguments", "") for tc in (nxt["response"].get("tool_calls") or []))
        for direction, A, B in (("instruction->premise", instruction, premise), ("report->planner", report, b1)):
            if not str(A).strip():
                continue
            prompt = f"{L._D3}\n\nDomain: {domain}\nBoundary: {row['tool']} {direction}\n\n--- TEXT A ---\n{str(A)[:4000]}\n\n--- TEXT B ---\n{(str(B).strip() or '(empty)')[:4000]}\n\nReturn JSON only."
            out.append({"run_id": run.name, "domain": domain, "handoff_id": row["id"], "planner_step_id": pstep, "wrapper": row["tool"],
                        "direction": direction, "B_empty": not str(B).strip(), "prompt": prompt})
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default="runs")
    ap.add_argument("--stats", action="store_true")
    a = ap.parse_args()
    tasks = []
    for run in sorted(Path(a.runs).glob("*/")):
        if (run / "steps.jsonl").exists() and (run / "tool_calls.sqlite").exists():
            tasks += handoff_tasks(run)
    rows = map_parallel(L.d3_score, tasks)
    for r in rows:
        r["judge"] = L.MODEL
    AUDIT.mkdir(exist_ok=True)
    with (AUDIT / "d3_handoff.jsonl").open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"D3 (LLM {L.MODEL}): boundaries {len(rows)}, parsed {sum(1 for r in rows if r['parsed'])}, mean latency {statistics.mean([r['latency'] for r in rows if r.get('latency')]):.1f}s")
    if a.stats:
        st = {}
        for d in ("instruction->premise", "report->planner"):
            v = [r["fidelity"] for r in rows if r["direction"] == d and r.get("fidelity") is not None]
            st[d] = {"n": len(v), "mean_fidelity": statistics.mean(v) if v else None, "B_empty": sum(1 for r in rows if r["direction"] == d and r["B_empty"])}
        st["judge"] = L.MODEL
        (AUDIT / "d3_handoff_stats.json").write_text(json.dumps(st, indent=1, ensure_ascii=False))
        print(json.dumps(st, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
