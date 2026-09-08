#!/usr/bin/env python
"""Probe the installed deepagents against `src/harness/deepagents_compat.py`.

Runs offline against a fake chat model: no LLM server, no GPU, no network.
Writes `docs/notes/deepagents_probe.md` and exits non-zero on any failed check.

    python scripts/probe_deepagents.py
"""

from __future__ import annotations

import itertools
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import deepagents  # noqa: E402
import deepagents.graph  # noqa: E402
from langchain_core.language_models.fake_chat_models import (  # noqa: E402
    GenericFakeChatModel,
)
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage  # noqa: E402
from langchain_core.tools import StructuredTool  # noqa: E402
from langgraph.prebuilt import ToolRuntime  # noqa: E402
from langgraph.types import Command  # noqa: E402
from pydantic import BaseModel, Field  # noqa: E402

from deepagents.middleware.subagents import SubAgentMiddleware  # noqa: E402

from src.harness.deepagents_compat import (  # noqa: E402
    EXCLUDED_STATE_KEYS,
    PRIVATE_STATE_KEYS,
    QWEN_EXCLUDED_TOOLS,
    build_planner,
    default_backend,
    is_private_key,
    make_summarizer,
    make_wrapper_tool,
    register_qwen_profile,
)

MODEL_KEY = "openai:qwen32b"
FORBIDDEN_TOOLS = {"task", "ls", "glob", "grep", "execute", "edit_file", "delete"}
NOTE_PATH = REPO_ROOT / "docs" / "notes" / "deepagents_probe.md"

# Tool lists captured by `bind_tools`, one entry per model call.
BOUND_TOOLS: list[list[str]] = []


class FakeQwen(GenericFakeChatModel):
    """Fake model that resolves to the `openai:qwen32b` harness profile.

    `_harness_profile_for_model` (`harness_profiles.py:1255`) keys off
    `get_model_identifier` (`model_name` or `model`) and `get_model_provider`
    (`_get_ls_params()["ls_provider"]`) when the caller passes an instance
    rather than a spec string, so both are spoofed here. `bind_tools` is
    overridden because `BaseChatModel.bind_tools` raises `NotImplementedError`
    -- and because binding is the only place the post-middleware tool list is
    observable (`_ToolExclusionMiddleware` filters at `wrap_model_call` time,
    not on the compiled graph).
    """

    model_name: str = "qwen32b"

    def _get_ls_params(self, stop: Any = None, **kwargs: Any) -> dict[str, Any]:
        return {
            "ls_provider": "openai",
            "ls_model_name": self.model_name,
            "ls_model_type": "chat",
        }

    def bind_tools(self, tools: Any, **kwargs: Any) -> Any:
        BOUND_TOOLS.append([getattr(t, "name", str(t)) for t in tools])
        return self


def fake_model(reply: str = "done") -> FakeQwen:
    return FakeQwen(messages=itertools.cycle([AIMessage(content=reply)]))


class DummyArgs(BaseModel):
    query: str = Field(description="Anything.")


def dummy_tool() -> StructuredTool:
    def run(query: str) -> str:
        return f"dummy:{query}"

    return StructuredTool.from_function(
        name="dummy_probe_tool",
        func=run,
        description="A no-op tool used only to prove user tools survive.",
        args_schema=DummyArgs,
    )


class Report:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.sections: list[tuple[str, str]] = []

    def check(self, ok: bool, label: str) -> bool:
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {label}")
        if not ok:
            self.failures.append(label)
        return ok

    def section(self, title: str, body: str) -> None:
        self.sections.append((title, body))


class RecordedStack:
    """Capture the middleware list `create_deep_agent` hands to `create_agent`.

    LIBRARY LIMITATION: the compiled graph does **not** expose its middleware.
    `CompiledStateGraph` has no `.middleware`, and only middleware that
    implements a node-producing hook (`before_agent`/`before_model`/...) shows
    up in `graph.nodes` -- `SummarizationMiddleware` implements only
    `wrap_model_call`, so it is invisible there. deepagents assembles the stack
    in a local (`deepagent_middleware`, `deepagents/graph.py:862`) and passes
    it straight into `create_agent` (`graph.py:956`), which closes over it.

    So the stack is read at the only observable seam: `deepagents.graph`'s
    module-level reference to `create_agent`. This is a read-only tap -- the
    original is always called and always restored.
    """

    def __init__(self) -> None:
        self.stacks: list[list[Any]] = []
        self._original: Any = None

    def __enter__(self) -> RecordedStack:
        self._original = deepagents.graph.create_agent

        def _tap(*args: Any, **kwargs: Any) -> Any:
            self.stacks.append(list(kwargs.get("middleware", ())))
            return self._original(*args, **kwargs)

        deepagents.graph.create_agent = _tap
        return self

    def __exit__(self, *exc: Any) -> None:
        deepagents.graph.create_agent = self._original

    @property
    def last(self) -> list[Any]:
        return self.stacks[-1] if self.stacks else []


def state_keys(graph: Any) -> list[str]:
    """Return the declared state channel names of a compiled agent graph."""
    target = graph
    for _ in range(5):
        schema = getattr(target, "stream_channels_list", None)
        if schema is not None:
            return sorted(schema)
        channels = getattr(target, "channels", None)
        if channels is not None:
            return sorted(channels)
        target = getattr(target, "bound", None)
        if target is None:
            break
    return []


def summarizer_settings(mw: Any) -> tuple[Any, Any]:
    """Read `(trigger, keep)` off a deepagents SummarizationMiddleware.

    The deepagents wrapper delegates core logic to a LangChain helper stored on
    `._lc_helper` (`summarization.py:589`), which is where `trigger`/`keep`
    actually live (`langchain/agents/middleware/summarization.py:361,372`).
    The wrapper exposes no `trigger`/`keep` property of its own.
    """
    helper = getattr(mw, "_lc_helper", mw)
    return getattr(helper, "trigger", None), getattr(helper, "keep", None)


def probe_planner(rep: Report) -> Any:
    """(1) Tool visibility + (2) middleware stack."""
    profile = register_qwen_profile(MODEL_KEY)
    rep.check(
        profile.excluded_tools == QWEN_EXCLUDED_TOOLS,
        f"profile excluded_tools == {sorted(QWEN_EXCLUDED_TOOLS)}",
    )
    rep.check(
        profile.general_purpose_subagent is not None
        and profile.general_purpose_subagent.enabled is False,
        "profile disables the general-purpose subagent",
    )

    model = fake_model()
    backend = default_backend()
    summarizer = make_summarizer(model, backend, trigger_tokens=16_000, keep_messages=8)
    with RecordedStack() as rec:
        planner = build_planner(
            model=model,
            tools=[dummy_tool()],
            summarizer=summarizer,
            system_prompt="You are the planner. Delegate, then answer.",
            backend=backend,
        )
    rep.check(len(rec.stacks) == 1, f"create_agent called once (got {len(rec.stacks)})")

    BOUND_TOOLS.clear()
    planner.invoke({"messages": [HumanMessage(content="probe")]})
    rep.check(bool(BOUND_TOOLS), "model was bound with a tool list")
    visible = BOUND_TOOLS[0] if BOUND_TOOLS else []
    leaked = sorted(set(visible) & FORBIDDEN_TOOLS)
    rep.check(not leaked, f"no forbidden tools visible (leaked={leaked})")
    rep.check("dummy_probe_tool" in visible, "user-supplied tool is visible")
    print(f"       visible tools: {visible}")

    stack = rec.last
    names = [f"{type(m).__name__}(name={m.name})" for m in stack]
    summarizers = [m for m in stack if m.name == "SummarizationMiddleware"]
    rep.check(
        len(summarizers) == 1,
        f"exactly 1 SummarizationMiddleware in stack (found {len(summarizers)})",
    )
    lines = []
    for m in summarizers:
        trig, keep = summarizer_settings(m)
        lines.append(f"- `{type(m).__name__}` name=`{m.name}` trigger={trig!r} keep={keep!r}")
        print(f"       summarizer trigger={trig!r} keep={keep!r}")
    if summarizers:
        trig, keep = summarizer_settings(summarizers[0])
        rep.check(tuple(trig) == ("tokens", 16000), f"trigger == ('tokens', 16000) (got {trig!r})")
        rep.check(tuple(keep) == ("messages", 8), f"keep == ('messages', 8) (got {keep!r})")
        rep.check(summarizers[0] is summarizer, "our instance replaced the auto-added one")
    rep.check(
        not any(isinstance(m, SubAgentMiddleware) for m in stack),
        f"SubAgentMiddleware absent (stack={names})",
    )

    rep.section(
        "Tool list the model sees",
        "Captured from the fake model's `bind_tools` during one real "
        "`planner.invoke` -- `_ToolExclusionMiddleware` strips names at "
        "`wrap_model_call` time, so the compiled graph's tool node still holds "
        "them and static inspection of the graph would over-report.\n\n"
        f"- visible: `{visible}`\n"
        f"- asserted absent: `{sorted(FORBIDDEN_TOOLS)}` -> leaked `{leaked}`\n",
    )
    rep.section(
        "Middleware stack",
        f"Planner stack (in order): `{names}`\n\n"
        f"SummarizationMiddleware instances: {len(summarizers)}\n\n"
        + "\n".join(lines)
        + "\n\n`SubAgentMiddleware` is absent, which is why no `task` tool exists.\n",
    )
    return planner


def probe_wrapper(rep: Report) -> None:
    """(3) Subagent graph + wrapper tool Command shape."""
    backend = default_backend()
    worker_model = fake_model("worker report body")
    summarizer = make_summarizer(
        worker_model, backend, trigger_tokens=16_000, keep_messages=8
    )
    with RecordedStack() as rec:
        worker = build_planner(
            model=worker_model,
            tools=[dummy_tool()],
            summarizer=summarizer,
            system_prompt="You are the worker.",
            backend=backend,
        )
    worker_summarizers = [m for m in rec.last if m.name == "SummarizationMiddleware"]
    rep.check(len(worker_summarizers) == 1, "worker graph also has exactly 1 summarizer")

    keys = state_keys(worker)
    rep.check("files" in keys, f"`files` is a state key of the worker graph (keys={keys})")
    rep.check("messages" in keys, "`messages` is a state key of the worker graph")

    calls: list[tuple[str, str, str]] = []
    tool = make_wrapper_tool(
        "run_worker",
        "Delegate one self-contained unit of work to the worker agent.",
        worker,
        log_fn=lambda n, i, r: calls.append((n, i, r)),
    )
    rep.check(isinstance(tool, StructuredTool), "wrapper is a StructuredTool")
    rep.check(tool.name == "run_worker", "wrapper tool name is preserved")
    schema_props = sorted(tool.args_schema.model_json_schema()["properties"])
    rep.check(schema_props == ["instruction"], f"args schema is {{instruction}} (got {schema_props})")
    rep.check(tool.coroutine is not None, "wrapper exposes an async coroutine")

    # --- direct call with a hand-built ToolRuntime: inspect the Command object.
    parent_state: dict[str, Any] = {
        "messages": [HumanMessage(content="parent turn")],
        "files": {},
        "todos": [{"content": "parent todo", "status": "pending"}],
        "jump_to": "model",
        "_summarization_session_id": "parent-session",
    }
    runtime = ToolRuntime(
        state=parent_state,
        context=None,
        config={},
        stream_writer=lambda _: None,
        tool_call_id="probe_call_1",
        store=None,
    )
    result = tool.func("do the thing", runtime)
    rep.check(isinstance(result, Command), f"wrapper returns a Command (got {type(result).__name__})")
    update = getattr(result, "update", {}) or {}
    msgs = update.get("messages", [])
    rep.check(len(msgs) == 1, f"Command carries exactly 1 message (got {len(msgs)})")
    tm = msgs[0] if msgs else None
    rep.check(isinstance(tm, ToolMessage), f"message is a ToolMessage (got {type(tm).__name__})")
    rep.check(
        getattr(tm, "tool_call_id", None) == "probe_call_1",
        "ToolMessage carries the parent tool_call_id",
    )
    rep.check(
        getattr(tm, "content", "") == "worker report body",
        f"report is the last AIMessage text (got {getattr(tm, 'content', '')!r})",
    )
    rep.check(len(calls) == 1 and calls[0][0] == "run_worker", "log_fn was called once")
    leaked_state = sorted(k for k in update if k != "messages" and k in EXCLUDED_STATE_KEYS)
    rep.check(not leaked_state, f"no excluded/private keys in the Command update (leaked={leaked_state})")
    rep.check(
        "jump_to" not in update,
        "`jump_to` (PrivateStateAttr, no underscore) is not merged back",
    )
    print(f"       Command update keys: {sorted(update)}")

    # --- end-to-end: prove `runtime: ToolRuntime` is really injected by the
    # executor for a StructuredTool built with infer_schema=False.
    planner_model = FakeQwen(
        messages=iter(
            [
                AIMessage(
                    content="",
                    tool_calls=[
                        {
                            "name": "run_worker",
                            "args": {"instruction": "do the thing"},
                            "id": "e2e_call_1",
                            "type": "tool_call",
                        }
                    ],
                ),
                AIMessage(content="relayed"),
            ]
        )
    )
    e2e_backend = default_backend()
    planner = build_planner(
        model=planner_model,
        tools=[tool],
        summarizer=make_summarizer(planner_model, e2e_backend),
        system_prompt="You are the planner.",
        backend=e2e_backend,
    )
    final = planner.invoke({"messages": [HumanMessage(content="go")]})
    tool_msgs = [m for m in final["messages"] if isinstance(m, ToolMessage)]
    rep.check(len(tool_msgs) == 1, f"end-to-end produced 1 ToolMessage (got {len(tool_msgs)})")
    rep.check(
        bool(tool_msgs) and tool_msgs[0].tool_call_id == "e2e_call_1",
        "end-to-end ToolMessage answers the model's tool_call_id",
    )
    rep.check(
        bool(tool_msgs) and tool_msgs[0].content == "worker report body",
        "end-to-end ToolMessage carries the worker's report",
    )
    rep.check(len(calls) == 2, f"log_fn fired again through the agent loop (calls={len(calls)})")

    rep.section(
        "State keys",
        f"Worker graph channels: `{keys}`\n\n"
        "`files` comes from `FilesystemState` "
        "(`deepagents/middleware/filesystem.py:1090`): "
        "`files: Annotated[NotRequired[dict[str, FileData]], DeltaChannel(_file_data_delta_reducer, ...)]`, "
        "i.e. a `path -> FileData` mapping owned by `StateBackend`, merged by a "
        "delta reducer. It is a normal (non-private) channel, so it is forwarded "
        "into a wrapped graph and merged back out of it.\n\n"
        f"- `EXCLUDED_STATE_KEYS` = `{sorted(EXCLUDED_STATE_KEYS)}`\n"
        f"- `PRIVATE_STATE_KEYS` (resolved from `PrivateStateAttr`) = `{sorted(PRIVATE_STATE_KEYS)}`\n"
        "- plus anything matching `is_private_key` (leading `_`)\n\n"
        "`jump_to` is the trap: it is `PrivateStateAttr` "
        "(`langchain/agents/middleware/types.py:353`) with **no** leading "
        "underscore, and it is the agent loop's control channel. Filtering on "
        "the underscore convention alone would merge a worker's `jump_to` into "
        "the parent.\n",
    )
    rep.section(
        "Wrapper Command shape",
        "```python\n"
        "Command(update={\n"
        "    **parent_state_minus_excluded_and_private,\n"
        '    "messages": [ToolMessage(content=report, tool_call_id=runtime.tool_call_id)],\n'
        "})\n"
        "```\n\n"
        f"- parent state fed in: `{sorted(parent_state)}`\n"
        f"- observed update keys: `{sorted(update)}`\n"
        f"- `ToolMessage.tool_call_id` = `{getattr(tm, 'tool_call_id', None)}`\n"
        f"- `ToolMessage.content` = `{getattr(tm, 'content', '')!r}`\n\n"
        "`runtime: ToolRuntime` is injected positionally by the tool executor even "
        "with `infer_schema=False` -- the pydantic `args_schema` covers only "
        "`instruction`. Verified end-to-end: a planner whose model emits a "
        "`run_worker` tool call gets back a `ToolMessage` with the worker's "
        "report and the model's own `tool_call_id`. This mirrors deepagents' own "
        "`task` tool (`deepagents/middleware/subagents.py:832`).\n\n"
        "Note: `tool.invoke({...})` called **directly** does NOT inject the "
        "runtime (`TypeError: missing 1 required positional argument: 'runtime'`) "
        "-- injection happens in the executor, so a direct probe must build a "
        "`ToolRuntime` itself.\n",
    )


def probe_dead_editables(rep: Report) -> None:
    """(4) Dead editable installs must be gone."""
    dead = ["agentbench", "agent-handoff", "handoffbench", "handoffcheck"]
    rows = []
    for pkg in dead:
        proc = subprocess.run(
            [sys.executable, "-m", "pip", "show", pkg],
            capture_output=True,
            text=True,
            check=False,
        )
        gone = proc.returncode != 0
        rep.check(gone, f"pip show {pkg} fails (package absent)")
        rows.append(f"- `pip show {pkg}` -> exit {proc.returncode} ({'absent' if gone else 'STILL INSTALLED'})")
    rep.section("Dead editable installs", "\n".join(rows) + "\n")


def write_note(rep: Report) -> None:
    imports = """```python
from deepagents import (
    GeneralPurposeSubagentProfile,   # deepagents/profiles/harness/harness_profiles.py:83
    HarnessProfile,                  # deepagents/profiles/harness/harness_profiles.py:483
    create_deep_agent,               # deepagents/graph.py:271
    register_harness_profile,        # deepagents/profiles/harness/harness_profiles.py:980
)
from deepagents.backends import BackendProtocol, StateBackend   # deepagents/backends/__init__.py
from deepagents.middleware.subagents import _EXCLUDED_STATE_KEYS  # subagents.py:392
from deepagents.middleware.summarization import SummarizationMiddleware  # summarization.py:1629 (alias)
from langchain.tools import ToolRuntime          # re-export of langgraph.prebuilt.ToolRuntime
from langchain_core.tools import StructuredTool
from langgraph.types import Command
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
```

`deepagents.middleware.subagents` imports the same three at
`subagents.py:22,27,28`: `from langchain.tools import BaseTool, ToolRuntime`,
`from langchain_core.tools import StructuredTool`,
`from langgraph.types import Command`.
"""
    deviations = """- **`SummarizationMiddleware` is an alias, not a class.** The concrete class is
  the private `_DeepAgentsSummarizationMiddleware` (`summarization.py:500`);
  `SummarizationMiddleware` is a module-level alias assigned at
  `summarization.py:1629`. Its `.name` property returns the string
  `"SummarizationMiddleware"` so profile string-exclusion and
  `_apply_custom_middleware` name-matching both work.
- **`trigger`/`keep` are not readable off the deepagents wrapper.** They live on
  the LangChain helper at `mw._lc_helper.trigger` / `.keep`
  (`summarization.py:589`). The wrapper delegates only `model` and
  `token_counter` as properties.
- **`backend=` is a required keyword arg** on `SummarizationMiddleware.__init__`
  (`summarization.py:524`), so `make_summarizer` takes a backend rather than
  defaulting one.
- **`create_deep_agent` always adds its own summarizer** (`graph.py:888`,
  `create_summarization_middleware(model, backend)`). Passing ours via
  `middleware=[...]` does not stack a second one: `_apply_custom_middleware`
  (`graph.py:204`) replaces a base entry **in place** when `.name` matches.
  Hence exactly one instance -- ours.
- **The `task` tool cannot be removed via `excluded_middleware`.**
  `SubAgentMiddleware` is required scaffolding (`graph.py:241`) and
  `_validate_excluded_middleware_config` raises `ValueError` on it. The
  supported route -- and the one used here -- is
  `GeneralPurposeSubagentProfile(enabled=False)` plus `subagents=None`, which
  leaves `inline_subagents` empty so `SubAgentMiddleware` is never appended
  (`graph.py:873`).
- **`excluded_tools` is enforced at `wrap_model_call`, not on the graph.**
  `_ToolExclusionMiddleware` (`middleware/_tool_exclusion.py:34`) filters
  `request.tools` per call and rejects calls naming an excluded tool at the
  tool-call boundary. The compiled graph's tool node still *registers* them, so
  the probe reads the tool list from `bind_tools` during a real invoke rather
  than from the graph.
- **Profile lookup for a pre-built model instance ignores the registry key you
  registered under unless the model's identity matches.**
  `_harness_profile_for_model` (`harness_profiles.py:1255`) uses the spec string
  only when `model=` was a string; for an instance it derives
  `f"{ls_provider}:{model_name}"`. The probe's fake model therefore spoofs
  `model_name="qwen32b"` and `ls_provider="openai"`. **The real harness must
  either pass `model="openai:qwen32b"` as a string, or use a `ChatOpenAI`
  instance whose `model_name` is exactly `qwen32b`** -- otherwise the profile
  silently does not apply and both the `task` tool and the excluded filesystem
  tools come back.
- **`register_harness_profile` is additive, not idempotent-by-replacement**
  (`harness_profiles.py:963`): re-registering the same key merges on top. Sets
  union; scalars prefer the newer value. It can never *clear* a prior exclusion.
- **All six excluded tool names are real.** `FsToolName`
  (`middleware/filesystem.py:1366`) is
  `Literal["ls","read_file","write_file","edit_file","delete","glob","grep","execute"]`,
  so none of the six is a silent no-op. (`excluded_tools` has no coverage check,
  unlike `excluded_middleware` -- a typo there would fail silently.)
- **No fake-model deviation was needed for `profile`.** `BaseChatModel.profile`
  returns `None` for the fake model, which `compute_summarization_defaults`
  (`summarization.py:262`) tolerates -- it just picks token/message defaults.
  We override those anyway with explicit `("tokens", N)` / `("messages", N)`.
- **`jump_to` is private but has no underscore.** It is annotated
  `PrivateStateAttr` at `langchain/agents/middleware/types.py:353` and is the
  agent loop's control channel. The plan called for `EXCLUDED_STATE_KEYS` =
  deepagents' `_EXCLUDED_STATE_KEYS` + an underscore predicate; that would leak
  `jump_to` back into the parent and could make the parent graph jump.
  **Deviation:** `EXCLUDED_STATE_KEYS` also unions `PRIVATE_STATE_KEYS`,
  resolved with deepagents' own `private_state_field_names`
  (`deepagents/middleware/_state.py:13`) over `AgentState`, `DeepAgentState`,
  `FilesystemState` and `SummarizationState` -- the same helper
  `create_deep_agent` uses at `graph.py:941`. `is_private_key` is kept as a
  cheap superset for middleware this module does not import, and `strip_state`
  applies both.
- **LIBRARY LIMITATION: a compiled agent graph does not expose its middleware.**
  `CompiledStateGraph` has no `.middleware` attribute, and `graph.nodes` lists
  only middleware with a node-producing hook -- for this stack just
  `PatchToolCallsMiddleware.before_agent`. `SummarizationMiddleware` implements
  only `wrap_model_call`, so it never appears. deepagents builds the stack in a
  local (`deepagents/graph.py:862`) and passes it into `create_agent`
  (`graph.py:956`), which closes over it. The probe therefore taps
  `deepagents.graph.create_agent` (read-only, original always called and
  restored) to read the assembled stack. **Any runtime harness that needs to
  assert on its own middleware stack must do the same, or keep its own
  references to the instances it passed in** -- which is the cheaper option and
  what `build_planner`'s caller should do.
- **LIBRARY LIMITATION: excluded tools are not visible on the graph either.**
  The tool node still registers `ls`/`glob`/`grep`/`execute`/`edit_file`/`delete`;
  only `_ToolExclusionMiddleware.wrap_model_call` removes them from
  `request.tools`, and `wrap_tool_call` rejects a call naming one with
  `"Error: <name> is not available."`. The probe reads the real list from the
  model's `bind_tools` during an actual invoke.
- **`AnthropicPromptCachingMiddleware` is always in the stack**
  (`append_prompt_caching_middleware`, `graph.py:905`), even for an
  OpenAI-compatible model. It is a no-op off Anthropic, but it will show up in
  any stack dump.
"""
    body = [
        "# deepagents probe",
        "",
        f"- deepagents `{deepagents.__version__}`",
        f"- probe: `scripts/probe_deepagents.py`, compat layer: `src/harness/deepagents_compat.py`",
        "- run offline against a fake chat model; no server, no GPU, no network",
        "",
    ]
    for title, text in rep.sections:
        body.append(f"## {title}")
        body.append("")
        body.append(text.rstrip())
        body.append("")
    body.append("## Exact import paths used")
    body.append("")
    body.append(imports.rstrip())
    body.append("")
    body.append("## Deviations from the plan / library facts to carry forward")
    body.append("")
    body.append(deviations.rstrip())
    body.append("")
    body.append("## Result")
    body.append("")
    if rep.failures:
        body.append("**FAILED checks:**")
        body.append("")
        body.extend(f"- {f}" for f in rep.failures)
    else:
        body.append("All checks passed.")
    body.append("")
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.write_text("\n".join(body))


def main() -> int:
    rep = Report()
    probe_planner(rep)
    probe_wrapper(rep)
    probe_dead_editables(rep)
    write_note(rep)
    print(f"\nnote written: {NOTE_PATH.relative_to(REPO_ROOT)}")
    if rep.failures:
        print(f"FAILED {len(rep.failures)} check(s):")
        for f in rep.failures:
            print(f"  - {f}")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
