"""P2 deferred check: the explicit SummarizationMiddleware (trigger 16k) actually fires on a long dialogue.
Builds a planner with one dummy tool, feeds ~20k tokens of prior turns, invokes once, and inspects the captured request."""
import json, sys, tempfile
from pathlib import Path
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from src.harness.capture import RunContext
from src.harness.model import make_chat
from src.harness.deepagents_compat import build_planner, default_backend, make_summarizer, register_qwen_profile

register_qwen_profile()
d = Path(tempfile.mkdtemp(prefix="summ_"))
ctx = RunContext(d)
class A(BaseModel):
    x: str = Field(..., description="anything")
noop = StructuredTool.from_function(func=lambda x: "ok", name="noop", description="does nothing", args_schema=A, infer_schema=False)
backend = default_backend()
chat = make_chat("planner", ctx)
planner = build_planner(chat, [noop], make_summarizer(make_chat("summarizer", ctx), backend), "You are a terse assistant. Answer in one short sentence.", backend)
filler = ("Customer detail line: reservation ZFA04Y, cabin economy, total $340, flight HAT136 on 2024-05-20. " * 12)
msgs = []
for i in range(40):
    msgs.append(HumanMessage(content=f"Turn {i}: " + filler))
    msgs.append(AIMessage(content=f"Ack {i}: noted " + filler[:300]))
msgs.append(HumanMessage(content="Finally: what was the reservation id? Answer in one sentence without tools."))
n_in_chars = sum(len(m.content) for m in msgs)
out = planner.invoke({"messages": msgs}, config={"recursion_limit": 20})
rows = [json.loads(l) for l in (d / "steps.jsonl").read_text().splitlines()]
agents = [r["agent"] for r in rows]
planner_rows = [r for r in rows if r["agent"] == "planner"]
req_chars = sum(len(json.dumps(m)) for m in planner_rows[-1]["request"]["messages"])
n_msgs_seen = len(planner_rows[-1]["request"]["messages"])
summary_present = any("summar" in json.dumps(m).lower() for m in planner_rows[-1]["request"]["messages"])
print(json.dumps({"input_chars": n_in_chars, "input_msgs": len(msgs)+1, "planner_request_msgs": n_msgs_seen, "planner_request_chars": req_chars,
                  "agents_called": agents, "summary_marker_in_request": summary_present,
                  "summarization_fired": n_msgs_seen < len(msgs) and ("summarizer" in agents or summary_present),
                  "final": out["messages"][-1].content[:120], "run_dir": str(d)}, indent=1))
sys.exit(0 if (n_msgs_seen < len(msgs)) else 1)
