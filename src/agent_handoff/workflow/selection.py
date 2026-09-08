"""B0: candidate selection handoff (task-unknown setting).

At the start, the orchestrator sees the full catalog (agents/skills with descriptions) and the task, and selects
3-4 candidates. Afterwards the catalog text is removed from all contexts: the team runs with the selected
candidates only, each mapped to a role slot (Researcher/Executor/Verifier) so the fixed-slot action space and
the probe still apply. Selection loss = required capabilities of the scenario that no selected candidate provides.
"""
from __future__ import annotations
import json
from typing import Any
from agent_handoff.llm import LLM

SELECT = """You are the Orchestrator assembling a team for the task below. From the CATALOG choose the 3-4 agents you will need (at least one per role: Researcher, Executor, Verifier when useful). After this step the catalog will no longer be visible; agents you do not select cannot be used later.

TASK:
{task}

CATALOG:
{catalog}

Reply with ONLY JSON: {{"selected": ["<id>", ...], "reason": "<one sentence>"}}"""


def load_catalog(path="data/catalog.jsonl") -> list[dict]:
    return [json.loads(l) for l in open(path)]


def select_team(llm: LLM, task: str, catalog: list[dict], max_n: int = 4) -> dict[str, Any]:
    cat_txt = "\n".join(f"- {c['id']} [{c['role_slot']}]: {c['description']}" for c in catalog)
    r = llm.chat_json("You assemble agent teams. Reply with ONLY JSON.", SELECT.format(task=task, catalog=cat_txt), thinking=False, max_tokens=300, temperature=0.0)
    ids = [x for x in (r.get("selected", []) if isinstance(r, dict) else []) if any(c["id"] == x for c in catalog)][:max_n]
    chosen = [c for c in catalog if c["id"] in ids]
    return {"selected": ids, "reason": (r.get("reason", "") if isinstance(r, dict) else ""), "chosen": chosen,
            "slots": sorted({c["role_slot"] for c in chosen}), "capabilities": sorted({cap for c in chosen for cap in c["capabilities"]})}


def selection_loss(selection: dict[str, Any], required: list[str]) -> dict[str, Any]:
    have = set(selection["capabilities"])
    missing = [cap for cap in required if cap not in have]
    return {"required": required, "missing": missing, "loss": len(missing) / max(1, len(required)), "slots_missing": [s for s in ("Researcher", "Executor", "Verifier") if s not in selection["slots"]]}
