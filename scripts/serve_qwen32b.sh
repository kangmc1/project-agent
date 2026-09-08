#!/usr/bin/env bash
# Executor server: Qwen3-32B, TP=2 on GPUs 1-2, port 18001 (hermes tool parser, prefix caching)
source "$(dirname "$0")/serve_common.sh"
CUDA_VISIBLE_DEVICES=1,2 exec $PY -m vllm.entrypoints.openai.api_server \
  --model "$Q32" --served-model-name qwen32b --port 18001 \
  --tensor-parallel-size 2 --max-model-len 40960 \
  --enable-auto-tool-choice --tool-call-parser hermes \
  --enable-prefix-caching --max-num-seqs 16 --max-num-batched-tokens 8192 \
  --gpu-memory-utilization 0.90 --dtype bfloat16
