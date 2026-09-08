#!/usr/bin/env bash
# Extractor / judge server: Qwen3-8B on GPU 3, port 18002
source "$(dirname "$0")/serve_common.sh"
CUDA_VISIBLE_DEVICES=3 exec $PY -m vllm.entrypoints.openai.api_server \
  --model "$Q8" --served-model-name qwen8b --port 18002 \
  --max-model-len 32768 --enable-auto-tool-choice --tool-call-parser hermes \
  --enable-prefix-caching --max-num-seqs 32 --gpu-memory-utilization 0.90 --dtype bfloat16
