"""Render stored request bodies into the exact token-id prefix the executor saw (verified against /tokenize in P1(e))."""
from __future__ import annotations

import glob
import os
from functools import lru_cache

from transformers import AutoTokenizer

TOOL_CALL_ID = 151657
TOOL_CALL_HEAD = '<tool_call>\n{"name": "'


@lru_cache(maxsize=1)
def tokenizer():
    path = os.environ.get("Q32") or sorted(glob.glob(os.path.expanduser("~/.cache/huggingface/hub/models--Qwen--Qwen3-32B/snapshots/*")))[0]
    return AutoTokenizer.from_pretrained(path)


def render_text(messages: list[dict], tools: list[dict] | None) -> str:
    tok = tokenizer()
    return tok.apply_chat_template(messages, tools=tools or None, add_generation_prompt=True,
                                   tokenize=False, enable_thinking=False)


def encode(text: str) -> list[int]:
    return tokenizer()(text, add_special_tokens=False)["input_ids"]


def prefix_ids(messages: list[dict], tools: list[dict] | None) -> list[int]:
    return encode(render_text(messages, tools))


def candidate_ids(prefix: list[int], prefix_text: str, name: str) -> tuple[list[int], bool]:
    """Token ids of '<tool_call>\\n{"name": "<name>' continuing the prefix (no closing quote: the model emits '",'
    as a single token after the name, so a lone '"' would be a rare path with noisy logprobs).

    Returns (candidate_ids, boundary_ok). boundary_ok is False when tokenizing prefix+candidate as one string
    changes the prefix tokens (BPE merge across the boundary) — such decision points are recorded as
    boundary_assert_fail and scored with method 2 only.
    """
    full = encode(prefix_text + TOOL_CALL_HEAD + name)
    ok = full[: len(prefix)] == prefix
    return full[len(prefix):], ok
