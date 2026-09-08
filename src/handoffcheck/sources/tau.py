"""Parser for the tau-bench airline traces parquet dataset.

Each row is a full customer-service conversation (list of messages with
roles system/user/assistant/tool). We serialize each conversation into a
flat list of {"role", "content"} turns and emit one candidate handoff
Boundary per valid cut point (right after a tool_result message, once
enough context has accumulated and there is still work left to hand off).
"""
from __future__ import annotations

from pathlib import Path
from typing import Callable

import pyarrow.parquet as pq

from handoffcheck.schema import Boundary, context_to_text

TOOL_RESULT_TRUNCATE_LEN = 1500
TRUNCATE_MARKER = " …[truncated]"

_DEFAULT_COUNT_TOKENS: Callable[[str], int] = lambda t: max(1, len(t) // 3)


def _serialize_messages(messages: list[dict]) -> tuple[list[dict], list[int]]:
    """Serialize one conversation's raw messages into flat turns.

    Returns (serialized, orig_idx) where orig_idx[i] is the index into
    `messages` that produced serialized[i] (system messages are dropped;
    an assistant message with both content and tool_calls yields multiple
    serialized entries, all mapped back to the same original index).
    """
    serialized: list[dict] = []
    orig_idx: list[int] = []

    for i, m in enumerate(messages):
        role = m.get("role")
        if role == "system":
            continue
        elif role == "user":
            content = m.get("content") or ""
            serialized.append({"role": "user", "content": content})
            orig_idx.append(i)
        elif role == "assistant":
            content = m.get("content")
            if content:
                serialized.append({"role": "assistant", "content": content})
                orig_idx.append(i)
            for tc in m.get("tool_calls") or []:
                func = tc.get("function") or {}
                name = func.get("name")
                arguments = func.get("arguments")
                serialized.append(
                    {"role": "assistant", "content": f"[tool_call] {name}({arguments})"}
                )
                orig_idx.append(i)
        elif role == "tool":
            content = m.get("content") or ""
            if len(content) > TOOL_RESULT_TRUNCATE_LEN:
                content = content[:TOOL_RESULT_TRUNCATE_LEN] + TRUNCATE_MARKER
            serialized.append({"role": "tool", "content": f"[tool_result] {content}"})
            orig_idx.append(i)
        else:
            continue

    return serialized, orig_idx


def _apply_token_cap(
    context: list[dict], count_tokens: Callable[[str], int], max_context_tokens: int
) -> tuple[list[dict], bool, int]:
    """Drop from the front (keeping the first user message) until under cap."""
    ctx = list(context)
    if not ctx:
        return ctx, False, 0

    protected = next((m for m in ctx if m.get("role") == "user"), ctx[0])
    dropped = 0

    while count_tokens(context_to_text(ctx)) > max_context_tokens and len(ctx) > 1:
        idx = 1 if ctx[0] is protected else 0
        if idx >= len(ctx):
            break
        del ctx[idx]
        dropped += 1

    return ctx, dropped > 0, dropped


def parse(
    path: str | Path,
    count_tokens: Callable[[str], int] | None = None,
    max_context_tokens: int = 6000,
) -> list[Boundary]:
    """Parse the tau airline traces parquet into candidate handoff Boundaries."""
    count_tokens = count_tokens or _DEFAULT_COUNT_TOKENS

    table = pq.read_table(str(path))
    rows = table.to_pylist()

    boundaries: list[Boundary] = []

    for row_index, row in enumerate(rows):
        messages = row.get("messages") or []
        serialized, orig_idx = _serialize_messages(messages)

        tool_result_count = 0
        user_turn_count = 0

        for k, entry in enumerate(serialized):
            role = entry.get("role")
            if role == "tool":
                tool_result_count += 1
            elif role == "user":
                user_turn_count += 1

            if role != "tool":
                continue

            if tool_result_count < 2 or user_turn_count < 3:
                continue

            orig_message_idx = orig_idx[k]
            has_assistant_after = any(
                m.get("role") == "assistant" for m in messages[orig_message_idx + 1 :]
            )
            if not has_assistant_after:
                continue

            context = serialized[: k + 1]
            n_serialized_total = len(serialized)
            n_serialized_kept = k + 1

            capped_context, truncated, dropped = _apply_token_cap(
                context, count_tokens, max_context_tokens
            )

            meta = {
                "row": row_index,
                "cut_index": k,
                "n_user_turns": user_turn_count,
                "n_tool_results": tool_result_count,
                "n_serialized_total": n_serialized_total,
                "n_serialized_kept": n_serialized_kept,
            }
            if truncated:
                meta["truncated"] = True
                meta["dropped"] = dropped

            boundaries.append(
                Boundary(
                    id=f"tau-{row_index}-{k}",
                    domain="tau",
                    source_ref=f"row{row_index}#cut{k}",
                    sender_role="customer service agent",
                    receiver_role="the next agent who will continue this task",
                    context=capped_context,
                    message=None,
                    meta=meta,
                )
            )

    return boundaries
