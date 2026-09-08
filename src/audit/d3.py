"""D3 — tool-called / tool-log checks (deterministic, label-free).

For every assistant utterance: which tool evidence do its claims require (d3_rules), and was such a tool called
with a result BEFORE the utterance (value must appear in the result when the claim carries a value)?
Plus five tool-log checks per tool call: error, empty, repeat, schema violation, ignored error.
Output: audit/d3.jsonl (one row per step or tool call).   Usage: python -m src.audit.d3 [--runs runs]
"""
from __future__ import annotations

import argparse
import json
import sqlite3
from collections import Counter
from pathlib import Path

from .d3_rules import extract_claims, rules_for

AUX = {"user_sim", "summarizer"}
AUDIT = Path("audit")


def _norm(v: str) -> str:
    return v.replace(",", "").replace("$", "").strip().lower()


def _validate_args(args: dict, schema: dict) -> list[str]:
    errs = []
    props = (schema or {}).get("properties", {}) or {}
    for req in (schema or {}).get("required", []) or []:
        if req not in args:
            errs.append(f"missing:{req}")
    types = {"string": str, "integer": int, "number": (int, float), "boolean": bool, "array": list, "object": dict}
    for k, v in (args or {}).items():
        if k not in props:
            errs.append(f"unknown:{k}")
            continue
        t = props[k].get("type")
        if t in types and v is not None and not isinstance(v, types[t]):
            errs.append(f"type:{k}")
    return errs


def audit_run(run: Path) -> list[dict]:
    steps = [json.loads(l) for l in (run / "steps.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    meta = json.loads((run / "meta.json").read_text()) if (run / "meta.json").exists() else {}
    domain = meta.get("domain", run.name.split("_")[0])
    con = sqlite3.connect(str(run / "tool_calls.sqlite"))
    calls = [dict(zip(["id", "step_id", "agent", "tool", "args_json", "result_json", "status", "latency", "ts"], r))
             for r in con.execute("SELECT id, step_id, agent, tool, args_json, result_json, status, latency, ts FROM tool_calls ORDER BY id")]
    con.close()
    for c in calls:
        try:
            c["args"] = json.loads(c["args_json"]) if c["args_json"] else {}
        except Exception:
            c["args"] = {"_raw": c["args_json"]}
        c["result"] = c["result_json"] or ""
    schemas = {}
    for s in steps:
        for t in (s["request"].get("tools") or []):
            schemas[t["function"]["name"]] = t["function"].get("parameters") or {}
    rules = rules_for(domain)
    rows: list[dict] = []

    # ---- per tool call checks ----
    seen: Counter = Counter()
    for i, c in enumerate(calls):
        res = c["result"]
        low = res.lower()
        checks = {
            "error": c["status"] != "ok" or any(k in low[:400] for k in ("error", "exception", "traceback", "not found", "invalid")),
            "empty": res.strip() in ("", "null", "[]", "{}", '""', "None"),
            "repeat": False,
            "schema": bool(_validate_args(c["args"], schemas.get(c["tool"], {}))) if c["tool"] in schemas else False,
            "ignored": False,
        }
        key = (c["tool"], json.dumps(c["args"], sort_keys=True, default=str))
        seen[key] += 1
        checks["repeat"] = seen[key] >= 2
        if checks["error"]:
            # ignored: no retry of the same tool and no mention of the problem in the next 2 steps by any agent
            later_steps = [s for s in steps if s["step_id"] > c["step_id"]][:2]
            retried = any(cc["tool"] == c["tool"] for cc in calls[i + 1:i + 3])
            mentioned = any(any(w in (s["response"].get("content") or "").lower() for w in ("error", "fail", "could not", "unable", "not found", "retry", "issue"))
                            for s in later_steps)
            checks["ignored"] = not (retried or mentioned)
        rows.append({"run_id": run.name, "domain": domain, "kind": "tool_call", "call_id": c["id"], "step_id": c["step_id"],
                     "agent": c["agent"], "tool": c["tool"], "checks": checks, "schema_errors": _validate_args(c["args"], schemas.get(c["tool"], {})) if c["tool"] in schemas else []})

    # ---- per utterance: required tools ----
    for s in steps:
        if s["agent"] in AUX:
            continue
        text = s["response"].get("content") or ""
        claims = extract_claims(domain, text)
        if not claims:
            continue
        prior = [c for c in calls if c["step_id"] < s["step_id"] or (c["step_id"] == s["step_id"])]
        required, missing = [], []
        for ctype, value in claims:
            tools = rules.get(ctype, [])
            required.append({"type": ctype, "value": value, "tools": tools})
            ok = False
            for c in prior:
                if c["tool"] in tools and c["status"] == "ok":
                    if not value or _norm(value) in _norm(c["result"]) or _norm(value) in _norm(json.dumps(c["args"], default=str)):
                        ok = True
                        break
            if not ok:
                missing.append({"type": ctype, "value": value})
        rows.append({"run_id": run.name, "domain": domain, "kind": "utterance", "step_id": s["step_id"], "agent": s["agent"],
                     "required_tools": required, "satisfied": not missing, "missing": missing,
                     "pointers": [f"step {c['step_id']} {c['tool']}" for c in prior[-3:]]})
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default="runs")
    a = ap.parse_args()
    AUDIT.mkdir(exist_ok=True)
    out = AUDIT / "d3.jsonl"
    n = 0
    agg = Counter()
    with out.open("w", encoding="utf-8") as f:
        for run in sorted(Path(a.runs).glob("*/")):
            if not (run / "steps.jsonl").exists() or not (run / "tool_calls.sqlite").exists():
                continue
            for r in audit_run(run):
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
                n += 1
                if r["kind"] == "tool_call":
                    for k, v in r["checks"].items():
                        agg[k] += int(v)
                else:
                    agg["utterances"] += 1
                    agg["unsatisfied"] += int(not r["satisfied"])
    print(f"D3 rows={n}", dict(agg))


if __name__ == "__main__":
    main()
