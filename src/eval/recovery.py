"""Recovery / cascade profiles around labeled error steps, and a per-subtag item breakdown.

eval/recovery.png
  (a) mean D1 instability (1 - confidence) and D2 unsupported aligned at **transient** error steps
      (offsets -3..+5 in non-aux step order; the mean recovery offset is marked);
  (b) the same aligned at **decisive** steps, with the cascade region (offset > 0) shaded.
eval/subtags.md
  per label subtag: the mean of every item score at the labeled step and the fraction of those steps
  flagged by that item at its own 90th-percentile threshold.

Usage:  python -m src.eval.recovery [--out eval/recovery.png] [--subtags eval/subtags.md] [--root .]
"""
from __future__ import annotations

import argparse
import sys
import time
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .labels import labeled_run_ids, load_index, load_label, non_aux_steps
from .metrics import labeled_steps, load_items, pct_thresholds

OFFSETS = list(range(-3, 6))
D1 = "D1_1-conf"
D2 = "D2_unsupported"


def anchors(root: str | Path, index: dict) -> tuple[list[tuple[str, int, int | None]], list[tuple[str, int]]]:
    """([(run_id, transient_step, recovery_step)], [(run_id, decisive_step)]) over labeled runs."""
    transient, decisive = [], []
    for run_id in labeled_run_ids(root):
        lab = load_label(root, run_id) or {}
        ds = lab.get("decisive_step")
        for e in lab.get("error_events") or []:
            if e.get("recovered") and isinstance(e.get("step"), int):
                transient.append((run_id, int(e["step"]), e.get("recovery_step")))
        if isinstance(ds, int):
            decisive.append((run_id, ds))
    return transient, decisive


def profile(items, root, anchor_list, key_of_anchor) -> dict[str, dict[int, tuple[float, int]]]:
    """{item_name: {offset: (mean_score, n)}} aligned on the anchor's position in the non-aux step order."""
    acc: dict[str, dict[int, list[float]]] = {n: defaultdict(list) for n in items}
    for a in anchor_list:
        run_id, step = key_of_anchor(a)
        order = [s for s, _ag, _r in non_aux_steps(Path(root) / "runs" / run_id)]
        if step not in order:
            continue
        i = order.index(step)
        for o in OFFSETS:
            j = i + o
            if not (0 <= j < len(order)):
                continue
            k = (run_id, order[j])
            for name, item in items.items():
                if k in item.scores:
                    acc[name][o].append(item.scores[k])
    return {n: {o: (float(np.mean(v)), len(v)) for o, v in d.items() if v} for n, d in acc.items()}


def mean_recovery_offset(root, transient) -> float | None:
    offs = []
    for run_id, step, rec in transient:
        if not isinstance(rec, int):
            continue
        order = [s for s, _a, _r in non_aux_steps(Path(root) / "runs" / run_id)]
        if step in order and rec in order:
            offs.append(order.index(rec) - order.index(step))
    return float(np.mean(offs)) if offs else None


def draw_panel(ax, prof, title: str, n_anchor: int) -> None:
    ax.set_title(f"{title}  (n={n_anchor})", fontsize=10)
    ax.set_xlabel("offset from anchor step (non-aux order)")
    ax.set_xticks(OFFSETS)
    ax.axvline(0, color="0.35", lw=1.2)
    ax.set_ylabel("mean 1 - confidence (D1)", color="tab:blue")
    ax.tick_params(axis="y", labelcolor="tab:blue")
    ax2 = ax.twinx()
    ax2.set_ylabel("mean unsupported (D2)", color="tab:orange")
    ax2.tick_params(axis="y", labelcolor="tab:orange")
    for name, axis, color, marker in ((D1, ax, "tab:blue", "o"), (D2, ax2, "tab:orange", "s")):
        d = prof.get(name) or {}
        xs = [o for o in OFFSETS if o in d]
        if not xs:
            continue
        ys = [d[o][0] for o in xs]
        axis.plot(xs, ys, marker=marker, color=color, lw=1.6, ms=4, label=name)
        if name == D1:
            for x, y in zip(xs, ys):
                axis.annotate(str(d[x][1]), (x, y), textcoords="offset points", xytext=(0, -11),
                              fontsize=6, color="0.45", ha="center")
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    if h1 or h2:
        ax.legend(h1 + h2, l1 + l2, fontsize=7, loc="upper left")


def make_figure(items, root, out: Path) -> tuple[int, int]:
    index = load_index(root)
    transient, decisive = anchors(root, index)
    sub = {n: items[n] for n in (D1, D2) if n in items}
    p_tr = profile(sub, root, transient, lambda a: (a[0], a[1]))
    p_de = profile(sub, root, decisive, lambda a: (a[0], a[1]))

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.2))
    draw_panel(axes[0], p_tr, "(a) aligned at transient (recovered) error steps", len(transient))
    rec_off = mean_recovery_offset(root, transient)
    if rec_off is not None:
        axes[0].axvline(rec_off, color="tab:green", ls="--", lw=1.2)
        axes[0].annotate(f"mean recovery +{rec_off:.1f}", (rec_off, 1.0), xycoords=("data", "axes fraction"),
                         xytext=(3, -10), textcoords="offset points", fontsize=7, color="tab:green")
    draw_panel(axes[1], p_de, "(b) aligned at decisive steps", len(decisive))
    axes[1].axvspan(0.5, OFFSETS[-1] + 0.4, color="tab:red", alpha=0.07)   # cascade = steps after the decisive one
    axes[1].annotate("cascade region", (0.42, 0.02), xycoords="axes fraction", fontsize=7, color="tab:red")
    for ax in axes:
        ax.set_xlim(OFFSETS[0] - 0.4, OFFSETS[-1] + 0.4)
        ax.grid(alpha=0.25, axis="y")
    fig.suptitle("Instability around labeled error steps", fontsize=11)
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return len(transient), len(decisive)


def subtags_md(items, root) -> list[str]:
    index = load_index(root)
    rows = labeled_steps(root, index)
    thr = pct_thresholds(items, rows, 90.0)
    by_sub: dict[str, set[tuple[str, int]]] = defaultdict(set)
    for run_id in labeled_run_ids(root):
        lab = load_label(root, run_id) or {}
        for e in lab.get("error_events") or []:
            if isinstance(e.get("step"), int):
                by_sub[e.get("subtag") or "none"].add((run_id, int(e["step"])))

    md = ["# Item scores by label subtag", "",
          f"- generated: {time.strftime('%Y-%m-%d %H:%M:%S %Z')}",
          "- `mean` is over the labeled error steps of that subtag where the item has a score; "
          "`flagged` is the fraction of those steps at or above the item's 90th-percentile threshold "
          "(percentile taken over the item's scores on all labeled non-aux steps).", ""]
    md.append("| subtag | n_steps | item | n_scored | mean | flagged@p90 | threshold |")
    md.append("|---|---|---|---|---|---|---|")
    for sub in sorted(by_sub):
        steps = sorted(by_sub[sub])
        for name, item in items.items():
            vals = [item.scores[k] for k in steps if k in item.scores]
            if not vals:
                md.append(f"| {sub} | {len(steps)} | {name} | 0 | - | - | "
                          f"{thr.get(name, float('nan')):.4f} |")
                continue
            t = thr.get(name)
            flag = "-" if t is None else f"{np.mean(np.asarray(vals) >= t):.3f}"
            md.append(f"| {sub} | {len(steps)} | {name} | {len(vals)} | {np.mean(vals):.4f} | {flag} | "
                      f"{'-' if t is None else f'{t:.4f}'} |")
    md.append("")
    if not by_sub:
        md.append("_No labeled error events._")
        md.append("")
    return md


def main() -> int:
    ap = argparse.ArgumentParser(description="recovery/cascade profiles and subtag breakdown")
    ap.add_argument("--root", default=".", help="directory holding runs/ labels/ audit/ eval/")
    ap.add_argument("--out", default=None, help="figure path (default <root>/eval/recovery.png)")
    ap.add_argument("--subtags", default=None, help="markdown path (default <root>/eval/subtags.md)")
    a = ap.parse_args()
    png = Path(a.out) if a.out else Path(a.root) / "eval" / "recovery.png"
    smd = Path(a.subtags) if a.subtags else Path(a.root) / "eval" / "subtags.md"
    items = load_items(a.root)
    n_tr, n_de = make_figure(items, a.root, png)
    md = subtags_md(items, a.root)
    smd.parent.mkdir(parents=True, exist_ok=True)
    smd.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"wrote {png} (transient anchors={n_tr}, decisive anchors={n_de}) and {smd} ({len(md)} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
