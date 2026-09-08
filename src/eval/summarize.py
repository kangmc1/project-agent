"""Write runs/<run_id>/summary.md for each run — a fixed-schema, human-labeling-friendly transcript.

Usage: python -m src.eval.summarize [--runs runs]
"""
from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

UTTER_LIMIT = 500
ARG_LIMIT = 300
RESULT_LIMIT = 300

_SQL_COLS = ["id", "step_id", "agent", "tool", "args_json", "result_json", "status", "latency", "ts"]


def _truncate(s: str | None, n: int) -> str:
    s = s or ""
    return s if len(s) <= n else s[:n] + "…"


def _load_steps(run: Path) -> list[dict]:
    sp = run / "steps.jsonl"
    if not sp.exists():
        return []
    return [json.loads(l) for l in sp.read_text(encoding="utf-8").splitlines() if l.strip()]


def _load_tool_calls(run: Path) -> dict[int, list[dict]]:
    by_step: dict[int, list[dict]] = {}
    db_path = run / "tool_calls.sqlite"
    if not db_path.exists():
        return by_step
    con = sqlite3.connect(str(db_path))
    try:
        for row in con.execute(f"SELECT {', '.join(_SQL_COLS)} FROM tool_calls ORDER BY id"):
            rec = dict(zip(_SQL_COLS, row))
            by_step.setdefault(rec["step_id"], []).append(rec)
    finally:
        con.close()
    return by_step


def _header(meta: dict) -> list[str]:
    result = meta.get("result") or {}
    lines = [
        f"# {meta.get('run_id', '?')}",
        "",
        f"- domain: {meta.get('domain')}",
        f"- task: {meta.get('task')}",
        f"- status: {meta.get('status')}",
        f"- success: {meta.get('success')}",
    ]
    if meta.get("domain") == "aime":
        lines.append(f"- answer (gold): {result.get('answer')}")
        lines.append(f"- submitted: {result.get('submitted')}")
    elif meta.get("domain") == "airline":
        lines.append(f"- reward: {result.get('reward')}")
    lines.append("")
    return lines


def _step_section(s: dict, tool_calls_by_step: dict[int, list[dict]]) -> list[str]:
    agent = s.get("agent")
    step_id = s.get("step_id")
    lines = [f"### step {step_id} — {agent}", ""]

    if agent == "summarizer":
        lines += ["(context summarized here)", ""]
        return lines

    content = (s.get("response") or {}).get("content") or ""
    if agent == "user_sim":
        if content:
            lines.append(f"[customer]: {_truncate(content, UTTER_LIMIT)}")
            lines.append("")
        return lines

    if content:
        lines.append(_truncate(content, UTTER_LIMIT))
        lines.append("")
    for tc in ((s.get("response") or {}).get("tool_calls") or []):
        fn = tc.get("function") or {}
        lines.append(f"- tool_call: `{fn.get('name', '?')}({_truncate(fn.get('arguments'), ARG_LIMIT)})`")
    for tc in tool_calls_by_step.get(step_id, []):
        lines.append(f"  result ({tc.get('tool')}, {tc.get('status')}): {_truncate(tc.get('result_json'), RESULT_LIMIT)}")
    lines.append("")
    return lines


def write_summary(run: Path) -> Path | None:
    meta_path = run / "meta.json"
    if not meta_path.exists():
        return None
    meta = json.loads(meta_path.read_text())
    steps = sorted(_load_steps(run), key=lambda s: s["step_id"])
    tool_calls_by_step = _load_tool_calls(run)

    lines = _header(meta)
    for s in steps:
        lines += _step_section(s, tool_calls_by_step)
    lines.append("## Final outcome")
    lines.append(f"status={meta.get('status')} success={meta.get('success')}")

    out_path = run / "summary.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default="runs")
    a = ap.parse_args()
    n = 0
    for run in sorted(Path(a.runs).glob("*/")):
        if write_summary(run) is not None:
            n += 1
    print(f"wrote {n} summaries")


if __name__ == "__main__":
    main()
