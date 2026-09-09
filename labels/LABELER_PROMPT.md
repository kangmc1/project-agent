# Labeler subagent prompt (template)

You are a careful annotator producing evaluation gold for a failure-detection study. Follow `labels/RUBRIC.md` exactly.
You must NOT read anything under `audit/` (detector outputs) — only `runs/<run_id>/summary.md` files listed below and,
if a summary is ambiguous, `runs/<run_id>/steps.jsonl` for the exact text of a step.

For each run_id in your assignment:
1. Read `runs/<run_id>/summary.md` completely.
2. Determine success/failure from the header (reward / gold vs submitted).
3. Walk the steps in order; for every planner / policy_checker / db_agent / solver / verifier step decide whether an
   error event occurred (categories: handoff, tool, reasoning_stability; subtags as in the rubric). Ignore [customer]
   and summarizer steps. Every event needs a concrete `evidence` string quoting the offending content and the record it
   contradicts (tool result, customer statement, policy clause, subagent report, python output).
4. Mark `recovered` (+ `recovery_step`) when a later step corrects the error.
5. Set `decisive_step` = the first unrecovered error on the path to the failure (null for successful runs, or for a
   failed run with no identifiable erroneous step — then explain in `labels/notes.md`).
6. Write `labels/<run_id>.json` with exactly this schema:
   {"run_id": str, "batch": int, "decisive_step": int|null,
    "error_events": [{"step": int, "agent": str, "category": "handoff"|"tool"|"reasoning_stability",
                      "subtag": "hallucination_like"|"reasoning_like"|"handoff_induced"|"compression_induced"|null,
                      "recovered": bool, "recovery_step": int|null, "evidence": str}]}
7. Be conservative: no event without evidence; do not label style, verbosity, or the customer's own errors.

Assignment: <RUN_IDS>. After writing the files, run
`PYTHONPATH=/home/kangmc1/agent_failure_trace python -m src.eval.labels --validate` (env: `source /home/kangmc1/miniforge3/etc/profile.d/conda.sh && conda activate agentbench`)
and fix any schema errors. Report: per run_id — success flag, n_events, decisive_step, one-line rationale.
