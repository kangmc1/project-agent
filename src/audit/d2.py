"""D2 - groundedness: are an assistant step's factual claims backed by tool evidence seen so far?

For every assistant step (agent not in {user_sim, summarizer}) with non-empty response.content: extract atomic
claims (entity/attribute/value) with the qwen8b extractor, then for each claim whose value looks like a number,
ID, or date, search for it (normalized) in the raw text of every tool_calls row (result_json and args_json) with
step_id <= this step's step_id in the same run, and in the content of earlier user_sim steps (things the customer
itself stated are grounded too). s = fraction of such "values" found; claims with no countable value get s = null.

Output: audit/d2.jsonl (one row per scored step).  --stats also writes audit/d2_stats.json.
Usage: python -m src.audit.d2 [--runs runs] [--run-id ID] [--stats] [--out audit/d2.jsonl]
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
from pathlib import Path

from .extract import extract_claims, get_extract_stats, map_parallel

AUX = {"user_sim", "summarizer"}
AUDIT = Path("audit")


def _norm(v: str) -> str:
    return v.replace(",", "").replace("$", "").strip().lower()


def _is_countable(value: str) -> bool:
    """A claim 'counts' toward the groundedness score if its value contains a digit or looks like an ID/code."""
    if re.search(r"\d", value):
        return True
    # all-caps alphabetic code (e.g. a confirmation letter code with no digits)
    return bool(re.fullmatch(r"[A-Z]{3,}", value.strip()))


def _load_run(run: Path) -> tuple[list[dict], list[dict], dict]:
    steps = [json.loads(l) for l in (run / "steps.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    meta = json.loads((run / "meta.json").read_text()) if (run / "meta.json").exists() else {}
    con = sqlite3.connect(str(run / "tool_calls.sqlite"))
    calls = [dict(zip(["id", "step_id", "agent", "tool", "args_json", "result_json", "status", "latency", "ts"], r))
             for r in con.execute("SELECT id, step_id, agent, tool, args_json, result_json, status, latency, ts "
                                   "FROM tool_calls ORDER BY id")]
    con.close()
    return steps, calls, meta


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


def score_step(step: dict, calls: list[dict], user_sim_texts: list[tuple[int, str]], run_id: str, domain: str) -> dict:
    content = step["response"]["content"]
    claims = extract_claims(content)
    prior_calls = [c for c in calls if c["step_id"] <= step["step_id"]]
    prior_user = [(sid, txt) for sid, txt in user_sim_texts if sid < step["step_id"]]
    # Everything the model was GIVEN in this request is a legitimate source too: the task statement and policy
    # (system/user), the planner's instruction to a subagent (user), tool results (tool). Its own earlier assistant
    # turns are excluded so a restated fabrication stays unsupported. (Added 09-09 05:00; before, AIME problem-statement
    # values and instruction values were counted as unsupported.)
    given_norm = _norm(_input_text(step))

    scored_claims = []
    n_values = 0
    n_found = 0
    pointers = []
    for c in claims:
        value = c["value"]
        countable = _is_countable(value)
        norm_v = _norm(value)
        found = False
        source = None
        if norm_v:
            for call in prior_calls:
                haystack_r = _norm(call["result_json"] or "")
                haystack_a = _norm(call["args_json"] or "")
                if norm_v in haystack_r or norm_v in haystack_a:
                    found = True
                    source = {"step_id": call["step_id"], "tool": call["tool"]}
                    break
            if not found:
                for sid, txt in prior_user:
                    if norm_v in _norm(txt):
                        found = True
                        source = {"step_id": sid, "tool": "user_sim"}
                        break
            if not found and norm_v in given_norm:
                found = True
                source = {"step_id": step["step_id"], "tool": "input"}
        scored_claims.append({"entity": c["entity"], "attribute": c["attribute"], "value": value,
                               "found": found, "source": source})
        if countable:
            n_values += 1
            if found:
                n_found += 1
                if source and source not in pointers:
                    pointers.append(source)

    s = (n_found / n_values) if n_values else None
    unsupported = (1 - s) if s is not None else None
    return {"run_id": run_id, "domain": domain, "step_id": step["step_id"], "agent": step["agent"],
            "claims": scored_claims, "n_values": n_values, "s": s, "unsupported": unsupported, "pointers": pointers}


def audit_run(run: Path) -> list[dict]:
    steps, calls, meta = _load_run(run)
    domain = meta.get("domain", run.name.split("_")[0])
    user_sim_texts = [(s["step_id"], s["response"]["content"] or "") for s in steps if s["agent"] == "user_sim"]
    targets = [s for s in steps if s["agent"] not in AUX and (s["response"].get("content") or "").strip()]
    return list(map_parallel(lambda s: score_step(s, calls, user_sim_texts, run.name, domain), targets))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default="runs")
    ap.add_argument("--run-id")
    ap.add_argument("--out", default=str(AUDIT / "d2.jsonl"))
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
    print(f"D2 done: {len(rows)} rows -> {out_path}")

    if a.stats:
        na = [r for r in rows if r["s"] is None]
        scored = [r for r in rows if r["s"] is not None]
        ex_stats = get_extract_stats()
        out = {
            "n_rows": len(rows),
            "na_ratio": (len(na) / len(rows)) if rows else None,
            "mean_s": (sum(r["s"] for r in scored) / len(scored)) if scored else None,
            "extract_failure_rate": ex_stats["failure_rate"],
            "extract_calls": ex_stats["calls"],
            "extract_failures": ex_stats["failures"],
        }
        (AUDIT / "d2_stats.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
        print("D2 stats:", json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
