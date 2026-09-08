#!/usr/bin/env bash
# Shared settings for the three vLLM servers (GPUs 1-4 only; see docs/notes/timeline.md)
export PY=/home/kangmc1/miniforge3/envs/math_infer/bin/python
export Q32=/home/kangmc1/.cache/huggingface/hub/models--Qwen--Qwen3-32B/snapshots/9216db5781bf21249d130ec9da846c4624c16137
export Q8=/home/kangmc1/.cache/huggingface/hub/models--Qwen--Qwen3-8B/snapshots/b968826d9c46dd6066d109eabc6255188de91218
export VLLM_LOGGING_LEVEL=INFO
export PATH="$(dirname "$PY"):$PATH"
export VLLM_USE_FLASHINFER_SAMPLER=0
