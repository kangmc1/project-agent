"""Render handoff events into compact text for prompts, under a character budget.

Priority when truncating: task + team + latest fact sheet/plan + most recent reports first;
older reports are truncated from the front. Truncation is recorded so that detector
accuracy can later be analysed as a function of how much context was dropped.
"""
from __future__ import annotations

import json
import re
from typing import Any

TASK_RE = re.compile(r"# Task\s*(.*?)(?=\n# Important Constraint|\n# Output format|\n\nTo answer this request|\Z)", re.S)


def _msg_text(m: dict) -> str:
    c = m.get("content")
    if isinstance(c, str):
        return c
    if isinstance(c, list):  # multimodal parts
        return "\n".join(p.get("text", "") for p in c if isinstance(p, dict) and p.get("type") == "text")
    return json.dumps(c, ensure_ascii=False)


def _trim(s: str, n: int, where: str = "tail") -> str:
    if len(s) <= n:
        return s
    if where == "head":
        return "…[truncated " + str(len(s) - n) + " chars]…" + s[-n:]
    return s[:n] + "…[truncated " + str(len(s) - n) + " chars]…"


def render_transcript(messages: list[dict], budget: int, per_msg: int = 1500) -> tuple[str, dict]:
    """Render a Magentic-One shared transcript. messages[0] = task+team(+facts+plan)."""
    if not messages:
        return "", {"dropped_msgs": 0, "kept_msgs": 0}
    head = _msg_text(messages[0])
    rest = messages[1:]
    lines = []
    for m in rest:
        role = m.get("role", "?")
        lines.append(f"[{role}]\n{_trim(_msg_text(m), per_msg)}")
    # keep the most recent messages that fit
    kept, used = [], 0
    for ln in reversed(lines):
        if used + len(ln) > budget:
            break
        kept.append(ln); used += len(ln)
    kept.reverse()
    stats = {"dropped_msgs": len(lines) - len(kept), "kept_msgs": len(kept), "total_msgs": len(lines)}
    body = "\n\n".join(kept)
    if stats["dropped_msgs"]:
        body = f"…[{stats['dropped_msgs']} earlier messages omitted]…\n\n" + body
    return head + "\n\n=== TRANSCRIPT ===\n" + body, stats


def render_instruction_handoff(h: dict[str, Any], budget: int = 24000) -> dict[str, Any]:
    ctx, stats = render_transcript(h["sender_context"][:-1], budget)  # last msg is the ledger prompt itself
    artifact = f"NEXT SPEAKER: {h['receiver']}\nINSTRUCTION: {h['instruction']}\nREASON: {h.get('instruction_reason','')}"
    beh = []
    for st in h.get("receiver_steps", []):
        for tc in st.get("tool_calls", []):
            beh.append(f"[{st['agent_name']} tool_call] {tc['name']}({_trim(tc['arguments'], 600)})")
        if st.get("content"):
            beh.append(f"[{st['agent_name']} says] {_trim(st['content'], 1500)}")
    for m in h.get("receiver_report", []):
        beh.append(f"[{m['role']} report] {_trim(m['content'], 2500)}")
    return {"sender_context": ctx, "artifact": artifact, "receiver_behavior": "\n".join(beh) or "(no receiver activity recorded)",
            "task": h["task_instruction"], "render_stats": stats}


def render_reset_handoff(r: dict[str, Any], budget: int = 24000) -> dict[str, Any]:
    ctx, stats = render_transcript(r["pre_reset_transcript"][:-1], budget)
    # The team restarts from messages[0] of the reset step = task + team + updated fact sheet + new plan.
    # That whole text is the artifact (task constraints are re-shown, so they count as preserved).
    artifact = _trim(r["post_reset_context"], 9000) if r.get("post_reset_context") else ("UPDATED FACT SHEET:\n" + r["facts_text"] + "\n\nNEW PLAN:\n" + _trim(r["plan_text"], 4000))
    beh = []
    for st in r.get("post_reset_steps", [])[:12]:
        for tc in st.get("tool_calls", []):
            beh.append(f"[{st['agent_name']} tool_call] {tc['name']}({_trim(tc['arguments'], 400)})")
        if st.get("content"):
            beh.append(f"[{st['agent_name']} says] {_trim(st['content'], 800)}")
    return {"sender_context": ctx, "artifact": artifact, "receiver_behavior": "\n".join(beh) or "(no post-reset activity recorded)",
            "task": r["task_instruction"], "render_stats": stats}
