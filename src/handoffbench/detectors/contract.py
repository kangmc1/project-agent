"""D2: handoff-contract checker. obligations -> survival in artifact -> adherence by receiver -> fault labels."""
from __future__ import annotations

import json
from typing import Any

from handoffbench.llm import LLM
from handoffbench.detectors import prompts as P

SENDER_FAULT_FROM_SURVIVAL = {"absent": "S1", "weakened": "S2", "corrupted": "S3"}


def _fmt_obligations(obs: list[dict]) -> str:
    return "\n".join(f"- {o['id']} [{o['type']}] {o['text']}" for o in obs)


def contract_check(llm: LLM, rendered: dict[str, Any], stages: tuple[str, ...] = ("obligations", "survival", "adherence"), think_judgement: bool = True) -> dict[str, Any]:
    """think_judgement: enable the model's thinking mode for the survival/adherence judgement calls (not for extraction)."""
    task, ctx, art, beh = rendered["task"], rendered["sender_context"], rendered["artifact"], rendered["receiver_behavior"]
    out: dict[str, Any] = {}
    obs = llm.chat_json(P.SYSTEM, P.OBLIGATIONS.format(task=task, sender_context=ctx)).get("obligations", [])
    obs = [o for o in obs if isinstance(o, dict) and "id" in o and "text" in o]
    out["obligations"] = obs
    if "survival" in stages and obs:
        svr = llm.chat_json(P.SYSTEM, P.SURVIVAL.format(task=task, obligations=_fmt_obligations(obs), artifact=art), thinking=think_judgement, max_tokens=6000)
        sv = svr.get("survival", []) if isinstance(svr, dict) else []
        out["survival"] = {s["id"]: s for s in sv if isinstance(s, dict) and "id" in s}
        out["artifact_claims"] = [c for c in (svr.get("artifact_claims", []) if isinstance(svr, dict) else []) if isinstance(c, dict)]
    if "adherence" in stages and obs:
        ad = llm.chat_json(P.SYSTEM, P.ADHERENCE.format(task=task, obligations=_fmt_obligations(obs), artifact=art, receiver_behavior=beh), thinking=think_judgement, max_tokens=6000)
        out["adherence"] = {s["id"]: s for s in ad.get("adherence", []) if isinstance(s, dict) and "id" in s}
        out["receiver_deviate"] = bool(ad.get("receiver_deviate"))
        out["receiver_false_report"] = bool(ad.get("receiver_false_report"))
        out["adherence_notes"] = ad.get("notes", "")
    out.update(aggregate(out))
    return out


def aggregate(res: dict[str, Any]) -> dict[str, Any]:
    faults: set[str] = set()
    items: list[str] = []
    obs_by_id = {o["id"]: o for o in res.get("obligations", [])}
    for oid, s in res.get("survival", {}).items():
        code = SENDER_FAULT_FROM_SURVIVAL.get(str(s.get("status", "")).lower())
        if code:
            faults.add(code); items.append(f"{code}:{obs_by_id.get(oid, {}).get('text', oid)}")
    for c in res.get("artifact_claims", []):
        if str(c.get("status", "")).lower() in ("unsupported", "contradicted"):
            faults.add("S3"); items.append(f"S3:{c.get('claim', '')}")
    for oid, s in res.get("adherence", {}).items():
        if str(s.get("status", "")).lower() == "violated":
            surv = str(res.get("survival", {}).get(oid, {}).get("status", "")).lower()
            otype = str(obs_by_id.get(oid, {}).get("type", ""))
            # receiver fault only if the obligation actually reached the receiver and is a hard item (not a soft goal)
            if surv in ("preserved", "weakened", "") and otype in ("constraint", "fact", "prohibition"):
                faults.add("R1"); items.append(f"R1:{obs_by_id.get(oid, {}).get('text', oid)}")
    if res.get("receiver_deviate"):
        faults.add("R2")
    if res.get("receiver_false_report"):
        faults.add("R3")
    sender = any(f.startswith("S") for f in faults)
    receiver = any(f.startswith("R") for f in faults)
    resp = "both" if sender and receiver else "sender" if sender else "receiver" if receiver else "none"
    return {"faults": sorted(faults) or ["N0"], "responsibility": resp, "fault_items": items}
