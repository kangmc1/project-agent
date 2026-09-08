"""D1: holistic judge — one call, direct fault labels."""
from __future__ import annotations
from typing import Any
from handoffbench.llm import LLM
from handoffbench.detectors import prompts as P


def holistic_judge(llm: LLM, rendered: dict[str, Any]) -> dict[str, Any]:
    r = llm.chat_json(P.SYSTEM, P.HOLISTIC.format(task=rendered["task"], sender_context=rendered["sender_context"],
                                                  artifact=rendered["artifact"], receiver_behavior=rendered["receiver_behavior"]))
    faults = r.get("faults") or ["N0"]
    if isinstance(faults, str):
        faults = [faults]
    return {"faults": sorted(set(faults)), "responsibility": r.get("responsibility", "none"),
            "fault_items": r.get("dropped_or_corrupted_items", []), "explanation": r.get("explanation", "")}
