"""P2 / P2b validation of a run directory.  Usage: python -m src.harness.validate runs/<run_id> [...]"""
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

WRAPPER_NAMES = {"policy_checker", "db_agent", "solver", "verifier"}
AUX_AGENTS = {"user_sim", "summarizer"}


def load_steps(run_dir: Path) -> list[dict]:
    p = run_dir / "steps.jsonl"
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def validate(run_dir: Path) -> dict:
    steps = load_steps(run_dir)
    meta = json.loads((run_dir / "meta.json").read_text()) if (run_dir / "meta.json").exists() else {}
    res: dict[str, object] = {"run": run_dir.name, "n_steps": len(steps)}
    checks: dict[str, bool] = {}

    checks["steps_exist"] = len(steps) >= 3
    checks["required_fields"] = all(
        s.get("request", {}).get("messages") is not None and "tools" in s.get("request", {})
        and s.get("agent") and "tool_calls" in s.get("response", {}) and "logprobs" in s.get("response", {})
        and "finish_reason" in s.get("response", {}) for s in steps
    ) if steps else False
    checks["sqlite_exists"] = (run_dir / "tool_calls.sqlite").exists()
    checks["fs_snapshots"] = any((run_dir / "fs").glob("step_*.json"))
    checks["meta_status"] = meta.get("status") in {"ok", "exception", "timeout"} and "success" in meta

    chat_steps = [s for s in steps if s["agent"] not in AUX_AGENTS]
    checks["no_length_cutoff"] = all(s["response"].get("finish_reason") != "length" for s in chat_steps)
    expected = meta.get("chat_model_starts")
    checks["step_count_matches_callbacks"] = (expected is None) or (len(chat_steps) == expected)
    res["chat_steps"] = len(chat_steps)
    res["chat_model_starts"] = expected

    planner = [s for s in chat_steps if s["agent"] == "planner"]
    # the last planner step is the designed final answer (no tool call) -> excluded from the ratio
    planner_body = planner[:-1] if len(planner) > 1 else planner
    tool_led = sum(1 for s in planner_body if s["response"].get("tool_calls"))
    res["planner_tool_call_ratio"] = (tool_led / len(planner_body)) if planner_body else None
    checks["planner_tool_ratio_ge_0_9"] = (res["planner_tool_call_ratio"] or 0) >= 0.9 if planner else False

    agents = {s["agent"] for s in steps}
    res["agents"] = sorted(agents)
    checks["subagents_tagged"] = bool(agents & WRAPPER_NAMES)
    if meta.get("domain") == "airline":
        checks["user_sim_tagged"] = "user_sim" in agents
        # shared FS: case_notes.md written by a subagent must appear in a later planner-visible snapshot
        seen = False
        for f in sorted((run_dir / "fs").glob("step_*.json"), key=lambda p: int(p.stem.split("_")[1])):
            d = json.loads(f.read_text())
            if any("case_notes" in k for k in (d.get("files") or {})):
                seen = True
                break
        checks["shared_fs_case_notes"] = seen

    res["checks"] = checks
    res["pass"] = all(checks.values())
    return res


def main(argv: list[str]) -> int:
    ok = True
    for a in argv:
        r = validate(Path(a))
        print(json.dumps(r, ensure_ascii=False, indent=1))
        ok &= bool(r["pass"])
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
