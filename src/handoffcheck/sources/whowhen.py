"""whowhen: parse Magentic-One "Who&When" hand-crafted traces into Boundary candidates.

Each trace is a JSON file with a `history` list of
{"role": str, "content": str, "name": null} messages produced by an
Orchestrator coordinating worker agents (WebSurfer, Coder, FileSurfer,
ComputerTerminal, Assistant, ...). A candidate boundary is an Orchestrator
handoff message (role matching `Orchestrator (-> <Worker>)`) together with
everything that happened before it in the trace. This module returns every
structurally valid candidate; downstream selection (which candidates to keep
for the benchmark) happens elsewhere.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Callable

from ..schema import Boundary, context_to_text

_HANDOFF_RE = re.compile(r"^Orchestrator \(-> (.+)\)$")

_MIN_WORKER_MSGS_BEFORE = 2
_MIN_MESSAGE_CHARS = 40


def _default_count_tokens(text: str) -> int:
    return max(1, len(text) // 3)


def _is_worker_reply(role: str) -> bool:
    """A worker reply is anything that isn't an Orchestrator message or the human."""
    return not role.startswith("Orchestrator") and role != "human"


def _truncate_context(
    context: list[dict],
    count_tokens: Callable[[str], int],
    max_context_tokens: int,
) -> tuple[list[dict], bool, int]:
    """Drop messages from the front of `context` until it fits under the token cap.

    Always keeps the first 'human' message and the first 'Orchestrator (thought)'
    message (the initial plan), dropping the oldest of the remaining messages
    until the cap is satisfied (or nothing more can be dropped). The most
    recent worker replies (up to `_MIN_WORKER_MSGS_BEFORE`) are protected the
    same way, since a candidate is only ever created when that many worker
    replies precede the handoff -- truncation must not silently erase the
    very messages that made the boundary a candidate in the first place.
    """

    def fits(ctx: list[dict]) -> bool:
        return count_tokens(context_to_text(ctx)) <= max_context_tokens

    if fits(context):
        return context, False, 0

    human_idx = next((i for i, m in enumerate(context) if m.get("role") == "human"), None)
    plan_idx = next((i for i, m in enumerate(context) if m.get("role") == "Orchestrator (thought)"), None)
    worker_idxs = [i for i, m in enumerate(context) if _is_worker_reply(m.get("role") or "")]
    protected_worker_idxs = worker_idxs[-_MIN_WORKER_MSGS_BEFORE:]
    kept = {i for i in (human_idx, plan_idx) if i is not None} | set(protected_worker_idxs)
    rest = [i for i in range(len(context)) if i not in kept]

    dropped = 0
    order = sorted(kept | set(rest))
    while rest and not fits([context[i] for i in order]):
        rest.pop(0)
        dropped += 1
        order = sorted(kept | set(rest))

    return [context[i] for i in order], True, dropped


def parse(
    root: str | Path,
    count_tokens: Callable[[str], int] | None = None,
    max_context_tokens: int = 6000,
) -> list[Boundary]:
    """Parse all hand-crafted whowhen traces under `root` into handoff candidates.

    `root` should point at a directory of Magentic-One trace JSON files
    (e.g. data/external/whowhen/hand_crafted). Returns candidates in
    deterministic (file name, cut index) order.
    """
    count_tokens = count_tokens or _default_count_tokens
    root = Path(root)
    boundaries: list[Boundary] = []

    for path in sorted(root.glob("*.json"), key=lambda p: p.name):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        history = data.get("history", [])
        file_stem = path.stem
        file_name = path.name

        n_worker_before = 0
        for i, msg in enumerate(history):
            role = msg.get("role", "") or ""
            content = msg.get("content") or ""

            match = _HANDOFF_RE.match(role)
            if (
                match
                and n_worker_before >= _MIN_WORKER_MSGS_BEFORE
                and len(content.strip()) >= _MIN_MESSAGE_CHARS
            ):
                context = [{"role": h.get("role"), "content": h.get("content")} for h in history[:i]]
                context, truncated, dropped = _truncate_context(context, count_tokens, max_context_tokens)

                meta = {
                    "question_id": data.get("question_ID"),
                    "question": data.get("question"),
                    "cut_index": i,
                    "n_history": len(history),
                    "mistake_step": data.get("mistake_step"),
                    "mistake_agent": data.get("mistake_agent"),
                    "n_worker_msgs_before": n_worker_before,
                }
                if truncated:
                    meta["truncated"] = True
                    meta["dropped"] = dropped

                boundaries.append(
                    Boundary(
                        id=f"whowhen-{file_stem}-{i}",
                        domain="whowhen",
                        source_ref=f"{file_name}#{i}",
                        sender_role="Orchestrator",
                        receiver_role=match.group(1),
                        context=context,
                        message=content,
                        meta=meta,
                    )
                )

            if _is_worker_reply(role):
                n_worker_before += 1

    return boundaries
