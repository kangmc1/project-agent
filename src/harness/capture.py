"""Full-observability capture for one run.

Everything the executing model actually saw is recorded from the raw HTTP layer:
  * request hook  -> messages, tools, extra body, X-Agent header
  * response hook -> content, tool_calls, generated-token logprobs, finish_reason, usage
Tool calls are recorded from LangChain callbacks into a per-run SQLite file, and
file-system / todo snapshots are dumped by the run loop via `snapshot_state`.
"""
from __future__ import annotations

import json
import sqlite3
import threading
import time
from pathlib import Path
from typing import Any, Callable

try:
    import httpx2 as hx
except ImportError:  # pragma: no cover
    import httpx as hx

from langchain_core.callbacks import BaseCallbackHandler


def approx_tokens(obj: Any) -> int:
    """Cheap token estimate used only for the summarization-drop heuristic."""
    return len(json.dumps(obj, ensure_ascii=False)) // 4


class RunContext:
    """Owns the artefacts of a single run directory."""

    def __init__(self, run_dir: str | Path, token_counter: Callable[[Any], int] | None = None):
        self.run_dir = Path(run_dir)
        self.run_dir.mkdir(parents=True, exist_ok=True)
        (self.run_dir / "fs").mkdir(exist_ok=True)
        (self.run_dir / "summarization_pre").mkdir(exist_ok=True)
        self.steps_path = self.run_dir / "steps.jsonl"
        self.db = sqlite3.connect(str(self.run_dir / "tool_calls.sqlite"), check_same_thread=False)
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS tool_calls (id INTEGER PRIMARY KEY, step_id INTEGER, agent TEXT, tool TEXT,"
            " args_json TEXT, result_json TEXT, status TEXT, latency REAL, ts REAL)"
        )
        self.db.commit()
        self.lock = threading.Lock()
        self.step_id = 0
        self.chat_model_starts = 0
        self.pending: dict[int, dict[str, Any]] = {}
        self.last_tokens_by_agent: dict[str, tuple[int, dict[str, Any], str]] = {}
        self.count_tokens = token_counter or approx_tokens
        self._open_tools: dict[str, dict[str, Any]] = {}
        self.last_agent = "planner"  # agent of the most recent LLM call = issuer of the next tool call
        self.skip_tools = {"policy_checker", "db_agent", "solver", "verifier"}  # wrappers log themselves via log_fn

    # ---------------- httpx event hooks ----------------
    def hooks(self) -> dict[str, list]:
        return {"request": [self._on_request], "response": [self._on_response]}

    def _on_request(self, request) -> None:
        path = str(request.url.path)
        if not (path.endswith("/chat/completions") or path.endswith("/completions")):
            return
        try:
            body = json.loads(request.content.decode("utf-8")) if request.content else {}
        except Exception:
            body = {"_raw": request.content.decode("utf-8", "replace")[:2000]}
        agent = request.headers.get("X-Agent", "unknown")
        self.pending[id(request)] = {"agent": agent, "body": body, "t0": time.time()}

    def _on_response(self, response) -> None:
        meta = self.pending.pop(id(response.request), None)
        if meta is None:
            return
        ctype = response.headers.get("content-type", "")
        try:
            response.read()
            data = response.json() if "json" in ctype else {"_non_json": response.text[:2000]}
        except Exception as e:  # pragma: no cover
            data = {"_error": repr(e)}
        choice = (data.get("choices") or [{}])[0] if isinstance(data, dict) else {}
        msg = choice.get("message") or {}
        body = meta["body"]
        with self.lock:
            self.step_id += 1
            sid = self.step_id
            agent = meta["agent"]
            msgs = body.get("messages", []) or []
            n_tok = self.count_tokens(msgs)
            thread_key = json.dumps(next((m.get("content") for m in msgs if m.get("role") == "user"), None))[:400]
            prev = self.last_tokens_by_agent.get(agent)
            if prev and prev[2] == thread_key and n_tok < 0.6 * prev[0]:
                # same conversation thread for the same agent shrank sharply -> summarization happened; keep the pre-summary body
                (self.run_dir / "summarization_pre" / f"step_{sid}.json").write_text(
                    json.dumps(prev[1], ensure_ascii=False), encoding="utf-8"
                )
            self.last_tokens_by_agent[agent] = (n_tok, body, thread_key)
            if agent not in ("user_sim", "summarizer"):
                self.last_agent = agent
            row = {
                "step_id": sid,
                "agent": agent,
                "ts": meta["t0"],
                "latency": time.time() - meta["t0"],
                "endpoint": str(response.request.url.path),
                "request": {
                    "messages": body.get("messages"),
                    "tools": body.get("tools"),
                    "extra": {k: v for k, v in body.items() if k not in ("messages", "tools")},
                },
                "response": {
                    "content": msg.get("content"),
                    "tool_calls": msg.get("tool_calls"),
                    "logprobs": choice.get("logprobs"),
                    "finish_reason": choice.get("finish_reason"),
                    "usage": data.get("usage") if isinstance(data, dict) else None,
                    "status_code": response.status_code,
                },
            }
            with self.steps_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")

    # ---------------- tool logging (LangChain callbacks) ----------------
    def log_tool(self, agent: str | None, tool: str, args: Any, result: Any, status: str, latency: float) -> None:
        agent = agent or self.last_agent
        with self.lock:
            self.db.execute(
                "INSERT INTO tool_calls (step_id, agent, tool, args_json, result_json, status, latency, ts) VALUES (?,?,?,?,?,?,?,?)",
                (self.step_id, agent, tool, json.dumps(args, ensure_ascii=False, default=str),
                 json.dumps(result, ensure_ascii=False, default=str)[:20000], status, latency, time.time()),
            )
            self.db.commit()

    def callback(self, agent: str) -> "ToolCallback":
        return ToolCallback(self, agent)

    # ---------------- state snapshots ----------------
    def snapshot_state(self, state: dict[str, Any]) -> None:
        payload = {k: state.get(k) for k in ("files", "todos") if k in state}
        if not payload:
            return
        (self.run_dir / "fs" / f"step_{self.step_id}.json").write_text(
            json.dumps(payload, ensure_ascii=False, default=str), encoding="utf-8"
        )

    def write_meta(self, **kw: Any) -> None:
        (self.run_dir / "meta.json").write_text(json.dumps(kw, ensure_ascii=False, indent=2, default=str), encoding="utf-8")

    def close(self) -> None:
        self.db.close()


class ToolCallback(BaseCallbackHandler):
    """Records tool start/end into the run's SQLite and counts chat-model starts."""

    def __init__(self, ctx: RunContext, agent: str):
        self.ctx = ctx
        self.agent = agent
        self._open: dict[str, tuple[str, Any, float]] = {}

    def on_chat_model_start(self, serialized, messages, *, run_id, **kwargs):  # type: ignore[override]
        with self.ctx.lock:
            self.ctx.chat_model_starts += 1

    def on_tool_start(self, serialized, input_str, *, run_id, inputs=None, **kwargs):  # type: ignore[override]
        name = (serialized or {}).get("name") or kwargs.get("name") or "tool"
        if name in self.ctx.skip_tools:
            return
        self._open[str(run_id)] = (name, inputs if inputs is not None else input_str, time.time())

    def on_tool_end(self, output, *, run_id, **kwargs):  # type: ignore[override]
        if str(run_id) not in self._open:
            return
        name, args, t0 = self._open.pop(str(run_id))
        out = getattr(output, "content", output)
        self.ctx.log_tool(None, name, args, out, "ok", time.time() - t0)

    def on_tool_error(self, error, *, run_id, **kwargs):  # type: ignore[override]
        if str(run_id) not in self._open:
            return
        name, args, t0 = self._open.pop(str(run_id))
        self.ctx.log_tool(None, name, args, repr(error), "error", time.time() - t0)


def make_http_client(ctx: RunContext, timeout: float = 600.0):
    return hx.Client(event_hooks=ctx.hooks(), timeout=timeout)
