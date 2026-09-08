# deepagents probe

- deepagents `0.7.13`
- probe: `scripts/probe_deepagents.py`, compat layer: `src/harness/deepagents_compat.py`
- run offline against a fake chat model; no server, no GPU, no network

## Tool list the model sees

Captured from the fake model's `bind_tools` during one real `planner.invoke` -- `_ToolExclusionMiddleware` strips names at `wrap_model_call` time, so the compiled graph's tool node still holds them and static inspection of the graph would over-report.

- visible: `['read_file', 'write_file', 'dummy_probe_tool']`
- asserted absent: `['delete', 'edit_file', 'execute', 'glob', 'grep', 'ls', 'task']` -> leaked `[]`

## Middleware stack

Planner stack (in order): `['FilesystemMiddleware(name=FilesystemMiddleware)', '_DeepAgentsSummarizationMiddleware(name=SummarizationMiddleware)', 'PatchToolCallsMiddleware(name=PatchToolCallsMiddleware)', 'AnthropicPromptCachingMiddleware(name=AnthropicPromptCachingMiddleware)', '_ToolExclusionMiddleware(name=_ToolExclusionMiddleware)']`

SummarizationMiddleware instances: 1

- `_DeepAgentsSummarizationMiddleware` name=`SummarizationMiddleware` trigger=('tokens', 16000) keep=('messages', 8)

`SubAgentMiddleware` is absent, which is why no `task` tool exists.

## State keys

Worker graph channels: `['_summarization_event', '_summarization_session_id', 'files', 'jump_to', 'messages', 'structured_response']`

`files` comes from `FilesystemState` (`deepagents/middleware/filesystem.py:1090`): `files: Annotated[NotRequired[dict[str, FileData]], DeltaChannel(_file_data_delta_reducer, ...)]`, i.e. a `path -> FileData` mapping owned by `StateBackend`, merged by a delta reducer. It is a normal (non-private) channel, so it is forwarded into a wrapped graph and merged back out of it.

- `EXCLUDED_STATE_KEYS` = `['_deepagents_forked_context', '_summarization_event', '_summarization_session_id', 'jump_to', 'messages', 'structured_response', 'todos']`
- `PRIVATE_STATE_KEYS` (resolved from `PrivateStateAttr`) = `['_summarization_event', '_summarization_session_id', 'jump_to']`
- plus anything matching `is_private_key` (leading `_`)

`jump_to` is the trap: it is `PrivateStateAttr` (`langchain/agents/middleware/types.py:353`) with **no** leading underscore, and it is the agent loop's control channel. Filtering on the underscore convention alone would merge a worker's `jump_to` into the parent.

## Wrapper Command shape

```python
Command(update={
    **parent_state_minus_excluded_and_private,
    "messages": [ToolMessage(content=report, tool_call_id=runtime.tool_call_id)],
})
```

- parent state fed in: `['_summarization_session_id', 'files', 'jump_to', 'messages', 'todos']`
- observed update keys: `['files', 'messages']`
- `ToolMessage.tool_call_id` = `probe_call_1`
- `ToolMessage.content` = `'worker report body'`

`runtime: ToolRuntime` is injected positionally by the tool executor even with `infer_schema=False` -- the pydantic `args_schema` covers only `instruction`. Verified end-to-end: a planner whose model emits a `run_worker` tool call gets back a `ToolMessage` with the worker's report and the model's own `tool_call_id`. This mirrors deepagents' own `task` tool (`deepagents/middleware/subagents.py:832`).

Note: `tool.invoke({...})` called **directly** does NOT inject the runtime (`TypeError: missing 1 required positional argument: 'runtime'`) -- injection happens in the executor, so a direct probe must build a `ToolRuntime` itself.

## Dead editable installs

- `pip show agentbench` -> exit 1 (absent)
- `pip show agent-handoff` -> exit 1 (absent)
- `pip show handoffbench` -> exit 1 (absent)
- `pip show handoffcheck` -> exit 1 (absent)

## Exact import paths used

```python
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

## Deviations from the plan / library facts to carry forward

- **`SummarizationMiddleware` is an alias, not a class.** The concrete class is
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

## Result

All checks passed.
