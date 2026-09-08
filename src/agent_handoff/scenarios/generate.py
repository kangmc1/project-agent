"""Generate synthetic scenarios with the local model, validate them by rules."""
from __future__ import annotations
import json, random
from agent_handoff.llm import LLM
from agent_handoff.scenarios.schema import Scenario, Obligation, validate

DOMAINS = {
    "customer_support": "an e-commerce / airline / telecom customer-support case handled by an orchestrator agent that delegates to a lookup agent and an action agent (refunds, rebooking, plan changes), with company policy rules",
    "coding": "a software maintenance task (bug fix or small feature) where an orchestrator delegates to a code-reading agent and a code-editing agent, with repository conventions, test requirements and a production-safety rule",
    "research": "a fact-finding research question (dates, quantities, named entities) where an orchestrator delegates web searches and file reading to worker agents, with a temporal/scope constraint from the user",
    "scheduling": "a travel / event / logistics planning task where an orchestrator delegates calendar, booking and map lookups, with budget, time-window and preference constraints from the user",
}

PROMPT = """Create ONE realistic scenario for a benchmark about information loss when AI agents hand work to each other.

Domain: {domain_desc}

Write:
1. `task`: the user's original request (2-4 sentences). It must contain at least two hard constraints (numbers, dates, formats, scopes) and one explicit prohibition (something the agents must NOT do).
2. `transcript`: a realistic prior interaction of 350-600 words between an Orchestrator and worker agents (e.g. Lookup, Browser, Coder, Executor). Use the format "[Orchestrator] ...", "[Lookup] ...", with tool results shown as "[Lookup] Result: ...". The transcript must establish, in natural language:
   - at least 3 VERIFIED facts that come from tool results (with concrete values: ids, numbers, dates, names),
   - at least 2 OPEN questions that a worker explicitly reports as NOT yet verified / could not confirm / assumed,
   - the constraints and the prohibition from the task restated or applied.
   Make it messy and realistic: partial results, one dead end, one correction.
3. `obligations`: exactly 8 items: 2 constraint, 3 verified_fact, 2 open_question, 1 prohibition. Each item:
   - `id`: o1..o8
   - `type`
   - `text`: one self-contained sentence a downstream agent must know/respect
   - `key_span`: an EXACT substring copied verbatim from the transcript (or task) that establishes it (10-60 words)
   - `key_values`: 1-3 distinctive tokens from that span (numbers, ids, names, dates) that must survive any summary

Reply with ONLY a JSON object: {{"task": "...", "transcript": "...", "obligations": [...]}}
Seed for variety: {seed}"""


def generate_one(llm: LLM, domain: str, idx: int, seed: str) -> tuple[Scenario | None, list[str]]:
    r = llm.chat_json("You write realistic multi-agent interaction data. Reply with ONLY JSON.", PROMPT.format(domain_desc=DOMAINS[domain], seed=seed), thinking=False, max_tokens=3500, temperature=0.9)
    if not isinstance(r, dict) or "obligations" not in r:
        return None, ["bad json"]
    try:
        obls = [Obligation(id=o["id"], type=o["type"], text=o["text"], key_span=str(o.get("key_span", "")), key_values=[str(v) for v in o.get("key_values", [])]) for o in r["obligations"]]
    except (KeyError, TypeError) as e:
        return None, [f"bad obligation: {e}"]
    sc = Scenario(id=f"{domain}_{idx:02d}", domain=domain, task=str(r.get("task", "")), transcript=str(r.get("transcript", "")), obligations=obls)
    return sc, validate(sc)
