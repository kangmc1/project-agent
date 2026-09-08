"""Aggregate grid results -> results/summary.json + printed tables."""
import json, statistics
from pathlib import Path
from agent_handoff.eval.aggregate import load, stress_curves, workflow_table, compression_events, auroc

stress = load("results/raw/stress_grid.jsonl"); wf = load("results/raw/workflow_grid.jsonl")
summary = {"stress": stress_curves(stress), "workflow": workflow_table(wf)}
ev = compression_events(wf); summary["compression_events_n"] = len(ev)
if ev:
    pos = [x["jsd"] for x in ev if x["loss"]]; neg = [x["jsd"] for x in ev if not x["loss"]]
    summary["jsd_auroc_loss"] = auroc(pos, neg); summary["entropy_auroc_loss"] = auroc([x["entropy"] for x in ev if x["loss"]], [x["entropy"] for x in ev if not x["loss"]])
    summary["loss_rate"] = statistics.mean(x["loss"] for x in ev)
json.dump(summary, open("results/summary.json", "w"), indent=1)
json.dump(ev, open("results/compression_events.json", "w"), indent=0)

print(f"stress chains: {len(stress)} | workflow runs: {len(wf)} | compression events: {len(ev)}")
print("\n== STRESS S(k): preserved per hop ==")
for k, v in summary["stress"].items():
    print(f"{k:16s} n={v['n']:2d} " + " ".join(f"{c['preserved']:.2f}" for c in v["curve"]) + f" | half-life hop={v['half_life_hop']} | promoted@last={v['curve'][-1]['promoted']:.2f}")
print("\n== WORKFLOW final metrics ==")
for k, v in summary["workflow"].items():
    print(f"{k:22s} n={v['n']:2d} final_pres={v['final_preserved']:.2f} promoted={v['final_promoted']:.2f} constraints={v['constraints_kept']:.2f} prohib_viol={v['prohibition_violation_rate']:.2f} fab={v['fabricated_final_mean']:.1f} compr={v['compressions_mean']:.1f} compr_pres={v['compression_preserved_mean'] if v['compression_preserved_mean'] is None else round(v['compression_preserved_mean'],2)} jsd={v['jsd_mean'] if v['jsd_mean'] is None else round(v['jsd_mean'],3)} revise={v['verifier_revise_rate'] if v['verifier_revise_rate'] is None else round(v['verifier_revise_rate'],2)} H={v['entropy_mean']:.2f}")
if ev:
    print(f"\ncompression events: n={len(ev)} loss_rate={summary['loss_rate']:.2f} | AUROC(JSD→loss)={summary['jsd_auroc_loss']:.2f} | AUROC(entropy→loss)={summary['entropy_auroc_loss']:.2f}")
