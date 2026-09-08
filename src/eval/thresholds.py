"""Label-free percentile thresholds vs the label-optimal threshold (Youden J).

For D1 (1-confidence), D2 (unsupported), D7 (report->planner) and D9 (1-consistency):
  * top 5% / top 10% = the 95th / 90th percentile of that item's score distribution over ALL scored steps,
    including runs that were never labeled (this is the operating rule an unlabeled deployment can apply);
  * label-optimal = the threshold maximising Youden J (TPR - FPR) on labeled steps
    (positives = decisive + transient, negatives = clean, cascade excluded).
Each row reports the threshold value, its FPR and recall on the labeled steps, and the gap to label-optimal.

Usage:  python -m src.eval.thresholds [--out eval/thresholds.md] [--root .]
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np

from .labels import load_index, non_aux_steps
from .metrics import (DOMAIN_SCOPES, ROLE_SCOPES, Item, applicable, cell_rows, d7_report_to_planner,
                      labeled_steps, load_items)

WANTED = ("D1_1-conf", "D2_unsupported", "D9_1-consistency")


def pool_scores(item: Item, roles: set[str], domains: set[str] | None, index, root) -> np.ndarray:
    """Every score of the item over all runs in the index (labeled or not) inside the role/domain scope."""
    vals: list[float] = []
    for run_id, info in index.items():
        if domains is not None and info.get("domain") not in domains:
            continue
        for step_id, _agent, role in non_aux_steps(Path(root) / "runs" / run_id):
            if role in roles and (run_id, step_id) in item.scores:
                vals.append(item.scores[(run_id, step_id)])
    return np.asarray(vals, dtype=float)


def rates(thr: float, pos: np.ndarray, neg: np.ndarray) -> tuple[float, float]:
    """(recall on all-error positives, FPR on clean negatives)."""
    rec = float(np.mean(pos >= thr)) if len(pos) else float("nan")
    fpr = float(np.mean(neg >= thr)) if len(neg) else float("nan")
    return rec, fpr


def youden_optimal(pos: np.ndarray, neg: np.ndarray) -> tuple[float, float, float, float]:
    """(threshold, J, recall, fpr) maximising TPR - FPR; ties go to the higher (stricter) threshold."""
    cands = np.unique(np.concatenate([pos, neg]))
    best = (float(cands[0]), -2.0, 0.0, 0.0)
    for t in cands:
        rec, fpr = rates(float(t), pos, neg)
        j = rec - fpr
        if j > best[1] or (j == best[1] and float(t) > best[0]):
            best = (float(t), j, rec, fpr)
    return best


def build(root: str | Path = ".") -> list[str]:
    index = load_index(root)
    items = load_items(root)
    rows = labeled_steps(root, index)
    names = [n for n in WANTED if n in items]
    d7 = d7_report_to_planner(items)
    if d7:
        names.insert(2 if len(names) > 2 else len(names), d7)

    md: list[str] = ["# Percentile vs label-optimal thresholds", ""]
    md.append(f"- generated: {time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    md.append(f"- items: {', '.join(names) if names else 'none present in audit/'}")
    md.append(f"- percentile pool: every scored step of {len(index)} run(s) in `runs/index.csv`, labeled or not")
    md.append("- FPR / recall are always measured on labeled steps (cascade excluded); "
              "`d recall` / `d FPR` are the gaps to the label-optimal row of the same cell.")
    md.append("")
    md.append("| item | role | domain | rule | threshold | n_pool | n_pos | n_neg | FPR | recall | d recall | d FPR |")
    md.append("|---|---|---|---|---|---|---|---|---|---|---|---|")

    n_cells = 0
    for name in names:
        item = items[name]
        for role in ROLE_SCOPES:
            for domain in DOMAIN_SCOPES:
                ap = applicable(item, role, domain)
                if ap is None:
                    continue
                roles, domains = ap
                scope = [r for r in cell_rows(rows, roles, domains) if r.cls != "cascade"]
                scored = [(r, item.scores[(r.run_id, r.step_id)]) for r in scope if (r.run_id, r.step_id) in item.scores]
                pos = np.array([s for r, s in scored if r.cls in ("decisive", "transient", "error")], dtype=float)
                neg = np.array([s for r, s in scored if r.cls == "clean"], dtype=float)
                if len(pos) < 1 or len(neg) < 3:
                    continue
                pool = pool_scores(item, roles, domains, index, root)
                if pool.size == 0:
                    continue
                opt_thr, _j, opt_rec, opt_fpr = youden_optimal(pos, neg)
                cells = [("top 5% (p95)", float(np.percentile(pool, 95))),
                         ("top 10% (p90)", float(np.percentile(pool, 90))),
                         ("label-optimal (max J)", opt_thr)]
                for rule, thr in cells:
                    rec, fpr = rates(thr, pos, neg)
                    d_rec = "-" if rule.startswith("label") else f"{rec - opt_rec:+.3f}"
                    d_fpr = "-" if rule.startswith("label") else f"{fpr - opt_fpr:+.3f}"
                    md.append(f"| {name} | {role} | {domain} | {rule} | {thr:.4g} | {pool.size} | "
                              f"{len(pos)} | {len(neg)} | {fpr:.3f} | {rec:.3f} | {d_rec} | {d_fpr} |")
                n_cells += 1
    md.append("")
    if not n_cells:
        md.append("_No cell had >= 1 positive and >= 3 clean labeled steps._")
        md.append("")
    md.append(f"cells: {n_cells}")
    md.append("")
    return md


def main() -> int:
    ap = argparse.ArgumentParser(description="percentile vs label-optimal detection thresholds")
    ap.add_argument("--root", default=".", help="directory holding runs/ labels/ audit/ eval/")
    ap.add_argument("--out", default=None, help="markdown output (default <root>/eval/thresholds.md)")
    a = ap.parse_args()
    out = Path(a.out) if a.out else Path(a.root) / "eval" / "thresholds.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    md = build(a.root)
    out.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"wrote {out} ({len(md)} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
