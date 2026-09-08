#!/usr/bin/env bash
# D1 full scoring, decode-path teacher-forced (stepwise) on ALL decision points, planner-first, resumable.
# 04:35: common-prefix (trie) call sharing added — identical values per (prompt, token); ~16.6 calls/decision instead of ~43.
# Reference for validity = original run-time logprobs of the chosen action (template check), not method 2.
# Method-2 partial rows (211, 03:52-04:12) kept in audit/d1_m2_partial.jsonl as a comparison sample only.
cd /home/kangmc1/project-agent
source /home/kangmc1/miniforge3/etc/profile.d/conda.sh && conda activate agent_failure_trace
echo "d1 stepwise full start $(date)"
flock audit/d1.lock python -m src.audit.d1 --all --runs runs --method stepwise --out audit/d1.jsonl 2>&1 | grep -v PyTorch | tail -2
echo "stepwise done $(date) rows=$(wc -l < audit/d1.jsonl)"
