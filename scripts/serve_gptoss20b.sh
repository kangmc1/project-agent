#!/usr/bin/env bash
# Comparator judge server: openai/gpt-oss-20b on GPU 4, port 18004 (math_infer env after the vLLM upgrade; MXFP4 weights).
source "$(dirname "$0")/serve_common.sh"
CUDA_VISIBLE_DEVICES=4 exec $PY -m vllm.entrypoints.openai.api_server \
  --model openai/gpt-oss-20b --served-model-name gptoss20b --port 18004 \
  --max-model-len 32768 --enable-prefix-caching --max-num-seqs 32 --gpu-memory-utilization 0.90
