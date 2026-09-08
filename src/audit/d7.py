"""D7 - handoff fidelity: does information survive the planner <-> subagent (policy_checker/db_agent/solver/verifier)
round trip intact?

Handoffs are wrapper rows in tool_calls.sqlite (tool in WRAPPERS, args_json = {"instruction": ...}). Two rows are
compared for each handoff:

  direction "instruction->premise": A = facts in the instruction the planner sent; B = facts in the premise the
  subagent restates in the FIRST steps.jsonl row for that subagent after the planner step that issued the call.

  direction "report->planner": A = facts in the subagent's final report (the wrapper row's result_json); B = facts
  in what the planner does immediately after (its next step's response.content plus its next tool call's arguments,
  e.g. what it tells the user via respond_to_user).

missing/added are VALUE-level diffs (normalized, containment-tolerant); altered = same key, different value; fidelity = |A values present in B| / |A values|.

Output: audit/d7.jsonl (two rows per handoff).  --stats also writes audit/d7_stats.json.
Usage: python -m src.audit.d7 [--runs runs] [--run-id ID] [--stats] [--out audit/d7.jsonl]
"""
from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

from .extract import extract_atomic_facts, map_parallel

WRAPPERS = {"policy_checker", "db_agent", "solver", "verifier"}
AUDIT = Path("audit")


def _norm(v: str) -> str:
    return str(v).replace(",", "").replace("$", "").strip().lower()


def _load_run(run: Path) -> tuple[list[dict], list[dict], dict]:
    steps = [json.loads(l) for l in (run / "steps.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    meta = json.loads((run / "meta.json").read_text()) if (run / "meta.json").exists() else {}
    con = sqlite3.connect(str(run / "tool_calls.sqlite"))
    calls = [dict(zip(["id", "step_id", "agent", "tool", "args_json", "result_json", "status", "latency", "ts"], r))
             for r in con.execute("SELECT id, step_id, agent, tool, args_json, result_json, status, latency, ts "
                                   "FROM tool_calls ORDER BY id")]
    con.close()
    return steps, calls, meta


def _load_text(raw: str | None) -> str:
    """result_json / args_json values are JSON-encoded; unwrap a JSON string, else stringify whatever's there."""
    if not raw:
        return ""
    try:
        v = json.loads(raw)
    except Exception:
        return raw
    return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)


def _dedupe_wrapper_rows(calls: list[dict]) -> list[dict]:
    """The harness logs two sqlite rows per handoff (same step_id/tool/args_json): one with the subagent's clean
    text report as result_json, one with a raw `Command(update=...)` object repr. Keep the clean-text one."""
    groups: dict[tuple, list[dict]] = {}
    for c in calls:
        if c["tool"] not in WRAPPERS:
            continue
        groups.setdefault((c["step_id"], c["tool"], c["args_json"]), []).append(c)
    canon = []
    for rows in groups.values():
        rows_sorted = sorted(rows, key=lambda r: r["id"])
        pick = rows_sorted[0]
        for r in rows_sorted:
            try:
                v = json.loads(r["result_json"])
            except Exception:
                continue
            if isinstance(v, str) and not v.startswith("Command("):
                pick = r
                break
        canon.append(pick)
    return sorted(canon, key=lambda r: r["id"])


def _planner_wrapper_calls(steps: list[dict]) -> list[tuple[int, str, dict | None]]:
    out = []
    for s in steps:
        if s["agent"] != "planner":
            continue
        for tc in (s["response"].get("tool_calls") or []):
            name = tc["function"]["name"]
            if name not in WRAPPERS:
                continue
            try:
                args = json.loads(tc["function"]["arguments"])
            except Exception:
                args = None
            out.append((s["step_id"], name, args))
    return out


def _find_planner_step_id(planner_calls: list[tuple[int, str, dict | None]], tool: str, args: dict | None,
                           row_step_id: int) -> int | None:
    """Nearest preceding planner tool_call matching (tool, args). The wrapper row's step_id is normally the
    subagent's LAST step (strictly after the planner step that issued the call -- see module docstring), but
    allow equality too so a handoff whose subagent trace is empty/cut short still resolves."""
    best = None
    for step_id, name, a in planner_calls:
        if name != tool or step_id > row_step_id or a != args:
            continue
        if best is None or step_id > best:
            best = step_id
    return best


def _diff(a: dict, b: dict, raw_b: str = "") -> tuple[list[str], list[str], list[str], float | None]:
    # value-level comparison (robust to key-naming drift of the 8B extractor): a fact survives the boundary if its
    # normalized value appears in (or contains) any value on the other side. A value that appears literally in the raw
    # B text (e.g. inside the planner's next tool-call arguments) also counts as preserved — the 8B extractor misses
    # values in terse text such as "Submitted 277." (added 09-09 05:00). `added` still uses extracted B facts only.
    def _vals(d):
        return {_norm(v) for v in d.values() if v and _norm(v)}
    av, bv = _vals(a), _vals(b)
    raw = _norm(raw_b) if raw_b else ""
    def _present(v, pool):
        return any(v == w or (len(v) >= 3 and (v in w or w in v)) for w in pool)
    def _kept(v):
        return _present(v, bv) or (len(v) >= 2 and raw and v in raw)
    missing = sorted(v for v in av if not _kept(v))
    added = sorted(v for v in bv if not _present(v, av))
    altered = sorted(k for k in a if k in b and _norm(a[k]) != _norm(b[k]) and not _kept(_norm(a[k])))
    equal = sum(1 for v in av if _kept(v))
    fidelity = (equal / len(av)) if av else None
    return missing, added, altered, fidelity


def build_handoff(row: dict, steps_by_id: dict[int, dict], planner_steps: list[dict], subagent_first_step: dict | None,
                   planner_step_id: int | None, run_id: str, domain: str) -> list[dict]:
    tool = row["tool"]
    args = None
    try:
        args = json.loads(row["args_json"])
    except Exception:
        pass
    instruction = (args or {}).get("instruction", "") if isinstance(args, dict) else _load_text(row["args_json"])

    # direction: instruction -> premise
    A2 = extract_atomic_facts(instruction)
    if subagent_first_step is not None:
        premise = subagent_first_step["response"].get("content") or ""
        B_empty2 = not premise.strip()
    else:
        premise = ""
        B_empty2 = True
    B2 = extract_atomic_facts(premise) if premise.strip() else {}
    missing2, added2, altered2, fidelity2 = _diff(A2, B2, premise)

    # direction: report -> planner
    report = _load_text(row["result_json"])
    A1 = extract_atomic_facts(report)
    next_planner = next((s for s in planner_steps if s["step_id"] > row["step_id"]), None)
    if next_planner is not None:
        content = next_planner["response"].get("content") or ""
        tc_args = [tc["function"]["arguments"] for tc in (next_planner["response"].get("tool_calls") or [])]
        b1_text = "\n".join([content] + tc_args)
        B_empty1 = not b1_text.strip()
    else:
        b1_text = ""
        B_empty1 = True
    B1 = extract_atomic_facts(b1_text) if b1_text.strip() else {}
    missing1, added1, altered1, fidelity1 = _diff(A1, B1, b1_text)

    base = {"run_id": run_id, "domain": domain, "handoff_id": row["id"], "planner_step_id": planner_step_id,
            "wrapper": tool}
    return [
        {**base, "direction": "instruction->premise", "A": A2, "B": B2, "missing": missing2, "added": added2,
         "altered": altered2, "fidelity": fidelity2, "B_empty": B_empty2},
        {**base, "direction": "report->planner", "A": A1, "B": B1, "missing": missing1, "added": added1,
         "altered": altered1, "fidelity": fidelity1, "B_empty": B_empty1},
    ]


def audit_run(run: Path) -> list[dict]:
    steps, calls, meta = _load_run(run)
    domain = meta.get("domain", run.name.split("_")[0])
    wrapper_rows = _dedupe_wrapper_rows(calls)
    planner_calls = _planner_wrapper_calls(steps)
    planner_steps = [s for s in steps if s["agent"] == "planner"]

    def _one(row: dict) -> list[dict]:
        args = None
        try:
            args = json.loads(row["args_json"])
        except Exception:
            pass
        planner_step_id = _find_planner_step_id(planner_calls, row["tool"], args, row["step_id"])
        subagent_first_step = None
        if planner_step_id is not None:
            subagent_first_step = next(
                (s for s in steps if s["agent"] == row["tool"] and s["step_id"] > planner_step_id), None)
        return build_handoff(row, {}, planner_steps, subagent_first_step, planner_step_id, run.name, domain)

    results = map_parallel(_one, wrapper_rows)
    rows = []
    for r in results:
        rows.extend(r)
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default="runs")
    ap.add_argument("--run-id")
    ap.add_argument("--out", default=str(AUDIT / "d7.jsonl"))
    ap.add_argument("--stats", action="store_true")
    a = ap.parse_args()

    runs_dir = Path(a.runs)
    out_path = Path(a.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    for run in sorted(runs_dir.glob("*/")):
        if a.run_id and run.name != a.run_id:
            continue
        if not (run / "steps.jsonl").exists() or not (run / "tool_calls.sqlite").exists():
            continue
        rows.extend(audit_run(run))

    with out_path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"D7 done: {len(rows)} rows -> {out_path}")

    if a.stats:
        by_dir: dict[str, list[dict]] = {}
        for r in rows:
            by_dir.setdefault(r["direction"], []).append(r)
        out = {}
        d2rows = by_dir.get("instruction->premise", [])
        out["direction2_nonempty_ratio"] = (sum(1 for r in d2rows if not r["B_empty"]) / len(d2rows)) if d2rows else None
        for direction, rs in by_dir.items():
            fids = [r["fidelity"] for r in rs if r["fidelity"] is not None]
            out[f"mean_fidelity[{direction}]"] = (sum(fids) / len(fids)) if fids else None
            out[f"n[{direction}]"] = len(rs)
        (AUDIT / "d7_stats.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
        print("D7 stats:", json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
