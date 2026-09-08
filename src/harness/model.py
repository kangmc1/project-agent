"""Chat model factory.  Create clients INSIDE the worker process (openai clients are not picklable)."""
from __future__ import annotations

import os

from langchain_openai import ChatOpenAI

from .capture import RunContext, make_http_client

EXEC_BASE = os.environ.get("EXEC_BASE_URL", "http://localhost:18001/v1")
EXTRACT_BASE = os.environ.get("EXTRACT_BASE_URL", "http://localhost:18002/v1")
NO_THINK = {"chat_template_kwargs": {"enable_thinking": False}}
# The exact generated token ids are recorded so that D1 rescoring can place the decision point (right before
# <tool_call>) on the very tokens the model produced. vLLM 0.9.2 has no `return_token_ids`; the only channel that carries
# token ids in its OpenAI-compatible response is `logprobs` (tokens + their logprobs). The logprob VALUES are not used by
# D1 — the rescored value is the measurement. EXEC_RECORD_TOKENS=0 disables it (content is then re-tokenized: exact ids in 99.2%).
RECORD_TOKENS = os.environ.get("EXEC_RECORD_TOKENS", "1") == "1"


def make_chat(agent_name: str, ctx: RunContext | None = None, *, base_url: str = EXEC_BASE,
              model: str = "qwen32b", max_tokens: int = 2048, temperature: float = 0.0,
              logprobs: bool = RECORD_TOKENS) -> ChatOpenAI:
    """One ChatOpenAI per agent role; the X-Agent header is how steps are attributed."""
    kwargs = dict(
        base_url=base_url,
        api_key="dummy",
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        logprobs=logprobs,
        disable_streaming=True,
        extra_body=NO_THINK,
        default_headers={"X-Agent": agent_name},
        timeout=600,
        max_retries=1,
    )
    if ctx is not None:
        kwargs["http_client"] = make_http_client(ctx)
    return ChatOpenAI(**kwargs)
