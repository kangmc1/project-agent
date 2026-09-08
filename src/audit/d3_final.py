"""D3 — tool-use failure, procedural (user's definition, 2026-09-09 07:00).

For every non-aux step the module returns 1 if EITHER of the following holds, else 0:
  (1) missing_tool   : the subagent ended its handoff without calling a tool family the planner's instruction required
                       (d3_instruction.jsonl, scored at the report step)
  (2) fabricated_arg : a tool call at this step carries an identifier-like argument value the agent was never given
                       (d3_args.jsonl)
The user's definition is exactly (1) OR (2). "Result mishandling" (tool returned an error / ignored / repeated) is NOT part
of the flag: the user judged it ambiguous; `tool_error` is still recorded per step as a descriptive field so the
optional variant (1)∪(2)∪(3) can be reported for comparison, but D3 itself does not use it. Also dropped: the
utterance->required-tool rule (utterance layer) and the empty/schema/repeat/ignored log checks. Output: audit/d3_final.jsonl  Usage: python -m src.audit.d3_final
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

AUDIT = Path("audit")
AUX = {"user_sim", "summarizer"}


def _rows(name):
    p = AUDIT / name
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.exists() else []


def main() -> None:
    steps: dict[tuple[str, int], dict] = {}
    for run in sorted(Path("runs").glob("*/")):
        sp = run / "steps.jsonl"
        if not sp.exists():
            continue
        meta = json.loads((run / "meta.json").read_text()) if (run / "meta.json").exists() else {}
        for l in sp.read_text(encoding="utf-8").splitlines():
            s = json.loads(l)
            if s["agent"] in AUX:
                continue
            steps[(run.name, s["step_id"])] = {"run_id": run.name, "domain": meta.get("domain", run.name.split("_")[0]),
                                                "step_id": s["step_id"], "agent": s["agent"],
                                                "missing_tool": False, "fabricated_arg": False, "tool_error": False, "evidence": [], "tool_error_evidence": []}
    for r in _rows("d3_instruction.jsonl"):
        k = (r["run_id"], r["step_id"])
        if k in steps and r.get("applicable") and r.get("satisfied") is False:
            steps[k]["missing_tool"] = True
            steps[k]["evidence"].append("required but never called: " + ", ".join("/".join(m["tools"]) for m in r["missing"]))
    for r in _rows("d3_args.jsonl"):
        k = (r["run_id"], r["step_id"])
        if k in steps and r.get("n_ungrounded", 0) > 0:
            steps[k]["fabricated_arg"] = True
            steps[k]["evidence"].append("argument never given: " + ", ".join(f"{u['tool']}.{u['kind']}={u['value']}" for u in r["ungrounded"][:4]))
    for r in _rows("d3.jsonl"):
        k = (r["run_id"], r["step_id"])
        if k in steps and r.get("kind") == "tool_call" and (r.get("checks") or {}).get("error"):
            steps[k]["tool_error"] = True  # descriptive only, not in the flag
            steps[k]["tool_error_evidence"].append(f"tool {r.get('tool')} returned an error")
    n = 0
    with (AUDIT / "d3_final.jsonl").open("w", encoding="utf-8") as f:
        for k in sorted(steps):
            s = steps[k]
            s["d3"] = 1 if (s["missing_tool"] or s["fabricated_arg"]) else 0
            n += s["d3"]
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    print(f"D3 final: {len(steps)} steps, flagged {n} "
          f"(missing_tool {sum(s['missing_tool'] for s in steps.values())}, fabricated_arg {sum(s['fabricated_arg'] for s in steps.values())}, tool_error {sum(s['tool_error'] for s in steps.values())})")


if __name__ == "__main__":
    main()
