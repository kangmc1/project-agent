#!/usr/bin/env bash
# Full D1 scoring after the equivalence gate FAILED (ratio_within_0.01 = 0.62 < 0.95, 2026-09-09 03:50 KST).
# Primary = method 2 (forced-prefix prompt_logprobs; the definition) on ALL decision points, planner-first, resumable.
# Secondary = stepwise allowed_token_ids on all decision points, written to a separate file for the comparison table only.
cd /home/kangmc1/project-agent
source /home/kangmc1/miniforge3/etc/profile.d/conda.sh && conda activate agent_failure_trace
echo "d1 full start $(date)"
flock audit/d1.lock python -m src.audit.d1 --all --runs runs --method m2 --out audit/d1.jsonl 2>&1 | grep -v PyTorch | tail -2
echo "m2 done $(date) rows=$(wc -l < audit/d1.jsonl)"
flock audit/d1.lock python -m src.audit.d1 --all --runs runs --method stepwise --out audit/d1_stepwise.jsonl 2>&1 | grep -v PyTorch | tail -2
echo "stepwise done $(date) rows=$(wc -l < audit/d1_stepwise.jsonl)"
