#!/bin/bash
# Relaunch helper: Qwen3-8B judge on GPU 1, port 18001
export PATH=$HOME/miniforge3/envs/math_infer/bin:$PATH
CUDA_VISIBLE_DEVICES=1 exec python -m vllm.entrypoints.openai.api_server --model Qwen/Qwen3-8B --served-model-name qwen3-8b --port 18001 --max-model-len 16384 --gpu-memory-utilization 0.85 --dtype bfloat16
