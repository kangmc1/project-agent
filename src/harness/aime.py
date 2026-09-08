"""AIME 2026 graph: planner -> solver -> verifier wrapper tools, python execution, submit_answer."""
from __future__ import annotations

import time
from typing import Any

from langchain_core.messages import HumanMessage

from ..data.aime import load_aime2026
from .capture import RunContext
from .deepagents_compat import build_planner, build_subagent, default_backend, make_summarizer, make_wrapper_tool, register_qwen_profile
from .model import make_chat
from .tools import make_run_python, make_submit_answer

MAX_SECONDS = 15 * 60

PLANNER_PROMPT = """You coordinate solving an AIME problem (answer is an integer 0-999). You never compute yourself.
Procedure:
1. Send the full problem to `solver` and ask for a complete solution with the final integer answer and the key equations used.
2. Send the full problem (NOT the solver's answer) to `verifier` and ask for an independent solution and final integer.
3. If the two answers agree, call `submit_answer` with that integer. If they disagree, re-delegate to `solver` with the
   verifier's objection (at most 2 rounds), then submit the best-supported answer.
4. After `submit_answer`, reply with one line: 'Submitted <answer>.'
Do not call `submit_answer` more than once.
"""

SOLVER_PROMPT = """You are a careful competition mathematician. Begin your first message by restating the problem's premises
(3-5 bullet points: givens, constraints, what is asked). Then solve step by step, using `run_python` for every
non-trivial computation (arithmetic, enumeration, algebra checks). State each key equation explicitly on its own line.
Finish with exactly one line: FINAL ANSWER: <integer>.
"""

VERIFIER_PROMPT = """You independently solve the problem from scratch (you are NOT given anyone else's answer). Begin your first
message by restating the premises (3-5 bullet points). Solve step by step, using `run_python` to compute and to
brute-force check where possible. State key equations explicitly. Finish with exactly one line: FINAL ANSWER: <integer>.
"""


def build_aime(ctx: RunContext) -> dict[str, Any]:
    register_qwen_profile()
    backend = default_backend()
    store: dict[str, Any] = {}
    summ_chat = make_chat("summarizer", ctx)
    solver_graph = build_subagent(make_chat("solver", ctx), [make_run_python()], make_summarizer(summ_chat, backend), SOLVER_PROMPT, backend)
    verifier_graph = build_subagent(make_chat("verifier", ctx), [make_run_python()], make_summarizer(summ_chat, backend), VERIFIER_PROMPT, backend)

    def log_wrapper(name: str, instruction: str, report: str) -> None:
        ctx.log_tool("planner", name, {"instruction": instruction}, report, "ok", 0.0)

    solver_tool = make_wrapper_tool("solver", "Delegate the full problem to the solver; returns a worked solution with FINAL ANSWER.", solver_graph, log_fn=log_wrapper)
    verifier_tool = make_wrapper_tool("verifier", "Delegate the full problem to an independent verifier; returns its own solution with FINAL ANSWER.", verifier_graph, log_fn=log_wrapper)
    planner = build_planner(make_chat("planner", ctx), [solver_tool, verifier_tool, make_submit_answer(store)],
                            make_summarizer(summ_chat, backend), PLANNER_PROMPT, backend)
    return {"planner": planner, "store": store}


def run_aime(task_index: int, ctx: RunContext) -> dict[str, Any]:
    items = load_aime2026()
    item = next(i for i in items if str(i["id"]) == str(task_index)) if any(str(i["id"]) == str(task_index) for i in items) else items[int(task_index)]
    built = build_aime(ctx)
    planner, store = built["planner"], built["store"]
    t0 = time.time()
    cb = ctx.callback("planner")
    for chunk in planner.stream({"messages": [HumanMessage(content=f"Problem:\n{item['problem']}")]},
                                config={"recursion_limit": 200, "callbacks": [cb]}, stream_mode="values"):
        ctx.snapshot_state(chunk)
        if time.time() - t0 > MAX_SECONDS:
            break
    sub = store.get("submitted")
    return {"success": sub is not None and int(sub) == int(item["answer"]), "submitted": sub, "answer": item["answer"],
            "chat_model_starts": ctx.chat_model_starts, "task_index": task_index, "problem_id": item["id"]}
