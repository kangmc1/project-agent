# agent-handoff

How stable is an agent system across handoffs? A benchmark and pipeline that measures how much of what an agent team knows (constraints, verified facts, open questions, prohibitions) survives role boundaries and context compression, and whether the orchestrator's action distribution predicts the loss before it happens.

> Take-home task, 2026-09-08 ~ 09-09. Work in progress. The system definition that the code must follow is `docs/SETUP.md`; the proposal is `docs/proposal.md`.

## The setting in one paragraph

Every scenario has a user task and a private **source** (a synthetic work log with dated facts, amounts, ids). An Orchestrator (Qwen3-8B) runs a small team of three agents (same model, different roles): the **Researcher** is the only one who can read the source; the **Executor** drafts the concrete action from what the team has; the **Verifier** checks the draft against the team's state. Facts enter the team only through Researcher reports, then have to survive compression (triggered by a word budget) and reach the final deliverable. Eight seeded obligations per scenario give ground truth by construction, so survival is scored by a rule matcher, not an LLM judge. The orchestrator's next-agent choice is a fixed 4-way action; its distribution is read from constrained-decoding logprobs and used as an early signal of upcoming loss.

## Layout

```
src/agent_handoff/
  llm.py             OpenAI-compatible client for local vLLM (AH_BASE_URL overrides the endpoint)
  matching.py        rule matcher: preserved / altered / absent / promoted per obligation
  scenarios/         scenario schema + generator (task, source transcript, 8 typed obligations)
  workflow/          orchestrator-worker engine (roles.py prompts, engine.py loop, selection.py B0 catalog)
  chain/             B3-only control: compress the source K times in a row
  eval/              aggregation of raw runs into tables / probe events
  detectors/         LLM-judge baselines (optional comparison, unused by default)
data/scenarios/      20 scenarios (scheduling 6, research 6, coding 5, customer_support 3)
data/catalog.jsonl   agent/skill catalog for the task-unknown extension (B0 selection)
scripts/             CLI entry points (see below)
results/             raw runs (gitignored), summary.json, figures/
docs/                SETUP.md (system definition), proposal.md, STATUS.md, design notes, related work
configs/judge.yaml   model endpoint config
```

## Setup

```bash
conda create -n agentbench python=3.11 && conda activate agentbench
pip install -e ".[dev]"
# serve Qwen3-8B with vLLM (one GPU per replica; edit the GPU id / port inside the script)
bash scripts/start_vllm.sh &
python scripts/smoke_judge.py     # prints JUDGE SMOKE OK
```

## Pipeline

```bash
python scripts/make_scenarios.py --per_domain 5 --out data/scenarios/scenarios.jsonl   # generate scenarios
python scripts/validate_matcher.py                                                     # matcher sanity (drop / alter / promote edits)
python scripts/run_stress.py   --hops 8 --budgets 80,150,300 --formats free,json --guards 0,1 --tag grid
python scripts/run_workflow.py --rounds 8 --visibility shared,summary --formats free,json --budgets 200,400,800 --guards 0,1 --tag grid
python scripts/run_selection.py                                                        # B0 extension
python scripts/aggregate.py && python scripts/train_probe.py && python scripts/make_figures.py
```

Runners accept `--shard k/n` and honour `AH_BASE_URL=http://localhost:1800X/v1`, so a grid can be split across several vLLM replicas; shard outputs are merged by `aggregate.py`.

## What is measured

| Boundary | What crosses | Measured |
|---|---|---|
| B2 return | Researcher report | acquisition of source-only obligations, fabricated values, unfounded Verifier PASS |
| B3 compression | new state (free or JSON) | loss rate among items the team had, policy JSD before/after, guard repairs |
| B4 final | deliverable | constraints kept, prohibition violations, promotions, fabricated values, lost-after-acquired vs never-acquired |
| B0 selection (ext.) | team chosen from catalog | missing required capabilities |
