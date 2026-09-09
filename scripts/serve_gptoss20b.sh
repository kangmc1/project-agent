#!/usr/bin/env bash
# Comparator judge server: openai/gpt-oss-20b on GPU 4, port 18004 (vLLM 0.21 in conda env idlm; MXFP4 weights).
source /home/kangmc1/miniforge3/etc/profile.d/conda.sh && conda activate idlm
CUDA_VISIBLE_DEVICES=4 exec python -m vllm.entrypoints.openai.api_server \
  --model openai/gpt-oss-20b --served-model-name gptoss20b --port 18004 \
  --max-model-len 32768 --enable-prefix-caching --max-num-seqs 32 --gpu-memory-utilization 0.90
