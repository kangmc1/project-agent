# Percentile vs label-optimal thresholds

- generated: 2026-09-09 05:59:36 KST
- items: D1_1-conf, D2_unsupported, D7_report->planner, D9_1-consistency
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
| D2_unsupported | planner | airline | top 5% (p95) | 0.2 | 17 | 1 | 3 | 0.000 | 1.000 | +0.000 | +0.000 |
| D2_unsupported | planner | airline | top 10% (p90) | 0 | 17 | 1 | 3 | 1.000 | 1.000 | +0.000 | +1.000 |
| D2_unsupported | planner | airline | label-optimal (max J) | 1 | 17 | 1 | 3 | 0.000 | 1.000 | - | - |
| D2_unsupported | planner | aime | top 5% (p95) | 0.5 | 32 | 2 | 8 | 0.500 | 0.500 | +0.000 | +0.000 |
| D2_unsupported | planner | aime | top 10% (p90) | 0.5 | 32 | 2 | 8 | 0.500 | 0.500 | +0.000 | +0.000 |
| D2_unsupported | planner | aime | label-optimal (max J) | 0.5 | 32 | 2 | 8 | 0.500 | 0.500 | - | - |
| D2_unsupported | planner | all | top 5% (p95) | 0.5 | 49 | 3 | 11 | 0.364 | 0.667 | +0.333 | +0.364 |
| D2_unsupported | planner | all | top 10% (p90) | 0.5 | 49 | 3 | 11 | 0.364 | 0.667 | +0.333 | +0.364 |
| D2_unsupported | planner | all | label-optimal (max J) | 1 | 49 | 3 | 11 | 0.000 | 0.333 | - | - |
| D2_unsupported | subagent | airline | top 5% (p95) | 0.5 | 412 | 44 | 170 | 0.112 | 0.068 | +0.000 | +0.065 |
| D2_unsupported | subagent | airline | top 10% (p90) | 0.3975 | 412 | 44 | 170 | 0.112 | 0.091 | +0.023 | +0.065 |
| D2_unsupported | subagent | airline | label-optimal (max J) | 0.5294 | 412 | 44 | 170 | 0.047 | 0.068 | - | - |
| D2_unsupported | subagent | aime | top 5% (p95) | 0.942 | 196 | 44 | 32 | 0.062 | 0.045 | -0.955 | -0.938 |
| D2_unsupported | subagent | aime | top 10% (p90) | 0.8 | 196 | 44 | 32 | 0.250 | 0.136 | -0.864 | -0.750 |
| D2_unsupported | subagent | aime | label-optimal (max J) | 0 | 196 | 44 | 32 | 1.000 | 1.000 | - | - |
| D2_unsupported | subagent | all | top 5% (p95) | 0.75 | 608 | 88 | 202 | 0.069 | 0.102 | -0.295 | -0.183 |
| D2_unsupported | subagent | all | top 10% (p90) | 0.58 | 608 | 88 | 202 | 0.109 | 0.182 | -0.216 | -0.144 |
| D2_unsupported | subagent | all | label-optimal (max J) | 0.2 | 608 | 88 | 202 | 0.252 | 0.398 | - | - |
| D2_unsupported | all | airline | top 5% (p95) | 0.5 | 429 | 45 | 173 | 0.110 | 0.089 | +0.000 | +0.064 |
| D2_unsupported | all | airline | top 10% (p90) | 0.38 | 429 | 45 | 173 | 0.110 | 0.111 | +0.022 | +0.064 |
| D2_unsupported | all | airline | label-optimal (max J) | 0.5294 | 429 | 45 | 173 | 0.046 | 0.089 | - | - |
| D2_unsupported | all | aime | top 5% (p95) | 0.9325 | 228 | 46 | 40 | 0.100 | 0.043 | -0.587 | -0.525 |
| D2_unsupported | all | aime | top 10% (p90) | 0.7813 | 228 | 46 | 40 | 0.225 | 0.130 | -0.500 | -0.400 |
| D2_unsupported | all | aime | label-optimal (max J) | 0.2 | 228 | 46 | 40 | 0.625 | 0.630 | - | - |
| D2_unsupported | all | all | top 5% (p95) | 0.75 | 657 | 91 | 213 | 0.066 | 0.110 | -0.297 | -0.192 |
| D2_unsupported | all | all | top 10% (p90) | 0.5556 | 657 | 91 | 213 | 0.113 | 0.187 | -0.220 | -0.146 |
| D2_unsupported | all | all | label-optimal (max J) | 0.2 | 657 | 91 | 213 | 0.258 | 0.407 | - | - |
| D7_report->planner | planner | airline | top 5% (p95) | 1 | 178 | 31 | 66 | 0.121 | 0.161 | -0.484 | -0.318 |
| D7_report->planner | planner | airline | top 10% (p90) | 1 | 178 | 31 | 66 | 0.121 | 0.161 | -0.484 | -0.318 |
| D7_report->planner | planner | airline | label-optimal (max J) | 0.6667 | 178 | 31 | 66 | 0.439 | 0.645 | - | - |
| D7_report->planner | planner | aime | top 5% (p95) | 1 | 70 | 3 | 41 | 0.293 | 0.333 | -0.667 | -0.122 |
| D7_report->planner | planner | aime | top 10% (p90) | 1 | 70 | 3 | 41 | 0.293 | 0.333 | -0.667 | -0.122 |
| D7_report->planner | planner | aime | label-optimal (max J) | 0.7778 | 70 | 3 | 41 | 0.415 | 1.000 | - | - |
| D7_report->planner | planner | all | top 5% (p95) | 1 | 248 | 34 | 107 | 0.187 | 0.176 | -0.412 | -0.206 |
| D7_report->planner | planner | all | top 10% (p90) | 1 | 248 | 34 | 107 | 0.187 | 0.176 | -0.412 | -0.206 |
| D7_report->planner | planner | all | label-optimal (max J) | 0.75 | 248 | 34 | 107 | 0.393 | 0.588 | - | - |
| D9_1-consistency | planner | aime | top 5% (p95) | 0 | 24 | 1 | 5 | 1.000 | 1.000 | +0.000 | +0.000 |
| D9_1-consistency | planner | aime | top 10% (p90) | 0 | 24 | 1 | 5 | 1.000 | 1.000 | +0.000 | +0.000 |
| D9_1-consistency | planner | aime | label-optimal (max J) | 0 | 24 | 1 | 5 | 1.000 | 1.000 | - | - |
| D9_1-consistency | subagent | aime | top 5% (p95) | 1 | 57 | 18 | 9 | 0.222 | 0.111 | -0.444 | -0.111 |
| D9_1-consistency | subagent | aime | top 10% (p90) | 1 | 57 | 18 | 9 | 0.222 | 0.111 | -0.444 | -0.111 |
| D9_1-consistency | subagent | aime | label-optimal (max J) | 0.2222 | 57 | 18 | 9 | 0.333 | 0.556 | - | - |
| D9_1-consistency | all | aime | top 5% (p95) | 1 | 81 | 19 | 14 | 0.143 | 0.105 | -0.421 | -0.071 |
| D9_1-consistency | all | aime | top 10% (p90) | 0.9333 | 81 | 19 | 14 | 0.143 | 0.105 | -0.421 | -0.071 |
| D9_1-consistency | all | aime | label-optimal (max J) | 0.2222 | 81 | 19 | 14 | 0.214 | 0.526 | - | - |

cells: 24

