"""Extract handoff events from TraceElephant runs into data/handoffs/<system>.jsonl and print stats."""
import argparse, collections, statistics
from pathlib import Path
from agent_handoff.data.traceelephant import iter_runs, extract_magentic_handoffs, to_jsonl

p = argparse.ArgumentParser()
p.add_argument("--data_root", default="data/external/TraceElephant_data/data")
p.add_argument("--out", default="data/handoffs/magentic_one.jsonl")
a = p.parse_args()

all_h = []
per_run = []
for run in iter_runs(Path(a.data_root), system="magentic-one"):
    hs = extract_magentic_handoffs(run)
    per_run.append(len(hs)); all_h.extend(hs)
to_jsonl(all_h, Path(a.out))

print(f"runs={len(per_run)} handoffs={len(all_h)} per-run min/median/max={min(per_run)}/{statistics.median(per_run)}/{max(per_run)} zero-handoff runs={sum(1 for n in per_run if n==0)}")
print("receivers:", dict(collections.Counter(h.receiver for h in all_h)))
print("mistake_in_segment:", sum(h.mistake_in_segment for h in all_h), "| mistake_at_this_handoff:", sum(h.mistake_at_this_handoff for h in all_h))
print("runs whose mistake_agent is Orchestrator:", len({h.run_id for h in all_h if h.mistake_agent=='Orchestrator'}))
toks = [h.sender_prompt_tokens for h in all_h if h.sender_prompt_tokens]
print(f"sender prompt tokens: min/median/p90/max = {min(toks)}/{statistics.median(toks)}/{sorted(toks)[int(len(toks)*0.9)]}/{max(toks)}")
seglen = [len(h.receiver_steps) for h in all_h]
print(f"receiver segment steps: min/median/max = {min(seglen)}/{statistics.median(seglen)}/{max(seglen)}")

# ---- Type II: context-reset handoffs ----
from agent_handoff.data.traceelephant import extract_magentic_resets
resets = []
for run in iter_runs(Path(a.data_root), system="magentic-one"):
    resets.extend(extract_magentic_resets(run))
to_jsonl(resets, Path(a.out).with_name("magentic_one_resets.jsonl"))
print(f"\nreset handoffs={len(resets)} in {len({r.run_id for r in resets})} runs")
print("mistake_position:", dict(collections.Counter(r.mistake_position for r in resets)))
print("facts/plan found:", sum(r.facts_text!='' for r in resets), sum(r.plan_text!='' for r in resets))
pt = [r.pre_reset_prompt_tokens for r in resets if r.pre_reset_prompt_tokens]
print(f"pre-reset transcript tokens: min/median/max = {min(pt)}/{statistics.median(pt)}/{max(pt)} | facts chars median {statistics.median(len(r.facts_text) for r in resets)}")
