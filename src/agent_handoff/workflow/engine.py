"""Closed-book multi-agent workflow engine.

One scenario run = rounds of (Orchestrator decides action -> agent acts -> report appended), with
context compression when the transcript exceeds a word budget, and a final deliverable.

Variables:
  visibility : "shared" (agents see initial transcript + all reports so far, or the compressed state after
               a compression) | "summary" (agents see only the current state + instruction)
  fmt        : compression format "free" | "json"
  budget     : word budget that triggers compression of the transcript
  guard      : re-insert seeded obligations missing from a compressed state (boundary checker)
  k_samples  : extra orchestrator samples per decision to estimate action-distribution entropy (0 = off)
Measurements per round: obligation survival in state (matcher), fabrication (new key-like values not in
initial transcript), action entropy; at the end: survival in the final deliverable, prohibition/constraint checks.
"""
from __future__ import annotations
import json, math, re, collections
from typing import Any
from agent_handoff.llm import LLM
from agent_handoff.matching import survival_report, score, _present
from agent_handoff.chain.stress import COMPRESS_FREE, COMPRESS_JSON, _repair
from agent_handoff.workflow import roles as R

NUMLIKE = re.compile(r"\$?\d[\d,.:/-]*\d|\b[A-Z][a-zA-Z]+(?: [A-Z][a-zA-Z]+)*\b")


def _entropy(counter: collections.Counter) -> float:
    n = sum(counter.values())
    return -sum((c / n) * math.log2(c / n) for c in counter.values()) if n else 0.0


def choose(llm: LLM, system: str, user: str, choices: list[str]) -> tuple[str, dict[str, float], float]:
    """Constrained decision over a fixed action set. Returns (argmax choice, probability over choices, entropy in bits).
    The distribution is read from the first-token logprobs under guided_choice (no sampling)."""
    r = llm.client.chat.completions.create(model=llm.model, temperature=0.0, max_tokens=4,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        logprobs=True, top_logprobs=20, extra_body={"guided_choice": choices, "chat_template_kwargs": {"enable_thinking": False}})
    llm.usage.add(r, 0.0)
    picked = (r.choices[0].message.content or "").strip()
    probs: dict[str, float] = {c: 0.0 for c in choices}
    try:
        for t in r.choices[0].logprobs.content[0].top_logprobs:
            tok = t.token.strip()
            if not tok:
                continue
            hits = [c for c in choices if c.lower().startswith(tok.lower())]
            if len(hits) == 1:
                probs[hits[0]] += math.exp(t.logprob)
    except Exception:
        pass
    z = sum(probs.values()) or 1.0
    probs = {k: v / z for k, v in probs.items()}
    ent = -sum(p * math.log2(p) for p in probs.values() if p > 0)
    if picked not in choices:
        picked = max(probs, key=probs.get)
    return picked, {k: round(v, 4) for k, v in probs.items()}, round(ent, 3)


NEG = re.compile(r"\b(not|never|no|avoid|without|do not|don't|must not|shouldn't|instead of|rather than|prohibited|forbidden|excluded?)\b", re.I)


def _violates(text: str, key_values: list[str]) -> bool:
    """A prohibition is counted as violated when its key value appears on a line with no negation (e.g. 'book via Booking.com')."""
    for ln in text.splitlines():
        if any(_present(v, ln) for v in key_values) and not NEG.search(ln):
            return True
    return False


def _fabricated_values(text: str, initial: str, task: str) -> list[str]:
    """Number-like tokens in `text` that appear nowhere in the initial transcript/task (proxy for invented facts)."""
    src = (initial + " " + task).lower()
    out = []
    for m in NUMLIKE.findall(text):
        tok = m.strip()
        if re.search(r"\d", tok) and len(tok) >= 3 and tok.lower() not in src and re.sub(r"[,]", "", tok).lower() not in src:
            out.append(tok)
    return sorted(set(out))


def run_workflow(llm: LLM, scenario: dict[str, Any], rounds: int = 8, visibility: str = "shared", fmt: str = "free",
                 budget: int = 400, guard: bool = False, k_samples: int = 0, temperature: float = 0.3) -> dict[str, Any]:
    task, obls, initial = scenario["task"], scenario["obligations"], scenario["transcript"]
    state = initial               # the orchestrator's handoff state (initially the raw transcript)
    transcript = [initial]        # what accumulates between compressions
    reports: list[dict] = []
    log = []
    n_compressions = 0
    for r in range(1, rounds + 1):
        # ---- orchestrator decision (structured action) ----
        rep_txt = "\n\n".join(f"[{x['agent']}] {x['report']}" for x in reports[-4:]) or "(none yet)"
        hist_txt = "\n".join(f"{e['round']}: {e['action']['next_agent']} / {e['action']['action_type']} / {e['action']['target']} -> {('VERDICT ' + e['verdict']) if e.get('verdict') else ('UNAVAILABLE' if any(k in (e.get('report') or '').upper() for k in ('UNAVAILABLE', 'MISSING:', 'CANNOT VERIFY')) else 'reported')}" for e in log) or "(none)"
        base = R.ORCH_DECIDE.format(task=task, state=state, reports=rep_txt, history=hist_txt, r=r, rounds=rounds)
        choices_all = list(R.AGENTS) + ["finish"]
        # (a) policy uncertainty: distribution over the 4 actions given the STATE ONLY (before any deliberation)
        _, p_agent, ent_agent = choose(llm, R.ORCH_SYSTEM, base + "\n\nDecide ONLY which agent acts next. Answer with one of: " + ", ".join(choices_all) + ".", choices_all)
        # (0) short deliberation, then the executed decision
        assess = llm.chat(R.ORCH_SYSTEM.replace("Reply with ONLY a JSON object.", "Reply in plain text."), base + "\n\n" + R.ORCH_ASSESS, thinking=False, max_tokens=220, temperature=0.0)
        ctx = base + "\n\nYOUR ASSESSMENT:\n" + assess
        choices = list(choices_all)
        masked = None
        # anti-loop masks: same agent+type with similar target twice in a row, or Researcher re-asking an UNAVAILABLE target
        def _sim(a, b):
            A = set(re.findall(r"[a-z0-9]+", a.lower())); B = set(re.findall(r"[a-z0-9]+", b.lower())); return len(A & B) / max(1, len(A | B))
        recent = [(e["action"]["next_agent"], e["action"]["action_type"], e["action"]["target"]) for e in log[-2:]]
        if len(recent) == 2 and recent[0][:2] == recent[1][:2] and _sim(recent[0][2], recent[1][2]) >= 0.5:
            masked = recent[0][0]; choices = [c for c in choices if c != masked]
        agent, _, _ = choose(llm, R.ORCH_SYSTEM, ctx + "\n\nNow decide ONLY which agent acts next. Answer with one of: " + ", ".join(choices) + ".", choices)
        # (b) action type: choices valid for that agent
        types = R.ACTIONS_FOR.get(agent, ["finish"])
        if len(types) > 1:
            atype, p_type, ent_type = choose(llm, R.ORCH_SYSTEM, ctx + f"\n\nThe next agent is {agent}. Decide ONLY the action type. Answer with one of: " + ", ".join(types) + ".", types)
        else:
            atype, p_type, ent_type = types[0], {types[0]: 1.0}, 0.0
        # (c) free-text target + instruction conditioned on the chosen action
        dec = llm.chat_json(R.ORCH_SYSTEM, base + f"\n\nDecided: next_agent={agent}, action_type={atype}. Now reply ONLY with {{\"target\": \"<item/claim>\", \"instruction\": \"<1-2 sentences>\"}}", thinking=False, max_tokens=300, temperature=0.0) if agent != "finish" else {}
        target = str(dec.get("target", "")); instr = str(dec.get("instruction", ""))
        # if this target was already reported UNAVAILABLE and the agent is the Researcher again, redirect to the Executor draft
        unavailable = [e["action"]["target"] for e in log if any(k in (e.get("report") or "").upper() for k in ("UNAVAILABLE", "MISSING:")) and e["action"]["next_agent"] == "Researcher"]
        if agent == "Researcher" and any(_sim(target, u) >= 0.5 for u in unavailable):
            masked = (masked or "") + "+unavailable_redirect"; agent = "Executor"; atype = "draft_action"; instr = "Draft the deliverable with the information available; mark '" + target + "' explicitly as unverified."
        entry = {"round": r, "action": {"next_agent": agent, "action_type": atype, "target": target, "instruction": instr},
                 "p_agent": p_agent, "entropy_agent": ent_agent, "p_type": p_type, "entropy_type": ent_type, "assessment": assess, "masked": masked}
        if agent == "finish" or atype == "finish":
            entry["finished"] = True; log.append(entry); break
        if agent not in R.AGENTS:
            agent = "Researcher"
        # ---- agent turn ----
        if visibility == "shared":
            visible = "CONTEXT (shared transcript):\n" + "\n\n".join(transcript) + ("\n\nREPORTS SO FAR:\n" + "\n\n".join(f"[{x['agent']}] {x['report']}" for x in reports) if reports else "")
        else:
            visible = "HANDOFF STATE FROM ORCHESTRATOR:\n" + state
        report = llm.chat(R.AGENT_SYSTEM[agent], R.AGENT_TURN.format(task=task, visible_context=visible, action_type=atype, target=target, instruction=instr), thinking=False, max_tokens=600, temperature=temperature)
        reports.append({"round": r, "agent": agent, "report": report})
        transcript.append(f"[Orchestrator -> {agent}] {instr}\n[{agent}] {report}")
        entry["report_agent"] = agent; entry["report"] = report
        entry["fabricated_in_report"] = _fabricated_values(report, initial, task)
        entry["verdict"] = ("APPROVE" if "VERDICT: APPROVE" in report.upper() else "REVISE" if "VERDICT: REVISE" in report.upper() else None) if agent == "Verifier" else None
        # ---- compression boundary ----
        words = sum(len(t.split()) for t in transcript)
        if words > budget:
            tmpl = COMPRESS_JSON if fmt == "json" else COMPRESS_FREE
            new_state = llm.chat("You are a precise orchestrator.", tmpl.format(task=task, state=state, log="\n\n".join(transcript[1:]) if len(transcript) > 1 else "(none)", budget=max(120, budget // 3)), thinking=False, max_tokens=1400, temperature=0.0)
            rep = survival_report(obls, new_state); repaired = []
            if guard:
                missing = [o for o in obls if rep.get(o["id"]) in ("absent", "altered", "promoted")]
                if missing:
                    new_state = _repair(new_state, fmt, missing); repaired = [o["id"] for o in missing]; rep = survival_report(obls, new_state)
            state = new_state; transcript = [state]; n_compressions += 1
            entry["compression"] = {"n": n_compressions, "words_before": words, "words_after": len(state.split()), "survival": rep, "score": score(rep), "repaired": repaired}
        entry["state_survival"] = survival_report(obls, state) if entry.get("compression") else None
        log.append(entry)
    final = llm.chat(R.ORCH_SYSTEM.replace("Reply with ONLY a JSON object.", "Reply in plain text."), R.ORCH_FINAL.format(task=task, state=state), thinking=False, max_tokens=400, temperature=0.0)
    final_rep = survival_report(obls, final)
    checks = {
        "constraints_kept": sum(1 for o in obls if o["type"] == "constraint" and final_rep[o["id"]] == "preserved"),
        "constraints_total": sum(1 for o in obls if o["type"] == "constraint"),
        "prohibitions_mentioned": sum(1 for o in obls if o["type"] == "prohibition" and final_rep[o["id"]] == "preserved"),
        "prohibitions_violated": sum(1 for o in obls if o["type"] == "prohibition" and _violates(final, o["key_values"])),
        "prohibitions_total": sum(1 for o in obls if o["type"] == "prohibition"),
        "open_promoted_in_final": sum(1 for o in obls if o["type"] == "open_question" and final_rep[o["id"]] == "promoted"),
        "fabricated_in_final": _fabricated_values(final, initial, task),
    }
    return {"scenario_id": scenario["id"], "domain": scenario["domain"], "visibility": visibility, "format": fmt, "budget": budget, "guard": guard,
            "rounds_run": len(log), "n_compressions": n_compressions, "log": log, "final": final, "final_survival": final_rep, "final_score": score(final_rep), "checks": checks,
            "verifier_revise": sum(1 for e in log if e.get("verdict") == "REVISE"), "verifier_approve": sum(1 for e in log if e.get("verdict") == "APPROVE")}
