"""Detection metrics — item score x role x domain, step / trace / attribution / latency.

Populations
  step-level  : labeled runs only, non-aux steps, item score non-NA, cascade steps EXCLUDED.
                positives = {decisive, transient, error(unrecovered non-decisive)} ("all errors") and separately {decisive}; negatives = clean.
  trace-level : every run in runs/index.csv whose item coverage is >= 80% of that run's non-aux steps in the
                role scope; positives = runs with success=false (index).
  ties        : AUROC is rank based with average ranks; CI = 1000 stratified bootstrap resamples, seed 0.

Usage:  python -m src.eval.metrics [--out eval/metrics.md] [--pre] [--root .]
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from .labels import (derive_step_classes, labeled_run_ids, load_index, load_label,
                     load_steps, non_aux_steps, role_of)

D2_CHECKS = ("error", "empty", "repeat", "schema", "ignored")
ROLE_SCOPES = ("planner", "subagent", "all")
DOMAIN_SCOPES = ("airline", "aime", "all")
N_BOOT = 1000
BOOT_SEED = 0
CSV_FIELDS = ["section", "item", "role", "domain", "metric", "value", "ci_lo", "ci_hi",
              "n_pos", "n_neg", "n_scored", "n_labeled", "note"]


# ===================================================================================== items
@dataclass
class Item:
    name: str
    scores: dict[tuple[str, int], float] = field(default_factory=dict)
    roles: tuple[str, ...] = ("planner", "subagent")
    domains: tuple[str, ...] | None = None
    note: str = ""


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                out.append(json.loads(line))
    return out


def _num(v):
    return None if v is None else float(v)


def load_items(root: str | Path = ".") -> dict[str, Item]:
    """All per-step item scores, keyed (run_id, step_id).  Higher = more suspicious."""
    audit = Path(root) / "audit"
    items: dict[str, Item] = {}

    def add(name, **kw):
        items[name] = Item(name=name, **kw)
        return items[name]

    d1_conf = add("D1_1-conf", note="1 - confidence")
    d1_pact = add("D1_1-p_actual", note="1 - p_actual")
    d1_marg = add("D1_1-margin", note="1 - margin")
    d1_hand = add("D1_handoff", roles=("planner",), note="layer2 H2 (delegation entropy)")
    for r in read_jsonl(audit / "d1.jsonl"):
        k = (r["run_id"], int(r["step_id"]))
        for it, key in ((d1_conf, "confidence"), (d1_pact, "p_actual"), (d1_marg, "margin")):
            v = _num(r.get(key))
            if v is not None:
                it.scores[k] = 1.0 - v
        role = r.get("role") or role_of(r.get("agent", ""))
        h2 = _num((r.get("layer2") or {}).get("H2"))
        if role == "planner" and h2 is not None:
            d1_hand.scores[k] = h2

    d3 = add("D2", note="action grounding (user definition): 1 if required tool never called OR fabricated argument OR tool call failed (excl. file/wrapper), else 0 (every non-aux step)")
    for r in read_jsonl(audit / "d2_action.jsonl"):
        d3.scores[(r["run_id"], int(r["step_id"]))] = float(r.get("d3", 0))

    d3c = add("D3", roles=("planner",), note="handoff 실행 가능성·수용 (user definition): 1 if the delegation lacks the identifiers the subagent needs OR re-issues a near-identical instruction after a failure report, else 0 (planner delegation steps)")
    for r in read_jsonl(audit / "d3_conditions.jsonl"):
        d3c.scores[(r["run_id"], int(r["step_id"]))] = float(r.get("d3", 0))
    by_dir: dict[str, dict[tuple[str, int], float]] = defaultdict(dict)  # descriptive: fact-set fidelity per direction
    for r in read_jsonl(audit / "d3_handoff.jsonl"):
        f = _num(r.get("fidelity"))
        if f is None:
            continue
        k = (r["run_id"], int(r["planner_step_id"]))
        d = str(r.get("direction", "?"))
        by_dir[d][k] = max(by_dir[d].get(k, 0.0), 1.0 - f)
    for d in sorted(by_dir):
        add(f"D3fid_{d}", roles=("planner",), note="descriptive only: 1 - fact-set fidelity (8B extraction), worst wrapper at the planner step").scores = by_dir[d]

    # LLM-only variants of D1/D2/D3 — same question as the module, LLM judgment. One item set per judge model:
    # default files llm_d{1,2,3}.jsonl = Qwen3-32B; llm_d{1,2,3}_<tag>.jsonl = other judges (e.g. gptoss20b).
    import glob as _glob
    tags = [""] + sorted({m.group(1) for f in _glob.glob(str(audit / "llm_d1_*.jsonl")) for m in [re.search(r"llm_d1_(.+)\.jsonl$", f)] if m})
    for tag in tags:
        sfx = f"_{tag}" if tag else ""
        lab = f"LLM{'-' + tag if tag else ''}"
        l1c = add(f"{lab}_D1_1-conf", note=f"LLM-only D1 ({tag or 'qwen32b'}): 1 - confidence from verbalized candidate probabilities")
        l1p = add(f"{lab}_D1_1-p_actual", note=f"LLM-only D1 ({tag or 'qwen32b'}): 1 - verbalized p(actual)")
        for r in read_jsonl(audit / f"llm_d1{sfx}.jsonl"):
            if r.get("parsed"):
                k = (r["run_id"], int(r["step_id"]))
                l1c.scores[k] = 1.0 - float(r["confidence"]); l1p.scores[k] = 1.0 - float(r["p_actual"])
        l2 = add(f"{lab}_D2", note=f"LLM-only D2 ({tag or 'qwen32b'}): any of skipped_required_tool / argument_not_in_record / call_failed")
        for r in read_jsonl(audit / f"llm_d2{sfx}.jsonl"):
            if r.get("parsed") and r.get("flag") is not None:
                l2.scores[(r["run_id"], int(r["step_id"]))] = float(r["flag"])
        by_dir3: dict[str, dict[tuple[str, int], float]] = defaultdict(dict)
        for r in read_jsonl(audit / f"llm_d3{sfx}.jsonl"):
            f = _num(r.get("fidelity"))
            if f is None:
                continue
            k = (r["run_id"], int(r["planner_step_id"])); d = str(r.get("direction", "?"))
            by_dir3[d][k] = max(by_dir3[d].get(k, 0.0), 1.0 - f)
        for d in sorted(by_dir3):
            add(f"{lab}_D3_{d}", roles=("planner",), note=f"LLM-only D3 ({tag or 'qwen32b'}): 1 - verbalized fidelity").scores = by_dir3[d]
    judge = add("Judge_p_fail", note="Qwen3-8B judge, thinking on, p_fail")
    judge_flag = add("Judge_flag", note="Qwen3-8B judge: p_fail >= 0.5 as a 0/1 flag (for P/R/F1 comparison with D2)")
    for r in read_jsonl(audit / "judge.jsonl"):
        v = _num(r.get("p_fail"))
        if v is not None:
            judge_flag.scores[(r["run_id"], int(r["step_id"]))] = 1.0 if v >= 0.5 else 0.0
            judge.scores[(r["run_id"], int(r["step_id"]))] = v

    return {k: v for k, v in items.items() if v.scores}


def load_d3_tool_flags(root: str | Path = ".") -> dict[tuple[str, int], dict[str, bool]]:
    flags: dict[tuple[str, int], dict[str, bool]] = {}
    for r in read_jsonl(Path(root) / "audit" / "d2_toolcalls.jsonl"):
        if r.get("kind") != "tool_call":
            continue
        k = (r["run_id"], int(r["step_id"]))
        cur = flags.setdefault(k, {c: False for c in D2_CHECKS})
        ch = r.get("checks") or {}
        for c in D2_CHECKS:
            cur[c] = cur[c] or bool(ch.get(c))
    return flags


def d7_report_to_planner(items: dict[str, Item]) -> str | None:
    """Name of the D3 item for the report->planner direction, if present."""
    for name in items:
        if not name.startswith("D3_"):
            continue
        d = "".join(ch for ch in name[3:].lower() if ch.isalnum())
        if d.startswith("report"):
            return name
    return None


# ===================================================================================== populations
@dataclass(frozen=True)
class StepRow:
    run_id: str
    step_id: int
    agent: str
    role: str
    domain: str
    cls: str


def labeled_steps(root: str | Path = ".", index: dict | None = None) -> list[StepRow]:
    index = load_index(root) if index is None else index
    rows: list[StepRow] = []
    for run_id in labeled_run_ids(root):
        classes = derive_step_classes(run_id, root)
        if not classes:
            continue
        domain = index.get(run_id, {}).get("domain") or run_id.split("_")[0]
        for step_id, agent, role in non_aux_steps(Path(root) / "runs" / run_id):
            rows.append(StepRow(run_id, step_id, agent, role, domain, classes[step_id]))
    return rows


def scope_roles(role: str) -> set[str]:
    return {"planner", "subagent"} if role == "all" else {role}


def applicable(item: Item, role: str, domain: str) -> tuple[set[str], set[str] | None] | None:
    """Effective (roles, domains) for this cell, or None when the item does not apply."""
    roles = scope_roles(role) & set(item.roles)
    if not roles:
        return None
    if role == "all" and len(item.roles) == 1:
        return None                                   # identical to the single-role row
    if domain == "all" and item.domains is not None and len(item.domains) == 1:
        return None                                   # identical to the single-domain row
    domains: set[str] | None = None if domain == "all" else {domain}
    if item.domains is not None:
        allowed = set(item.domains)
        domains = allowed if domains is None else (domains & allowed)
        if not domains:
            return None
    return roles, domains


def cell_rows(rows: list[StepRow], roles: set[str], domains: set[str] | None) -> list[StepRow]:
    return [r for r in rows if r.role in roles and (domains is None or r.domain in domains)]


# ===================================================================================== stats
def rankdata(a: np.ndarray) -> np.ndarray:
    order = np.argsort(a, kind="mergesort")
    s = a[order]
    n = len(a)
    start = np.flatnonzero(np.r_[True, s[1:] != s[:-1]])
    end = np.r_[start[1:], n]
    avg = (start + end - 1) / 2.0 + 1.0
    r = np.empty(n, dtype=float)
    r[order] = np.repeat(avg, end - start)
    return r


def auroc(pos: np.ndarray, neg: np.ndarray) -> float | None:
    n1, n0 = len(pos), len(neg)
    if n1 == 0 or n0 == 0:
        return None
    r = rankdata(np.concatenate([pos, neg]))
    return float((r[:n1].sum() - n1 * (n1 + 1) / 2.0) / (n1 * n0))


def auroc_ci(pos, neg, n_boot: int = N_BOOT, seed: int = BOOT_SEED):
    """(auc, lo, hi) or None when either class has < 3 members."""
    pos = np.asarray(pos, dtype=float)
    neg = np.asarray(neg, dtype=float)
    if len(pos) < 3 or len(neg) < 3:
        return None
    a = auroc(pos, neg)
    rng = np.random.default_rng(seed)
    boots = np.empty(n_boot, dtype=float)
    for i in range(n_boot):
        p = pos[rng.integers(0, len(pos), len(pos))]
        n = neg[rng.integers(0, len(neg), len(neg))]
        boots[i] = auroc(p, n)
    return a, float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))


def threshold_at_fpr(clean: np.ndarray, pos: np.ndarray, target: float = 0.10) -> float:
    """Smallest threshold whose FPR on clean steps is <= target (exact 10% is unreachable under ties)."""
    cands = np.unique(np.concatenate([clean, pos]))
    for t in cands:
        if float(np.mean(clean >= t)) <= target:
            return float(t)
    return float(cands[-1]) + 1e-9


def fmt_auc(res) -> str:
    return "n/a" if res is None else f"{res[0]:.3f} [{res[1]:.3f}, {res[2]:.3f}]"


def fmt(v, nd: int = 3) -> str:
    return "n/a" if v is None else f"{v:.{nd}f}"


# ===================================================================================== report
class Report:
    def __init__(self) -> None:
        self.md: list[str] = []
        self.csv: list[dict] = []

    def line(self, s: str = "") -> None:
        self.md.append(s)

    def table(self, headers: list[str], rows: list[list[str]]) -> None:
        if not rows:
            self.line("_(no rows)_")
            self.line()
            return
        self.line("| " + " | ".join(headers) + " |")
        self.line("|" + "|".join("---" for _ in headers) + "|")
        for r in rows:
            self.line("| " + " | ".join(str(c) for c in r) + " |")
        self.line()

    def rec(self, **kw) -> None:
        self.csv.append({k: kw.get(k, "") for k in CSV_FIELDS})


def _auc_csv(rep, section, item, role, domain, metric, res, n_pos, n_neg, n_scored="", n_labeled="", note=""):
    rep.rec(section=section, item=item, role=role, domain=domain, metric=metric,
            value="" if res is None else round(res[0], 6),
            ci_lo="" if res is None else round(res[1], 6),
            ci_hi="" if res is None else round(res[2], 6),
            n_pos=n_pos, n_neg=n_neg, n_scored=n_scored, n_labeled=n_labeled, note=note)


# ===================================================================================== sections
def section_step_auroc(rep: Report, items, rows: list[StepRow]) -> None:
    rep.line("## 1. Step-level AUROC")
    rep.line()
    rep.line("Labeled runs only; cascade steps excluded; negatives = clean steps. "
             "`n_scored/n_labeled` counts labeled non-aux steps in the role scope the item applies to.")
    rep.line()
    out = []
    for name, item in items.items():
        for role in ROLE_SCOPES:
            for domain in DOMAIN_SCOPES:
                ap = applicable(item, role, domain)
                if ap is None:
                    continue
                roles, domains = ap
                scope = cell_rows(rows, roles, domains)
                if not scope:
                    continue
                n_labeled = len(scope)
                scored = [(r, item.scores[(r.run_id, r.step_id)]) for r in scope if (r.run_id, r.step_id) in item.scores]
                n_scored = len(scored)
                usable = [(r, s) for r, s in scored if r.cls != "cascade"]
                neg = np.array([s for r, s in usable if r.cls == "clean"], dtype=float)
                pos_all = np.array([s for r, s in usable if r.cls in ("decisive", "transient", "error")], dtype=float)
                pos_dec = np.array([s for r, s in usable if r.cls == "decisive"], dtype=float)
                a_all = auroc_ci(pos_all, neg)
                a_dec = auroc_ci(pos_dec, neg)
                out.append([name, role, domain, f"{n_scored}/{n_labeled}", len(pos_all), len(neg),
                            fmt_auc(a_all), len(pos_dec), fmt_auc(a_dec)])
                _auc_csv(rep, "step_auroc", name, role, domain, "auroc_all_errors", a_all,
                         len(pos_all), len(neg), n_scored, n_labeled)
                _auc_csv(rep, "step_auroc", name, role, domain, "auroc_decisive", a_dec,
                         len(pos_dec), len(neg), n_scored, n_labeled)
    rep.table(["item", "role", "domain", "n_scored/n_labeled", "n_pos(all)", "n_neg",
               "AUROC all errors [95% CI]", "n_pos(dec)", "AUROC decisive [95% CI]"], out)


def section_flag_metrics(rep: Report, items, rows: list[StepRow]) -> None:
    """Flag-level metrics for BINARY items (scores in {0,1}): precision / recall / F1 / FPR at the flag, plus decisive recall.
    AUROC is the wrong summary for a 0/1 module (it equals (recall + 1 - FPR)/2); this table is the primary one for D2."""
    rep.line("## 1b. Flag-level metrics for binary items (precision / recall / F1)")
    rep.line()
    rep.line("Same population as §1 (labeled runs, cascade excluded). A step is flagged when its score is 1. "
             "F1 = 2PR/(P+R); FPR = flagged clean / clean. `decisive recall` = flagged decisive steps / decisive steps.")
    rep.line()
    out = []
    for name, item in items.items():
        vals = set(item.scores.values())
        if not vals or not vals <= {0.0, 1.0}:
            continue
        for role in ROLE_SCOPES:
            for domain in DOMAIN_SCOPES:
                ap = applicable(item, role, domain)
                if ap is None:
                    continue
                roles, domains = ap
                scope = cell_rows(rows, roles, domains)
                scored = [(r, item.scores[(r.run_id, r.step_id)]) for r in scope if (r.run_id, r.step_id) in item.scores]
                usable = [(r, sc) for r, sc in scored if r.cls != "cascade"]
                pos = [sc for r, sc in usable if r.cls in ("decisive", "transient", "error")]
                neg = [sc for r, sc in usable if r.cls == "clean"]
                dec = [sc for r, sc in usable if r.cls == "decisive"]
                if len(pos) < 3 or len(neg) < 3:
                    continue
                tp, fp, fn = sum(pos), sum(neg), len(pos) - sum(pos)
                prec = tp / (tp + fp) if tp + fp else None
                rec = tp / len(pos)
                f1 = (2 * prec * rec / (prec + rec)) if prec is not None and (prec + rec) > 0 else None
                fpr = fp / len(neg)
                out.append([name, role, domain, len(pos), len(neg), int(tp), int(fp), fmt(prec), fmt(rec), fmt(f1), fmt(fpr),
                            f"{int(sum(dec))}/{len(dec)}" if dec else "n/a"])
                for metric, val in (("precision", prec), ("recall", rec), ("f1", f1), ("fpr", fpr)):
                    rep.rec(section="flag_metrics", item=name, role=role, domain=domain, metric=metric,
                            value="" if val is None else round(val, 4), n_pos=len(pos), n_neg=len(neg))
    if out:
        rep.table(["item", "role", "domain", "n_pos", "n_neg", "TP", "FP", "precision", "recall", "F1", "FPR", "decisive recall"], out)
    else:
        rep.line("_(no binary items)_")
        rep.line()


def trace_population(item: Item, roles: set[str], domains: set[str] | None, index, root) -> list[tuple[str, bool, float, float]]:
    """[(run_id, failed, max_score, mean_score)] for runs with >= 80% item coverage of the role scope."""
    pop = []
    for run_id, info in index.items():
        if domains is not None and info.get("domain") not in domains:
            continue
        steps = [s for s, a, r in non_aux_steps(Path(root) / "runs" / run_id) if r in roles]
        if not steps:
            continue
        vals = [item.scores[(run_id, s)] for s in steps if (run_id, s) in item.scores]
        if len(vals) / len(steps) < 0.8:
            continue
        pop.append((run_id, info.get("success") is False, float(np.max(vals)), float(np.mean(vals))))
    return pop


def section_trace_auroc(rep: Report, items, index, root) -> None:
    rep.line("## 2. Trace-level AUROC (positives = runs with success=false)")
    rep.line()
    rep.line("All runs in `runs/index.csv` (labels not required); a run enters only if the item scored "
             ">= 80% of that run's non-aux steps in the role scope.")
    rep.line()
    out = []
    for name, item in items.items():
        for role in ROLE_SCOPES:
            for domain in DOMAIN_SCOPES:
                ap = applicable(item, role, domain)
                if ap is None:
                    continue
                roles, domains = ap
                pop = trace_population(item, roles, domains, index, root)
                if not pop:
                    continue
                n_fail = sum(1 for _, f, _, _ in pop if f)
                n_succ = len(pop) - n_fail
                if n_fail < 3 or n_succ < 3:
                    note = f"not computable (success={n_succ}, failure={n_fail})"
                    out.append([name, role, domain, len(pop), n_fail, n_succ, note, note])
                    rep.rec(section="trace_auroc", item=name, role=role, domain=domain, metric="auroc_max",
                            n_pos=n_fail, n_neg=n_succ, n_scored=len(pop), note=note)
                    rep.rec(section="trace_auroc", item=name, role=role, domain=domain, metric="auroc_mean",
                            n_pos=n_fail, n_neg=n_succ, n_scored=len(pop), note=note)
                    continue
                res = {}
                for agg, idx in (("max", 2), ("mean", 3)):
                    p = np.array([r[idx] for r in pop if r[1]], dtype=float)
                    n = np.array([r[idx] for r in pop if not r[1]], dtype=float)
                    res[agg] = auroc_ci(p, n)
                    _auc_csv(rep, "trace_auroc", name, role, domain, f"auroc_{agg}", res[agg],
                             n_fail, n_succ, len(pop))
                out.append([name, role, domain, len(pop), n_fail, n_succ, fmt_auc(res["max"]), fmt_auc(res["mean"])])
    rep.table(["item", "role", "domain", "n_runs", "n_fail", "n_succ", "AUROC max [95% CI]", "AUROC mean [95% CI]"], out)


def section_attribution(rep: Report, items, rows, index, root) -> None:
    rep.line("## 3. Decisive-step attribution (failed labeled runs)")
    rep.line()
    rep.line("Predicted decisive step = argmax score over the run's scored steps in the role scope; ties broken "
             "planner-first then earliest step.  `+/-1` is one position in the run's non-aux step order.")
    rep.line()
    by_run: dict[str, list[StepRow]] = defaultdict(list)
    for r in rows:
        by_run[r.run_id].append(r)
    targets = []
    for run_id in sorted(by_run):
        lab = load_label(root, run_id) or {}
        ds = lab.get("decisive_step")
        if ds is None or index.get(run_id, {}).get("success") is not False:
            continue
        order = [s for s, _a, _r in non_aux_steps(Path(root) / "runs" / run_id)]
        pos = {s: i for i, s in enumerate(order)}
        agent_of = dict(load_steps(Path(root) / "runs" / run_id))
        targets.append((run_id, index.get(run_id, {}).get("domain", ""), int(ds), pos, agent_of))

    out = []
    for name, item in items.items():
        for role in ROLE_SCOPES:
            for domain in DOMAIN_SCOPES:
                ap = applicable(item, role, domain)
                if ap is None:
                    continue
                roles, domains = ap
                n = exact = near = agent_ok = 0
                for run_id, dom, ds, pos, agent_of in targets:
                    if domains is not None and dom not in domains:
                        continue
                    cands = [(s, item.scores[(run_id, s)]) for s in pos
                             if role_of(agent_of.get(s, "")) in roles and (run_id, s) in item.scores]
                    if not cands:
                        continue
                    pred = sorted(cands, key=lambda c: (-c[1], 0 if agent_of.get(c[0]) == "planner" else 1, c[0]))[0][0]
                    n += 1
                    exact += int(pred == ds)
                    near += int(ds in pos and abs(pos[pred] - pos[ds]) <= 1)
                    agent_ok += int(agent_of.get(pred) == agent_of.get(ds))
                if not n:
                    continue
                out.append([name, role, domain, n, f"{exact/n:.3f}", f"{near/n:.3f}", f"{agent_ok/n:.3f}"])
                for metric, v in (("exact_acc", exact / n), ("pm1_acc", near / n), ("agent_acc", agent_ok / n)):
                    rep.rec(section="attribution", item=name, role=role, domain=domain, metric=metric,
                            value=round(v, 6), n_pos=n)
    rep.table(["item", "role", "domain", "n_runs", "exact acc", "+/-1 acc", "agent acc"], out)


def section_threshold_latency(rep: Report, items, rows, index, root) -> None:
    rep.line("## 4. recall@FPR10 and detection latency")
    rep.line()
    rep.line("Threshold = the smallest score whose FPR on labeled **clean** steps of that role/domain is <= 10% "
             "(the achieved FPR is reported: binary or heavily tied items cannot hit 10% exactly).  "
             "Latency = positions after the "
             "decisive step until the first score >= threshold (non-aux order); runs that never cross are censored.")
    rep.line()
    lab_cache = {r.run_id: (load_label(root, r.run_id) or {}) for r in rows}
    out = []
    for name, item in items.items():
        for role in ROLE_SCOPES:
            for domain in DOMAIN_SCOPES:
                ap = applicable(item, role, domain)
                if ap is None:
                    continue
                roles, domains = ap
                scope = cell_rows(rows, roles, domains)
                scored = [(r, item.scores[(r.run_id, r.step_id)]) for r in scope if (r.run_id, r.step_id) in item.scores]
                clean = np.array([s for r, s in scored if r.cls == "clean"], dtype=float)
                pos = np.array([s for r, s in scored if r.cls in ("decisive", "transient", "error")], dtype=float)
                if len(clean) < 3 or len(pos) == 0:
                    continue
                thr = threshold_at_fpr(clean, pos, 0.10)
                fpr = float(np.mean(clean >= thr))
                rec = float(np.mean(pos >= thr))
                lat, censored = [], 0
                for run_id in sorted({r.run_id for r in scope}):
                    ds = lab_cache.get(run_id, {}).get("decisive_step")
                    if ds is None or index.get(run_id, {}).get("success") is not False:
                        continue
                    order = [s for s, _a, r_ in non_aux_steps(Path(root) / "runs" / run_id) if r_ in roles]
                    full = [s for s, _a, _r in non_aux_steps(Path(root) / "runs" / run_id)]
                    if ds not in full:
                        continue
                    d_pos = full.index(ds)
                    hit = None
                    for s in order:
                        if full.index(s) < d_pos or (run_id, s) not in item.scores:
                            continue
                        if item.scores[(run_id, s)] >= thr:
                            hit = full.index(s) - d_pos
                            break
                    if hit is None:
                        censored += 1
                    else:
                        lat.append(hit)
                med = float(np.median(lat)) if lat else None
                out.append([name, role, domain, f"{thr:.4g}", f"{fpr:.3f}", f"{rec:.3f}", len(pos),
                            f"{len(lat)}/{len(lat)+censored}", "n/a" if med is None else f"{med:.1f}"])
                rep.rec(section="recall_at_fpr10", item=name, role=role, domain=domain, metric="threshold",
                        value=round(thr, 6), n_pos=len(pos), n_neg=len(clean))
                rep.rec(section="recall_at_fpr10", item=name, role=role, domain=domain, metric="fpr",
                        value=round(fpr, 6), n_pos=len(pos), n_neg=len(clean))
                rep.rec(section="recall_at_fpr10", item=name, role=role, domain=domain, metric="recall_all_errors",
                        value=round(rec, 6), n_pos=len(pos), n_neg=len(clean))
                rep.rec(section="latency", item=name, role=role, domain=domain, metric="median_steps_after_decisive",
                        value="" if med is None else round(med, 3), n_pos=len(lat),
                        note=f"censored={censored}")
    rep.table(["item", "role", "domain", "threshold", "FPR(clean)", "recall(all errors)", "n_pos",
               "n_crossed/n_failed", "median latency"], out)


def section_tool_checks(rep: Report, rows, flags, root) -> None:
    rep.line("## 5. D2 tool checks vs `category=\"tool\"` labels")
    rep.line()
    rep.line("Population = every labeled non-aux step (cascade included); positive = a labeled error event of "
             "category `tool` at that step; a step is flagged when any tool call at it trips the check.")
    rep.line()
    tool_pos: set[tuple[str, int]] = set()
    for run_id in {r.run_id for r in rows}:
        lab = load_label(root, run_id) or {}
        for e in lab.get("error_events") or []:
            if e.get("category") == "tool" and isinstance(e.get("step"), int):
                tool_pos.add((run_id, int(e["step"])))
    out = []
    for check in D2_CHECKS:
        for domain in DOMAIN_SCOPES:
            scope = [r for r in rows if domain == "all" or r.domain == domain]
            if not scope:
                continue
            npos = sum(1 for r in scope if (r.run_id, r.step_id) in tool_pos)
            flagged = [r for r in scope if flags.get((r.run_id, r.step_id), {}).get(check)]
            tp = sum(1 for r in flagged if (r.run_id, r.step_id) in tool_pos)
            prec = tp / len(flagged) if flagged else None
            recl = tp / npos if npos else None
            out.append([check, domain, len(scope), npos, len(flagged), tp, fmt(prec), fmt(recl)])
            rep.rec(section="tool_checks", item=f"D2_check_{check}", role="all", domain=domain, metric="precision",
                    value="" if prec is None else round(prec, 6), n_pos=npos, n_scored=len(flagged), n_labeled=len(scope))
            rep.rec(section="tool_checks", item=f"D2_check_{check}", role="all", domain=domain, metric="recall",
                    value="" if recl is None else round(recl, 6), n_pos=npos, n_scored=len(flagged), n_labeled=len(scope))
    rep.table(["check", "domain", "n_steps", "n_pos(tool)", "n_flagged", "TP", "precision", "recall"], out)


def section_matched(rep: Report, items, rows) -> None:
    rep.line("## 6. Matched sub-table (steps scored by D1 AND D2)")
    rep.line()
    names = [n for n in ("D1_1-conf", "D2") if n in items]
    if len(names) < 2:
        rep.line("_(needs D1 and D3; missing " + ", ".join(
            n for n in ("D1_1-conf", "D2") if n not in items) + ")_")
        rep.line()
        return
    keys = set(items[names[0]].scores)
    for n in names[1:]:
        keys &= set(items[n].scores)
    rep.line(f"Intersection = {len(keys)} step(s) scored by all of {', '.join(names)}.")
    rep.line()
    matched = [r for r in rows if (r.run_id, r.step_id) in keys]
    out = []
    for name in names:
        item = items[name]
        for role in ROLE_SCOPES:
            for domain in DOMAIN_SCOPES:
                ap = applicable(item, role, domain)
                if ap is None:
                    continue
                roles, domains = ap
                scope = [r for r in cell_rows(matched, roles, domains) if r.cls != "cascade"]
                if not scope:
                    continue
                neg = np.array([item.scores[(r.run_id, r.step_id)] for r in scope if r.cls == "clean"], dtype=float)
                pos = np.array([item.scores[(r.run_id, r.step_id)] for r in scope
                                if r.cls in ("decisive", "transient", "error")], dtype=float)
                res = auroc_ci(pos, neg)
                out.append([name, role, domain, len(pos), len(neg), fmt_auc(res)])
                _auc_csv(rep, "matched", name, role, domain, "auroc_all_errors", res, len(pos), len(neg),
                         n_scored=len(scope), note="matched intersection")
    rep.table(["item", "role", "domain", "n_pos", "n_neg", "AUROC all errors [95% CI]"], out)


def pct_thresholds(items, rows, pct: float = 90.0) -> dict[str, float]:
    """Per item: the pct-th percentile of its scores over all labeled scored steps."""
    out = {}
    for name, item in items.items():
        vals = [item.scores[(r.run_id, r.step_id)] for r in rows if (r.run_id, r.step_id) in item.scores]
        if vals:
            out[name] = float(np.percentile(np.asarray(vals, dtype=float), pct))
    return out


def section_any_flag(rep: Report, items, rows) -> None:
    rep.line("## 7. Any-flag coverage (descriptive)")
    rep.line()
    thr = pct_thresholds(items, rows, 90.0)
    err = [r for r in rows if r.cls in ("decisive", "transient", "error")]
    hit = 0
    for r in err:
        k = (r.run_id, r.step_id)
        if any(k in items[n].scores and items[n].scores[k] >= t for n, t in thr.items()):
            hit += 1
    frac = hit / len(err) if err else None
    rep.line(f"Of the {len(err)} labeled error steps (decisive + transient), **{fmt(frac)}** "
             f"({hit}/{len(err)}) are flagged by at least one item at its own 90th-percentile threshold "
             f"(percentiles taken over that item's scores on all labeled non-aux steps).")
    rep.line()
    rep.line("Item thresholds: " + ", ".join(f"`{n}`={t:.4f}" for n, t in sorted(thr.items())) + ".")
    rep.line()
    rep.rec(section="any_flag", item="any", role="all", domain="all", metric="frac_error_steps_flagged",
            value="" if frac is None else round(frac, 6), n_pos=len(err), note=f"hit={hit}")


# ===================================================================================== main
def build_report(root: str | Path = ".") -> Report:
    index = load_index(root)
    items = load_items(root)
    rows = labeled_steps(root, index)
    flags = load_d3_tool_flags(root)

    rep = Report()
    d1_rows = read_jsonl(Path(root) / "audit" / "d1.jsonl")
    methods = sorted({str(r.get("method")) for r in d1_rows if r.get("method")})
    lab_dom: dict[str, int] = defaultdict(int)
    for run_id in labeled_run_ids(root):
        lab_dom[index.get(run_id, {}).get("domain") or run_id.split("_")[0]] += 1

    rep.line("# Detection metrics")
    rep.line()
    rep.line(f"- generated: {time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    rep.line(f"- d1_scored_n: {len(d1_rows)} rows in `audit/d1.jsonl`")
    rep.line("- labeled runs: " + (", ".join(f"{d}={n}" for d, n in sorted(lab_dom.items())) or "none")
             + f" (total {sum(lab_dom.values())}); runs in index: {len(index)}")
    rep.line(f"- D1 method(s) present: {', '.join(methods) if methods else 'none'}")
    rep.line(f"- items scored: {', '.join(items) if items else 'none'}")
    rep.line("- bootstrap: 1000 stratified resamples, seed 0; AUROC is `n/a` when n_pos < 3 or n_neg < 3.")
    rep.line()
    if not rows:
        rep.line("**No labeled steps found — every table below is empty.**")
        rep.line()

    section_step_auroc(rep, items, rows)
    section_flag_metrics(rep, items, rows)
    section_trace_auroc(rep, items, index, root)
    section_attribution(rep, items, rows, index, root)
    section_threshold_latency(rep, items, rows, index, root)
    section_tool_checks(rep, rows, flags, root)
    section_matched(rep, items, rows)
    section_any_flag(rep, items, rows)
    return rep


def main() -> int:
    ap = argparse.ArgumentParser(description="step / trace / attribution detection metrics")
    ap.add_argument("--root", default=".", help="directory holding runs/ labels/ audit/ eval/")
    ap.add_argument("--out", default=None, help="markdown output (default <root>/eval/metrics.md)")
    ap.add_argument("--pre", action="store_true", help="write eval/metrics_pre.md instead (pre-D1-cut snapshot)")
    a = ap.parse_args()

    out = Path(a.out) if a.out else Path(a.root) / "eval" / ("metrics_pre.md" if a.pre else "metrics.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    rep = build_report(a.root)
    out.write_text("\n".join(rep.md) + "\n", encoding="utf-8")
    csv_path = out.with_suffix(".csv")
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        for r in rep.csv:
            w.writerow(r)
    print(f"wrote {out} ({len(rep.md)} lines) and {csv_path} ({len(rep.csv)} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
