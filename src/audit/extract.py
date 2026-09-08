"""Extractor client for the qwen8b judge/extractor LLM.

Thin wrapper around an OpenAI-compatible `/v1/chat/completions` endpoint that asks a small model to turn
free-text (assistant utterances, tool reports, math solutions) into structured JSON, used by d2 (groundedness)
and d7 (handoff fidelity). Disk-cached (keyed by sha1 of the exact prompt sent to the model) so reruns over the
same runs/ directory make zero LLM calls.

Usage (smoke test): python -m src.audit.extract --runs runs [--run-id ID] [--kind atomic_facts|claims|equations] [--limit N]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from openai import OpenAI

EXTRACT_BASE = "http://localhost:18002/v1"
MODEL = "qwen8b"
AUDIT = Path("audit")
CACHE_DB = AUDIT / "cache" / "extract.sqlite"
AUX = {"user_sim", "summarizer"}

_client: OpenAI | None = None
_client_lock = threading.Lock()

_stats_lock = threading.Lock()
_calls = 0
_failures = 0

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
            con.execute("CREATE TABLE IF NOT EXISTS cache (hash TEXT PRIMARY KEY, ok INTEGER, value TEXT)")
            con.commit()
            _cache_con = con
        return _cache_con


def _cache_get(h: str) -> tuple[bool, dict | None] | None:
    con = _get_cache()
    with _cache_lock:
        row = con.execute("SELECT ok, value FROM cache WHERE hash = ?", (h,)).fetchone()
    if row is None:
        return None
    ok, value = row
    return bool(ok), (json.loads(value) if ok else None)


def _cache_set(h: str, ok: bool, value: dict | None) -> None:
    con = _get_cache()
    with _cache_lock:
        con.execute("INSERT OR REPLACE INTO cache (hash, ok, value) VALUES (?, ?, ?)",
                    (h, int(ok), json.dumps(value, ensure_ascii=False) if ok else None))
        con.commit()


def get_extract_stats() -> dict:
    with _stats_lock:
        return {"calls": _calls, "failures": _failures,
                "failure_rate": (_failures / _calls) if _calls else None}


def reset_extract_stats() -> None:
    global _calls, _failures
    with _stats_lock:
        _calls = 0
        _failures = 0


_JSON_OBJ_RE = re.compile(r"\{.*\}", re.DOTALL)


def _parse_json_obj(text: str) -> dict | None:
    if not text:
        return None
    m = _JSON_OBJ_RE.search(text)
    if not m:
        return None
    try:
        obj = json.loads(m.group(0))
    except Exception:
        return None
    return obj if isinstance(obj, dict) else None


def extract_json(prompt: str, schema_hint: str, retries: int = 2) -> dict | None:
    """Call the extractor LLM, parse a single JSON object out of its reply. Cached on disk by sha1(full prompt)."""
    full_prompt = f"{schema_hint}\n\n{prompt}\n\nOutput JSON only."
    h = hashlib.sha1(full_prompt.encode("utf-8")).hexdigest()
    cached = _cache_get(h)
    if cached is not None:
        return cached[1]

    global _calls, _failures
    with _stats_lock:
        _calls += 1

    client = _get_client()
    messages = [{"role": "user", "content": full_prompt}]
    result: dict | None = None
    attempt = 0
    while attempt <= retries:
        try:
            resp = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=0,
                extra_body={"chat_template_kwargs": {"enable_thinking": False}},
            )
            content = resp.choices[0].message.content or ""
        except Exception:
            content = ""
        result = _parse_json_obj(content)
        if result is not None:
            break
        attempt += 1
        if attempt <= retries:
            messages.append({"role": "assistant", "content": content})
            messages.append({"role": "user", "content": "Your previous output was not valid JSON. Output ONLY a "
                                                          "single valid JSON object, with no markdown fences and "
                                                          "no explanation."})

    if result is None:
        with _stats_lock:
            _failures += 1
    _cache_set(h, result is not None, result)
    return result


def map_parallel(fn, items, max_workers: int = 16) -> list:
    """Run fn over items on a 16-thread pool, preserving input order."""
    items = list(items)
    if not items:
        return []
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        return list(ex.map(fn, items))


# ----------------------------------------------------------------------------- templated extractors
_CLAIMS_SCHEMA = (
    'Return a single JSON object: {"claims": [{"entity": str, "attribute": str, "value": str}, ...]}. '
    "Extract every atomic factual claim made in the text below, including EVERY number, ID, date, and price "
    "mentioned. entity is the subject the claim is about (e.g. 'reservation', 'flight HAT136'). attribute is the "
    "property being stated (e.g. 'total', 'departure_time', 'cabin'). value is the claimed value, always as a "
    "string, written exactly as it appears in the text (keep currency symbols, keep IDs verbatim)."
)


def extract_claims(text: str) -> list[dict]:
    if not text or not text.strip():
        return []
    out = extract_json(text, _CLAIMS_SCHEMA)
    if not out:
        return []
    claims = out.get("claims")
    if not isinstance(claims, list):
        return []
    result = []
    for c in claims:
        if not isinstance(c, dict):
            continue
        result.append({"entity": str(c.get("entity", "")), "attribute": str(c.get("attribute", "")),
                        "value": str(c.get("value", ""))})
    return result


_ATOMIC_FACTS_SCHEMA = (
    "Return a single flat JSON object of atomic facts EXPLICITLY STATED in the text below. Each key is a short "
    "snake_case name that YOU derive from the text to describe what the value is (examples of the style only: "
    "user_id, origin_city, destination_city, departure_date, cabin_class, flight_number, total_price, refund_amount, "
    "baggage_count, verdict, final_answer, distance_miles, value_of_x). Include EVERY identifier, code, number, "
    "amount, date, time, name, cabin, verdict and final answer that the text states; values are short verbatim strings "
    "(numbers as strings). Use numeric suffixes for repeated concepts (flight_number_1, flight_number_2). Do NOT "
    "include anything that is only asked about, requested, or missing -- only facts whose value is given in the text. "
    "Never reuse a key name from these examples unless the text actually contains that fact."
)


def extract_atomic_facts(text: str) -> dict:
    if not text or not text.strip():
        return {}
    out = extract_json(text, _ATOMIC_FACTS_SCHEMA)
    if not out:
        return {}
    facts = {}
    for k, v in out.items():
        if isinstance(v, (dict, list)):
            continue
        facts[str(k)] = str(v)
    return facts


_EQUATIONS_SCHEMA = (
    'Return a single JSON object: {"equations": [{"expr_python": str, "relation": str}, ...]}. For each equation, '
    "inequality, or variable binding explicitly stated in the math solution below, emit one entry. expr_python "
    "must be a Python-evaluable expression string using ONLY number literals, the operators + - * / **, and the "
    "functions sqrt(), factorial(), comb() plus variable names that are bound by an earlier entry in the list "
    "(e.g. '3*x + 2 == 11', '2**10 == 1024', 'x == 3'). relation is one of '==', '!=', '<', '<=', '>', '>='. "
    "Include every explicit variable binding (e.g. x = 3) as its own entry with relation '=='."
)


_RELATION_RE = re.compile(r"<=|>=|==|!=|<|>")


def _infer_relation(expr: str) -> str:
    m = _RELATION_RE.search(expr)
    return m.group(0) if m else "=="


def extract_equations(text: str) -> list[dict]:
    if not text or not text.strip():
        return []
    out = extract_json(text, _EQUATIONS_SCHEMA)
    if not out:
        return []
    eqs = out.get("equations")
    if not isinstance(eqs, list):
        return []
    result = []
    for e in eqs:
        if isinstance(e, dict):
            expr = str(e.get("expr_python", ""))
            relation = str(e.get("relation", "")) or _infer_relation(expr)
        elif isinstance(e, str):
            # small models sometimes flatten to a bare list of equation strings instead of the requested
            # {expr_python, relation} objects; salvage those rather than dropping the whole entry.
            expr = e
            relation = _infer_relation(e)
        else:
            continue
        if expr:
            result.append({"expr_python": expr, "relation": relation})
    return result


# ----------------------------------------------------------------------------- smoke-test CLI
def _iter_step_texts(runs_dir: Path, run_id: str | None):
    for run in sorted(runs_dir.glob("*/")):
        if run_id and run.name != run_id:
            continue
        sp = run / "steps.jsonl"
        if not sp.exists():
            continue
        for line in sp.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            if r["agent"] in AUX:
                continue
            content = r["response"].get("content")
            if content and content.strip():
                yield run.name, r["step_id"], r["agent"], content


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default="runs")
    ap.add_argument("--run-id")
    ap.add_argument("--kind", choices=["atomic_facts", "claims", "equations"], default="atomic_facts")
    ap.add_argument("--limit", type=int, default=5)
    a = ap.parse_args()

    fn = {"atomic_facts": extract_atomic_facts, "claims": extract_claims, "equations": extract_equations}[a.kind]
    n = 0
    for run_id, step_id, agent, content in _iter_step_texts(Path(a.runs), a.run_id):
        if n >= a.limit:
            break
        n += 1
        result = fn(content)
        print(json.dumps({"run_id": run_id, "step_id": step_id, "agent": agent, "result": result}, ensure_ascii=False)[:2000])
    print("stats:", get_extract_stats())


if __name__ == "__main__":
    main()
