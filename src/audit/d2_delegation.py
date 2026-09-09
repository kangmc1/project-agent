"""D2 — planner-side conditions of 행동 근거성 (user decision 2026-09-09): the planner's delegation (wrapper call) is a tool
call too, so D2's question "is this action one the record required and allowed?" is asked of it with two conditions:
  (a) missing_identifier     : the delegation asks db_agent to look up / modify a reservation or user but carries no reservation
                               code and no user id — τ-bench has no tool that searches by name, so the record does not allow the
                               subagent to execute it. Not applicable to policy_checker or to pure flight searches.
  (b) reissued_after_failure : the previous report of the same wrapper stated failure / impossibility and the new delegation is
                               nearly identical (normalized similarity >= 0.8, no new identifier) — the record (that report) does
                               not allow repeating the call. Fires mostly after the decisive step (a loop symptom).
Fabricated values inside the delegation text are already covered by D2 condition (2) (d2_args.py). Output: audit/d2_delegation.jsonl
Usage: python -m src.audit.d2_delegation [--runs runs]
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
from pathlib import Path

from .d2_rules import RESERVATION_ID, USER_ID
from .comparators.d3_factset import _load_run, _load_text, _dedupe_wrapper_rows, _planner_wrapper_calls, _find_planner_step_id

AUDIT = Path("audit")
DB_LOOKUP = re.compile(r"\b(reservation|booking|confirmation code|itinerary|user|customer|passenger'?s? (?:details|profile|information|record)|profile|membership|cancel|update|modify|change|refund|upgrade)\b", re.I)
FLIGHT_SEARCH_ONLY = re.compile(r"\b(search|find|look for)\b[^.]{0,60}\b(flights?|flight options?|availability)\b", re.I)
FAILURE = re.compile(r"\b(not found|could not be found|no (?:such|matching|available) (?:reservation|user|function|tool|flight)s?|unable to|cannot|can't|could not|none of the (?:available )?(?:functions|tools)|does not exist|failed|no results?)\b", re.I)
USER_ID_LOOSE = re.compile(r"\b[a-z]+_[a-z]+(?:_\d{2,5})?\b")
# any code the planner explicitly labels as a reservation/booking/confirmation id (customers sometimes give non-6-char codes)
LABELED_CODE = re.compile(r"(?i:reservation|booking|confirmation)\s*(?i:id|code|number|#)?\s*[:#]?\s*['\"]?([A-Z0-9]{4,12})\b")  # code must be UPPERCASE/digits


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", (s or "").lower())).strip()


def _has_identifier(instr: str) -> bool:
    if RESERVATION_ID.search(instr or "") or USER_ID.search(instr or "") or USER_ID_LOOSE.search(instr or ""):
        return True
    for m in LABELED_CODE.finditer(instr or ""):
        code = m.group(1)
        if code.upper() == code and not code.isalpha() or (code.isalpha() and code.isupper() and len(code) >= 5):
            return True
    return False


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
        rec["d2_planner"] = 1 if (rec["missing_identifier"] or rec["reissued_after_failure"]) else 0
        out.append(rec)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(); ap.add_argument("--runs", default="runs"); a = ap.parse_args()
    rows = []
    for run in sorted(Path(a.runs).glob("*/")):
        if (run / "steps.jsonl").exists() and (run / "tool_calls.sqlite").exists():
            rows += audit_run(run)
    AUDIT.mkdir(exist_ok=True)
    with (AUDIT / "d2_delegation.jsonl").open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"D2 delegation conditions: planner delegation steps {len(rows)}, flagged {sum(r['d2_planner'] for r in rows)} "
          f"(missing_identifier {sum(r['missing_identifier'] for r in rows)}, reissued_after_failure {sum(r['reissued_after_failure'] for r in rows)})")


if __name__ == "__main__":
    main()
