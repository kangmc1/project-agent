"""Figures from results/summary.json and results/compression_events.json -> results/figures/*.png"""
import json, collections
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
S = json.load(open("results/summary.json")); EV = json.load(open("results/compression_events.json"))
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})

# Fig 1: S(k) curves, one panel per budget, lines = format x guard
budgets = sorted({v["budget"] for v in S["stress"].values()})
fig, axes = plt.subplots(1, max(1, len(budgets)), figsize=(4.2 * max(1, len(budgets)), 3.6), sharey=True)
axes = [axes] if len(budgets) == 1 else list(axes)
style = {("free", False): ("#B23A3A", "-"), ("free", True): ("#B23A3A", "--"), ("json", False): ("#1D6F7A", "-"), ("json", True): ("#1D6F7A", "--")}
for ax, b in zip(axes, budgets):
    for k, v in S["stress"].items():
        if v["budget"] != b: continue
        col, ls = style[(v["format"], v["guard"])]
        ax.plot([c["hop"] for c in v["curve"]], [c["preserved"] for c in v["curve"]], color=col, ls=ls, marker="o", ms=3, label=f"{v['format']}{' + guard' if v['guard'] else ''} (n={v['n']})")
    ax.set_title(f"compression budget {b} words"); ax.set_xlabel("compression hop k"); ax.set_ylim(0, 1.02); ax.grid(alpha=.25)
axes[0].set_ylabel("seeded obligations preserved  S(k)"); axes[-1].legend(fontsize=8, loc="lower left")
fig.suptitle("Obligation survival across repeated compression (chain stress test)"); fig.tight_layout(); fig.savefig("results/figures/fig_stress_curves.png", dpi=160); plt.close(fig)

# Fig 2: workflow final metrics per condition (grouped bars)
W = S["workflow"]; keys = list(W.keys())
if keys:
    fig, ax = plt.subplots(figsize=(max(6, 1.1 * len(keys)), 3.8))
    x = range(len(keys)); w = 0.26
    ax.bar([i - w for i in x], [W[k]["final_preserved"] for k in keys], w, label="final: obligations preserved", color="#1D6F7A")
    ax.bar([i for i in x], [W[k]["constraints_kept"] for k in keys], w, label="final: constraints kept", color="#2C7A55")
    ax.bar([i + w for i in x], [min(1, W[k]["fabricated_final_mean"] / 4) for k in keys], w, label="final: fabricated values (/4)", color="#9A5B00")
    ax.set_xticks(list(x)); ax.set_xticklabels([k.replace("|w1", "") for k in keys], rotation=30, ha="right", fontsize=8); ax.set_ylim(0, 1.05); ax.legend(fontsize=8); ax.grid(axis="y", alpha=.25)
    ax.set_title("Workflow: what survives into the final deliverable (visibility | compression format | guard)"); fig.tight_layout(); fig.savefig("results/figures/fig_workflow_final.png", dpi=160); plt.close(fig)

# Fig 3: JSD vs preserved at compression events, colored by format
if EV:
    fig, ax = plt.subplots(figsize=(4.6, 3.6))
    for fmt, col in (("free", "#B23A3A"), ("json", "#1D6F7A")):
        xs = [e["jsd"] for e in EV if fmt in e["condition"]]; ys = [e["preserved"] for e in EV if fmt in e["condition"]]
        ax.scatter(xs, ys, s=18, alpha=.7, color=col, label=fmt)
    ax.set_xlabel("decision divergence across compression (JSD, bits)"); ax.set_ylabel("obligations preserved after compression"); ax.grid(alpha=.25); ax.legend(fontsize=8)
    ax.set_title(f"Policy shift vs. information loss (n={len(EV)}; AUROC={S.get('jsd_auroc_loss', 0):.2f})", fontsize=9); fig.tight_layout(); fig.savefig("results/figures/fig_jsd_vs_loss.png", dpi=160); plt.close(fig)
print("figures written:", sorted(p.name for p in __import__('pathlib').Path('results/figures').glob('*.png')))
