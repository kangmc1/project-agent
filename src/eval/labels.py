"""Gold labels — schema validation, labels/index.csv, and step-class derivation.

Label file (labels/<run_id>.json):
    {run_id, batch, decisive_step: int|null,
     error_events: [{step, agent, category, subtag, recovered, recovery_step, evidence}]}

Step classes (per non-aux step of a labeled run, in this precedence):
    decisive  = step == decisive_step
    transient = step is an error_event with recovered = true
    cascade   = step > decisive_step (only when decisive_step is not null)
    clean     = everything else
Aux-agent steps (user_sim, summarizer) are excluded from every population.

Usage:  python -m src.eval.labels --validate [--root .]
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

AUX_AGENTS = {"user_sim", "summarizer"}
SUBAGENTS = {"policy_checker", "db_agent", "solver", "verifier"}
CATEGORIES = {"handoff", "tool", "reasoning_stability"}
SUBTAGS = {"hallucination_like", "reasoning_like", "handoff_induced", "compression_induced"}
CLASSES = ("decisive", "transient", "cascade", "clean")

_HEAD_RE = re.compile(r'^\{\s*"step_id"\s*:\s*(\d+)\s*,\s*"agent"\s*:\s*"([^"]*)"')
_STEPS_CACHE: dict[str, list[tuple[int, str]]] = {}


# --------------------------------------------------------------------------------- basic loaders
def role_of(agent: str) -> str:
    """planner | subagent | aux.  Unknown agent names are treated as subagents."""
    if agent == "planner":
        return "planner"
    if agent in AUX_AGENTS:
        return "aux"
    return "subagent"


def load_steps(run_dir: Path) -> list[tuple[int, str]]:
    """[(step_id, agent)] in file order.  Only the two header fields are parsed."""
    key = str(run_dir)
    if key in _STEPS_CACHE:
        return _STEPS_CACHE[key]
    rows: list[tuple[int, str]] = []
    p = run_dir / "steps.jsonl"
    if p.exists():
        with p.open(encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                m = _HEAD_RE.match(line)
                if m:
                    rows.append((int(m.group(1)), m.group(2)))
                else:
                    r = json.loads(line)
                    rows.append((int(r["step_id"]), str(r["agent"])))
    _STEPS_CACHE[key] = rows
    return rows


def non_aux_steps(run_dir: Path) -> list[tuple[int, str, str]]:
    """[(step_id, agent, role)] for non-aux steps, in trace order."""
    return [(s, a, role_of(a)) for s, a in load_steps(run_dir) if role_of(a) != "aux"]


def load_index(root: str | Path = ".") -> dict[str, dict]:
    """runs/index.csv -> {run_id: {domain, task, batch, status, success, n_steps, wall_time}}."""
    p = Path(root) / "runs" / "index.csv"
    if not p.exists():
        raise SystemExit(f"missing {p} — run `python -m src.eval.index` first")
    out: dict[str, dict] = {}
    with p.open(encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            rid = (r.get("run_id") or "").strip()
            if not rid:
                continue
            out[rid] = {
                "run_id": rid,
                "domain": (r.get("domain") or "").strip(),
                "task": (r.get("task") or "").strip(),
                "batch": _int_or_none(r.get("batch")),
                "status": (r.get("status") or "").strip(),
                "success": _as_bool(r.get("success")),
                "n_steps": _int_or_none(r.get("n_steps")),
                "wall_time": _float_or_none(r.get("wall_time")),
            }
    return out


def _as_bool(v) -> bool | None:
    s = str(v).strip().lower()
    if s in ("true", "1", "yes", "t"):
        return True
    if s in ("false", "0", "no", "f"):
        return False
    return None


def _int_or_none(v):
    try:
        return int(str(v).strip())
    except (TypeError, ValueError):
        return None


def _float_or_none(v):
    try:
        return float(str(v).strip())
    except (TypeError, ValueError):
        return None


def label_path(root: str | Path, run_id: str) -> Path:
    return Path(root) / "labels" / f"{run_id}.json"


def load_label(root: str | Path, run_id: str) -> dict | None:
    p = label_path(root, run_id)
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def labeled_run_ids(root: str | Path = ".") -> list[str]:
    d = Path(root) / "labels"
    return sorted(p.stem for p in d.glob("*.json")) if d.exists() else []


# --------------------------------------------------------------------------------- step classes
def derive_step_classes(run_id: str, root: str | Path = ".") -> dict[int, str]:
    """{step_id: class} for every non-aux step of a labeled run ({} if the run has no label file)."""
    lab = load_label(root, run_id)
    if lab is None:
        return {}
    decisive = lab.get("decisive_step")
    transient = {int(e["step"]) for e in (lab.get("error_events") or []) if e.get("recovered")}
    out: dict[int, str] = {}
    for step_id, _agent, _role in non_aux_steps(Path(root) / "runs" / run_id):
        if decisive is not None and step_id == int(decisive):
            out[step_id] = "decisive"
        elif step_id in transient:
            out[step_id] = "transient"
        elif decisive is not None and step_id > int(decisive):
            out[step_id] = "cascade"
        else:
            out[step_id] = "clean"
    return out


# --------------------------------------------------------------------------------- validation
def validate_one(run_id: str, lab: dict, root: str | Path, index: dict[str, dict]) -> tuple[list[str], list[str]]:
    errs: list[str] = []
    warns: list[str] = []
    tag = f"labels/{run_id}.json"

    if lab.get("run_id") != run_id:
        errs.append(f"{tag}: run_id field {lab.get('run_id')!r} != filename {run_id!r}")
    if not isinstance(lab.get("batch"), int):
        errs.append(f"{tag}: batch must be an int (got {lab.get('batch')!r})")
    ds = lab.get("decisive_step")
    if ds is not None and not isinstance(ds, int):
        errs.append(f"{tag}: decisive_step must be int|null (got {ds!r})")
        ds = None
    events = lab.get("error_events")
    if not isinstance(events, list):
        errs.append(f"{tag}: error_events must be a list")
        events = []
    for k in set(lab) - {"run_id", "batch", "decisive_step", "error_events"}:
        warns.append(f"{tag}: unknown top-level key {k!r}")

    run_dir = Path(root) / "runs" / run_id
    steps = load_steps(run_dir)
    if not steps:
        errs.append(f"{tag}: no steps.jsonl for run {run_id}")
        return errs, warns
    agent_of = dict(steps)
    non_aux = {s for s, a in steps if role_of(a) != "aux"}

    if run_id not in index:
        warns.append(f"{tag}: run not in runs/index.csv")
    else:
        success = index[run_id]["success"]
        if success is False and ds is None:
            warns.append(f"{tag}: index says success=false but decisive_step is null")
        if success is True and ds is not None:
            warns.append(f"{tag}: index says success=true but decisive_step={ds}")

    if ds is not None:
        if ds not in agent_of:
            errs.append(f"{tag}: decisive_step {ds} not in steps.jsonl")
        elif ds not in non_aux:
            errs.append(f"{tag}: decisive_step {ds} is an aux agent ({agent_of[ds]})")

    for i, e in enumerate(events):
        et = f"{tag} event[{i}]"
        if not isinstance(e, dict):
            errs.append(f"{et}: not an object")
            continue
        step = e.get("step")
        if not isinstance(step, int):
            errs.append(f"{et}: step must be an int (got {step!r})")
        elif step not in agent_of:
            errs.append(f"{et}: step {step} not in steps.jsonl")
        elif step not in non_aux:
            errs.append(f"{et}: step {step} is an aux agent ({agent_of[step]}) — aux steps are never labeled")
        elif e.get("agent") != agent_of[step]:
            warns.append(f"{et}: agent {e.get('agent')!r} != steps.jsonl agent {agent_of[step]!r}")
        if e.get("category") not in CATEGORIES:
            errs.append(f"{et}: category must be one of {sorted(CATEGORIES)} (got {e.get('category')!r})")
        sub = e.get("subtag", None)
        if sub is not None and sub not in SUBTAGS:
            errs.append(f"{et}: subtag must be one of {sorted(SUBTAGS)}|null (got {sub!r})")
        rec = e.get("recovered")
        if not isinstance(rec, bool):
            errs.append(f"{et}: recovered must be a bool (got {rec!r})")
        rs = e.get("recovery_step", None)
        if rec is True:
            if not isinstance(rs, int):
                errs.append(f"{et}: recovery_step is required (int) when recovered=true")
            else:
                if rs not in agent_of:
                    errs.append(f"{et}: recovery_step {rs} not in steps.jsonl")
                if isinstance(step, int) and rs <= step:
                    warns.append(f"{et}: recovery_step {rs} <= step {step}")
        elif rs is not None:
            warns.append(f"{et}: recovered=false but recovery_step={rs}")
        if not isinstance(e.get("evidence"), str) or not e["evidence"].strip():
            errs.append(f"{et}: evidence must be a non-empty string")
        if isinstance(step, int) and ds is not None and step == ds and rec is True:
            warns.append(f"{et}: decisive step marked recovered=true")

    seen = Counter(e.get("step") for e in events if isinstance(e, dict))
    for step, n in seen.items():
        if n > 1:
            warns.append(f"{tag}: {n} events on step {step}")
    return errs, warns


def validate_all(root: str | Path = ".", index: dict[str, dict] | None = None) -> tuple[list[dict], list[str], list[str]]:
    index = load_index(root) if index is None else index
    rows: list[dict] = []
    errs: list[str] = []
    warns: list[str] = []
    for run_id in labeled_run_ids(root):
        try:
            lab = load_label(root, run_id)
        except json.JSONDecodeError as exc:
            errs.append(f"labels/{run_id}.json: invalid JSON — {exc}")
            continue
        if not isinstance(lab, dict):
            errs.append(f"labels/{run_id}.json: top level must be an object")
            continue
        e, w = validate_one(run_id, lab, root, index)
        errs += e
        warns += w
        classes = derive_step_classes(run_id, root)
        rows.append({
            "run_id": run_id,
            "batch": lab.get("batch"),
            "domain": index.get(run_id, {}).get("domain") or run_id.split("_")[0],
            "n_events": len(lab.get("error_events") or []),
            "decisive_step": "" if lab.get("decisive_step") is None else lab["decisive_step"],
            "n_labeled_steps": len(classes),
        })
    return rows, errs, warns


def write_index(rows: list[dict], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["run_id", "batch", "domain", "n_events", "decisive_step", "n_labeled_steps"])
        w.writeheader()
        for r in rows:
            w.writerow(r)


def main() -> int:
    ap = argparse.ArgumentParser(description="validate gold labels and write labels/index.csv")
    ap.add_argument("--root", default=".", help="directory holding runs/ labels/ audit/ eval/")
    ap.add_argument("--validate", action="store_true", help="validate every labels/*.json (default action)")
    ap.add_argument("--out", default=None, help="labels index csv (default <root>/labels/index.csv)")
    a = ap.parse_args()

    rows, errs, warns = validate_all(a.root)
    out = Path(a.out) if a.out else Path(a.root) / "labels" / "index.csv"
    write_index(rows, out)

    per_batch: dict = defaultdict(lambda: [0, 0, 0])
    per_domain: dict = defaultdict(lambda: [0, 0, 0])
    for r in rows:
        for d, k in ((per_batch, r["batch"]), (per_domain, r["domain"])):
            d[k][0] += 1
            d[k][1] += r["n_labeled_steps"]
            d[k][2] += r["n_events"]

    print(f"labeled runs: {len(rows)}  ->  {out}")
    print("\nn_labeled per batch")
    print(f"  {'batch':<10}{'n_runs':>8}{'n_steps':>10}{'n_events':>10}")
    for k in sorted(per_batch, key=lambda x: (x is None, str(x))):
        n_runs, n_steps, n_ev = per_batch[k]
        print(f"  {str(k):<10}{n_runs:>8}{n_steps:>10}{n_ev:>10}")
    print("\nn_labeled per domain")
    print(f"  {'domain':<10}{'n_runs':>8}{'n_steps':>10}{'n_events':>10}")
    for k in sorted(per_domain, key=str):
        n_runs, n_steps, n_ev = per_domain[k]
        print(f"  {str(k):<10}{n_runs:>8}{n_steps:>10}{n_ev:>10}")

    for w in warns:
        print(f"WARN  {w}", file=sys.stderr)
    for e in errs:
        print(f"ERROR {e}", file=sys.stderr)
    print(f"\n{len(errs)} error(s), {len(warns)} warning(s)")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
