#!/usr/bin/env bash
# Serve a model with vLLM (OpenAI-compatible). Usage:
#   scripts/serve_vllm.sh <model_path_or_hf_id> <served_name> <port> <cuda_visible_devices> [tensor_parallel] [max_model_len]
# Example (backbone, 2 GPUs): scripts/serve_vllm.sh Qwen/Qwen3-Coder-30B-A3B-Instruct coder30b 18011 3,4 2 16384
set -euo pipefail
MODEL=$1; NAME=$2; PORT=$3; GPUS=$4; TP=${5:-1}; LEN=${6:-16384}
PY=${VLLM_PY:-/home/kangmc1/miniforge3/envs/math_infer/bin/python}
mkdir -p logs
CUDA_VISIBLE_DEVICES=$GPUS nohup $PY -m vllm.entrypoints.openai.api_server \
  --model "$MODEL" --served-model-name "$NAME" --port "$PORT" \
  --tensor-parallel-size "$TP" --max-model-len "$LEN" --gpu-memory-utilization 0.90 --dtype bfloat16 \
  --max-num-seqs 64 --enable-prefix-caching \
  > "logs/vllm_${NAME}_${PORT}.log" 2>&1 &
echo "started $NAME on port $PORT (GPUs $GPUS, TP=$TP) pid $!  log: logs/vllm_${NAME}_${PORT}.log"
