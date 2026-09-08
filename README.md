# agent-handoff

How stable is an agent system across handoffs? A benchmark and pipeline that measures how much of what an agent knows (constraints, verified facts, open questions, prohibitions) survives context compression and agent-to-agent handoffs, how fast errors get baked in and spread, and how handoff format and boundary checking change that.

> Work in progress — take-home task (2026-09-08 ~ 09-09).

## Layout

```
src/agent_handoff/
  env/         mock tools + task templates
  generation/  clean trajectory generator + failure injector
  detectors/   rule-based and LLM-judge detectors
  eval/        metrics and reporting
data/          generated tasks and trajectories
results/       detector outputs, metrics, figures
scripts/       CLI entry points
docs/          proposal document (Markdown source)
configs/       judge backend config
```

## Setup

```bash
conda create -n agentbench python=3.11 && conda activate agentbench
pip install -e ".[dev]"
```

LLM judge uses any OpenAI-compatible endpoint. Default: local vLLM serving Qwen3-8B on port 18001 (see `configs/judge.yaml`).

Start the local judge (GPU 1, port 18001) and verify:

```bash
bash scripts/start_vllm.sh &      # requires an env with vllm (here: conda env `math_infer`)
python scripts/smoke_judge.py     # prints JUDGE SMOKE OK
```
