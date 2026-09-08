# agent-failure-bench

Failure-injection benchmark and step-level detector evaluation pipeline for LLM agent trajectories.

> Work in progress — take-home task (2026-09-08 ~ 09-09).

## Layout

```
src/agentbench/
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
