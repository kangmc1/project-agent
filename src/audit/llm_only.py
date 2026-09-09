"""LLM-only variants of D1, D2, D3 — same question, same inputs, LLM judgment instead of code/probability (user request,
2026-09-09). Judge = the executing model Qwen3-32B (thinking ON) on :18001; it sees NO labels, rewards or gold answers.

  d1 : the decision context + candidate action list -> verbalized probability for each candidate
       -> dist, p_actual, confidence, margin exactly like D1 (audit/llm_d1.jsonl)
  d2 : instruction, the step's tool calls with arguments and results, calls so far in the handoff, the record the agent
       was given -> three booleans (skipped required tool / argument not in record / call failed) -> flag (audit/llm_d2.jsonl)
  d3 : both sides of a handoff boundary -> facts of A missing or altered in B -> fidelity 0..1 (audit/llm_d3.jsonl)

Population: labeled runs only, non-aux steps, cascade steps (after the decisive step) skipped — the same steps the
evaluation uses. Disk-cached by sha1(prompt) in audit/cache/llm_only.sqlite. Usage: python -m src.audit.llm_only {d1,d2,d3,all}
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import math
import re
import sqlite3
import threading
import time
from pathlib import Path

from openai import OpenAI

from .extract import map_parallel
from .comparators.d3_factset import _load_run, _load_text, _dedupe_wrapper_rows, _planner_wrapper_calls, _find_planner_step_id, WRAPPERS

AUDIT = Path("audit")
CACHE_DB = AUDIT / "cache" / "llm_only.sqlite"
import os
BASE = os.environ.get("LLM_JUDGE_BASE", "http://localhost:18004/v1")  # default judge server = gpt-oss-20b
MODEL = os.environ.get("LLM_JUDGE_MODEL", "gptoss20b")
TAG = os.environ.get("LLM_JUDGE_TAG", "" if MODEL == "qwen32b" else MODEL)  # untagged files = Qwen3-32B runs (llm_d1.jsonl); others -> llm_d1_<model>.jsonl
AUX = {"user_sim", "summarizer"}
MAX_TOKENS = int(os.environ.get("LLM_JUDGE_MAX_TOKENS", "1800"))
N_CTX = 8
PER_MSG = 1800
_client = None
_lock = threading.Lock()
_con = None


def _cl():
    global _client
    if _client is None:
        _client = OpenAI(base_url=BASE, api_key="dummy", timeout=600)
    return _client


def _cache():
    global _con
    if _con is None:
        CACHE_DB.parent.mkdir(parents=True, exist_ok=True)
        _con = sqlite3.connect(str(CACHE_DB), check_same_thread=False)
        _con.execute("CREATE TABLE IF NOT EXISTS cache (hash TEXT PRIMARY KEY, value TEXT, latency REAL, out_tokens INTEGER)")
        _con.commit()
    return _con


def _strip_think(t: str) -> str:
    return re.sub(r"<think>.*?</think>", "", t, flags=re.S).strip()


def _json_obj(t: str) -> dict | None:
    m = re.search(r"\{.*\}", t, re.S)
    if not m:
        return None
    try:
        o = json.loads(m.group(0))
        return o if isinstance(o, dict) else None
    except Exception:
        return None


def ask(prompt: str) -> tuple[dict | None, float, int]:
    h = hashlib.sha1((MODEL + "\n" + prompt).encode()).hexdigest()
    with _lock:
        row = _cache().execute("SELECT value, latency, out_tokens FROM cache WHERE hash=?", (h,)).fetchone()
    if row:
        return (json.loads(row[0]) if row[0] else None), row[1], row[2] or 0
    t0 = time.time()
    out, toks = None, 0
    msgs = [{"role": "user", "content": prompt}]
    for attempt in range(2):
        try:
            r = _cl().chat.completions.create(model=MODEL, messages=msgs, temperature=0, max_tokens=MAX_TOKENS)
            txt = r.choices[0].message.content or ""
            toks += (r.usage.completion_tokens if r.usage else 0)
            out = _json_obj(_strip_think(txt))
        except Exception:
            out = None
        if out is not None:
            break
        msgs = [{"role": "user", "content": prompt + "\n\nYour previous output was not valid JSON. Output ONLY one JSON object."}]
    lat = time.time() - t0
    with _lock:
        _cache().execute("INSERT OR REPLACE INTO cache VALUES (?,?,?,?)", (h, json.dumps(out) if out is not None else None, lat, toks))
        _cache().commit()
    return out, lat, toks


def _msg_text(m: dict) -> str:
    c = m.get("content")
    if isinstance(c, list):
        c = " ".join(x.get("text", "") for x in c if isinstance(x, dict))
    c = str(c or "")
    tcs = m.get("tool_calls") or []
    if tcs:
        c += "\n" + "\n".join(f"[tool_call] {tc['function']['name']}({tc['function'].get('arguments','')})" for tc in tcs if isinstance(tc, dict) and 'function' in tc)
    if len(c) > PER_MSG:
        c = c[:PER_MSG] + " …[truncated]"
    return f"<{m.get('role')}> {c}"


def _context(msgs: list[dict]) -> str:
    sysm = [m for m in msgs if m.get("role") == "system"]
    tail = [m for m in msgs if m.get("role") != "system"][-N_CTX:]
    parts = []
    if sysm:
        parts.append(_msg_text(sysm[0])[:2500])
    parts += [_msg_text(m) for m in tail]
    return "\n".join(parts)


def _labeled() -> dict[str, dict]:
    return {json.load(open(f))["run_id"]: json.load(open(f)) for f in glob.glob("labels/*.json")}


DOMAIN = "airline"  # user decision 09:15: comparators on τ-bench airline (main experiment) only


def _population():
    """(run, domain, steps(non-aux, non-cascade), all_steps, calls) for labeled runs of DOMAIN."""
    lab = _labeled()
    for run in sorted(Path("runs").glob("*/")):
        if run.name not in lab or not (run / "steps.jsonl").exists():
            continue
        steps, calls, meta = _load_run(run)
        domain = meta.get("domain", run.name.split("_")[0])
        if domain != DOMAIN:
            continue
        ds = lab[run.name].get("decisive_step")
        keep = [s for s in steps if s["agent"] not in AUX and not (ds is not None and s["step_id"] > ds)]
        yield run.name, domain, keep, steps, calls


# ----------------------------------------------------------------------------- D1
_D1 = ("You are auditing one decision of an AI agent. Below is the context the agent saw and the list of actions it could take "
       "next (tool names, or no_tool = reply with text and call nothing). Estimate, for EACH candidate, the probability that it "
       "is the best next action given the context and the agent's instructions. Probabilities must be numbers in [0,1] and sum to 1. "
       'Return ONLY JSON: {"probs": {"<candidate>": p, ...}}.')


def d1_task(run_id, domain, s):
    names = [t["function"]["name"] for t in (s["request"].get("tools") or [])] + ["no_tool"]
    tcs = s["response"].get("tool_calls") or []
    actual = tcs[0]["function"]["name"] if tcs else "no_tool"
    if actual not in names:
        names.append(actual)
    prompt = f"{_D1}\n\nDomain: {domain}\nAgent: {s['agent']}\nCandidates: {json.dumps(names)}\n\n--- context ---\n{_context(s['request']['messages'])}\n\nReturn JSON only."
    return {"run_id": run_id, "domain": domain, "step_id": s["step_id"], "agent": s["agent"],
            "role": "planner" if s["agent"] == "planner" else "subagent", "A": names, "actual": actual, "prompt": prompt}


def d1_score(t):
    out, lat, toks = ask(t["prompt"])
    probs = (out or {}).get("probs") if isinstance((out or {}).get("probs"), dict) else None
    row = {k: t[k] for k in ("run_id", "domain", "step_id", "agent", "role", "A", "actual")}
    row.update({"latency": lat, "out_tokens": toks})
    if not probs:
        row.update({"parsed": False}); return row
    vals = {}
    for a in t["A"]:
        v = probs.get(a)
        try:
            vals[a] = max(0.0, float(v))
        except Exception:
            vals[a] = 0.0
    z = sum(vals.values())
    if z <= 0:
        row.update({"parsed": False}); return row
    dist = {a: v / z for a, v in vals.items()}
    n = len(dist); H = -sum(p * math.log2(p) for p in dist.values() if p > 0)
    ps = sorted(dist.values(), reverse=True)
    row.update({"parsed": True, "dist": dist, "confidence": 1 - H / math.log2(n) if n > 1 else 1.0,
                "p_actual": dist.get(t["actual"], 0.0), "margin": ps[0] - (ps[1] if len(ps) > 1 else 0.0)})
    return row


# ----------------------------------------------------------------------------- D2
_D2 = ("You are auditing one step of an AI agent that uses tools. Judge ONLY this step's tool use against the record the agent "
       "was given (its instruction, the messages and tool results it had received). Answer three yes/no questions:\n"
       "(1) skipped_required_tool: if this is the agent's final report of a delegated task, did it end WITHOUT calling a tool "
       "that its instruction clearly required (e.g. asked to look something up but never called a lookup tool)? For non-final steps answer false.\n"
       "(2) argument_not_in_record: does any argument value of this step's tool calls (ids, names, dates, codes, amounts) NOT appear "
       "anywhere in the record the agent was given (instruction, prior messages, tool results)? Values derived by legitimate "
       "reformatting (e.g. 'May 26' -> 2024-05-26, city -> airport code) count as in the record.\n"
       "(3) call_failed: did any tool call at this step return an error (excluding a read of a not-yet-created file)?\n"
       'Return ONLY JSON: {"skipped_required_tool": bool, "argument_not_in_record": bool, "call_failed": bool, "evidence": "<short>"}')


def d2_task(run_id, domain, s, all_steps, calls):
    msgs = s["request"]["messages"]
    instr = next((m.get("content") or "" for m in msgs if m.get("role") == "user"), "") if s["agent"] != "planner" else "(planner: no delegated instruction)"
    tcs = s["response"].get("tool_calls") or []
    own = "\n".join(f"{tc['function']['name']}({tc['function'].get('arguments','')})" for tc in tcs) or "(none — this step is a text reply / final report)"
    results = [c for c in calls if c["step_id"] == s["step_id"]]
    res_txt = "\n".join(f"{c['tool']} -> {_load_text(c['result_json'])[:600]}" for c in results) or "(no tool results at this step)"
    # calls so far in this handoff (same agent, since last planner step)
    prev = [x for x in all_steps if x["agent"] == s["agent"] and x["step_id"] < s["step_id"]]
    last_planner = max([x["step_id"] for x in all_steps if x["agent"] == "planner" and x["step_id"] < s["step_id"]] or [-1])
    sofar = [tc["function"]["name"] for x in prev if x["step_id"] > last_planner for tc in (x["response"].get("tool_calls") or [])]
    is_final = (not tcs) and s["agent"] != "planner"
    prompt = (f"{_D2}\n\nDomain: {domain}\nAgent: {s['agent']}\nIs this the agent's final report of the delegated task: {is_final}\n"
              f"Instruction given to the agent:\n{str(instr)[:2000]}\n\nTools the agent has called earlier in this task: {sofar or '(none)'}\n\n"
              f"--- record the agent was given (most recent messages, tool results verbatim) ---\n{_context(msgs)}\n\n"
              f"--- THIS STEP's tool calls ---\n{own}\n\n--- results returned for these calls ---\n{res_txt}\n\nReturn JSON only.")
    return {"run_id": run_id, "domain": domain, "step_id": s["step_id"], "agent": s["agent"],
            "role": "planner" if s["agent"] == "planner" else "subagent", "prompt": prompt}


def d2_score(t):
    out, lat, toks = ask(t["prompt"])
    row = {k: t[k] for k in ("run_id", "domain", "step_id", "agent", "role")}
    row.update({"latency": lat, "out_tokens": toks})
    if not out:
        row.update({"parsed": False, "flag": None}); return row
    b = {k: bool(out.get(k)) for k in ("skipped_required_tool", "argument_not_in_record", "call_failed")}
    row.update({"parsed": True, **b, "flag": int(any(b.values())), "evidence": str(out.get("evidence", ""))[:300]})
    return row


# ----------------------------------------------------------------------------- D3
_D3 = ("You are auditing a handoff between two AI agents. Text A is what was sent across the boundary; text B is what the "
       "receiving side stated or did right after. List every concrete fact of A (ids, values, dates, amounts, statuses, "
       "conclusions, constraints) and say whether it is preserved in B, missing from B, or altered in B. Then give "
       "fidelity = preserved / total facts of A (a number in [0,1]; if A has no facts, use null). "
       'Return ONLY JSON: {"n_facts": int, "preserved": int, "missing": [str], "altered": [str], "fidelity": number|null}')


def d3_tasks(run_id, domain, steps, calls):
    rows = _dedupe_wrapper_rows(calls)
    pcalls = _planner_wrapper_calls(steps)
    planner_steps = [s for s in steps if s["agent"] == "planner"]
    lab = _labeled()[run_id]; ds = lab.get("decisive_step")
    out = []
    for row in rows:
        try:
            args = json.loads(row["args_json"])
        except Exception:
            args = None
        pstep = _find_planner_step_id(pcalls, row["tool"], args, row["step_id"])
        if pstep is None or (ds is not None and pstep > ds):
            continue
        instruction = (args or {}).get("instruction", "") if isinstance(args, dict) else _load_text(row["args_json"])
        first = next((s for s in steps if s["agent"] == row["tool"] and s["step_id"] > pstep), None)
        premise = (first["response"].get("content") or "") if first else ""
        report = _load_text(row["result_json"])
        nxt = next((s for s in planner_steps if s["step_id"] > row["step_id"]), None)
        b1 = ""
        if nxt is not None:
            b1 = (nxt["response"].get("content") or "") + "\n" + "\n".join(tc["function"].get("arguments", "") for tc in (nxt["response"].get("tool_calls") or []))
        for direction, A, B in (("instruction->premise", instruction, premise), ("report->planner", report, b1)):
            if not str(A).strip():
                continue
            prompt = f"{_D3}\n\nDomain: {domain}\nBoundary: {row['tool']} {direction}\n\n--- TEXT A ---\n{str(A)[:4000]}\n\n--- TEXT B ---\n{(str(B).strip() or '(empty)')[:4000]}\n\nReturn JSON only."
            out.append({"run_id": run_id, "domain": domain, "handoff_id": row["id"], "planner_step_id": pstep, "wrapper": row["tool"],
                        "direction": direction, "B_empty": not str(B).strip(), "prompt": prompt})
    return out


def d3_score(t):
    out, lat, toks = ask(t["prompt"])
    row = {k: t[k] for k in ("run_id", "domain", "handoff_id", "planner_step_id", "wrapper", "direction", "B_empty")}
    row.update({"latency": lat, "out_tokens": toks})
    f = (out or {}).get("fidelity") if out else None
    try:
        f = None if f is None else min(1.0, max(0.0, float(f)))
    except Exception:
        f = None
    row.update({"parsed": out is not None, "fidelity": f, "missing": (out or {}).get("missing", [])[:8] if out else [], "altered": (out or {}).get("altered", [])[:8] if out else []})
    return row


def run(which: str) -> None:
    pop = list(_population())
    if which in ("d1", "all"):
        tasks = [d1_task(r, d, s) for r, d, keep, allst, calls in pop for s in keep]
        rows = map_parallel(d1_score, tasks)
        _write("llm_d1.jsonl", rows); _report("LLM-D1", rows, lambda r: r.get("parsed"))
    if which in ("d2", "all"):
        tasks = [d2_task(r, d, s, allst, calls) for r, d, keep, allst, calls in pop for s in keep]
        rows = map_parallel(d2_score, tasks)
        _write("llm_d2.jsonl", rows); _report("LLM-D2", rows, lambda r: r.get("parsed"))
    if which in ("d3", "all"):
        tasks = [t for r, d, keep, allst, calls in pop for t in d3_tasks(r, d, allst, calls)]
        rows = map_parallel(d3_score, tasks)
        _write("llm_d3.jsonl", rows); _report("LLM-D3", rows, lambda r: r.get("parsed"))


def _write(name, rows):
    if TAG:
        name = name.replace(".jsonl", f"_{TAG}.jsonl")
    with (AUDIT / name).open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def _report(name, rows, ok):
    n = len(rows); k = sum(1 for r in rows if ok(r))
    lat = [r["latency"] for r in rows if r.get("latency")]; tk = sum(r.get("out_tokens", 0) for r in rows)
    print(f"{name}: rows {n}, parsed {k}, mean latency {sum(lat)/len(lat) if lat else 0:.1f}s, output tokens {tk}", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("which", choices=["d1", "d2", "d3", "all"]); a = ap.parse_args()
    run(a.which)
