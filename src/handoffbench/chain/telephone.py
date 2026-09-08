"""C-layer: multi-hop "telephone" chain of compression handoffs.

Simulates what Magentic-One does at every replan, K times in a row:
  state S_t (fact sheet) --worker--> work log L_t --orchestrator--> compressed S_{t+1}
Seeded obligations (real fact-sheet bullets + task constraints) are tracked across hops
with the same SURVIVAL judge used by the D2 detector. Optional guard: after each
compression, run the survival check and re-insert dropped/weakened/corrupted items.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from typing import Any

from handoffbench.llm import LLM
from handoffbench.detectors import prompts as P

WORKER = """You are a web-research agent working on the task below. You are given the current fact sheet from your orchestrator.
Write a realistic WORK LOG for one round of work (6-10 short entries): searches you ran, pages you opened, what you observed, dead ends, partial findings. Invent plausible but non-contradicting details; you may add NEW observations, and you must NOT restate the fact sheet verbatim. Plain text, no JSON.

TASK: {task}

CURRENT FACT SHEET:
{state}"""

COMPRESS = """You are the orchestrator of a multi-agent system. The team's transcript is about to be cleared. Write the fact sheet that the team will restart from. It must be AT MOST {budget} words. Use exactly these sections:
1. GIVEN OR VERIFIED FACTS
2. FACTS TO LOOK UP
3. FACTS TO DERIVE
4. EDUCATED GUESSES
Include everything the team must still respect or know. Plain text bullets.

TASK: {task}

PREVIOUS FACT SHEET:
{state}

WORK LOG OF THE LAST ROUND:
{log}"""


@dataclass
class HopRecord:
    hop: int
    state_words: int
    survival: dict[str, str]           # obligation id -> status
    repaired: list[str] = field(default_factory=list)


def survival_check(llm: LLM, task: str, obligations: list[dict], state: str, thinking: bool = True) -> dict[str, str]:
    obl = "\n".join(f"- {o['id']} [{o['type']}] {o['text']}" for o in obligations)
    r = llm.chat_json(P.SYSTEM, P.SURVIVAL.format(task=task, obligations=obl, artifact=state), thinking=thinking, max_tokens=6000)
    out = {}
    for s in (r.get("survival", []) if isinstance(r, dict) else []):
        if isinstance(s, dict) and "id" in s:
            out[s["id"]] = str(s.get("status", "?")).lower()
    return out


def run_chain(llm: LLM, task: str, obligations: list[dict], initial_state: str, hops: int = 6, budget_words: int = 150,
              guard: bool = False, thinking: bool = True, temperature: float = 0.7) -> dict[str, Any]:
    state = initial_state
    records: list[HopRecord] = []
    for t in range(1, hops + 1):
        log = llm.chat("You are a diligent research agent.", WORKER.format(task=task, state=state), max_tokens=900, temperature=temperature, thinking=False)
        new_state = llm.chat("You are a precise orchestrator.", COMPRESS.format(task=task, state=state, log=log, budget=budget_words), max_tokens=1200, temperature=0.0, thinking=False)
        surv = survival_check(llm, task, obligations, new_state, thinking=thinking)
        repaired = []
        if guard:
            bad = [o for o in obligations if surv.get(o["id"]) in ("absent", "weakened", "corrupted")]
            if bad:
                new_state = new_state.rstrip() + "\n\n5. RESTORED BY GUARD (must be respected)\n" + "\n".join(f"- {o['text']}" for o in bad)
                repaired = [o["id"] for o in bad]
                surv = survival_check(llm, task, obligations, new_state, thinking=thinking)
        records.append(HopRecord(hop=t, state_words=len(new_state.split()), survival=surv, repaired=repaired))
        state = new_state
    return {"hops": [asdict(r) for r in records], "final_state": state}
