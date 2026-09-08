#!/usr/bin/env bash
# Kill our previous coder30b vLLM replicas (parents + EngineCore children), then wait until GPUs 1-4 are free.
set -u
for pid in $(pgrep -u "$USER" -f 'served-model-name coder30b'); do pkill -P "$pid" 2>/dev/null; kill "$pid" 2>/dev/null; done
sleep 3
pkill -u "$USER" -f 'served-model-name coder30b' 2>/dev/null || true
for i in $(seq 1 30); do
  used=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits -i 1,2,3,4 | awk '{s+=$1} END{print s}')
  if [ "$used" -lt 4000 ]; then echo "GPUs 1-4 free (used=${used}MiB)"; exit 0; fi
  sleep 2
done
echo "timeout: force killing remaining vllm procs of $USER on GPUs 1-4"
for pid in $(nvidia-smi --query-compute-apps=pid --format=csv,noheader -i 1,2,3,4); do
  if ps -o user= -p "$pid" 2>/dev/null | grep -q "^$USER$"; then kill -9 "$pid" 2>/dev/null; fi
done
sleep 5; nvidia-smi --query-gpu=index,memory.used --format=csv -i 1,2,3,4
