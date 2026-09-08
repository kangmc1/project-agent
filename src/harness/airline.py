"""tau-bench airline graph: planner -> {policy_checker, db_agent} wrapper tools, shared FS case_notes.md."""
from __future__ import annotations

import time
from typing import Any

from langchain_core.messages import HumanMessage
from tau_bench.types import Action

from ..data.tau import make_airline_env
from ..data.tau_user import install_user_sim
from .capture import RunContext, make_http_client
from .deepagents_compat import build_planner, build_subagent, default_backend, make_summarizer, make_wrapper_tool, register_qwen_profile
from .model import make_chat
from .tools import make_think, openai_tool_to_structured, schema_to_model
from langchain_core.tools import StructuredTool
from pydantic import Field, create_model

MAX_TURNS = 30
MAX_SECONDS = 20 * 60

PLANNER_PROMPT = """You are the lead airline customer-service agent (planner). You talk to the customer ONLY through the
`respond_to_user` tool; every message you want the customer to see must be sent with it, and its return value is the
customer's next message. You never access the reservation database yourself.

Work method for each customer request:
1. Understand the request and gather identifying details (user id, reservation id) via `respond_to_user`.
2. Delegate policy questions to `policy_checker` (give it the exact situation and ask whether the action is allowed).
3. Delegate every database read/write to `db_agent` (give it precise instructions: which tool, which ids/values).
4. Keep `case_notes.md` up to date with facts, decisions and pending items using `write_file` / `read_file`.
5. Tell the customer the outcome with `respond_to_user`. Before any irreversible change, confirm with the customer.
When `respond_to_user` returns [CONVERSATION_ENDED], stop and write one line summarizing the case as your final answer.
Never invent reservation details, prices, or policy rules — obtain them from db_agent / policy_checker.
"""

POLICY_PROMPT_TMPL = """You are the airline policy checker. You receive a described situation and must decide whether the requested
action is allowed under the policy below. Begin your first message by restating the premises you were given
(3-5 bullet points: who, which reservation/flight, what is requested, relevant dates/cabin/membership), then reason
using the policy, and finish with exactly one line:
VERDICT: allowed | not_allowed | need_info — <policy clause(s) and a one-sentence justification>.
You have a `think` tool for scratch reasoning. You cannot access the database.

# Airline Agent Policy
{wiki}
"""

DB_PROMPT = """You are the airline database agent. You receive precise instructions from the planner and execute them with the
database tools. Begin your first message by restating the premises you were given (3-5 bullet points: ids, values,
requested operation), then call the tools. Report back exactly what the tools returned (ids, prices, dates, statuses)
without altering values, and clearly state anything that failed or was not found. Do not invent data.
"""


def build_airline(task_index: int, ctx: RunContext) -> dict[str, Any]:
    register_qwen_profile()
    env = make_airline_env(task_index=None)
    install_user_sim(env, client=make_http_client(ctx))
    backend = default_backend()
    state: dict[str, Any] = {"turns": 0, "done": False, "reward": None, "last_obs": None}

    # ---- db_agent tools (all tau-bench tools) ----
    db_tools = []
    for info in env.tools_info:
        name = info["function"]["name"]

        def _mk(n):
            def call(**kw):
                res = env.step(Action(name=n, kwargs=kw))
                if res.done:
                    state["done"] = True
                    state["reward"] = res.reward
                return res.observation
            return call
        db_tools.append(openai_tool_to_structured(info, _mk(name)))

    # ---- respond_to_user (planner) ----
    RespArgs = create_model("respond_to_user_Args", content=(str, Field(..., description="Message to send to the customer")))

    def respond_to_user(content: str) -> str:
        if state["done"]:
            return "[CONVERSATION_ENDED]"
        state["turns"] += 1
        res = env.step(Action(name="respond", kwargs={"content": content}))
        state["last_obs"] = res.observation
        if res.done or state["turns"] >= MAX_TURNS or (time.time() - state["t0"]) > MAX_SECONDS:
            state["done"] = True
            state["reward"] = res.reward if res.done else None
            return f"{res.observation}\n[CONVERSATION_ENDED]"
        return res.observation

    respond_tool = StructuredTool.from_function(func=respond_to_user, name="respond_to_user",
                                                description="Send a message to the customer and receive their reply.",
                                                args_schema=RespArgs, infer_schema=False)

    # ---- subagents ----
    pc_chat = make_chat("policy_checker", ctx)
    db_chat = make_chat("db_agent", ctx)
    summ_chat = make_chat("summarizer", ctx)
    pc_graph = build_subagent(pc_chat, [make_think()], make_summarizer(summ_chat, backend),
                              POLICY_PROMPT_TMPL.format(wiki=env.wiki), backend)
    db_graph = build_subagent(db_chat, db_tools, make_summarizer(summ_chat, backend), DB_PROMPT, backend)

    def log_wrapper(name: str, instruction: str, report: str) -> None:
        ctx.log_tool("planner", name, {"instruction": instruction}, report, "ok", 0.0)

    policy_tool = make_wrapper_tool("policy_checker", "Ask the policy checker whether a described action is allowed under airline policy. Provide the full situation.", pc_graph, log_fn=log_wrapper)
    db_tool = make_wrapper_tool("db_agent", "Delegate a precise database operation (lookups, bookings, changes, cancellations) to the database agent.", db_graph, log_fn=log_wrapper)

    planner_chat = make_chat("planner", ctx)
    planner = build_planner(planner_chat, [policy_tool, db_tool, respond_tool], make_summarizer(summ_chat, backend), PLANNER_PROMPT, backend)
    return {"env": env, "planner": planner, "state": state}


def run_airline(task_index: int, ctx: RunContext) -> dict[str, Any]:
    built = build_airline(task_index, ctx)
    env, planner, state = built["env"], built["planner"], built["state"]
    reset = env.reset(task_index=task_index)
    first_user = reset.observation
    state["t0"] = time.time()
    cb = ctx.callback("planner")
    final_state = None
    for chunk in planner.stream({"messages": [HumanMessage(content=f"[Customer]: {first_user}")]},
                                config={"recursion_limit": 200, "callbacks": [cb]}, stream_mode="values"):
        final_state = chunk
        ctx.snapshot_state(chunk)
    if state["reward"] is None:
        try:
            state["reward"] = env.calculate_reward().reward
        except Exception:
            state["reward"] = 0.0
    return {"success": bool(state["reward"] and state["reward"] >= 1.0), "reward": state["reward"],
            "turns": state["turns"], "chat_model_starts": ctx.chat_model_starts, "task_index": task_index}
