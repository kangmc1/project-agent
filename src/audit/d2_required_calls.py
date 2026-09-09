"""D2 rule 2 — instruction -> action coverage (label-free, deterministic).

For every handoff (planner wrapper call -> subagent steps until the planner's next step), derive from the planner's
INSTRUCTION which tool families the subagent must call, and check the subagent's actual tool calls inside the handoff.
The score is attached to the subagent's REPORT step (its last step in the handoff, normally a no_tool step): 1 if some
required family was never called ("ended early"), else 0. This is the third handoff boundary (instruction -> actions);
D3 covers instruction -> premise (text) and report -> planner (text). Motivation (2026-09-09 05:55): subagent no_tool is
structurally "report and return" (260/260 followed by a planner step), so the question is not the confidence of ending
but whether the requested work was done before ending. D2 rule 1 judges the utterance ("numbers need tool evidence");
this rule judges the instruction.

Output: audit/d2_required_calls.jsonl   Usage: python -m src.audit.d2_required_calls [--runs runs]
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

WRAPPERS = {"policy_checker", "db_agent", "solver", "verifier"}
AUX = {"user_sim", "summarizer"}
AUDIT = Path("audit")
REPORTED_FAILURE = re.compile(r"\b(no (?:direct|one-stop|available|matching|such)?\s*(?:flights?|reservations?|results?|options?) (?:were |was )?(?:found|available)|not available|unable to|could not|cannot proceed|can't proceed|not found|does not exist|failed)\b", re.I)

# family -> (instruction regex, tools that satisfy it — any one suffices)
AIRLINE_DB: list[tuple[str, re.Pattern, list[str]]] = [
    ("cancel", re.compile(r"\bcancel", re.I), ["cancel_reservation"]),
    ("book", re.compile(r"\b(book|reserve|make)\s+(?:a|an|the|one|two|three|\d+|new|economy|business|basic|round|one-way|tickets?|flights?|seats?|reservation)\b", re.I),
     ["book_reservation"]),
    ("price", re.compile(r"\b(current |latest |updated |new )?(prices?|fares?|costs?)\b", re.I),
     ["search_direct_flight", "search_onestop_flight", "book_reservation", "calculate"]),
    # flight SEARCH intent only: "search for flights", "available/alternative flights", "flight options"; NOT "the reservation's
    # flight details" (that is a reservation lookup). If the instruction is about an existing reservation/booking, its flight
    # details also come from get_reservation_details, so that tool satisfies the family too (see required_families).
    ("search_flights", re.compile(r"\b(search|look)\s+for\b[^.]{0,60}\bflights?\b|\b(available|alternative|one-stop|direct|nonstop|other|new)\s+flights?\b|\bflight options?\b|\bflight availability\b", re.I),
     ["search_direct_flight", "search_onestop_flight"]),
    ("reservation_lookup", re.compile(r"\b(retrieve|get|fetch|look\s*up|pull|check|find|search|verify|confirm)\b[^.]{0,80}\b(reservation|booking|confirmation code|itinerary)", re.I),
     ["get_reservation_details", "get_user_details"]),
    ("user_lookup", re.compile(r"\b(retrieve|get|fetch|look\s*up|pull|check|find|verify)\b[^.]{0,60}\b(user|profile|membership|payment method|customer'?s? (?:details|information|profile))", re.I),
     ["get_user_details"]),
    ("update_flights", re.compile(r"\b(update|change|modify|rebook|move)\b[^.]{0,60}\bflights?\b", re.I), ["update_reservation_flights"]),
    ("update_baggages", re.compile(r"\b(update|change|add|modify)\b[^.]{0,60}\bbag", re.I), ["update_reservation_baggages"]),
    ("update_passengers", re.compile(r"\b(update|change|modify|add|remove)\b[^.]{0,60}\bpassenger", re.I), ["update_reservation_passengers"]),
    ("calculate", re.compile(r"\b(calculate|compute|total (?:price|cost|amount)|price difference)\b", re.I), ["calculate"]),
    ("certificate", re.compile(r"\b(certificate|compensation|voucher)\b", re.I), ["send_certificate"]),
    ("transfer", re.compile(r"\btransfer\b[^.]{0,40}\bhuman", re.I), ["transfer_to_human_agents"]),
]
# AIME: solver/verifier are numeric agents by design — an instruction always requires at least one run_python.
AIME_ANY: list[tuple[str, re.Pattern, list[str]]] = [
    ("compute", re.compile(r".", re.S), ["run_python"]),
]


def required_families(agent: str, domain: str, instruction: str) -> list[dict]:
    if domain == "airline" and agent == "db_agent":
        rules = AIRLINE_DB
    elif domain == "aime" and agent in ("solver", "verifier"):
        rules = AIME_ANY
    else:
        return []  # policy_checker: policy text is in its prompt; no tool requirement derivable
    out = []
    about_reservation = bool(re.search(r"\b(reservation|booking|confirmation code|itinerary)\b", instruction or "", re.I))
    for fam, rx, tools in rules:
        if rx.search(instruction or ""):
            t = list(tools)
            if fam == "search_flights" and about_reservation:
                t.append("get_reservation_details")
            out.append({"family": fam, "tools": t})
    return out


def _handoffs(steps: list[dict]):
    """Yield (planner_step, wrapper, instruction, subagent_steps) — subagent steps of that wrapper between this planner
    step and the next planner step."""
    idx = [i for i, s in enumerate(steps) if s["agent"] == "planner"]
    for n, i in enumerate(idx):
        s = steps[i]
        end = idx[n + 1] if n + 1 < len(idx) else len(steps)
        between = steps[i + 1:end]
        for tc in (s["response"].get("tool_calls") or []):
            w = tc["function"]["name"]
            if w not in WRAPPERS:
                continue
            try:
                args = json.loads(tc["function"]["arguments"])
            except Exception:
                args = {}
            instr = args.get("instruction") if isinstance(args, dict) else None
            if not isinstance(instr, str):
                instr = json.dumps(args, ensure_ascii=False)
            sub = [x for x in between if x["agent"] == w]
            yield s["step_id"], w, instr, sub


def audit_run(run: Path) -> list[dict]:
    steps = [json.loads(l) for l in (run / "steps.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    steps = [s for s in steps if s["agent"] not in AUX]
    meta = json.loads((run / "meta.json").read_text()) if (run / "meta.json").exists() else {}
    domain = meta.get("domain", run.name.split("_")[0])
    rows = []
    for pstep, w, instr, sub in _handoffs(steps):
        req = required_families(w, domain, instr)
        if not sub:
            continue  # subagent trace missing/cut: nothing to attach the score to
        called = sorted({tc["function"]["name"] for x in sub for tc in (x["response"].get("tool_calls") or [])})
        missing = [r for r in req if not any(t in called for t in r["tools"])]
        report = sub[-1]
        # NOTE (07:35): an exemption for reports that state failure ("no flights found", "unable to") was tried and reverted —
        # it removed 8 false positives but also 5 true positives (incl. a decisive step) where the reported failure was caused
        # by the agent's own mistake. Failure wording cannot separate honest failure from self-inflicted failure, so it is only
        # recorded as a descriptive field here.
        report_text = report["response"].get("content") or ""
        reported_failure = bool(REPORTED_FAILURE.search(report_text))
        rows.append({"run_id": run.name, "domain": domain, "step_id": report["step_id"], "agent": w,
                     "planner_step_id": pstep, "n_subagent_steps": len(sub), "instruction": instr[:300],
                     "required": req, "called": called, "missing": missing,
                     "applicable": bool(req), "satisfied": (not missing) if req else None, "reported_failure": reported_failure,
                     "report_is_no_tool": not (report["response"].get("tool_calls") or [])})
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default="runs")
    a = ap.parse_args()
    AUDIT.mkdir(exist_ok=True)
    rows = []
    for run in sorted(Path(a.runs).glob("*/")):
        if (run / "steps.jsonl").exists():
            rows += audit_run(run)
    with (AUDIT / "d2_required_calls.jsonl").open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    n_app = sum(r["applicable"] for r in rows)
    n_uns = sum(1 for r in rows if r["satisfied"] is False)
    print(f"D2-instruction: handoffs {len(rows)}, applicable {n_app}, unsatisfied {n_uns}")


if __name__ == "__main__":
    main()
