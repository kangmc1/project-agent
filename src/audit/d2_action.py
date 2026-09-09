"""D2 — tool-use failure, procedural (user's definition, 2026-09-09 07:00).

D2 = ACTION GROUNDING: is this action (tool call) one the record required and allowed? For every non-aux step the module
returns 1 if ANY of the following holds, else 0 (user's definition, 2026-09-09 07:55):
  (1) missing_tool      : the subagent ended its handoff without calling a tool family the planner's instruction required
                          (d2_required_calls.jsonl, scored at the report step)
  (2) fabricated_arg    : a tool call at this step carries an identifier-like argument value the agent was never given
                          (d2_argument_grounding.jsonl)
  (3') tool_call_failed : a tool call at this step returned an error, EXCLUDING file tools (a first read_file of the
                          not-yet-created case-notes file fails by design) and wrapper rows (subagent-level errors are
                          judged inside the subagent's own steps). Mostly the symptom of (2): a call made with values the
                          record never supplied. (d3.jsonl check "error")
Not in D2: the utterance->required-tool rule (utterance layer), and the empty/schema/repeat/ignored log checks
("result handling" cannot be judged from the log stream). `tool_error` (all errors) stays as a descriptive field. Output: audit/d2_action.jsonl  Usage: python -m src.audit.d2_action
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

AUDIT = Path("audit")
AUX = {"user_sim", "summarizer"}
BENIGN_ERROR_TOOLS = {"read_file", "write_file", "edit_file", "ls", "glob", "grep", "policy_checker", "db_agent", "solver", "verifier"}


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
                                                "missing_tool": False, "fabricated_arg": False, "tool_error": False, "tool_call_failed": False, "missing_identifier": False, "reissued_after_failure": False, "evidence": [], "tool_error_evidence": []}
    for r in _rows("d2_required_calls.jsonl"):
        k = (r["run_id"], r["step_id"])
        if k in steps and r.get("applicable") and r.get("satisfied") is False:
            steps[k]["missing_tool"] = True
            steps[k]["evidence"].append("required but never called: " + ", ".join("/".join(m["tools"]) for m in r["missing"]))
    for r in _rows("d2_argument_grounding.jsonl"):
        k = (r["run_id"], r["step_id"])
        if k in steps and r.get("n_ungrounded", 0) > 0:
            steps[k]["fabricated_arg"] = True
            steps[k]["evidence"].append("argument never given: " + ", ".join(f"{u['tool']}.{u['kind']}={u['value']}" for u in r["ungrounded"][:4]))
    for r in _rows("d2_delegation.jsonl"):  # planner-side conditions (a)(b)
        k = (r["run_id"], r["step_id"])
        if k in steps:
            steps[k]["missing_identifier"] = bool(r.get("missing_identifier"))
            steps[k]["reissued_after_failure"] = bool(r.get("reissued_after_failure"))
            steps[k]["evidence"] += list(r.get("evidence") or [])
    for r in _rows("d2_tool_log.jsonl"):
        k = (r["run_id"], r["step_id"])
        if k in steps and r.get("kind") == "tool_call" and (r.get("checks") or {}).get("error"):
            steps[k]["tool_error"] = True  # descriptive: any error
            steps[k]["tool_error_evidence"].append(f"tool {r.get('tool')} returned an error")
            if r.get("tool") not in BENIGN_ERROR_TOOLS:
                steps[k]["tool_call_failed"] = True  # condition (3')
                steps[k]["evidence"].append(f"call failed: {r.get('tool')} returned an error")
    n = 0
    with (AUDIT / "d2_action.jsonl").open("w", encoding="utf-8") as f:
        for k in sorted(steps):
            s = steps[k]
            s["d3"] = 1 if (s["missing_tool"] or s["fabricated_arg"] or s["tool_call_failed"] or s["missing_identifier"] or s["reissued_after_failure"]) else 0
            n += s["d3"]
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    print(f"D2 final: {len(steps)} steps, flagged {n} "
          f"(missing_tool {sum(s['missing_tool'] for s in steps.values())}, fabricated_arg {sum(s['fabricated_arg'] for s in steps.values())}, tool_call_failed {sum(s['tool_call_failed'] for s in steps.values())}, planner missing_identifier {sum(s['missing_identifier'] for s in steps.values())}, planner reissued_after_failure {sum(s['reissued_after_failure'] for s in steps.values())})")


if __name__ == "__main__":
    main()
