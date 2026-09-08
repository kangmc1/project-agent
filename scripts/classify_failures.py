"""Classify TraceElephant's 220 human-written failure reasons into failure types (data-driven problem definition)."""
import json, collections
from pathlib import Path
from handoffbench.llm import LLM
from handoffbench.data.traceelephant import iter_runs

CATS = {
 "hallucination": "agent asserted information not supported by any observation (fabricated fact, invented number/name, unsupported conclusion)",
 "reasoning_error": "agent had the correct information but inferred/calculated/interpreted it wrongly (logic, arithmetic, wrong unit, misread requirement)",
 "perception_error": "agent misread or misinterpreted an observation it actually had (page content, OCR, cell colours, transcription, table structure)",
 "tool_misuse": "agent used a tool wrongly: wrong tool, wrong arguments, wrong query, wrong website/section, did not use an available better tool (e.g. should have used Google Maps / Python)",
 "tool_env_failure": "the environment/tool failed independent of the agent: CAPTCHA, page not loading, site blocked, API error, OCR service wrong output",
 "planning_strategy": "wrong or inefficient overall approach: looping/repeating, giving up, exploring the wrong path, not decomposing the task, wasting rounds",
 "verification_failure": "accepted an answer/result without checking, did not double-check, premature termination, incorrect verification",
 "coordination_handoff": "problem at the boundary between agents: orchestrator delegated to the wrong agent, instruction omitted a needed constraint, context/plan lost at replanning, receiver ignored the instruction, wrong task decomposition across agents",
 "other": "none of the above",
}
SYS = "You classify failure descriptions of LLM agent runs. Reply with ONLY a JSON object."
PROMPT = """A multi-agent system ({system}) failed a task. A human annotator identified the responsible agent ({agent}) at step {step} and wrote this reason:

"{reason}"

Task: "{task}"

Classify the ROOT failure described by the reason. Categories:
{cats}

Reply: {{"primary": "<category>", "secondary": "<category or none>", "handoff_related": true|false, "why": "<=20 words"}}
handoff_related = true only if the reason involves the boundary between agents (delegation, instruction, replanning summary, ignored instruction)."""

llm = LLM()
out = []
cats_txt = "\n".join(f"- {k}: {v}" for k, v in CATS.items())
for run in iter_runs(Path("data/external/TraceElephant_data/data")):
    r = llm.chat_json(SYS, PROMPT.format(system=run.system, agent=run.mistake_agent, step=run.mistake_step, reason=run.mistake_reason, task=run.task_instruction[:300], cats=cats_txt), thinking=False, max_tokens=300)
    out.append({"run_id": run.run_id, "system": run.system, "mistake_agent": run.mistake_agent, "mistake_step": run.mistake_step, "reason": run.mistake_reason,
                "primary": r.get("primary"), "secondary": r.get("secondary"), "handoff_related": bool(r.get("handoff_related")), "why": r.get("why", "")})
Path("results").mkdir(exist_ok=True)
json.dump(out, open("results/traceelephant_failure_types.json", "w"), ensure_ascii=False, indent=1)
tot = collections.Counter(o["primary"] for o in out)
print("N =", len(out)); print("primary:", tot.most_common())
for s in sorted({o["system"] for o in out}):
    c = collections.Counter(o["primary"] for o in out if o["system"] == s); n = sum(c.values())
    print(f"  {s} (n={n}):", ", ".join(f"{k} {v/n:.0%}" for k, v in c.most_common()))
print("handoff_related:", sum(o["handoff_related"] for o in out), "| by mistake_agent=Orchestrator:", sum(o["handoff_related"] for o in out if o["mistake_agent"] == "Orchestrator"), "/", sum(1 for o in out if o["mistake_agent"] == "Orchestrator"))
print("usage", llm.usage.as_dict())
