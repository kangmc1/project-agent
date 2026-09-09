"""D3 — handoff 실행 가능성·수용 (procedural flag at the planner step that issues a delegation; user decision 2026-09-09).

Fidelity-style overlap measures (8B fact sets, LLM comparison, value-token coverage/Jaccard) did not separate labeled handoff
failures (all ~0.4-0.6 AUROC). The labeled failures were about the CONTENT of the handoff, not the amount transferred:
  (a) missing_identifier : the instruction asks the db_agent to look up / modify a reservation or user but carries no reservation
                           id (6-char code) and no user id (first_last_1234) — τ-bench has no tool that searches by name, so
                           the subagent cannot execute it. Not applicable to policy_checker (no identifiers needed) or to
                           pure flight searches (origin/destination/date suffice).
  (b) reissued_after_failure : the previous report of the same wrapper stated failure / impossibility, and the new instruction is
                           nearly the same as the previous one (normalized similarity >= 0.8) with no new identifier added —
                           the planner did not take the report in.
Fabricated values inside the instruction are NOT part of D3: D2 condition (2) already checks wrapper-call arguments.
D3 = 1 if (a) or (b), else 0, on every planner step that issues at least one wrapper call. Output: audit/d3_conditions.jsonl
Usage: python -m src.audit.d3_conditions [--runs runs]
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
from pathlib import Path

from .d2_rules import RESERVATION_ID, USER_ID
from .d3_handoff import _load_run, _load_text, _dedupe_wrapper_rows, _planner_wrapper_calls, _find_planner_step_id

AUDIT = Path("audit")
DB_LOOKUP = re.compile(r"\b(reservation|booking|confirmation code|itinerary|user|customer|passenger'?s? (?:details|profile|information|record)|profile|membership|cancel|update|modify|change|refund|upgrade)\b", re.I)
FLIGHT_SEARCH_ONLY = re.compile(r"\b(search|find|look for)\b[^.]{0,60}\b(flights?|flight options?|availability)\b", re.I)
FAILURE = re.compile(r"\b(not found|could not be found|no (?:such|matching|available) (?:reservation|user|function|tool|flight)s?|unable to|cannot|can't|could not|none of the (?:available )?(?:functions|tools)|does not exist|failed|no results?)\b", re.I)
USER_ID_LOOSE = re.compile(r"\b[a-z]+_[a-z]+(?:_\d{2,5})?\b")
# any code the planner explicitly labels as a reservation/booking/confirmation id (customers sometimes give non-6-char codes)
LABELED_CODE = re.compile(r"\b(?:reservation|booking|confirmation)\s*(?:id|code|number|#)?\s*[:#]?\s*['\"]?([A-Z0-9]{4,12})\b", re.I)


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", (s or "").lower())).strip()


def _has_identifier(instr: str) -> bool:
    if RESERVATION_ID.search(instr or "") or USER_ID.search(instr or "") or USER_ID_LOOSE.search(instr or ""):
        return True
    m = LABELED_CODE.search(instr or "")
    return bool(m and any(ch.isdigit() for ch in m.group(1)))


def missing_identifier(wrapper: str, instr: str) -> bool:
    if wrapper != "db_agent" or not instr:
        return False
    if _has_identifier(instr):
        return False
    if FLIGHT_SEARCH_ONLY.search(instr) and not re.search(r"\b(reservation|booking|user|customer|passenger)\b", instr, re.I):
        return False  # a flight search needs no id
    return bool(DB_LOOKUP.search(instr))


def audit_run(run: Path) -> list[dict]:
    steps, calls, meta = _load_run(run)
    domain = meta.get("domain", run.name.split("_")[0])
    rows = _dedupe_wrapper_rows(calls)
    pcalls = _planner_wrapper_calls(steps)
    handoffs = []
    for row in rows:
        try:
            args = json.loads(row["args_json"])
        except Exception:
            args = None
        pstep = _find_planner_step_id(pcalls, row["tool"], args, row["step_id"])
        if pstep is None:
            continue
        instr = (args or {}).get("instruction", "") if isinstance(args, dict) else _load_text(row["args_json"])
        handoffs.append({"planner_step_id": pstep, "wrapper": row["tool"], "instruction": str(instr), "report": _load_text(row["result_json"])})
    handoffs.sort(key=lambda h: h["planner_step_id"])
    out = []
    last_by_wrapper: dict[str, dict] = {}
    by_step: dict[int, dict] = {}
    for h in handoffs:
        a = missing_identifier(h["wrapper"], h["instruction"])
        b = False
        prev = last_by_wrapper.get(h["wrapper"])
        sim = None
        if prev is not None:
            sim = difflib.SequenceMatcher(None, _norm(prev["instruction"]), _norm(h["instruction"])).ratio()
            new_ids = set(RESERVATION_ID.findall(h["instruction"])) | set(USER_ID.findall(h["instruction"]))
            old_ids = set(RESERVATION_ID.findall(prev["instruction"])) | set(USER_ID.findall(prev["instruction"]))
            if FAILURE.search(prev["report"] or "") and sim >= 0.8 and not (new_ids - old_ids):
                b = True
        last_by_wrapper[h["wrapper"]] = h
        rec = by_step.setdefault(h["planner_step_id"], {"run_id": run.name, "domain": domain, "step_id": h["planner_step_id"], "agent": "planner",
                                                        "missing_identifier": False, "reissued_after_failure": False, "evidence": []})
        if a:
            rec["missing_identifier"] = True
            rec["evidence"].append(f"{h['wrapper']}: lookup/modification requested without reservation or user id: {h['instruction'][:120]!r}")
        if b:
            rec["reissued_after_failure"] = True
            rec["evidence"].append(f"{h['wrapper']}: re-issued after a failure report (similarity {sim:.2f}): {h['instruction'][:100]!r}")
    for rec in by_step.values():
        rec["d3"] = 1 if (rec["missing_identifier"] or rec["reissued_after_failure"]) else 0
        out.append(rec)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(); ap.add_argument("--runs", default="runs"); a = ap.parse_args()
    rows = []
    for run in sorted(Path(a.runs).glob("*/")):
        if (run / "steps.jsonl").exists() and (run / "tool_calls.sqlite").exists():
            rows += audit_run(run)
    AUDIT.mkdir(exist_ok=True)
    with (AUDIT / "d3_conditions.jsonl").open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"D3 conditions: planner delegation steps {len(rows)}, flagged {sum(r['d3'] for r in rows)} "
          f"(missing_identifier {sum(r['missing_identifier'] for r in rows)}, reissued_after_failure {sum(r['reissued_after_failure'] for r in rows)})")


if __name__ == "__main__":
    main()
