"""SWE-smith trajectory source: candidate handoff cut points from coding-agent trajectories.

Each row of the parquet dataset is one agent trajectory attempting a SWE-bench-style
task: a system prompt, a PR-description user turn, then alternating assistant turns
and tool-observation user turns. We treat "after the k-th assistant turn" (for a small
set of k) as a candidate point where the coding agent could hand off to a successor who
must continue the task from the accumulated context.

Observed structure of this dataset (swe_smith_traj_00000.parquet, 3229 rows, inspected
in full): every message dict has exactly the keys {"role", "content"}; "content" is
always a plain string (never a list of content parts); no message ever carries a
"tool_calls" field and no assistant content ever contains a "<function=...>" tag — tool
invocations are embedded as plain text/markdown inside assistant content (e.g. a
```\nstr_replace_editor view ...\n``` block), and tool results arrive as the next
"user" message, always prefixed "OBSERVATION:\n" (or similar) in this dataset, though we
don't rely on that prefix. Roles seen: {"system", "user", "assistant"}. Assistant-turn
counts per row range from 3 to 82+ (median row has ~57 messages total), so cut points at
6/10/14 assistant turns are reachable for the large majority of rows but not all.

We still implement the structured tool_calls path (spec'd below) defensively, in case a
future/other swe-smith shard uses OpenAI-style tool_calls messages.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Callable

import pyarrow.parquet as pq

from handoffcheck.schema import Boundary, context_to_text

DEFAULT_COUNT_TOKENS: Callable[[str], int] = lambda t: max(1, len(t) // 3)

CUT_POINTS: tuple[int, ...] = (6, 10, 14)
TOOL_TRUNCATE_CHARS = 1500
TRUNCATE_MARKER = " …[truncated]"
MIN_FIRST_USER_CHARS = 200

_COLUMNS = ["messages", "instance_id", "resolved", "model", "traj_id"]


def _truncate_tool_content(content: str) -> str:
    text = "[tool_result] " + (content or "")
    if len(text) > TOOL_TRUNCATE_CHARS:
        keep = max(0, TOOL_TRUNCATE_CHARS - len(TRUNCATE_MARKER))
        text = text[:keep] + TRUNCATE_MARKER
    return text


def _tool_call_lines(tool_calls: list) -> list[str]:
    lines = []
    for tc in tool_calls:
        fn = tc.get("function", tc) if isinstance(tc, dict) else {}
        name = fn.get("name", "?")
        arguments = fn.get("arguments", "")
        lines.append(f"[tool_call] {name}({arguments})")
    return lines


def _serialize_messages(raw_messages: list[dict]) -> list[dict]:
    """Map raw {role, content[, tool_calls]} messages onto our {"role", "content"} vocabulary.

    system -> "system"; first user -> "user" (PR description); subsequent user ->
    "tool" (tool observation, prefixed "[tool_result] " and truncated to 1500 chars);
    assistant -> "assistant" (with any structured tool_calls appended as text lines).
    """
    serialized: list[dict] = []
    seen_user = False
    for m in raw_messages:
        role = m.get("role")
        content = m.get("content")
        if not isinstance(content, str):
            content = "" if content is None else str(content)

        if role == "system":
            serialized.append({"role": "system", "content": content})
        elif role == "user":
            if not seen_user:
                seen_user = True
                serialized.append({"role": "user", "content": content})
            else:
                serialized.append({"role": "tool", "content": _truncate_tool_content(content)})
        elif role == "assistant":
            text = content
            tool_calls = m.get("tool_calls")
            if tool_calls:
                lines = _tool_call_lines(tool_calls)
                if lines:
                    text = (text + "\n" if text else "") + "\n".join(lines)
            serialized.append({"role": "assistant", "content": text})
        else:
            serialized.append({"role": role or "?", "content": content})
    return serialized


def _apply_token_cap(
    context: list[dict], count_tokens: Callable[[str], int], max_context_tokens: int
) -> tuple[list[dict], bool, int]:
    """Drop the oldest messages after the first user turn until under the token cap.

    Always keeps the leading system message (if present) and the first user message
    (the PR description) — those two never count against the drop order.
    """
    head = 0
    if context and context[0].get("role") == "system":
        head += 1
    if len(context) > head and context[head].get("role") == "user":
        head += 1

    work = list(context)
    dropped = 0
    while count_tokens(context_to_text(work)) > max_context_tokens and len(work) > head:
        work.pop(head)
        dropped += 1
    truncated = dropped > 0
    return work, truncated, dropped


def _boundaries_for_row(
    row: dict,
    row_index: int,
    count_tokens: Callable[[str], int],
    max_context_tokens: int,
) -> list[Boundary]:
    raw_messages = json.loads(row["messages"])
    if not raw_messages:
        return []

    first_user_content = None
    for m in raw_messages:
        if m.get("role") == "user":
            first_user_content = m.get("content") or ""
            break
    if first_user_content is None or len(first_user_content) < MIN_FIRST_USER_CHARS:
        return []

    serialized = _serialize_messages(raw_messages)
    assistant_indices = [i for i, m in enumerate(serialized) if m["role"] == "assistant"]
    n_assistant_total = len(assistant_indices)

    out: list[Boundary] = []
    for k in CUT_POINTS:
        # need the k-th assistant turn to exist AND at least one more to follow it
        if n_assistant_total <= k:
            continue
        cut_idx = assistant_indices[k - 1]
        context_full = serialized[: cut_idx + 1]
        context, truncated, dropped = _apply_token_cap(context_full, count_tokens, max_context_tokens)

        boundary = Boundary(
            id=f"swe-{row_index}-{k}",
            domain="swe",
            source_ref=f"{row['instance_id']}#assist{k}",
            sender_role="coding agent",
            receiver_role="the next agent who will continue this task",
            context=context,
            message=None,
            meta={
                "row": row_index,
                "instance_id": row["instance_id"],
                "resolved": bool(row["resolved"]),
                "model": row["model"],
                "traj_id": row.get("traj_id"),
                "cut_assistant_turns": k,
                "n_messages_total": len(raw_messages),
                "n_assistant_turns_total": n_assistant_total,
                "n_messages_in_context_full": len(context_full),
                "n_messages_in_context": len(context),
                "truncated": truncated,
                "dropped": dropped,
            },
        )
        out.append(boundary)
    return out


def parse(
    path: str | Path,
    count_tokens: Callable[[str], int] | None = None,
    max_context_tokens: int = 6000,
    limit_rows: int | None = 400,
) -> list[Boundary]:
    """Parse SWE-smith trajectories into candidate handoff-boundary cut points.

    Reads at most `limit_rows` rows (in file order) via pyarrow's batched reader for
    speed. Rows whose first user message (PR description) is under 200 chars are
    skipped. For each remaining row, emits one Boundary per k in {6, 10, 14} assistant
    turns for which the k-th assistant turn exists and at least one assistant turn
    follows it. Ordering is deterministic: rows in file order, k in ascending order
    within a row.
    """
    if count_tokens is None:
        count_tokens = DEFAULT_COUNT_TOKENS

    boundaries: list[Boundary] = []
    pf = pq.ParquetFile(str(path))

    row_index = 0
    for batch in pf.iter_batches(batch_size=200, columns=_COLUMNS):
        for row in batch.to_pylist():
            if limit_rows is not None and row_index >= limit_rows:
                return boundaries
            boundaries.extend(_boundaries_for_row(row, row_index, count_tokens, max_context_tokens))
            row_index += 1
    return boundaries
