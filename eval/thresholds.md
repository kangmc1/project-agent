# Percentile vs label-optimal thresholds

- generated: 2026-09-09 10:47:02 KST
- items: D1_1-conf, D2, D3_report->planner, D3_report->planner
- percentile pool: every scored step of 62 run(s) in `runs/index.csv`, labeled or not
- FPR / recall are always measured on labeled steps (cascade excluded); `d recall` / `d FPR` are the gaps to the label-optimal row of the same cell.

| item | role | domain | rule | threshold | n_pool | n_pos | n_neg | FPR | recall | d recall | d FPR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D1_1-conf | planner | airline | top 5% (p95) | 0.4307 | 431 | 46 | 148 | 0.027 | 0.043 | -0.870 | -0.622 |
| D1_1-conf | planner | airline | top 10% (p90) | 0.3512 | 431 | 46 | 148 | 0.074 | 0.174 | -0.739 | -0.574 |
| D1_1-conf | planner | airline | label-optimal (max J) | 0.007369 | 431 | 46 | 148 | 0.649 | 0.913 | - | - |
| D1_1-conf | planner | aime | top 5% (p95) | 0.3799 | 127 | 6 | 56 | 0.036 | 0.167 | -0.333 | -0.054 |
| D1_1-conf | planner | aime | top 10% (p90) | 0.3193 | 127 | 6 | 56 | 0.071 | 0.333 | -0.167 | -0.018 |
| D1_1-conf | planner | aime | label-optimal (max J) | 0.2561 | 127 | 6 | 56 | 0.089 | 0.500 | - | - |
| D1_1-conf | planner | all | top 5% (p95) | 0.4188 | 558 | 52 | 204 | 0.029 | 0.038 | -0.827 | -0.490 |
| D1_1-conf | planner | all | top 10% (p90) | 0.3402 | 558 | 52 | 204 | 0.064 | 0.192 | -0.673 | -0.456 |
| D1_1-conf | planner | all | label-optimal (max J) | 0.007369 | 558 | 52 | 204 | 0.520 | 0.865 | - | - |
| D1_1-conf | subagent | airline | top 5% (p95) | 0.3284 | 475 | 48 | 190 | 0.068 | 0.083 | -0.458 | -0.268 |
| D1_1-conf | subagent | airline | top 10% (p90) | 0.2409 | 475 | 48 | 190 | 0.105 | 0.146 | -0.396 | -0.232 |
| D1_1-conf | subagent | airline | label-optimal (max J) | 0.002659 | 475 | 48 | 190 | 0.337 | 0.542 | - | - |
| D1_1-conf | subagent | aime | top 5% (p95) | 0.2507 | 263 | 72 | 36 | 0.083 | 0.028 | -0.583 | -0.333 |
| D1_1-conf | subagent | aime | top 10% (p90) | 0.106 | 263 | 72 | 36 | 0.083 | 0.139 | -0.472 | -0.333 |
| D1_1-conf | subagent | aime | label-optimal (max J) | 0.000546 | 263 | 72 | 36 | 0.417 | 0.611 | - | - |
| D1_1-conf | subagent | all | top 5% (p95) | 0.3085 | 738 | 120 | 226 | 0.071 | 0.050 | -0.425 | -0.257 |
| D1_1-conf | subagent | all | top 10% (p90) | 0.2227 | 738 | 120 | 226 | 0.115 | 0.083 | -0.392 | -0.212 |
| D1_1-conf | subagent | all | label-optimal (max J) | 0.002562 | 738 | 120 | 226 | 0.327 | 0.475 | - | - |
| D1_1-conf | all | airline | top 5% (p95) | 0.3823 | 906 | 94 | 338 | 0.038 | 0.074 | -0.617 | -0.414 |
| D1_1-conf | all | airline | top 10% (p90) | 0.3001 | 906 | 94 | 338 | 0.107 | 0.160 | -0.532 | -0.346 |
| D1_1-conf | all | airline | label-optimal (max J) | 0.006476 | 906 | 94 | 338 | 0.453 | 0.691 | - | - |
| D1_1-conf | all | aime | top 5% (p95) | 0.3288 | 390 | 78 | 92 | 0.065 | 0.038 | -0.487 | -0.207 |
| D1_1-conf | all | aime | top 10% (p90) | 0.1881 | 390 | 78 | 92 | 0.109 | 0.090 | -0.436 | -0.163 |
| D1_1-conf | all | aime | label-optimal (max J) | 0.001389 | 390 | 78 | 92 | 0.272 | 0.526 | - | - |
| D1_1-conf | all | all | top 5% (p95) | 0.3707 | 1296 | 172 | 430 | 0.044 | 0.058 | -0.541 | -0.433 |
| D1_1-conf | all | all | top 10% (p90) | 0.2772 | 1296 | 172 | 430 | 0.119 | 0.110 | -0.488 | -0.358 |
| D1_1-conf | all | all | label-optimal (max J) | 0.002367 | 1296 | 172 | 430 | 0.477 | 0.599 | - | - |
| D2 | planner | airline | top 5% (p95) | 1 | 431 | 46 | 148 | 0.007 | 0.217 | +0.000 | +0.000 |
| D2 | planner | airline | top 10% (p90) | 0 | 431 | 46 | 148 | 1.000 | 1.000 | +0.783 | +0.993 |
| D2 | planner | airline | label-optimal (max J) | 1 | 431 | 46 | 148 | 0.007 | 0.217 | - | - |
| D2 | planner | aime | top 5% (p95) | 0 | 127 | 6 | 56 | 1.000 | 1.000 | +0.000 | +0.000 |
| D2 | planner | aime | top 10% (p90) | 0 | 127 | 6 | 56 | 1.000 | 1.000 | +0.000 | +0.000 |
| D2 | planner | aime | label-optimal (max J) | 0 | 127 | 6 | 56 | 1.000 | 1.000 | - | - |
| D2 | planner | all | top 5% (p95) | 1 | 558 | 52 | 204 | 0.005 | 0.192 | +0.000 | +0.000 |
| D2 | planner | all | top 10% (p90) | 0 | 558 | 52 | 204 | 1.000 | 1.000 | +0.808 | +0.995 |
| D2 | planner | all | label-optimal (max J) | 1 | 558 | 52 | 204 | 0.005 | 0.192 | - | - |
| D2 | subagent | airline | top 5% (p95) | 1 | 475 | 48 | 190 | 0.074 | 0.479 | +0.000 | +0.000 |
| D2 | subagent | airline | top 10% (p90) | 1 | 475 | 48 | 190 | 0.074 | 0.479 | +0.000 | +0.000 |
| D2 | subagent | airline | label-optimal (max J) | 1 | 475 | 48 | 190 | 0.074 | 0.479 | - | - |
| D2 | subagent | aime | top 5% (p95) | 1 | 263 | 72 | 36 | 0.083 | 0.417 | +0.000 | +0.000 |
| D2 | subagent | aime | top 10% (p90) | 1 | 263 | 72 | 36 | 0.083 | 0.417 | +0.000 | +0.000 |
| D2 | subagent | aime | label-optimal (max J) | 1 | 263 | 72 | 36 | 0.083 | 0.417 | - | - |
| D2 | subagent | all | top 5% (p95) | 1 | 738 | 120 | 226 | 0.075 | 0.442 | +0.000 | +0.000 |
| D2 | subagent | all | top 10% (p90) | 1 | 738 | 120 | 226 | 0.075 | 0.442 | +0.000 | +0.000 |
| D2 | subagent | all | label-optimal (max J) | 1 | 738 | 120 | 226 | 0.075 | 0.442 | - | - |
| D2 | all | airline | top 5% (p95) | 1 | 906 | 94 | 338 | 0.044 | 0.351 | +0.000 | +0.000 |
| D2 | all | airline | top 10% (p90) | 1 | 906 | 94 | 338 | 0.044 | 0.351 | +0.000 | +0.000 |
| D2 | all | airline | label-optimal (max J) | 1 | 906 | 94 | 338 | 0.044 | 0.351 | - | - |
| D2 | all | aime | top 5% (p95) | 1 | 390 | 78 | 92 | 0.033 | 0.385 | +0.000 | +0.000 |
| D2 | all | aime | top 10% (p90) | 1 | 390 | 78 | 92 | 0.033 | 0.385 | +0.000 | +0.000 |
| D2 | all | aime | label-optimal (max J) | 1 | 390 | 78 | 92 | 0.033 | 0.385 | - | - |
| D2 | all | all | top 5% (p95) | 1 | 1296 | 172 | 430 | 0.042 | 0.366 | +0.000 | +0.000 |
| D2 | all | all | top 10% (p90) | 1 | 1296 | 172 | 430 | 0.042 | 0.366 | +0.000 | +0.000 |
| D2 | all | all | label-optimal (max J) | 1 | 1296 | 172 | 430 | 0.042 | 0.366 | - | - |
| D3_report->planner | planner | airline | top 5% (p95) | 1 | 177 | 30 | 66 | 0.167 | 0.233 | -0.300 | -0.182 |
| D3_report->planner | planner | airline | top 10% (p90) | 1 | 177 | 30 | 66 | 0.167 | 0.233 | -0.300 | -0.182 |
| D3_report->planner | planner | airline | label-optimal (max J) | 0.75 | 177 | 30 | 66 | 0.348 | 0.533 | - | - |
| D3_report->planner | planner | aime | top 5% (p95) | 1 | 69 | 3 | 40 | 0.300 | 0.333 | -0.667 | -0.150 |
| D3_report->planner | planner | aime | top 10% (p90) | 1 | 69 | 3 | 40 | 0.300 | 0.333 | -0.667 | -0.150 |
| D3_report->planner | planner | aime | label-optimal (max J) | 0.7143 | 69 | 3 | 40 | 0.450 | 1.000 | - | - |
| D3_report->planner | planner | all | top 5% (p95) | 1 | 246 | 33 | 106 | 0.217 | 0.242 | -0.303 | -0.151 |
| D3_report->planner | planner | all | top 10% (p90) | 1 | 246 | 33 | 106 | 0.217 | 0.242 | -0.303 | -0.151 |
| D3_report->planner | planner | all | label-optimal (max J) | 0.75 | 246 | 33 | 106 | 0.368 | 0.545 | - | - |
| D3_report->planner | planner | airline | top 5% (p95) | 1 | 177 | 30 | 66 | 0.167 | 0.233 | -0.300 | -0.182 |
| D3_report->planner | planner | airline | top 10% (p90) | 1 | 177 | 30 | 66 | 0.167 | 0.233 | -0.300 | -0.182 |
| D3_report->planner | planner | airline | label-optimal (max J) | 0.75 | 177 | 30 | 66 | 0.348 | 0.533 | - | - |
| D3_report->planner | planner | aime | top 5% (p95) | 1 | 69 | 3 | 40 | 0.300 | 0.333 | -0.667 | -0.150 |
| D3_report->planner | planner | aime | top 10% (p90) | 1 | 69 | 3 | 40 | 0.300 | 0.333 | -0.667 | -0.150 |
| D3_report->planner | planner | aime | label-optimal (max J) | 0.7143 | 69 | 3 | 40 | 0.450 | 1.000 | - | - |
| D3_report->planner | planner | all | top 5% (p95) | 1 | 246 | 33 | 106 | 0.217 | 0.242 | -0.303 | -0.151 |
| D3_report->planner | planner | all | top 10% (p90) | 1 | 246 | 33 | 106 | 0.217 | 0.242 | -0.303 | -0.151 |
| D3_report->planner | planner | all | label-optimal (max J) | 0.75 | 246 | 33 | 106 | 0.368 | 0.545 | - | - |

cells: 24

