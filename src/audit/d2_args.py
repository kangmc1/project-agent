"""D2 rule 3 — groundedness of TOOL-CALL ARGUMENTS (formerly D4 rule 2; moved into D2 = tool-call layer, 09-09 06:25) (label-free, deterministic).

Finding (2026-09-09 06:10): 38 of 49 hallucination_like subagent errors had D4 s = 1.0 because the fabricated values were
not in the utterance but in the arguments of the tool call (e.g. get_user_details(user_id='rossi_123') when the customer
gave only 'Rossi'). D4 rule 1 reads utterance text; this rule reads every tool-call argument the agent emitted at a step
and asks whether each identifier-like value was GIVEN to the agent: present in the non-assistant messages of that request
(system/user/instruction/tool results) or in earlier customer turns of the run. Arguments are structured JSON, so no LLM
extraction is needed. Score = fraction of identifier-like argument values that are ungrounded (0 = all given).

Checked value kinds (tau-bench conventions + AIME): reservation ids, user ids, flight numbers, ISO dates, money, IATA codes
under origin/destination keys, person names under *name* keys, and the final integer of submit_answer (must appear in a
prior run_python result). Skipped tools: run_python / file tools / think (code and prose, not claims).
Output: audit/d2_args.jsonl   Usage: python -m src.audit.d2_args [--runs runs]
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import sqlite3
from .d2_rules import RESERVATION_ID, FLIGHT_NO, MONEY, DATE

USER_ID = re.compile(r"\b[a-z]+(?:_[a-z]+)?_\d{2,5}\b")  # tau-bench first_last_1234; also catches invented 'rossi_123'
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]


def date_forms(iso: str) -> list[str]:
    """Natural-language forms a customer or instruction may have used for an ISO date."""
    try:
        y, m, d = iso.split("-"); mi, di = int(m), int(d)
    except Exception:
        return [iso]
    mon = MONTHS[mi - 1]
    return [iso, f"{mon} {di}", f"{mon} {di:02d}", f"{di} {mon}", f"{mon[:3]} {di}", f"{mi}/{di}", f"{mi:02d}/{di:02d}", f"{di}th of {mon}", f"{di}st of {mon}", f"{di}nd of {mon}", f"{di}rd of {mon}"]

AUX = {"user_sim", "summarizer"}


def _load_run(run: Path) -> tuple[list[dict], list[dict], dict]:
    steps = [json.loads(l) for l in (run / "steps.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    meta = json.loads((run / "meta.json").read_text()) if (run / "meta.json").exists() else {}
    con = sqlite3.connect(str(run / "tool_calls.sqlite"))
    calls = [dict(zip(["id", "step_id", "agent", "tool", "args_json", "result_json", "status", "latency", "ts"], r))
             for r in con.execute("SELECT id, step_id, agent, tool, args_json, result_json, status, latency, ts "
                                   "FROM tool_calls ORDER BY id")]
    con.close()
    return steps, calls, meta


def _norm(v: str) -> str:
    return v.replace(",", "").replace("$", "").strip().lower()


def _input_text(step: dict) -> str:
    """Concatenated non-assistant message contents of the request the model saw at this step."""
    parts = []
    for m in step.get("request", {}).get("messages") or []:
        if m.get("role") == "assistant":
            continue
        c = m.get("content")
        if isinstance(c, list):
            c = " ".join(x.get("text", "") for x in c if isinstance(x, dict))
        if c:
            parts.append(str(c))
    return "\n".join(parts)


SKIP_TOOLS = {"run_python", "read_file", "write_file", "edit_file", "think", "ls", "glob", "grep"}
AUDIT = Path("audit")
IATA_KEYS = {"origin", "destination", "departure_airport", "arrival_airport"}
IATA = re.compile(r"^[A-Z]{3}$")
AIRPORT_CITY: dict[str, list[str]] = {"SFO": ["san francisco"], "JFK": ["new york"], "LAX": ["los angeles"], "ORD": ["chicago"], "DFW": ["dallas"], "DEN": ["denver"], "SEA": ["seattle"], "ATL": ["atlanta"], "MIA": ["miami"], "BOS": ["boston"], "PHX": ["phoenix"], "IAH": ["houston"], "LAS": ["las vegas"], "MCO": ["orlando"], "EWR": ["newark"], "CLT": ["charlotte"], "MSP": ["minneapolis"], "DTW": ["detroit"], "PHL": ["philadelphia"], "LGA": ["laguardia"]}  # tau-bench list_all_airports


def _leaves(obj, key=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from _leaves(v, k)
    elif isinstance(obj, list):
        for v in obj:
            yield from _leaves(v, key)
    else:
        yield key, obj


def arg_values(tool: str, args_json: str) -> list[tuple[str, str]]:
    """(kind, value) pairs worth grounding, extracted from the argument JSON."""
    try:
        args = json.loads(args_json)
    except Exception:
        args = {"_raw": args_json}
    out: list[tuple[str, str]] = []
    if tool == "submit_answer":
        for k, v in _leaves(args):
            if isinstance(v, (int, float)) or (isinstance(v, str) and v.strip().isdigit()):
                out.append(("final_answer", str(v).strip()))
        return out
    for k, v in _leaves(args):
        if not isinstance(v, str):
            continue
        kl = (k or "").lower()
        if kl == "user_id" and v.strip():
            out.append(("user_id", v.strip()))
        if kl in IATA_KEYS and IATA.match(v.strip()):
            out.append(("airport", v.strip()))
        if "name" in kl and " " in v.strip() and len(v.strip()) <= 60:
            out.append(("name", v.strip()))
        out += [("reservation_id", m) for m in set(RESERVATION_ID.findall(v))]
        out += [("user_id", m) for m in set(USER_ID.findall(v))]
        out += [("flight_no", m) for m in set(FLIGHT_NO.findall(v))]
        out += [("date", m) for m in set(DATE.findall(v))]
        out += [("money", m.replace(",", "")) for m in set(MONEY.findall(v))]
    # dedupe
    seen = set(); res = []
    for kv in out:
        if kv not in seen:
            seen.add(kv); res.append(kv)
    return res


def audit_run(run: Path) -> list[dict]:
    steps, calls, meta = _load_run(run)
    domain = meta.get("domain", run.name.split("_")[0])
    user_sim = [(s["step_id"], s["response"].get("content") or "") for s in steps if s["agent"] == "user_sim"]
    results_by_step = {}
    for c in calls:
        results_by_step.setdefault(c["step_id"], []).append(_norm(c["result_json"] or ""))
    rows = []
    for s in steps:
        if s["agent"] in AUX:
            continue
        tcs = [tc for tc in (s["response"].get("tool_calls") or []) if tc["function"]["name"] not in SKIP_TOOLS]
        if not tcs:
            continue
        pool = _norm(_input_text(s))
        pool += "\n" + "\n".join(_norm(t) for sid, t in user_sim if sid < s["step_id"])
        prior_results = "\n".join(r for sid, rs in results_by_step.items() if sid < s["step_id"] for r in rs)
        vals, ungrounded = [], []
        for tc in tcs:
            tool = tc["function"]["name"]
            for kind, v in arg_values(tool, tc["function"]["arguments"]):
                nv = _norm(v)
                if kind == "final_answer":
                    ok = nv in prior_results  # the answer must come from a computation result
                elif kind == "name":
                    ok = nv in pool or all(part in pool for part in nv.split())
                elif kind == "date":
                    ok = any(f in pool for f in date_forms(nv))
                elif kind == "airport":
                    ok = nv in pool or any(c in pool for c in AIRPORT_CITY.get(v.strip().upper(), []))
                else:
                    ok = nv in pool
                vals.append({"tool": tool, "kind": kind, "value": v, "grounded": ok})
                if not ok:
                    ungrounded.append({"tool": tool, "kind": kind, "value": v})
        if not vals:
            continue
        rows.append({"run_id": run.name, "domain": domain, "step_id": s["step_id"], "agent": s["agent"],
                     "n_values": len(vals), "n_ungrounded": len(ungrounded),
                     "ungrounded_ratio": len(ungrounded) / len(vals), "ungrounded": ungrounded, "values": vals})
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default="runs")
    a = ap.parse_args()
    AUDIT.mkdir(exist_ok=True)
    rows = []
    for run in sorted(Path(a.runs).glob("*/")):
        if (run / "steps.jsonl").exists() and (run / "tool_calls.sqlite").exists():
            rows += audit_run(run)
    with (AUDIT / "d2_args.jsonl").open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"D2-args: steps {len(rows)}, values {sum(r['n_values'] for r in rows)}, "
          f"ungrounded {sum(r['n_ungrounded'] for r in rows)}, steps with any ungrounded {sum(r['n_ungrounded']>0 for r in rows)}")


if __name__ == "__main__":
    main()
