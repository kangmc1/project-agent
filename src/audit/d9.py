"""D9 — equation-consistency check for AIME assistant utterances (solver, verifier, planner).

For each assistant step of those agents (non-empty content) in AIME-domain runs, candidate equations
are pulled from the utterance via `src.audit.extract.extract_equations` (imported lazily, and injectable
for tests) and each is checked with a restricted, non-evaluating sympy parse: never `sympify` on raw
text, never `eval` ourselves — `sympy.parsing.sympy_parser.parse_expr` is the only string interpreter,
restricted to a small numeric-function allowlist (ALLOWED).

Note on `global_dict`: literally passing `global_dict={}` alongside `evaluate=False` makes parse_expr
fail on any expression beyond a bare literal — sympy's own evaluate=False rewrite emits references to
`Add`/`Mul`/`Symbol`/`Eq`/... that must resolve somewhere (verified against the installed sympy==1.14.0:
`parse_expr("3+4", evaluate=False, local_dict=ALLOWED, global_dict={}, ...)` raises `NameError: name
'Add' is not defined`). _STRUCTURAL below supplies exactly those inert math-object constructors (no I/O,
no code execution) so the allowlist's safety intent — no arbitrary/expensive sympy functions callable
from equation text — is preserved while arithmetic actually parses.

Outputs: audit/d9.jsonl, audit/d9_stats.json (with --stats)
Usage:  python -m src.audit.d9 [--runs runs] [--stats]
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Callable

import sympy
from sympy.parsing.sympy_parser import parse_expr, standard_transformations

AGENTS = {"solver", "verifier", "planner"}
AUDIT = Path("audit")
TOL = 1e-9
RELATIONS = ("==", "<=", ">=", "!=", "<", ">")

# functions equation text may call — sympy numeric-function allowlist only (P1 spec)
ALLOWED: dict[str, Any] = {
    "sqrt": sympy.sqrt, "factorial": sympy.factorial, "binomial": sympy.binomial,
    "Rational": sympy.Rational, "Integer": sympy.Integer, "pi": sympy.pi, "E": sympy.E,
    "floor": sympy.floor, "ceiling": sympy.ceiling, "gcd": sympy.gcd, "lcm": sympy.lcm,
    "Abs": sympy.Abs, "log": sympy.log, "exp": sympy.exp, "sin": sympy.sin, "cos": sympy.cos,
}
# structural names sympy's parser injects internally for evaluate=False / auto_symbol — see module
# docstring. Inert constructors only; does not widen what equation text can call.
_STRUCTURAL: dict[str, Any] = {
    "Symbol": sympy.Symbol, "Function": sympy.Function, "Integer": sympy.Integer, "Float": sympy.Float,
    "Rational": sympy.Rational, "I": sympy.I, "Add": sympy.Add, "Mul": sympy.Mul, "Pow": sympy.Pow,
    "Or": sympy.Or, "And": sympy.And, "Not": sympy.Not, "Eq": sympy.Eq, "Ne": sympy.Ne,
    "Lt": sympy.Lt, "Le": sympy.Le, "Gt": sympy.Gt, "Ge": sympy.Ge,
}


# ----------------------------------------------------------------------------- safe sympy evaluation
def _parse_side(s: str) -> sympy.Basic:
    e = parse_expr(s.strip(), evaluate=False, local_dict=dict(ALLOWED), global_dict=dict(_STRUCTURAL),
                   transformations=standard_transformations)
    if not isinstance(e, sympy.Basic):  # e.g. "1, 2" parses to a tuple; treat as unparseable
        raise ValueError(f"not a sympy expression: {type(e).__name__}")
    return e


def _split_relation(expr_python: str, relation: str) -> tuple[str, str] | None:
    idx = expr_python.find(relation)
    if idx < 0:
        return None
    lhs, rhs = expr_python[:idx].strip(), expr_python[idx + len(relation):].strip()
    return (lhs, rhs) if lhs and rhs else None


def _isclose(a: float, b: float) -> bool:
    return abs(a - b) <= TOL * max(1.0, abs(a), abs(b))


def _compare(a: float, b: float, relation: str) -> bool:
    if relation == "==":
        return _isclose(a, b)
    if relation == "!=":
        return not _isclose(a, b)
    if relation == "<":
        return a < b and not _isclose(a, b)
    if relation == "<=":
        return a < b or _isclose(a, b)
    if relation == ">":
        return a > b and not _isclose(a, b)
    if relation == ">=":
        return a > b or _isclose(a, b)
    raise ValueError(f"unsupported relation {relation!r}")


def _to_real_float(expr: sympy.Basic) -> float:
    val = complex(expr.evalf(30))
    if not (math.isfinite(val.real) and math.isfinite(val.imag)):
        raise ValueError("non-finite value")  # e.g. 1/0 -> zoo -> nan+nanj; nan comparisons are never True
    if abs(val.imag) > 1e-9:
        raise ValueError("non-real value")
    return val.real


def _maybe_bind(lhs: sympy.Basic, rhs: sympy.Basic, relation: str, bindings: dict) -> None:
    """Register 'x == 3'-style equalities as bindings for later equations in the same step."""
    if relation != "==":
        return
    if isinstance(lhs, sympy.Symbol) and not rhs.free_symbols:
        bindings[lhs] = rhs
    elif isinstance(rhs, sympy.Symbol) and not lhs.free_symbols:
        bindings[rhs] = lhs


def evaluate_equation(expr_python: str, relation: str, bindings: dict) -> dict:
    """Returns {"verdict": "true"|"false"|"unknown", "method": "numeric"|"substituted"|"unknown"|"parse_error"}."""
    if relation not in RELATIONS:
        return {"verdict": "unknown", "method": "parse_error"}
    split = _split_relation(expr_python, relation)
    if split is None:
        return {"verdict": "unknown", "method": "parse_error"}
    lhs_s, rhs_s = split
    try:
        lhs, rhs = _parse_side(lhs_s), _parse_side(rhs_s)
    except Exception:
        return {"verdict": "unknown", "method": "parse_error"}

    substituted = False
    free = lhs.free_symbols | rhs.free_symbols
    if free:
        bound = {s: bindings[s] for s in free if s in bindings}
        if bound:
            lhs, rhs = lhs.subs(bound), rhs.subs(bound)
            substituted = True
            free = lhs.free_symbols | rhs.free_symbols

    _maybe_bind(lhs, rhs, relation, bindings)

    if free:
        return {"verdict": "unknown", "method": "unknown"}

    try:
        ok = _compare(_to_real_float(lhs), _to_real_float(rhs), relation)
    except Exception:
        return {"verdict": "unknown", "method": "parse_error"}
    return {"verdict": "true" if ok else "false", "method": "substituted" if substituted else "numeric"}


# ----------------------------------------------------------------------------- extraction (lazy)
def _default_extractor(text: str) -> list[dict]:
    from .extract import extract_equations  # lazy: 8B LLM client, only needed when actually used

    return extract_equations(text)


# ----------------------------------------------------------------------------- run scanning
def iter_aime_steps(runs_dir: Path):
    for run in sorted(runs_dir.glob("*/")):
        sp = run / "steps.jsonl"
        if not sp.exists():
            continue
        meta_path = run / "meta.json"
        meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
        domain = meta.get("domain", run.name.split("_")[0])
        if domain != "aime":
            continue
        for line in sp.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            if r.get("agent") not in AGENTS:
                continue
            content = (r.get("response") or {}).get("content")
            if not content:
                continue
            yield run.name, r["step_id"], r["agent"], content


def process_step(run_id: str, step_id: int, agent: str, content: str,
                  extractor: Callable[[str], list[dict]]) -> dict | None:
    eqs = extractor(content) or []
    if not eqs:
        return None
    bindings: dict = {}
    equations: list[dict] = []
    false_pointers: list[dict] = []
    n_true = n_false = 0
    for eq in eqs:
        expr_python = eq.get("expr_python", "")
        relation = eq.get("relation", "")
        out = evaluate_equation(expr_python, relation, bindings)
        equations.append({"expr": expr_python, "verdict": out["verdict"], "method": out["method"]})
        if out["verdict"] == "true":
            n_true += 1
        elif out["verdict"] == "false":
            n_false += 1
            false_pointers.append({"step_id": step_id, "expr": expr_python})
    consistency = n_true / (n_true + n_false) if (n_true + n_false) > 0 else None
    return {"run_id": run_id, "step_id": step_id, "agent": agent, "equations": equations,
            "consistency": consistency, "false_pointers": false_pointers}


def run_all(runs_dir: Path, extractor: Callable[[str], list[dict]] | None = None) -> list[dict]:
    extractor = extractor or _default_extractor
    steps = list(iter_aime_steps(runs_dir))
    # Extraction (8B calls) in parallel like D2/D7 — the loop was sequential and one long JSON generation per step made
    # the pass take >1 h. Order is preserved; equation evaluation stays sequential per step (bindings are per step).
    from .extract import map_parallel
    rows = []
    for row in map_parallel(lambda t: process_step(t[0], t[1], t[2], t[3], extractor), steps):
        if row is not None:
            rows.append(row)
    return rows


# ----------------------------------------------------------------------------- stats
def compute_stats(rows: list[dict]) -> dict:
    def ratio(rs: list[dict]) -> tuple[int, int, float | None]:
        n = sum(len(r["equations"]) for r in rs)
        u = sum(1 for r in rs for e in r["equations"] if e["verdict"] == "unknown")
        return n, u, (u / n if n else None)

    n_all, u_all, r_all = ratio(rows)
    trace_order: list[str] = []
    for r in rows:
        if r["run_id"] not in trace_order:
            trace_order.append(r["run_id"])
    first3 = set(trace_order[:3])
    n3, u3, r3 = ratio([r for r in rows if r["run_id"] in first3])
    return {
        "overall": {"n_equations": n_all, "n_unknown": u_all, "unknown_ratio": r_all},
        "first3": {"traces": sorted(first3), "n_equations": n3, "n_unknown": u3, "unknown_ratio": r3},
        "narrow_to_numeric_only": bool(r3 is not None and r3 > 0.8),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default="runs")
    ap.add_argument("--stats", action="store_true")
    a = ap.parse_args()
    AUDIT.mkdir(exist_ok=True)
    rows = run_all(Path(a.runs))
    with (AUDIT / "d9.jsonl").open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"D9 rows={len(rows)}")
    if a.stats:
        stats = compute_stats(rows)
        (AUDIT / "d9_stats.json").write_text(json.dumps(stats, indent=2, ensure_ascii=False))
        print(json.dumps(stats, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
