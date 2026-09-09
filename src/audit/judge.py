"""LLM-judge baseline (OPTIONAL comparator) — a single small model asked "did THIS step fail?".

Comparison baseline for the code-judged auditor items (D1/D4/D2/D3/D9). For every labeled-agent step it shows the
same 8B model that the extractor uses (Qwen3-8B on :18002) the run's domain, the agent's role, the last ~6 messages
of context the agent actually saw (tool results verbatim), and the step's own output, then asks for
{failure, p_fail, category, rationale} as strict JSON. Thinking is ON (no enable_thinking=False), so the
`<think>...</think>` prefix is stripped before parsing. The judge sees NO labels, NO rewards, NO gold answers.

Disk-cached (audit/cache/judge.sqlite, keyed by sha1 of the exact prompt) so reruns are free / resumable.

Output: audit/judge.jsonl (one row per labeled-agent step).  --stats also writes audit/judge_stats.json.
Usage: python -m src.audit.judge [--runs runs] [--run-id ID] [--stats] [--out audit/judge.jsonl]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
import threading
import time
from collections import Counter
from pathlib import Path

from openai import OpenAI

from .extract import EXTRACT_BASE, MODEL, map_parallel

AUDIT = Path("audit")
CACHE_DB = AUDIT / "cache" / "judge.sqlite"
AUX = {"user_sim", "summarizer"}
MAX_WORKERS = 8            # the 8B server is shared with the running D9 job
MAX_TOKENS = 2048          # room for the thinking block plus the JSON
N_CONTEXT_MSGS = 6
CONTEXT_CHARS = 6000
PER_MSG_CHARS = 1500
CATEGORIES = ("handoff", "tool", "reasoning_stability")

_client: OpenAI | None = None
_client_lock = threading.Lock()
_cache_lock = threading.Lock()
_cache_con: sqlite3.Connection | None = None


def _get_client() -> OpenAI:
    global _client
    with _client_lock:
        if _client is None:
            _client = OpenAI(base_url=EXTRACT_BASE, api_key="dummy")
        return _client


def _get_cache() -> sqlite3.Connection:
    global _cache_con
    with _cache_lock:
        if _cache_con is None:
            CACHE_DB.parent.mkdir(parents=True, exist_ok=True)
            con = sqlite3.connect(str(CACHE_DB), check_same_thread=False)
            con.execute("CREATE TABLE IF NOT EXISTS cache "
                        "(hash TEXT PRIMARY KEY, ok INTEGER, value TEXT, latency REAL)")
            con.commit()
            _cache_con = con
        return _cache_con


def _cache_get(h: str) -> tuple[dict | None, float] | None:
    con = _get_cache()
    with _cache_lock:
        row = con.execute("SELECT ok, value, latency FROM cache WHERE hash = ?", (h,)).fetchone()
    if row is None:
        return None
    ok, value, latency = row
    return (json.loads(value) if ok else None), float(latency or 0.0)


def _cache_set(h: str, value: dict | None, latency: float) -> None:
    con = _get_cache()
    with _cache_lock:
        con.execute("INSERT OR REPLACE INTO cache (hash, ok, value, latency) VALUES (?, ?, ?, ?)",
                    (h, int(value is not None), json.dumps(value, ensure_ascii=False) if value else None, latency))
        con.commit()


# ----------------------------------------------------------------------------- model call
_THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL)
_OPEN_THINK_RE = re.compile(r"^.*?</think>", re.DOTALL)
_JSON_OBJ_RE = re.compile(r"\{.*\}", re.DOTALL)


def _strip_think(text: str) -> str:
    """Qwen3 with thinking on emits <think>...</think> before the answer (the server has no reasoning parser)."""
    text = _THINK_RE.sub("", text)
    if "</think>" in text:
        text = _OPEN_THINK_RE.sub("", text)  # opening tag can be swallowed by the chat template
    return text.strip()


def _parse_json_obj(text: str) -> dict | None:
    if not text:
        return None
    m = _JSON_OBJ_RE.search(_strip_think(text))
    if not m:
        return None
    try:
        obj = json.loads(m.group(0))
    except Exception:
        return None
    return obj if isinstance(obj, dict) else None


def judge_json(prompt: str, retries: int = 1) -> tuple[dict | None, float]:
    """Ask the 8B judge (thinking ON) for one JSON verdict. Cached on disk by sha1(prompt). Retries once on
    a JSON parse failure; returns (None, latency) when the second attempt also fails."""
    h = hashlib.sha1(prompt.encode("utf-8")).hexdigest()
    cached = _cache_get(h)
    if cached is not None:
        return cached

    client = _get_client()
    messages = [{"role": "user", "content": prompt}]
    result: dict | None = None
    t0 = time.time()
    attempt = 0
    while attempt <= retries:
        try:
            resp = client.chat.completions.create(model=MODEL, messages=messages, temperature=0,
                                                  max_tokens=MAX_TOKENS)
            content = resp.choices[0].message.content or ""
        except Exception:
            content = ""
        result = _parse_json_obj(content)
        if result is not None:
            break
        attempt += 1
        if attempt <= retries:
            messages.append({"role": "assistant", "content": _strip_think(content)})
            messages.append({"role": "user", "content": "Your previous output was not valid JSON. Output ONLY a "
                                                        "single valid JSON object, with no markdown fences and "
                                                        "no explanation."})
    latency = time.time() - t0
    _cache_set(h, result, latency)
    return result, latency


# ----------------------------------------------------------------------------- prompt
_TASK = """You are auditing one step of a multi-agent LLM system. You see only the transcript: no labels, no rewards, no gold answers.

Failure categories:
handoff = information lost/altered/added when crossing an agent boundary (instruction vs subagent premise, subagent report vs planner relay, wrong subagent, missing ids)
tool = wrong tool/args, tool error ignored, result misread, required tool never called, needless repetition
reasoning_stability = conclusion unsupported by the record (fabricated value, wrong policy/arithmetic/logic, belief only consistent with summarized-away context)

Decide whether THIS STEP (the step's own output below, not any earlier step) contains an agent failure.

Output a single JSON object and nothing else:
{"failure": true|false, "p_fail": 0.0-1.0, "category": "handoff"|"tool"|"reasoning_stability"|null, "rationale": "<=200 chars"}
p_fail is your probability that this step contains a failure. category is null when failure is false."""


def _msg_text(m: dict) -> str:
    """One context message rendered the way the agent saw it (tool results verbatim), capped per message."""
    role = str(m.get("role", "?"))
    parts = []
    content = m.get("content")
    if isinstance(content, str) and content.strip():
        parts.append(content.strip())
    elif content:
        parts.append(json.dumps(content, ensure_ascii=False))
    for tc in (m.get("tool_calls") or []):
        fn = (tc.get("function") or {}) if isinstance(tc, dict) else {}
        parts.append(f"[tool_call] {fn.get('name')}({fn.get('arguments')})")
    body = "\n".join(parts)
    if len(body) > PER_MSG_CHARS:
        body = body[:PER_MSG_CHARS] + " ...[truncated]"
    return f"[{role}]\n{body}"


def _context(messages: list[dict]) -> str:
    """Last N_CONTEXT_MSGS messages, newest-first budget of CONTEXT_CHARS, rendered oldest-first."""
    kept: list[str] = []
    used = 0
    for m in reversed(messages[-N_CONTEXT_MSGS:]):
        t = _msg_text(m)
        if kept and used + len(t) > CONTEXT_CHARS:
            break
        kept.append(t)
        used += len(t)
    return "\n\n".join(reversed(kept))


def build_prompt(step: dict, domain: str, role: str) -> str:
    resp = step["response"]
    own = (resp.get("content") or "").strip() or "(no text)"
    calls = []
    for tc in (resp.get("tool_calls") or []):
        fn = (tc.get("function") or {}) if isinstance(tc, dict) else {}
        calls.append(f"{fn.get('name')}({fn.get('arguments')})")
    own_calls = "\n".join(calls) if calls else "(none)"
    return (f"{_TASK}\n\n"
            f"Domain: {domain}\n"
            f"Agent: {step['agent']} (role: {role})\n\n"
            f"--- context the agent saw (most recent messages) ---\n{_context(step['request'].get('messages') or [])}\n\n"
            f"--- THIS STEP's output ---\ntext:\n{own}\n\ntool_calls:\n{own_calls}\n\n"
            f"Output JSON only.")


# ----------------------------------------------------------------------------- scoring
def _coerce(out: dict | None) -> tuple[float | None, bool | None, str | None, str]:
    if out is None:
        return None, None, None, ""
    failure = out.get("failure")
    failure = bool(failure) if isinstance(failure, bool) else (None if failure is None else bool(failure))
    p = out.get("p_fail")
    if isinstance(p, bool):
        p = float(p)
    elif isinstance(p, (int, float)):
        p = float(p)
    elif isinstance(p, str):
        try:
            p = float(p.strip())
        except Exception:
            p = None
    else:
        p = None
    if p is None and failure is not None:
        p = 1.0 if failure else 0.0
    if p is not None:
        p = min(1.0, max(0.0, p))
    if failure is None and p is not None:
        failure = p >= 0.5
    cat = out.get("category")
    cat = cat if isinstance(cat, str) and cat in CATEGORIES else None
    rationale = out.get("rationale")
    rationale = str(rationale)[:200] if rationale is not None else ""
    return p, failure, cat, rationale


def score_step(step: dict, run_id: str, domain: str) -> dict:
    role = "planner" if step["agent"] == "planner" else "subagent"
    out, latency = judge_json(build_prompt(step, domain, role))
    p, failure, cat, rationale = _coerce(out)
    return {"run_id": run_id, "step_id": step["step_id"], "agent": step["agent"], "role": role,
            "p_fail": p, "failure": failure, "category": cat, "rationale": rationale,
            "latency_s": round(latency, 3)}


def audit_run(run: Path) -> list[dict]:
    steps = [json.loads(l) for l in (run / "steps.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    meta = json.loads((run / "meta.json").read_text()) if (run / "meta.json").exists() else {}
    domain = meta.get("domain", run.name.split("_")[0])
    targets = [s for s in steps if s["agent"] not in AUX]
    return list(map_parallel(lambda s: score_step(s, run.name, domain), targets, max_workers=MAX_WORKERS))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default="runs")
    ap.add_argument("--run-id")
    ap.add_argument("--domain", default="airline", help="restrict to runs of this domain (default airline)")
    ap.add_argument("--out", default=str(AUDIT / "judge.jsonl"))
    ap.add_argument("--stats", action="store_true")
    a = ap.parse_args()

    out_path = Path(a.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    for run in sorted(Path(a.runs).glob("*/")):
        _meta = json.loads((run / "meta.json").read_text()) if (run / "meta.json").exists() else {}
        if a.domain and _meta.get("domain", run.name.split("_")[0]) != a.domain:
            continue
        if a.run_id and run.name != a.run_id:
            continue
        if not (run / "steps.jsonl").exists():
            continue
        r = audit_run(run)
        rows.extend(r)
        print(f"  {run.name}: {len(r)} steps ({len(rows)} total)", flush=True)

    with out_path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Judge done: {len(rows)} rows -> {out_path}")

    if a.stats:
        scored = [r for r in rows if r["p_fail"] is not None]
        na = len(rows) - len(scored)
        cats = Counter(r["category"] for r in scored if r["category"])
        out = {
            "n_steps": len(rows),
            "failure_rate": (sum(1 for r in scored if r["failure"]) / len(scored)) if scored else None,
            "mean_p_fail": (sum(r["p_fail"] for r in scored) / len(scored)) if scored else None,
            "extract_failure_rate": (na / len(rows)) if rows else None,
            "extract_failures": na,
            "mean_latency_s": (sum(r["latency_s"] for r in rows) / len(rows)) if rows else None,
            "category_counts": dict(sorted(cats.items())),
        }
        (AUDIT / "judge_stats.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
        print("Judge stats:", json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
