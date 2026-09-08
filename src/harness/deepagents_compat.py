"""Thin compatibility layer over deepagents 0.7.13.

Every import path below was verified against the installed package source at
`site-packages/deepagents` (see `docs/notes/deepagents_probe.md`). Nothing here
is guessed: the names, kwargs and return shapes mirror what deepagents' own
`task` tool and `create_deep_agent` do.
"""

from __future__ import annotations

from typing import Any, Callable, Iterable, Sequence

from langchain.tools import ToolRuntime
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import BaseTool, StructuredTool
from langgraph.types import Command
from pydantic import BaseModel, Field

from deepagents import (
    GeneralPurposeSubagentProfile,
    HarnessProfile,
    create_deep_agent,
    register_harness_profile,
)
from deepagents.backends import BackendProtocol, StateBackend
from deepagents.middleware.subagents import _EXCLUDED_STATE_KEYS
from deepagents.middleware.summarization import SummarizationMiddleware

__all__ = [
    "EXCLUDED_STATE_KEYS",
    "QWEN_EXCLUDED_TOOLS",
    "build_planner",
    "default_backend",
    "is_private_key",
    "make_summarizer",
    "make_wrapper_tool",
    "register_qwen_profile",
    "strip_state",
]

QWEN_EXCLUDED_TOOLS: frozenset[str] = frozenset(
    {"ls", "glob", "grep", "execute", "edit_file", "delete"}
)
"""Built-in tool names hidden from the model.

All six are real deepagents tool names: `FsToolName` in
`deepagents/middleware/filesystem.py:1366` is
`Literal["ls","read_file","write_file","edit_file","delete","glob","grep","execute"]`,
so every entry matches a tool that `FilesystemMiddleware` actually injects.
`read_file` and `write_file` are deliberately left visible.
"""

EXCLUDED_STATE_KEYS: frozenset[str] = frozenset(_EXCLUDED_STATE_KEYS)
"""State keys never forwarded to a subgraph nor merged back from one.

Sourced verbatim from `deepagents/middleware/subagents.py:392`:
`{"messages", "todos", "structured_response", "_deepagents_forked_context"}`.
`messages` is handled explicitly; the rest have no meaningful cross-graph reducer.
"""


def is_private_key(key: str) -> bool:
    """Return `True` for agent-private state keys (leading underscore).

    deepagents marks private channels with `PrivateStateAttr` and resolves them
    at build time via `private_state_field_names`
    (`deepagents/middleware/_state.py:14`). All shipped private fields are
    underscore-prefixed (`_summarization_event`, `_summarization_session_id`,
    `_deepagents_forked_context`), so the underscore rule is a superset that
    needs no compiled graph to evaluate.
    """
    return key.startswith("_")


def strip_state(state: Any) -> dict[str, Any]:
    """Copy `state` dropping excluded and private keys."""
    return {
        k: v
        for k, v in dict(state).items()
        if k not in EXCLUDED_STATE_KEYS and not is_private_key(k)
    }


def register_qwen_profile(
    model_key: str = "openai:qwen32b",
    excluded_tools: Iterable[str] = QWEN_EXCLUDED_TOOLS,
) -> HarnessProfile:
    """Register (and return) the harness profile for the Qwen planner/worker.

    Disables the auto-added `general-purpose` subagent. Combined with
    `subagents=None` on `create_deep_agent`, that removes the `task` tool
    entirely: `graph.py:873` only appends `SubAgentMiddleware` when
    `inline_subagents` is non-empty, and `graph.py:796` skips the auto-added
    general-purpose spec when `gp_profile.enabled is False`.

    Excluding `SubAgentMiddleware` via `excluded_middleware` is *not* an option —
    `graph.py:241` lists it as required scaffolding and
    `_validate_excluded_middleware_config` raises `ValueError` on it.

    Note: `register_harness_profile` is **additive** — re-registering the same
    key merges on top of the previous registration rather than replacing it
    (`harness_profiles.py:963`). Calling this twice in one process is therefore
    idempotent for these settings but never clears them.

    Args:
        model_key: Registry key, `provider` or `provider:model`.
        excluded_tools: Tool names hidden from the model.

    Returns:
        The `HarnessProfile` that was registered.
    """
    profile = HarnessProfile(
        excluded_tools=frozenset(excluded_tools),
        general_purpose_subagent=GeneralPurposeSubagentProfile(enabled=False),
    )
    register_harness_profile(model_key, profile)
    return profile


def make_summarizer(
    model: BaseChatModel,
    backend: BackendProtocol,
    trigger_tokens: int = 16_000,
    keep_messages: int = 8,
    token_counter: Callable[..., int] | None = None,
) -> SummarizationMiddleware:
    """Build a deepagents `SummarizationMiddleware` with explicit thresholds.

    `SummarizationMiddleware` is the public alias for the private impl class
    `_DeepAgentsSummarizationMiddleware`
    (`deepagents/middleware/summarization.py:1629`). Its `__init__`
    (`summarization.py:524`) is
    `(model, *, backend, trigger=None, keep=("messages", N),
    token_counter=count_tokens_approximately, summary_prompt=...,
    trim_tokens_to_summarize=..., truncate_args_settings=None)` — so `trigger`
    and `keep` are `ContextSize` 2-tuples of `(kind, value)` and `backend` is a
    required keyword argument.

    Explicit `("tokens", N)` / `("messages", N)` values are used rather than
    `create_summarization_middleware`, whose defaults depend on whether the
    model exposes a `profile["max_input_tokens"]`
    (`compute_summarization_defaults`, `summarization.py:262`) — a
    vLLM-served model does not, and would silently fall back to
    `("tokens", 170000)`.

    The returned instance reports `.name == "SummarizationMiddleware"`, which is
    the same name `create_deep_agent` gives the summarizer it adds by default.
    Passing this instance through `middleware=[...]` therefore *replaces* that
    default in place instead of stacking a second one
    (`_apply_custom_middleware`, `graph.py:204`).

    Args:
        model: Resolved chat model used to write summaries.
        backend: Backend that evicted history is offloaded to.
        trigger_tokens: Summarize once the conversation reaches this many tokens.
        keep_messages: Recent messages left untouched by a summarization pass.
        token_counter: Optional token counter; deepagents' default
            (`count_tokens_approximately`) is used when `None`.

    Returns:
        A configured `SummarizationMiddleware` instance.
    """
    kwargs: dict[str, Any] = {
        "model": model,
        "backend": backend,
        "trigger": ("tokens", trigger_tokens),
        "keep": ("messages", keep_messages),
    }
    if token_counter is not None:
        kwargs["token_counter"] = token_counter
    return SummarizationMiddleware(**kwargs)


class WrapperToolSchema(BaseModel):
    """Input schema for a graph-wrapping tool."""

    instruction: str = Field(
        description=(
            "The complete instruction for the wrapped agent. It sees only this "
            "text, so include all context and state exactly what to return."
        )
    )


def _last_ai_text(messages: Sequence[Any]) -> str:
    """Return the text of the last non-empty `AIMessage`, or `""`.

    Mirrors `_return_command_with_state_update`
    (`deepagents/middleware/subagents.py:677`), which walks backwards past a
    trailing empty `end_turn` `AIMessage`.
    """
    for msg in reversed(list(messages)):
        if isinstance(msg, AIMessage):
            text = msg.text.rstrip() if msg.text else ""
            if text:
                return text
    return ""


def make_wrapper_tool(
    name: str,
    description: str,
    graph: Any,
    log_fn: Callable[[str, str, str], None] | None = None,
    recursion_limit: int = 100,
) -> StructuredTool:
    """Wrap a compiled graph as a single-argument tool on the parent agent.

    This is a hand-rolled stand-in for deepagents' `task` tool: same
    construction (`StructuredTool.from_function(..., infer_schema=False,
    args_schema=...)`, `subagents.py:832`), same `runtime: ToolRuntime`
    injection, same `Command(update={**state, "messages": [ToolMessage(...)]})`
    return shape (`subagents.py:710`). One wrapped graph per tool, so the model
    picks the worker by tool name instead of by a `subagent_type` string.

    Args:
        name: Tool name the model calls.
        description: Tool description shown to the model.
        graph: Compiled graph (anything with `.invoke` / `.ainvoke`).
        log_fn: Optional `(name, instruction, report)` callback for tracing.
        recursion_limit: Per-invocation recursion limit for the wrapped graph.

    Returns:
        A `StructuredTool` with both a sync `func` and an async `coroutine`.
    """

    def _command(result: Any, instruction: str, tool_call_id: str) -> Command:
        result = dict(result)
        if "messages" not in result:
            msg = (
                f"Wrapped graph for tool {name!r} returned no 'messages' key; "
                "its state schema must include 'messages'."
            )
            raise ValueError(msg)
        report = _last_ai_text(result["messages"])
        if log_fn is not None:
            log_fn(name, instruction, report)
        return Command(
            update={
                **strip_state(result),
                "messages": [ToolMessage(content=report, tool_call_id=tool_call_id)],
            }
        )

    def _payload(runtime: ToolRuntime, instruction: str) -> dict[str, Any]:
        return {
            **strip_state(runtime.state),
            "messages": [HumanMessage(content=instruction)],
        }

    def call(instruction: str, runtime: ToolRuntime) -> Command:
        if not runtime.tool_call_id:
            msg = f"Tool call ID is required to invoke wrapped graph {name!r}"
            raise ValueError(msg)
        result = graph.invoke(
            _payload(runtime, instruction),
            config={"recursion_limit": recursion_limit},
        )
        return _command(result, instruction, runtime.tool_call_id)

    async def acall(instruction: str, runtime: ToolRuntime) -> Command:
        if not runtime.tool_call_id:
            msg = f"Tool call ID is required to invoke wrapped graph {name!r}"
            raise ValueError(msg)
        result = await graph.ainvoke(
            _payload(runtime, instruction),
            config={"recursion_limit": recursion_limit},
        )
        return _command(result, instruction, runtime.tool_call_id)

    return StructuredTool.from_function(
        name=name,
        func=call,
        coroutine=acall,
        description=description,
        infer_schema=False,
        args_schema=WrapperToolSchema,
    )


def default_backend() -> StateBackend:
    """Return deepagents' default in-state backend.

    `create_deep_agent` falls back to `StateBackend()` when `backend=None`
    (`deepagents/graph.py:637`). Files live in the graph's `files` state key
    (`FilesystemState.files`, `middleware/filesystem.py:1090`).
    """
    return StateBackend()


def build_planner(
    model: BaseChatModel,
    tools: Sequence[BaseTool],
    summarizer: SummarizationMiddleware,
    system_prompt: str,
    backend: BackendProtocol,
) -> Any:
    """Build a deep agent with no subagents and a caller-supplied summarizer.

    `subagents=None` plus a harness profile that disables the general-purpose
    subagent means `SubAgentMiddleware` is never added, so the `task` tool does
    not exist. Delegation happens through `make_wrapper_tool` tools in `tools`.

    Verified `create_deep_agent` signature (`deepagents/graph.py:271`):
    `(model=None, tools=None, *, system_prompt=None, middleware=(),
    subagents=None, skills=None, memory=None, permissions=None, backend=None,
    interrupt_on=None, response_format=None, state_schema=None,
    context_schema=None, checkpointer=None, store=None, debug=False,
    name=None, cache=None)`.

    Returns:
        The compiled agent graph (`CompiledStateGraph` with a bound config).
    """
    return create_deep_agent(
        model=model,
        tools=list(tools),
        subagents=None,
        middleware=[summarizer],
        system_prompt=system_prompt,
        backend=backend,
    )
