#!/usr/bin/env bash
# Resumable D1 full-scoring loop (planner-first, serial). Runs until 13:00 KST or logs/STOP_D1 exists.
cd /home/kangmc1/project-agent
source /home/kangmc1/miniforge3/etc/profile.d/conda.sh && conda activate agentbench
until [ -f audit/d1_check.json ]; do sleep 20; done
echo "check ready $(date): policy=$(python3 -c "import json;print(json.load(open('audit/d1_check.json'))['policy'])")"
while [ ! -f logs/STOP_D1 ]; do
  flock -n audit/d1.lock python -m src.audit.d1 --all --runs runs --cut 2026-09-09T13:00 2>&1 | grep -v PyTorch | tail -1
  echo "d1 pass done $(date) rows=$(wc -l < audit/d1.jsonl 2>/dev/null || echo 0)"
  if [ "$(date +%H%M)" -ge 1300 ]; then break; fi
  sleep 300
done
echo "d1 loop ended $(date)"
