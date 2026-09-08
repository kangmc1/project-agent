"""C-layer v2: K-hop compression stress test on synthetic scenarios.

state_0 = scenario transcript (or a fact sheet built from it)
hop t : worker writes a work log given state_{t-1}  ->  orchestrator compresses (state_{t-1}, log_t) into state_t
formats:
  free : free-text fact sheet (Magentic-One style sections), <= budget words
  json : structured JSON {constraints[], verified_facts[], open_questions[], prohibitions[], goal}
         every item {"text", "status": "verified"|"unverified"|"extraction_failed", "source"}; <= budget words
guard : after each compression, rule matcher checks seeded obligations; absent/altered/promoted items are re-inserted
Survival is judged by the rule matcher only (agent_handoff.matching).
"""
from __future__ import annotations
import json
from dataclasses import asdict
from typing import Any
from agent_handoff.llm import LLM
from agent_handoff.matching import survival_report, score

WORKER = """You are a worker agent continuing the task below. You are given the current handoff state from your orchestrator.
Write a realistic WORK LOG for one round (6-10 short entries): tool calls you made, results (invent plausible concrete details that do not contradict the state), one partial finding, one dead end. Do NOT restate the handoff state. Plain text.

TASK: {task}

HANDOFF STATE:
{state}"""

COMPRESS_FREE = """You are the orchestrator. The transcript will be cleared; write the handoff state the team restarts from, in AT MOST {budget} words. Use these sections:
1. GIVEN OR VERIFIED FACTS
2. FACTS TO LOOK UP / UNVERIFIED
3. CONSTRAINTS AND PROHIBITIONS
4. NEXT STEPS
Include everything the team must still respect or know. Plain text bullets.

TASK: {task}

PREVIOUS HANDOFF STATE:
{state}

WORK LOG OF THE LAST ROUND:
{log}"""

COMPRESS_JSON = """You are the orchestrator. The transcript will be cleared; write the handoff state the team restarts from as ONE JSON object, AT MOST {budget} words of text inside it:
{{"constraints": [{{"text": "...", "status": "verified|unverified|extraction_failed"}}],
 "verified_facts": [{{"text": "...", "status": "verified", "source": "tool/step"}}],
 "open_questions": [{{"text": "...", "status": "unverified"}}],
 "prohibitions": [{{"text": "...", "status": "verified"}}],
 "goal": "..."}}
Rules: a fact goes to verified_facts ONLY if a tool result established it; anything assumed or not yet confirmed goes to open_questions with status "unverified"; if you cannot recover a value, write the item with status "extraction_failed" instead of dropping or guessing it. Reply with ONLY the JSON.

TASK: {task}

PREVIOUS HANDOFF STATE:
{state}

WORK LOG OF THE LAST ROUND:
{log}"""


def _repair(state: str, fmt: str, missing: list[dict]) -> str:
    if not missing:
        return state
    if fmt == "json":
        try:
            obj = json.loads(state[state.find("{"): state.rfind("}") + 1])
            key = {"constraint": "constraints", "verified_fact": "verified_facts", "open_question": "open_questions", "prohibition": "prohibitions"}
            for o in missing:
                obj.setdefault(key[o["type"]], []).append({"text": o["text"], "status": "unverified" if o["type"] == "open_question" else "verified", "source": "restored_by_guard"})
            return json.dumps(obj, ensure_ascii=False, indent=1)
        except Exception:
            pass
    return state.rstrip() + "\n\n5. RESTORED BY GUARD (must be respected)\n" + "\n".join(f"- [{o['type']}] {o['text']}" for o in missing)


def run_stress(llm: LLM, scenario: dict[str, Any], fmt: str = "free", hops: int = 8, budget: int = 150, guard: bool = False, temperature: float = 0.7) -> dict[str, Any]:
    task, obls = scenario["task"], scenario["obligations"]
    state = scenario["transcript"]
    records = []
    for t in range(1, hops + 1):
        log = llm.chat("You are a diligent worker agent.", WORKER.format(task=task, state=state), max_tokens=700, temperature=temperature, thinking=False)
        tmpl = COMPRESS_JSON if fmt == "json" else COMPRESS_FREE
        new_state = llm.chat("You are a precise orchestrator.", tmpl.format(task=task, state=state, log=log, budget=budget), max_tokens=1400, temperature=0.0, thinking=False)
        rep = survival_report(obls, new_state)
        repaired = []
        if guard:
            missing = [o for o in obls if rep.get(o["id"]) in ("absent", "altered", "promoted")]
            if missing:
                new_state = _repair(new_state, fmt, missing)
                repaired = [o["id"] for o in missing]
                rep = survival_report(obls, new_state)
        records.append({"hop": t, "words": len(new_state.split()), "survival": rep, "score": score(rep), "repaired": repaired, "log": log, "state": new_state})
        state = new_state
    return {"scenario_id": scenario["id"], "domain": scenario["domain"], "format": fmt, "budget": budget, "guard": guard, "hops": records, "final_state": state}
