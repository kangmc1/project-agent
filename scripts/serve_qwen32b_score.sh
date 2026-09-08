#!/usr/bin/env bash
# D1 scoring server: Qwen3-32B TP=1 on GPU 4, port 18003 (same weights as executor)
source "$(dirname "$0")/serve_common.sh"
CUDA_VISIBLE_DEVICES=4 exec $PY -m vllm.entrypoints.openai.api_server \
  --model "$Q32" --served-model-name qwen32b-score --port 18003 \
  --tensor-parallel-size 1 --max-model-len 24576 --max-num-seqs 1 \
  --max-num-batched-tokens 2048 --gpu-memory-utilization 0.90 \
  --enable-prefix-caching --dtype bfloat16
