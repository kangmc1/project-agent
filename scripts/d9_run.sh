#!/usr/bin/env bash
cd /home/kangmc1/project-agent
source /home/kangmc1/miniforge3/etc/profile.d/conda.sh && conda activate agentbench
PYTHONPATH=. exec python -m src.audit.d9 --runs runs --stats
