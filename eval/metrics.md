# Detection metrics

- generated: 2026-09-09 07:26:51 KST
- d1_scored_n: 1296 rows in `audit/d1.jsonl`
- labeled runs: aime=30, airline=30 (total 60); runs in index: 62
- D1 method(s) present: stepwise
- items scored: D1_1-conf, D1_1-p_actual, D1_1-margin, D1_handoff, D2, D3_instruction->premise, D3_report->planner
- bootstrap: 1000 stratified resamples, seed 0; AUROC is `n/a` when n_pos < 3 or n_neg < 3.

## 1. Step-level AUROC

Labeled runs only; cascade steps excluded; negatives = clean steps. `n_scored/n_labeled` counts labeled non-aux steps in the role scope the item applies to.

| item | role | domain | n_scored/n_labeled | n_pos(all) | n_neg | AUROC all errors [95% CI] | n_pos(dec) | AUROC decisive [95% CI] |
|---|---|---|---|---|---|---|---|---|
| D1_1-conf | planner | airline | 391/391 | 46 | 148 | 0.616 [0.530, 0.702] | 16 | 0.705 [0.577, 0.823] |
| D1_1-conf | planner | aime | 123/123 | 6 | 56 | 0.610 [0.318, 0.881] | 2 | n/a |
| D1_1-conf | planner | all | 514/514 | 52 | 204 | 0.667 [0.590, 0.741] | 18 | 0.726 [0.603, 0.835] |
| D1_1-conf | subagent | airline | 435/435 | 48 | 190 | 0.539 [0.439, 0.629] | 8 | 0.361 [0.211, 0.518] |
| D1_1-conf | subagent | aime | 259/259 | 72 | 36 | 0.534 [0.415, 0.651] | 21 | 0.407 [0.250, 0.577] |
| D1_1-conf | subagent | all | 694/694 | 120 | 226 | 0.540 [0.477, 0.603] | 29 | 0.433 [0.330, 0.545] |
| D1_1-conf | all | airline | 826/826 | 94 | 338 | 0.583 [0.516, 0.645] | 24 | 0.609 [0.474, 0.732] |
| D1_1-conf | all | aime | 382/382 | 78 | 92 | 0.544 [0.456, 0.639] | 23 | 0.424 [0.278, 0.577] |
| D1_1-conf | all | all | 1208/1208 | 172 | 430 | 0.538 [0.489, 0.586] | 47 | 0.513 [0.413, 0.612] |
| D1_1-p_actual | planner | airline | 391/391 | 46 | 148 | 0.627 [0.543, 0.713] | 16 | 0.746 [0.611, 0.862] |
| D1_1-p_actual | planner | aime | 123/123 | 6 | 56 | 0.729 [0.464, 0.964] | 2 | n/a |
| D1_1-p_actual | planner | all | 514/514 | 52 | 204 | 0.691 [0.618, 0.764] | 18 | 0.806 [0.708, 0.888] |
| D1_1-p_actual | subagent | airline | 435/435 | 48 | 190 | 0.544 [0.442, 0.634] | 8 | 0.357 [0.208, 0.512] |
| D1_1-p_actual | subagent | aime | 259/259 | 72 | 36 | 0.533 [0.414, 0.648] | 21 | 0.407 [0.250, 0.577] |
| D1_1-p_actual | subagent | all | 694/694 | 120 | 226 | 0.524 [0.459, 0.586] | 29 | 0.414 [0.314, 0.523] |
| D1_1-p_actual | all | airline | 826/826 | 94 | 338 | 0.590 [0.519, 0.653] | 24 | 0.619 [0.486, 0.743] |
| D1_1-p_actual | all | aime | 382/382 | 78 | 92 | 0.543 [0.456, 0.634] | 23 | 0.448 [0.292, 0.596] |
| D1_1-p_actual | all | all | 1208/1208 | 172 | 430 | 0.536 [0.488, 0.587] | 47 | 0.525 [0.426, 0.621] |
| D1_1-margin | planner | airline | 391/391 | 46 | 148 | 0.613 [0.526, 0.703] | 16 | 0.710 [0.581, 0.831] |
| D1_1-margin | planner | aime | 123/123 | 6 | 56 | 0.595 [0.312, 0.872] | 2 | n/a |
| D1_1-margin | planner | all | 514/514 | 52 | 204 | 0.664 [0.586, 0.739] | 18 | 0.734 [0.610, 0.844] |
| D1_1-margin | subagent | airline | 435/435 | 48 | 190 | 0.541 [0.441, 0.630] | 8 | 0.355 [0.208, 0.509] |
| D1_1-margin | subagent | aime | 259/259 | 72 | 36 | 0.535 [0.415, 0.654] | 21 | 0.414 [0.257, 0.579] |
| D1_1-margin | subagent | all | 694/694 | 120 | 226 | 0.523 [0.458, 0.585] | 29 | 0.414 [0.315, 0.524] |
| D1_1-margin | all | airline | 826/826 | 94 | 338 | 0.584 [0.514, 0.647] | 24 | 0.604 [0.472, 0.729] |
| D1_1-margin | all | aime | 382/382 | 78 | 92 | 0.536 [0.446, 0.627] | 23 | 0.423 [0.282, 0.573] |
| D1_1-margin | all | all | 1208/1208 | 172 | 430 | 0.530 [0.481, 0.579] | 47 | 0.505 [0.405, 0.604] |
| D1_handoff | planner | airline | 391/391 | 46 | 148 | 0.579 [0.493, 0.667] | 16 | 0.552 [0.430, 0.685] |
| D1_handoff | planner | aime | 123/123 | 6 | 56 | 0.518 [0.241, 0.795] | 2 | n/a |
| D1_handoff | planner | all | 514/514 | 52 | 204 | 0.610 [0.524, 0.685] | 18 | 0.559 [0.411, 0.684] |
| D2 | planner | airline | 391/391 | 46 | 148 | 0.522 [0.500, 0.554] | 16 | 0.500 [0.500, 0.500] |
| D2 | planner | aime | 123/123 | 6 | 56 | 0.500 [0.500, 0.500] | 2 | n/a |
| D2 | planner | all | 514/514 | 52 | 204 | 0.519 [0.500, 0.548] | 18 | 0.500 [0.500, 0.500] |
| D2 | subagent | airline | 435/435 | 48 | 190 | 0.703 [0.625, 0.778] | 8 | 0.588 [0.458, 0.768] |
| D2 | subagent | aime | 259/259 | 72 | 36 | 0.667 [0.597, 0.736] | 21 | 0.577 [0.478, 0.673] |
| D2 | subagent | all | 694/694 | 120 | 226 | 0.683 [0.633, 0.730] | 29 | 0.583 [0.512, 0.663] |
| D2 | all | airline | 826/826 | 94 | 338 | 0.612 [0.569, 0.662] | 24 | 0.521 [0.475, 0.586] |
| D2 | all | aime | 382/382 | 78 | 92 | 0.676 [0.619, 0.732] | 23 | 0.592 [0.511, 0.685] |
| D2 | all | all | 1208/1208 | 172 | 430 | 0.640 [0.605, 0.673] | 47 | 0.555 [0.505, 0.607] |
| D3_instruction->premise | planner | airline | 105/391 | 21 | 44 | 0.401 [0.254, 0.554] | 7 | 0.349 [0.125, 0.609] |
| D3_instruction->premise | planner | aime | 66/123 | 3 | 39 | 0.513 [0.128, 0.821] | 0 | n/a |
| D3_instruction->premise | planner | all | 171/514 | 24 | 83 | 0.388 [0.260, 0.517] | 7 | 0.335 [0.114, 0.608] |
| D3_report->planner | planner | airline | 161/391 | 31 | 66 | 0.590 [0.470, 0.716] | 11 | 0.598 [0.399, 0.775] |
| D3_report->planner | planner | aime | 68/123 | 3 | 41 | 0.715 [0.537, 0.866] | 0 | n/a |
| D3_report->planner | planner | all | 229/514 | 34 | 107 | 0.579 [0.476, 0.687] | 11 | 0.566 [0.392, 0.737] |

## 1b. Flag-level metrics for binary items (precision / recall / F1)

Same population as §1 (labeled runs, cascade excluded). A step is flagged when its score is 1. F1 = 2PR/(P+R); FPR = flagged clean / clean. `decisive recall` = flagged decisive steps / decisive steps.

| item | role | domain | n_pos | n_neg | TP | FP | precision | recall | F1 | FPR | decisive recall |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D2 | planner | airline | 46 | 148 | 2 | 0 | 1.000 | 0.043 | 0.083 | 0.000 | 0/16 |
| D2 | planner | aime | 6 | 56 | 0 | 0 | n/a | 0.000 | n/a | 0.000 | 0/2 |
| D2 | planner | all | 52 | 204 | 2 | 0 | 1.000 | 0.038 | 0.074 | 0.000 | 0/18 |
| D2 | subagent | airline | 48 | 190 | 23 | 14 | 0.622 | 0.479 | 0.541 | 0.074 | 2/8 |
| D2 | subagent | aime | 72 | 36 | 30 | 3 | 0.909 | 0.417 | 0.571 | 0.083 | 5/21 |
| D2 | subagent | all | 120 | 226 | 53 | 17 | 0.757 | 0.442 | 0.558 | 0.075 | 7/29 |
| D2 | all | airline | 94 | 338 | 25 | 14 | 0.641 | 0.266 | 0.376 | 0.041 | 2/24 |
| D2 | all | aime | 78 | 92 | 30 | 3 | 0.909 | 0.385 | 0.541 | 0.033 | 5/23 |
| D2 | all | all | 172 | 430 | 55 | 17 | 0.764 | 0.320 | 0.451 | 0.040 | 7/47 |

## 2. Trace-level AUROC (positives = runs with success=false)

All runs in `runs/index.csv` (labels not required); a run enters only if the item scored >= 80% of that run's non-aux steps in the role scope.

| item | role | domain | n_runs | n_fail | n_succ | AUROC max [95% CI] | AUROC mean [95% CI] |
|---|---|---|---|---|---|---|---|
| D1_1-conf | planner | airline | 31 | 25 | 6 | 0.780 [0.593, 0.927] | 0.720 [0.553, 0.880] |
| D1_1-conf | planner | aime | 31 | 23 | 8 | 0.315 [0.114, 0.533] | 0.370 [0.152, 0.576] |
| D1_1-conf | planner | all | 62 | 48 | 14 | 0.522 [0.362, 0.679] | 0.534 [0.385, 0.677] |
| D1_1-conf | subagent | airline | 31 | 25 | 6 | 0.513 [0.233, 0.813] | 0.560 [0.253, 0.867] |
| D1_1-conf | subagent | aime | 30 | 22 | 8 | 0.648 [0.443, 0.841] | 0.670 [0.477, 0.858] |
| D1_1-conf | subagent | all | 61 | 47 | 14 | 0.617 [0.444, 0.786] | 0.652 [0.488, 0.809] |
| D1_1-conf | all | airline | 31 | 25 | 6 | 0.547 [0.260, 0.853] | 0.660 [0.400, 0.887] |
| D1_1-conf | all | aime | 31 | 23 | 8 | 0.397 [0.174, 0.636] | 0.462 [0.250, 0.674] |
| D1_1-conf | all | all | 62 | 48 | 14 | 0.494 [0.318, 0.659] | 0.588 [0.437, 0.735] |
| D1_1-p_actual | planner | airline | 31 | 25 | 6 | 0.813 [0.627, 0.960] | 0.753 [0.580, 0.907] |
| D1_1-p_actual | planner | aime | 31 | 23 | 8 | 0.337 [0.141, 0.543] | 0.386 [0.179, 0.614] |
| D1_1-p_actual | planner | all | 62 | 48 | 14 | 0.564 [0.403, 0.710] | 0.554 [0.402, 0.701] |
| D1_1-p_actual | subagent | airline | 31 | 25 | 6 | 0.553 [0.273, 0.820] | 0.600 [0.360, 0.833] |
| D1_1-p_actual | subagent | aime | 30 | 22 | 8 | 0.648 [0.443, 0.841] | 0.665 [0.471, 0.852] |
| D1_1-p_actual | subagent | all | 61 | 47 | 14 | 0.626 [0.462, 0.786] | 0.649 [0.492, 0.803] |
| D1_1-p_actual | all | airline | 31 | 25 | 6 | 0.600 [0.353, 0.847] | 0.760 [0.573, 0.913] |
| D1_1-p_actual | all | aime | 31 | 23 | 8 | 0.440 [0.212, 0.668] | 0.440 [0.217, 0.663] |
| D1_1-p_actual | all | all | 62 | 48 | 14 | 0.546 [0.390, 0.711] | 0.612 [0.473, 0.753] |
| D1_1-margin | planner | airline | 31 | 25 | 6 | 0.767 [0.520, 0.947] | 0.727 [0.533, 0.880] |
| D1_1-margin | planner | aime | 31 | 23 | 8 | 0.332 [0.130, 0.527] | 0.364 [0.147, 0.582] |
| D1_1-margin | planner | all | 62 | 48 | 14 | 0.565 [0.412, 0.701] | 0.534 [0.387, 0.673] |
| D1_1-margin | subagent | airline | 31 | 25 | 6 | 0.633 [0.373, 0.873] | 0.607 [0.367, 0.847] |
| D1_1-margin | subagent | aime | 30 | 22 | 8 | 0.648 [0.443, 0.841] | 0.665 [0.471, 0.852] |
| D1_1-margin | subagent | all | 61 | 47 | 14 | 0.644 [0.489, 0.796] | 0.657 [0.495, 0.807] |
| D1_1-margin | all | airline | 31 | 25 | 6 | 0.633 [0.407, 0.867] | 0.740 [0.533, 0.913] |
| D1_1-margin | all | aime | 31 | 23 | 8 | 0.451 [0.228, 0.652] | 0.397 [0.174, 0.614] |
| D1_1-margin | all | all | 62 | 48 | 14 | 0.580 [0.427, 0.725] | 0.588 [0.443, 0.729] |
| D1_handoff | planner | airline | 31 | 25 | 6 | 0.673 [0.507, 0.840] | 0.467 [0.240, 0.693] |
| D1_handoff | planner | aime | 31 | 23 | 8 | 0.630 [0.380, 0.842] | 0.679 [0.424, 0.891] |
| D1_handoff | planner | all | 62 | 48 | 14 | 0.635 [0.463, 0.783] | 0.582 [0.402, 0.746] |
| D2 | planner | airline | 31 | 25 | 6 | 0.373 [0.187, 0.540] | 0.373 [0.173, 0.540] |
| D2 | planner | aime | 31 | 23 | 8 | 0.522 [0.500, 0.565] | 0.522 [0.500, 0.565] |
| D2 | planner | all | 62 | 48 | 14 | 0.460 [0.353, 0.542] | 0.461 [0.356, 0.542] |
| D2 | subagent | airline | 31 | 25 | 6 | 0.610 [0.400, 0.817] | 0.607 [0.347, 0.840] |
| D2 | subagent | aime | 30 | 22 | 8 | 0.500 [0.307, 0.699] | 0.432 [0.207, 0.676] |
| D2 | subagent | all | 61 | 47 | 14 | 0.559 [0.413, 0.704] | 0.518 [0.349, 0.690] |
| D2 | all | airline | 31 | 25 | 6 | 0.527 [0.340, 0.733] | 0.633 [0.420, 0.813] |
| D2 | all | aime | 31 | 23 | 8 | 0.489 [0.299, 0.698] | 0.429 [0.201, 0.669] |
| D2 | all | all | 62 | 48 | 14 | 0.516 [0.374, 0.682] | 0.518 [0.351, 0.699] |

## 3. Decisive-step attribution (failed labeled runs)

Predicted decisive step = argmax score over the run's scored steps in the role scope; ties broken planner-first then earliest step.  `+/-1` is one position in the run's non-aux step order.

| item | role | domain | n_runs | exact acc | +/-1 acc | agent acc |
|---|---|---|---|---|---|---|
| D1_1-conf | planner | airline | 24 | 0.042 | 0.167 | 0.667 |
| D1_1-conf | planner | aime | 23 | 0.087 | 0.217 | 0.087 |
| D1_1-conf | planner | all | 47 | 0.064 | 0.191 | 0.383 |
| D1_1-conf | subagent | airline | 24 | 0.000 | 0.208 | 0.125 |
| D1_1-conf | subagent | aime | 22 | 0.182 | 0.545 | 0.636 |
| D1_1-conf | subagent | all | 46 | 0.087 | 0.370 | 0.370 |
| D1_1-conf | all | airline | 24 | 0.000 | 0.125 | 0.500 |
| D1_1-conf | all | aime | 23 | 0.087 | 0.261 | 0.261 |
| D1_1-conf | all | all | 47 | 0.043 | 0.191 | 0.383 |
| D1_1-p_actual | planner | airline | 24 | 0.167 | 0.250 | 0.667 |
| D1_1-p_actual | planner | aime | 23 | 0.087 | 0.217 | 0.087 |
| D1_1-p_actual | planner | all | 47 | 0.128 | 0.234 | 0.383 |
| D1_1-p_actual | subagent | airline | 24 | 0.000 | 0.292 | 0.208 |
| D1_1-p_actual | subagent | aime | 22 | 0.182 | 0.500 | 0.636 |
| D1_1-p_actual | subagent | all | 46 | 0.087 | 0.391 | 0.413 |
| D1_1-p_actual | all | airline | 24 | 0.083 | 0.208 | 0.458 |
| D1_1-p_actual | all | aime | 23 | 0.087 | 0.217 | 0.261 |
| D1_1-p_actual | all | all | 47 | 0.085 | 0.213 | 0.362 |
| D1_1-margin | planner | airline | 24 | 0.125 | 0.208 | 0.667 |
| D1_1-margin | planner | aime | 23 | 0.087 | 0.217 | 0.087 |
| D1_1-margin | planner | all | 47 | 0.106 | 0.213 | 0.383 |
| D1_1-margin | subagent | airline | 24 | 0.000 | 0.208 | 0.208 |
| D1_1-margin | subagent | aime | 22 | 0.182 | 0.545 | 0.636 |
| D1_1-margin | subagent | all | 46 | 0.087 | 0.370 | 0.413 |
| D1_1-margin | all | airline | 24 | 0.083 | 0.125 | 0.375 |
| D1_1-margin | all | aime | 23 | 0.130 | 0.304 | 0.304 |
| D1_1-margin | all | all | 47 | 0.106 | 0.213 | 0.340 |
| D1_handoff | planner | airline | 24 | 0.208 | 0.292 | 0.667 |
| D1_handoff | planner | aime | 23 | 0.043 | 0.304 | 0.087 |
| D1_handoff | planner | all | 47 | 0.128 | 0.298 | 0.383 |
| D2 | planner | airline | 24 | 0.125 | 0.292 | 0.667 |
| D2 | planner | aime | 23 | 0.043 | 0.522 | 0.087 |
| D2 | planner | all | 47 | 0.085 | 0.404 | 0.383 |
| D2 | subagent | airline | 24 | 0.042 | 0.292 | 0.250 |
| D2 | subagent | aime | 22 | 0.500 | 0.545 | 0.864 |
| D2 | subagent | all | 46 | 0.261 | 0.413 | 0.543 |
| D2 | all | airline | 24 | 0.083 | 0.208 | 0.458 |
| D2 | all | aime | 23 | 0.217 | 0.478 | 0.435 |
| D2 | all | all | 47 | 0.149 | 0.340 | 0.447 |
| D3_instruction->premise | planner | airline | 21 | 0.286 | 0.333 | 0.619 |
| D3_instruction->premise | planner | aime | 21 | 0.000 | 0.381 | 0.048 |
| D3_instruction->premise | planner | all | 42 | 0.143 | 0.357 | 0.333 |
| D3_report->planner | planner | airline | 23 | 0.174 | 0.217 | 0.652 |
| D3_report->planner | planner | aime | 22 | 0.000 | 0.455 | 0.045 |
| D3_report->planner | planner | all | 45 | 0.089 | 0.333 | 0.356 |

## 4. recall@FPR10 and detection latency

Threshold = the smallest score whose FPR on labeled **clean** steps of that role/domain is <= 10% (the achieved FPR is reported: binary or heavily tied items cannot hit 10% exactly).  Latency = positions after the decisive step until the first score >= threshold (non-aux order); runs that never cross are censored.

| item | role | domain | threshold | FPR(clean) | recall(all errors) | n_pos | n_crossed/n_failed | median latency |
|---|---|---|---|---|---|---|---|---|
| D1_1-conf | planner | airline | 0.333 | 0.095 | 0.174 | 46 | 16/24 | 5.5 |
| D1_1-conf | planner | aime | 0.2561 | 0.089 | 0.500 | 6 | 9/23 | 4.0 |
| D1_1-conf | planner | all | 0.3271 | 0.098 | 0.212 | 52 | 23/47 | 4.0 |
| D1_1-conf | subagent | airline | 0.2636 | 0.100 | 0.146 | 48 | 10/24 | 3.5 |
| D1_1-conf | subagent | aime | 0.09083 | 0.083 | 0.167 | 72 | 11/22 | 1.0 |
| D1_1-conf | subagent | all | 0.2455 | 0.097 | 0.083 | 120 | 19/46 | 3.0 |
| D1_1-conf | all | airline | 0.3102 | 0.098 | 0.149 | 94 | 17/24 | 1.0 |
| D1_1-conf | all | aime | 0.229 | 0.098 | 0.077 | 78 | 13/23 | 3.0 |
| D1_1-conf | all | all | 0.3026 | 0.100 | 0.105 | 172 | 27/47 | 3.0 |
| D1_1-p_actual | planner | airline | 0.2474 | 0.095 | 0.196 | 46 | 18/24 | 4.0 |
| D1_1-p_actual | planner | aime | 0.1719 | 0.089 | 0.667 | 6 | 9/23 | 3.0 |
| D1_1-p_actual | planner | all | 0.2308 | 0.098 | 0.231 | 52 | 26/47 | 3.5 |
| D1_1-p_actual | subagent | airline | 0.2938 | 0.100 | 0.146 | 48 | 12/24 | 3.0 |
| D1_1-p_actual | subagent | aime | 0.0273 | 0.083 | 0.167 | 72 | 11/22 | 1.0 |
| D1_1-p_actual | subagent | all | 0.2857 | 0.097 | 0.058 | 120 | 15/46 | 3.0 |
| D1_1-p_actual | all | airline | 0.2692 | 0.098 | 0.170 | 94 | 19/24 | 1.0 |
| D1_1-p_actual | all | aime | 0.1052 | 0.098 | 0.090 | 78 | 14/23 | 2.0 |
| D1_1-p_actual | all | all | 0.2308 | 0.100 | 0.110 | 172 | 29/47 | 3.0 |
| D1_1-margin | planner | airline | 0.4585 | 0.095 | 0.174 | 46 | 16/24 | 4.0 |
| D1_1-margin | planner | aime | 0.2937 | 0.089 | 0.500 | 6 | 8/23 | 3.5 |
| D1_1-margin | planner | all | 0.4484 | 0.098 | 0.192 | 52 | 23/47 | 4.0 |
| D1_1-margin | subagent | airline | 0.5379 | 0.100 | 0.125 | 48 | 12/24 | 3.0 |
| D1_1-margin | subagent | aime | 0.05451 | 0.083 | 0.167 | 72 | 11/22 | 1.0 |
| D1_1-margin | subagent | all | 0.4768 | 0.097 | 0.058 | 120 | 15/46 | 3.0 |
| D1_1-margin | all | airline | 0.4768 | 0.098 | 0.160 | 94 | 17/24 | 1.0 |
| D1_1-margin | all | aime | 0.2099 | 0.098 | 0.077 | 78 | 13/23 | 3.0 |
| D1_1-margin | all | all | 0.4462 | 0.100 | 0.099 | 172 | 26/47 | 3.0 |
| D1_handoff | planner | airline | 0.7041 | 0.095 | 0.065 | 46 | 8/24 | 5.5 |
| D1_handoff | planner | aime | 0.0853 | 0.089 | 0.333 | 6 | 10/23 | 4.5 |
| D1_handoff | planner | all | 0.6846 | 0.098 | 0.096 | 52 | 14/47 | 3.5 |
| D2 | planner | airline | 1 | 0.000 | 0.043 | 46 | 1/24 | 20.0 |
| D2 | planner | aime | 1e-09 | 0.000 | 0.000 | 6 | 1/23 | 29.0 |
| D2 | planner | all | 1 | 0.000 | 0.038 | 52 | 2/47 | 24.5 |
| D2 | subagent | airline | 1 | 0.074 | 0.479 | 48 | 17/24 | 2.0 |
| D2 | subagent | aime | 1 | 0.083 | 0.417 | 72 | 9/22 | 0.0 |
| D2 | subagent | all | 1 | 0.075 | 0.442 | 120 | 26/46 | 2.0 |
| D2 | all | airline | 1 | 0.041 | 0.266 | 94 | 17/24 | 2.0 |
| D2 | all | aime | 1 | 0.033 | 0.385 | 78 | 9/23 | 0.0 |
| D2 | all | all | 1 | 0.040 | 0.320 | 172 | 26/47 | 2.0 |
| D3_instruction->premise | planner | airline | 0.8 | 0.091 | 0.190 | 21 | 1/24 | 0.0 |
| D3_instruction->premise | planner | aime | 0.8889 | 0.077 | 0.000 | 3 | 2/23 | 4.5 |
| D3_instruction->premise | planner | all | 0.8667 | 0.072 | 0.083 | 24 | 3/47 | 3.0 |
| D3_report->planner | planner | airline | 1 | 0.000 | 0.000 | 31 | 0/24 | n/a |
| D3_report->planner | planner | aime | 1 | 0.000 | 0.000 | 3 | 0/23 | n/a |
| D3_report->planner | planner | all | 1 | 0.000 | 0.000 | 34 | 0/47 | n/a |

## 5. D2 tool checks vs `category="tool"` labels

Population = every labeled non-aux step (cascade included); positive = a labeled error event of category `tool` at that step; a step is flagged when any tool call at it trips the check.

| check | domain | n_steps | n_pos(tool) | n_flagged | TP | precision | recall |
|---|---|---|---|---|---|---|---|
| error | airline | 826 | 82 | 83 | 45 | 0.542 | 0.549 |
| error | aime | 382 | 134 | 27 | 21 | 0.778 | 0.157 |
| error | all | 1208 | 216 | 110 | 66 | 0.600 | 0.306 |
| empty | airline | 826 | 82 | 12 | 0 | 0.000 | 0.000 |
| empty | aime | 382 | 134 | 0 | 0 | n/a | 0.000 |
| empty | all | 1208 | 216 | 12 | 0 | 0.000 | 0.000 |
| repeat | airline | 826 | 82 | 78 | 17 | 0.218 | 0.207 |
| repeat | aime | 382 | 134 | 114 | 98 | 0.860 | 0.731 |
| repeat | all | 1208 | 216 | 192 | 115 | 0.599 | 0.532 |
| schema | airline | 826 | 82 | 0 | 0 | n/a | 0.000 |
| schema | aime | 382 | 134 | 0 | 0 | n/a | 0.000 |
| schema | all | 1208 | 216 | 0 | 0 | n/a | 0.000 |
| ignored | airline | 826 | 82 | 31 | 3 | 0.097 | 0.037 |
| ignored | aime | 382 | 134 | 2 | 0 | 0.000 | 0.000 |
| ignored | all | 1208 | 216 | 33 | 3 | 0.091 | 0.014 |

## 6. Matched sub-table (steps scored by D1 AND D2)

Intersection = 1296 step(s) scored by all of D1_1-conf, D2.

| item | role | domain | n_pos | n_neg | AUROC all errors [95% CI] |
|---|---|---|---|---|---|
| D1_1-conf | planner | airline | 46 | 148 | 0.616 [0.530, 0.702] |
| D1_1-conf | planner | aime | 6 | 56 | 0.610 [0.318, 0.881] |
| D1_1-conf | planner | all | 52 | 204 | 0.667 [0.590, 0.741] |
| D1_1-conf | subagent | airline | 48 | 190 | 0.539 [0.439, 0.629] |
| D1_1-conf | subagent | aime | 72 | 36 | 0.534 [0.415, 0.651] |
| D1_1-conf | subagent | all | 120 | 226 | 0.540 [0.477, 0.603] |
| D1_1-conf | all | airline | 94 | 338 | 0.583 [0.516, 0.645] |
| D1_1-conf | all | aime | 78 | 92 | 0.544 [0.456, 0.639] |
| D1_1-conf | all | all | 172 | 430 | 0.538 [0.489, 0.586] |
| D2 | planner | airline | 46 | 148 | 0.522 [0.500, 0.554] |
| D2 | planner | aime | 6 | 56 | 0.500 [0.500, 0.500] |
| D2 | planner | all | 52 | 204 | 0.519 [0.500, 0.548] |
| D2 | subagent | airline | 48 | 190 | 0.703 [0.625, 0.778] |
| D2 | subagent | aime | 72 | 36 | 0.667 [0.597, 0.736] |
| D2 | subagent | all | 120 | 226 | 0.683 [0.633, 0.730] |
| D2 | all | airline | 94 | 338 | 0.612 [0.569, 0.662] |
| D2 | all | aime | 78 | 92 | 0.676 [0.619, 0.732] |
| D2 | all | all | 172 | 430 | 0.640 [0.605, 0.673] |

## 7. Any-flag coverage (descriptive)

Of the 172 labeled error steps (decisive + transient), **0.488** (84/172) are flagged by at least one item at its own 90th-percentile threshold (percentiles taken over that item's scores on all labeled non-aux steps).

Item thresholds: `D1_1-conf`=0.2793, `D1_1-margin`=0.4443, `D1_1-p_actual`=0.2344, `D1_handoff`=0.4819, `D2`=1.0000, `D3_instruction->premise`=0.7500, `D3_report->planner`=1.0000.

