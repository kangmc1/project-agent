# Detection metrics

- generated: 2026-09-09 03:30:09 KST
- d1_scored_n: 0 rows in `audit/d1.jsonl`
- labeled runs: aime=30, airline=30 (total 60); runs in index: 62
- D1 method(s) present: none
- items scored: D2_unsupported, D3_unsatisfied, D7_instruction->premise, D7_report->planner
- bootstrap: 1000 stratified resamples, seed 0; AUROC is `n/a` when n_pos < 3 or n_neg < 3.

## 1. Step-level AUROC

Labeled runs only; cascade steps excluded; negatives = clean steps. `n_scored/n_labeled` counts labeled non-aux steps in the role scope the item applies to.

| item | role | domain | n_scored/n_labeled | n_pos(all) | n_neg | AUROC all errors [95% CI] | n_pos(dec) | AUROC decisive [95% CI] |
|---|---|---|---|---|---|---|---|---|
| D2_unsupported | planner | airline | 16/391 | 1 | 3 | n/a | 1 | n/a |
| D2_unsupported | planner | aime | 31/123 | 2 | 8 | n/a | 2 | n/a |
| D2_unsupported | planner | all | 47/514 | 3 | 11 | 0.773 [0.363, 1.000] | 3 | 0.773 [0.363, 1.000] |
| D2_unsupported | subagent | airline | 375/435 | 44 | 170 | 0.434 [0.369, 0.500] | 8 | 0.414 [0.324, 0.557] |
| D2_unsupported | subagent | aime | 192/259 | 44 | 32 | 0.408 [0.278, 0.541] | 17 | 0.427 [0.268, 0.588] |
| D2_unsupported | subagent | all | 567/694 | 88 | 202 | 0.525 [0.462, 0.591] | 25 | 0.576 [0.473, 0.683] |
| D2_unsupported | all | airline | 391/826 | 45 | 173 | 0.448 [0.388, 0.517] | 9 | 0.478 [0.338, 0.663] |
| D2_unsupported | all | aime | 223/382 | 46 | 40 | 0.459 [0.340, 0.592] | 19 | 0.482 [0.336, 0.634] |
| D2_unsupported | all | all | 614/1208 | 91 | 213 | 0.533 [0.473, 0.601] | 28 | 0.595 [0.497, 0.706] |
| D3_unsatisfied | planner | airline | 17/391 | 1 | 4 | n/a | 1 | n/a |
| D3_unsatisfied | planner | aime | 1/123 | 0 | 1 | n/a | 0 | n/a |
| D3_unsatisfied | planner | all | 18/514 | 1 | 5 | n/a | 1 | n/a |
| D3_unsatisfied | subagent | airline | 329/435 | 40 | 162 | 0.548 [0.467, 0.624] | 7 | 0.659 [0.457, 0.830] |
| D3_unsatisfied | subagent | aime | 220/259 | 69 | 34 | 0.445 [0.350, 0.555] | 20 | 0.646 [0.528, 0.759] |
| D3_unsatisfied | subagent | all | 549/694 | 109 | 196 | 0.553 [0.497, 0.609] | 27 | 0.736 [0.646, 0.816] |
| D3_unsatisfied | all | airline | 346/826 | 41 | 166 | 0.541 [0.459, 0.617] | 8 | 0.620 [0.445, 0.802] |
| D3_unsatisfied | all | aime | 221/382 | 69 | 35 | 0.453 [0.359, 0.560] | 20 | 0.654 [0.539, 0.775] |
| D3_unsatisfied | all | all | 567/1208 | 110 | 201 | 0.550 [0.493, 0.610] | 28 | 0.721 [0.637, 0.799] |
| D7_instruction->premise | planner | airline | 104/391 | 21 | 43 | 0.416 [0.271, 0.567] | 7 | 0.344 [0.128, 0.610] |
| D7_instruction->premise | planner | aime | 66/123 | 3 | 39 | 0.406 [0.064, 0.714] | 0 | n/a |
| D7_instruction->premise | planner | all | 170/514 | 24 | 82 | 0.358 [0.231, 0.486] | 7 | 0.299 [0.079, 0.571] |
| D7_report->planner | planner | airline | 161/391 | 31 | 66 | 0.610 [0.477, 0.733] | 11 | 0.576 [0.374, 0.764] |
| D7_report->planner | planner | aime | 68/123 | 3 | 41 | 0.659 [0.455, 0.837] | 0 | n/a |
| D7_report->planner | planner | all | 229/514 | 34 | 107 | 0.587 [0.478, 0.703] | 11 | 0.535 [0.357, 0.711] |

## 2. Trace-level AUROC (positives = runs with success=false)

All runs in `runs/index.csv` (labels not required); a run enters only if the item scored >= 80% of that run's non-aux steps in the role scope.

| item | role | domain | n_runs | n_fail | n_succ | AUROC max [95% CI] | AUROC mean [95% CI] |
|---|---|---|---|---|---|---|---|
| D2_unsupported | planner | aime | 1 | 1 | 0 | not computable (success=0, failure=1) | not computable (success=0, failure=1) |
| D2_unsupported | planner | all | 1 | 1 | 0 | not computable (success=0, failure=1) | not computable (success=0, failure=1) |
| D2_unsupported | subagent | airline | 23 | 18 | 5 | 0.544 [0.305, 0.783] | 0.511 [0.256, 0.745] |
| D2_unsupported | subagent | aime | 21 | 15 | 6 | 0.456 [0.139, 0.800] | 0.450 [0.200, 0.711] |
| D2_unsupported | subagent | all | 44 | 33 | 11 | 0.523 [0.326, 0.726] | 0.461 [0.264, 0.656] |
| D2_unsupported | all | aime | 4 | 4 | 0 | not computable (success=0, failure=4) | not computable (success=0, failure=4) |
| D2_unsupported | all | all | 4 | 4 | 0 | not computable (success=0, failure=4) | not computable (success=0, failure=4) |
| D3_unsatisfied | subagent | airline | 19 | 13 | 6 | 0.506 [0.346, 0.712] | 0.372 [0.090, 0.679] |
| D3_unsatisfied | subagent | aime | 26 | 18 | 8 | 0.444 [0.361, 0.500] | 0.622 [0.409, 0.823] |
| D3_unsatisfied | subagent | all | 45 | 31 | 14 | 0.471 [0.387, 0.575] | 0.479 [0.298, 0.658] |
| D3_unsatisfied | all | aime | 2 | 1 | 1 | not computable (success=1, failure=1) | not computable (success=1, failure=1) |
| D3_unsatisfied | all | all | 2 | 1 | 1 | not computable (success=1, failure=1) | not computable (success=1, failure=1) |

## 3. Decisive-step attribution (failed labeled runs)

Predicted decisive step = argmax score over the run's scored steps in the role scope; ties broken planner-first then earliest step.  `+/-1` is one position in the run's non-aux step order.

| item | role | domain | n_runs | exact acc | +/-1 acc | agent acc |
|---|---|---|---|---|---|---|
| D2_unsupported | planner | airline | 13 | 0.077 | 0.077 | 0.615 |
| D2_unsupported | planner | aime | 23 | 0.087 | 0.087 | 0.087 |
| D2_unsupported | planner | all | 36 | 0.083 | 0.083 | 0.278 |
| D2_unsupported | subagent | airline | 22 | 0.000 | 0.136 | 0.227 |
| D2_unsupported | subagent | aime | 22 | 0.273 | 0.409 | 0.682 |
| D2_unsupported | subagent | all | 44 | 0.136 | 0.273 | 0.455 |
| D2_unsupported | all | airline | 22 | 0.045 | 0.091 | 0.364 |
| D2_unsupported | all | aime | 23 | 0.304 | 0.391 | 0.652 |
| D2_unsupported | all | all | 45 | 0.178 | 0.244 | 0.511 |
| D3_unsatisfied | planner | airline | 13 | 0.077 | 0.077 | 0.615 |
| D3_unsatisfied | planner | all | 13 | 0.077 | 0.077 | 0.615 |
| D3_unsatisfied | subagent | airline | 21 | 0.048 | 0.286 | 0.190 |
| D3_unsatisfied | subagent | aime | 22 | 0.591 | 0.727 | 0.955 |
| D3_unsatisfied | subagent | all | 43 | 0.326 | 0.512 | 0.581 |
| D3_unsatisfied | all | airline | 21 | 0.048 | 0.143 | 0.286 |
| D3_unsatisfied | all | aime | 22 | 0.591 | 0.727 | 0.955 |
| D3_unsatisfied | all | all | 43 | 0.326 | 0.442 | 0.628 |
| D7_instruction->premise | planner | airline | 21 | 0.286 | 0.333 | 0.619 |
| D7_instruction->premise | planner | aime | 21 | 0.000 | 0.429 | 0.048 |
| D7_instruction->premise | planner | all | 42 | 0.143 | 0.381 | 0.333 |
| D7_report->planner | planner | airline | 23 | 0.174 | 0.217 | 0.652 |
| D7_report->planner | planner | aime | 22 | 0.000 | 0.455 | 0.045 |
| D7_report->planner | planner | all | 45 | 0.089 | 0.333 | 0.356 |

## 4. recall@FPR10 and detection latency

Threshold = the smallest score whose FPR on labeled **clean** steps of that role/domain is <= 10% (the achieved FPR is reported: binary or heavily tied items cannot hit 10% exactly).  Latency = positions after the decisive step until the first score >= threshold (non-aux order); runs that never cross are censored.

| item | role | domain | threshold | FPR(clean) | recall(all errors) | n_pos | n_crossed/n_failed | median latency |
|---|---|---|---|---|---|---|---|---|
| D2_unsupported | planner | airline | 1 | 0.000 | 1.000 | 1 | 1/24 | 0.0 |
| D2_unsupported | planner | aime | 1 | 0.000 | 0.500 | 2 | 1/23 | 0.0 |
| D2_unsupported | planner | all | 1 | 0.000 | 0.667 | 3 | 2/47 | 0.0 |
| D2_unsupported | subagent | airline | 0.8 | 0.076 | 0.023 | 44 | 2/24 | 2.0 |
| D2_unsupported | subagent | aime | 1 | 0.000 | 0.000 | 44 | 0/22 | n/a |
| D2_unsupported | subagent | all | 0.9375 | 0.099 | 0.023 | 88 | 7/46 | 3.0 |
| D2_unsupported | all | airline | 0.8 | 0.075 | 0.044 | 45 | 3/24 | 1.0 |
| D2_unsupported | all | aime | 1 | 0.000 | 0.000 | 46 | 0/23 | n/a |
| D2_unsupported | all | all | 0.875 | 0.099 | 0.077 | 91 | 10/47 | 1.5 |
| D3_unsatisfied | planner | airline | 1 | 0.000 | 0.000 | 1 | 0/24 | n/a |
| D3_unsatisfied | planner | all | 1 | 0.000 | 0.000 | 1 | 0/47 | n/a |
| D3_unsatisfied | subagent | airline | 1 | 0.000 | 0.000 | 40 | 0/24 | n/a |
| D3_unsatisfied | subagent | aime | 1 | 0.000 | 0.000 | 69 | 0/22 | n/a |
| D3_unsatisfied | subagent | all | 1 | 0.000 | 0.000 | 109 | 0/46 | n/a |
| D3_unsatisfied | all | airline | 1 | 0.000 | 0.000 | 41 | 0/24 | n/a |
| D3_unsatisfied | all | aime | 1 | 0.000 | 0.000 | 69 | 0/23 | n/a |
| D3_unsatisfied | all | all | 1 | 0.000 | 0.000 | 110 | 0/47 | n/a |
| D7_instruction->premise | planner | airline | 0.8 | 0.093 | 0.190 | 21 | 2/24 | 4.5 |
| D7_instruction->premise | planner | aime | 1 | 0.000 | 0.000 | 3 | 0/23 | n/a |
| D7_instruction->premise | planner | all | 1 | 0.000 | 0.000 | 24 | 0/47 | n/a |
| D7_report->planner | planner | airline | 1 | 0.000 | 0.000 | 31 | 0/24 | n/a |
| D7_report->planner | planner | aime | 1 | 0.000 | 0.000 | 3 | 0/23 | n/a |
| D7_report->planner | planner | all | 1 | 0.000 | 0.000 | 34 | 0/47 | n/a |

## 5. D3 tool checks vs `category="tool"` labels

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

## 6. Matched sub-table (steps scored by D1 AND D2 AND D3)

Intersection = 546 step(s) scored by all of D2_unsupported, D3_unsatisfied.

| item | role | domain | n_pos | n_neg | AUROC all errors [95% CI] |
|---|---|---|---|---|---|
| D2_unsupported | planner | airline | 1 | 3 | n/a |
| D2_unsupported | planner | aime | 0 | 1 | n/a |
| D2_unsupported | planner | all | 1 | 4 | n/a |
| D2_unsupported | subagent | airline | 40 | 155 | 0.431 [0.361, 0.503] |
| D2_unsupported | subagent | aime | 42 | 32 | 0.396 [0.272, 0.542] |
| D2_unsupported | subagent | all | 82 | 187 | 0.520 [0.458, 0.586] |
| D2_unsupported | all | airline | 41 | 158 | 0.447 [0.381, 0.522] |
| D2_unsupported | all | aime | 42 | 33 | 0.409 [0.281, 0.544] |
| D2_unsupported | all | all | 83 | 191 | 0.529 [0.467, 0.594] |
| D3_unsatisfied | planner | airline | 1 | 3 | n/a |
| D3_unsatisfied | planner | aime | 0 | 1 | n/a |
| D3_unsatisfied | planner | all | 1 | 4 | n/a |
| D3_unsatisfied | subagent | airline | 40 | 155 | 0.546 [0.471, 0.625] |
| D3_unsatisfied | subagent | aime | 42 | 32 | 0.540 [0.430, 0.655] |
| D3_unsatisfied | subagent | all | 82 | 187 | 0.595 [0.532, 0.655] |
| D3_unsatisfied | all | airline | 41 | 158 | 0.541 [0.465, 0.615] |
| D3_unsatisfied | all | aime | 42 | 33 | 0.549 [0.431, 0.660] |
| D3_unsatisfied | all | all | 83 | 191 | 0.593 [0.531, 0.656] |

## 7. Any-flag coverage (descriptive)

Of the 172 labeled error steps (decisive + transient), **0.395** (68/172) are flagged by at least one item at its own 90th-percentile threshold (percentiles taken over that item's scores on all labeled non-aux steps).

Item thresholds: `D2_unsupported`=0.6667, `D3_unsatisfied`=1.0000, `D7_instruction->premise`=0.8367, `D7_report->planner`=1.0000.

