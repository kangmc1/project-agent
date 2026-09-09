# Detection metrics

- generated: 2026-09-09 10:35:40 KST
- d1_scored_n: 1296 rows in `audit/d1.jsonl`
- labeled runs: aime=30, airline=30 (total 60); runs in index: 62
- D1 method(s) present: stepwise
- items scored: D1_1-conf, D1_1-p_actual, D1_1-margin, D1_handoff, D2, D3, D3fid_instruction->premise, D3fid_report->planner, LLM_D1_1-conf, LLM_D1_1-p_actual, LLM_D2, LLM_D3_instruction->premise, LLM_D3_report->planner, LLM-gptoss20b_D1_1-conf, LLM-gptoss20b_D1_1-p_actual, LLM-gptoss20b_D2, LLM-gptoss20b_D3_instruction->premise, LLM-gptoss20b_D3_report->planner, LLM-qwen8b_D1_1-conf, LLM-qwen8b_D1_1-p_actual, LLM-qwen8b_D2, LLM-qwen8b_D3_instruction->premise, LLM-qwen8b_D3_report->planner, Judge_p_fail, Judge_flag
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
| D3 | planner | airline | 170/391 | 33 | 67 | 0.599 [0.523, 0.675] | 13 | 0.708 [0.563, 0.847] |
| D3 | planner | aime | 70/123 | 3 | 42 | 0.500 [0.500, 0.500] | 0 | n/a |
| D3 | planner | all | 240/514 | 36 | 109 | 0.597 [0.532, 0.667] | 13 | 0.717 [0.579, 0.848] |
| D3fid_instruction->premise | planner | airline | 105/391 | 21 | 44 | 0.401 [0.254, 0.554] | 7 | 0.349 [0.125, 0.609] |
| D3fid_instruction->premise | planner | aime | 66/123 | 3 | 39 | 0.513 [0.128, 0.821] | 0 | n/a |
| D3fid_instruction->premise | planner | all | 171/514 | 24 | 83 | 0.388 [0.260, 0.517] | 7 | 0.335 [0.114, 0.608] |
| D3fid_report->planner | planner | airline | 161/391 | 31 | 66 | 0.590 [0.470, 0.716] | 11 | 0.598 [0.399, 0.775] |
| D3fid_report->planner | planner | aime | 68/123 | 3 | 41 | 0.715 [0.537, 0.866] | 0 | n/a |
| D3fid_report->planner | planner | all | 229/514 | 34 | 107 | 0.579 [0.476, 0.687] | 11 | 0.566 [0.392, 0.737] |
| LLM_D1_1-conf | planner | airline | 190/391 | 44 | 146 | 0.580 [0.479, 0.678] | 16 | 0.577 [0.403, 0.741] |
| LLM_D1_1-conf | planner | aime | 0/123 | 0 | 0 | n/a | 0 | n/a |
| LLM_D1_1-conf | planner | all | 190/514 | 44 | 146 | 0.580 [0.479, 0.678] | 16 | 0.577 [0.403, 0.741] |
| LLM_D1_1-conf | subagent | airline | 222/435 | 36 | 186 | 0.610 [0.508, 0.702] | 8 | 0.509 [0.320, 0.713] |
| LLM_D1_1-conf | subagent | aime | 0/259 | 0 | 0 | n/a | 0 | n/a |
| LLM_D1_1-conf | subagent | all | 222/694 | 36 | 186 | 0.610 [0.508, 0.702] | 8 | 0.509 [0.320, 0.713] |
| LLM_D1_1-conf | all | airline | 412/826 | 80 | 332 | 0.594 [0.527, 0.659] | 24 | 0.561 [0.441, 0.694] |
| LLM_D1_1-conf | all | aime | 0/382 | 0 | 0 | n/a | 0 | n/a |
| LLM_D1_1-conf | all | all | 412/1208 | 80 | 332 | 0.594 [0.527, 0.659] | 24 | 0.561 [0.441, 0.694] |
| LLM_D1_1-p_actual | planner | airline | 190/391 | 44 | 146 | 0.603 [0.516, 0.693] | 16 | 0.682 [0.560, 0.815] |
| LLM_D1_1-p_actual | planner | aime | 0/123 | 0 | 0 | n/a | 0 | n/a |
| LLM_D1_1-p_actual | planner | all | 190/514 | 44 | 146 | 0.603 [0.516, 0.693] | 16 | 0.682 [0.560, 0.815] |
| LLM_D1_1-p_actual | subagent | airline | 222/435 | 36 | 186 | 0.646 [0.552, 0.737] | 8 | 0.622 [0.408, 0.817] |
| LLM_D1_1-p_actual | subagent | aime | 0/259 | 0 | 0 | n/a | 0 | n/a |
| LLM_D1_1-p_actual | subagent | all | 222/694 | 36 | 186 | 0.646 [0.552, 0.737] | 8 | 0.622 [0.408, 0.817] |
| LLM_D1_1-p_actual | all | airline | 412/826 | 80 | 332 | 0.621 [0.555, 0.686] | 24 | 0.655 [0.538, 0.757] |
| LLM_D1_1-p_actual | all | aime | 0/382 | 0 | 0 | n/a | 0 | n/a |
| LLM_D1_1-p_actual | all | all | 412/1208 | 80 | 332 | 0.621 [0.555, 0.686] | 24 | 0.655 [0.538, 0.757] |
| LLM_D2 | planner | airline | 192/391 | 44 | 148 | 0.500 [0.463, 0.541] | 16 | 0.466 [0.446, 0.483] |
| LLM_D2 | planner | aime | 0/123 | 0 | 0 | n/a | 0 | n/a |
| LLM_D2 | planner | all | 192/514 | 44 | 148 | 0.500 [0.463, 0.541] | 16 | 0.466 [0.446, 0.483] |
| LLM_D2 | subagent | airline | 227/435 | 37 | 190 | 0.661 [0.578, 0.748] | 8 | 0.619 [0.473, 0.796] |
| LLM_D2 | subagent | aime | 0/259 | 0 | 0 | n/a | 0 | n/a |
| LLM_D2 | subagent | all | 227/694 | 37 | 190 | 0.661 [0.578, 0.748] | 8 | 0.619 [0.473, 0.796] |
| LLM_D2 | all | airline | 419/826 | 81 | 338 | 0.570 [0.520, 0.627] | 24 | 0.509 [0.451, 0.578] |
| LLM_D2 | all | aime | 0/382 | 0 | 0 | n/a | 0 | n/a |
| LLM_D2 | all | all | 419/1208 | 81 | 338 | 0.570 [0.520, 0.627] | 24 | 0.509 [0.451, 0.578] |
| LLM_D3_instruction->premise | planner | airline | 98/391 | 31 | 67 | 0.573 [0.490, 0.655] | 13 | 0.537 [0.440, 0.644] |
| LLM_D3_instruction->premise | planner | aime | 0/123 | 0 | 0 | n/a | 0 | n/a |
| LLM_D3_instruction->premise | planner | all | 98/514 | 31 | 67 | 0.573 [0.490, 0.655] | 13 | 0.537 [0.440, 0.644] |
| LLM_D3_report->planner | planner | airline | 84/391 | 29 | 55 | 0.434 [0.326, 0.559] | 12 | 0.398 [0.241, 0.553] |
| LLM_D3_report->planner | planner | aime | 0/123 | 0 | 0 | n/a | 0 | n/a |
| LLM_D3_report->planner | planner | all | 84/514 | 29 | 55 | 0.434 [0.326, 0.559] | 12 | 0.398 [0.241, 0.553] |
| LLM-gptoss20b_D1_1-conf | planner | airline | 192/391 | 44 | 148 | 0.549 [0.458, 0.643] | 16 | 0.524 [0.365, 0.681] |
| LLM-gptoss20b_D1_1-conf | planner | aime | 0/123 | 0 | 0 | n/a | 0 | n/a |
| LLM-gptoss20b_D1_1-conf | planner | all | 192/514 | 44 | 148 | 0.549 [0.458, 0.643] | 16 | 0.524 [0.365, 0.681] |
| LLM-gptoss20b_D1_1-conf | subagent | airline | 220/435 | 35 | 185 | 0.507 [0.398, 0.626] | 7 | 0.534 [0.362, 0.714] |
| LLM-gptoss20b_D1_1-conf | subagent | aime | 0/259 | 0 | 0 | n/a | 0 | n/a |
| LLM-gptoss20b_D1_1-conf | subagent | all | 220/694 | 35 | 185 | 0.507 [0.398, 0.626] | 7 | 0.534 [0.362, 0.714] |
| LLM-gptoss20b_D1_1-conf | all | airline | 412/826 | 79 | 333 | 0.545 [0.475, 0.613] | 23 | 0.549 [0.425, 0.672] |
| LLM-gptoss20b_D1_1-conf | all | aime | 0/382 | 0 | 0 | n/a | 0 | n/a |
| LLM-gptoss20b_D1_1-conf | all | all | 412/1208 | 79 | 333 | 0.545 [0.475, 0.613] | 23 | 0.549 [0.425, 0.672] |
| LLM-gptoss20b_D1_1-p_actual | planner | airline | 192/391 | 44 | 148 | 0.637 [0.548, 0.725] | 16 | 0.774 [0.660, 0.877] |
| LLM-gptoss20b_D1_1-p_actual | planner | aime | 0/123 | 0 | 0 | n/a | 0 | n/a |
| LLM-gptoss20b_D1_1-p_actual | planner | all | 192/514 | 44 | 148 | 0.637 [0.548, 0.725] | 16 | 0.774 [0.660, 0.877] |
| LLM-gptoss20b_D1_1-p_actual | subagent | airline | 220/435 | 35 | 185 | 0.617 [0.515, 0.710] | 7 | 0.784 [0.706, 0.858] |
| LLM-gptoss20b_D1_1-p_actual | subagent | aime | 0/259 | 0 | 0 | n/a | 0 | n/a |
| LLM-gptoss20b_D1_1-p_actual | subagent | all | 220/694 | 35 | 185 | 0.617 [0.515, 0.710] | 7 | 0.784 [0.706, 0.858] |
| LLM-gptoss20b_D1_1-p_actual | all | airline | 412/826 | 79 | 333 | 0.609 [0.542, 0.676] | 23 | 0.740 [0.658, 0.822] |
| LLM-gptoss20b_D1_1-p_actual | all | aime | 0/382 | 0 | 0 | n/a | 0 | n/a |
| LLM-gptoss20b_D1_1-p_actual | all | all | 412/1208 | 79 | 333 | 0.609 [0.542, 0.676] | 23 | 0.740 [0.658, 0.822] |
| LLM-gptoss20b_D2 | planner | airline | 192/391 | 44 | 148 | 0.616 [0.536, 0.697] | 16 | 0.605 [0.473, 0.730] |
| LLM-gptoss20b_D2 | planner | aime | 0/123 | 0 | 0 | n/a | 0 | n/a |
| LLM-gptoss20b_D2 | planner | all | 192/514 | 44 | 148 | 0.616 [0.536, 0.697] | 16 | 0.605 [0.473, 0.730] |
| LLM-gptoss20b_D2 | subagent | airline | 227/435 | 37 | 190 | 0.672 [0.591, 0.750] | 8 | 0.630 [0.486, 0.809] |
| LLM-gptoss20b_D2 | subagent | aime | 0/259 | 0 | 0 | n/a | 0 | n/a |
| LLM-gptoss20b_D2 | subagent | all | 227/694 | 37 | 190 | 0.672 [0.591, 0.750] | 8 | 0.630 [0.486, 0.809] |
| LLM-gptoss20b_D2 | all | airline | 419/826 | 81 | 338 | 0.651 [0.598, 0.708] | 24 | 0.633 [0.527, 0.731] |
| LLM-gptoss20b_D2 | all | aime | 0/382 | 0 | 0 | n/a | 0 | n/a |
| LLM-gptoss20b_D2 | all | all | 419/1208 | 81 | 338 | 0.651 [0.598, 0.708] | 24 | 0.633 [0.527, 0.731] |
| LLM-gptoss20b_D3_instruction->premise | planner | airline | 98/391 | 31 | 67 | 0.540 [0.444, 0.636] | 13 | 0.616 [0.470, 0.770] |
| LLM-gptoss20b_D3_instruction->premise | planner | aime | 0/123 | 0 | 0 | n/a | 0 | n/a |
| LLM-gptoss20b_D3_instruction->premise | planner | all | 98/514 | 31 | 67 | 0.540 [0.444, 0.636] | 13 | 0.616 [0.470, 0.770] |
| LLM-gptoss20b_D3_report->planner | planner | airline | 91/391 | 30 | 61 | 0.527 [0.412, 0.648] | 13 | 0.591 [0.449, 0.736] |
| LLM-gptoss20b_D3_report->planner | planner | aime | 0/123 | 0 | 0 | n/a | 0 | n/a |
| LLM-gptoss20b_D3_report->planner | planner | all | 91/514 | 30 | 61 | 0.527 [0.412, 0.648] | 13 | 0.591 [0.449, 0.736] |
| LLM-qwen8b_D1_1-conf | planner | airline | 179/391 | 41 | 138 | 0.473 [0.388, 0.565] | 15 | 0.419 [0.288, 0.583] |
| LLM-qwen8b_D1_1-conf | planner | aime | 0/123 | 0 | 0 | n/a | 0 | n/a |
| LLM-qwen8b_D1_1-conf | planner | all | 179/514 | 41 | 138 | 0.473 [0.388, 0.565] | 15 | 0.419 [0.288, 0.583] |
| LLM-qwen8b_D1_1-conf | subagent | airline | 188/435 | 27 | 161 | 0.547 [0.435, 0.670] | 5 | 0.431 [0.217, 0.673] |
| LLM-qwen8b_D1_1-conf | subagent | aime | 0/259 | 0 | 0 | n/a | 0 | n/a |
| LLM-qwen8b_D1_1-conf | subagent | all | 188/694 | 27 | 161 | 0.547 [0.435, 0.670] | 5 | 0.431 [0.217, 0.673] |
| LLM-qwen8b_D1_1-conf | all | airline | 367/826 | 68 | 299 | 0.515 [0.438, 0.588] | 20 | 0.439 [0.311, 0.582] |
| LLM-qwen8b_D1_1-conf | all | aime | 0/382 | 0 | 0 | n/a | 0 | n/a |
| LLM-qwen8b_D1_1-conf | all | all | 367/1208 | 68 | 299 | 0.515 [0.438, 0.588] | 20 | 0.439 [0.311, 0.582] |
| LLM-qwen8b_D1_1-p_actual | planner | airline | 179/391 | 41 | 138 | 0.599 [0.501, 0.691] | 15 | 0.697 [0.533, 0.850] |
| LLM-qwen8b_D1_1-p_actual | planner | aime | 0/123 | 0 | 0 | n/a | 0 | n/a |
| LLM-qwen8b_D1_1-p_actual | planner | all | 179/514 | 41 | 138 | 0.599 [0.501, 0.691] | 15 | 0.697 [0.533, 0.850] |
| LLM-qwen8b_D1_1-p_actual | subagent | airline | 188/435 | 27 | 161 | 0.518 [0.404, 0.631] | 5 | 0.658 [0.373, 0.851] |
| LLM-qwen8b_D1_1-p_actual | subagent | aime | 0/259 | 0 | 0 | n/a | 0 | n/a |
| LLM-qwen8b_D1_1-p_actual | subagent | all | 188/694 | 27 | 161 | 0.518 [0.404, 0.631] | 5 | 0.658 [0.373, 0.851] |
| LLM-qwen8b_D1_1-p_actual | all | airline | 367/826 | 68 | 299 | 0.558 [0.486, 0.632] | 20 | 0.666 [0.533, 0.786] |
| LLM-qwen8b_D1_1-p_actual | all | aime | 0/382 | 0 | 0 | n/a | 0 | n/a |
| LLM-qwen8b_D1_1-p_actual | all | all | 367/1208 | 68 | 299 | 0.558 [0.486, 0.632] | 20 | 0.666 [0.533, 0.786] |
| LLM-qwen8b_D2 | planner | airline | 192/391 | 44 | 148 | 0.526 [0.481, 0.580] | 16 | 0.501 [0.453, 0.573] |
| LLM-qwen8b_D2 | planner | aime | 0/123 | 0 | 0 | n/a | 0 | n/a |
| LLM-qwen8b_D2 | planner | all | 192/514 | 44 | 148 | 0.526 [0.481, 0.580] | 16 | 0.501 [0.453, 0.573] |
| LLM-qwen8b_D2 | subagent | airline | 227/435 | 37 | 190 | 0.626 [0.548, 0.705] | 8 | 0.549 [0.418, 0.695] |
| LLM-qwen8b_D2 | subagent | aime | 0/259 | 0 | 0 | n/a | 0 | n/a |
| LLM-qwen8b_D2 | subagent | all | 227/694 | 37 | 190 | 0.626 [0.548, 0.705] | 8 | 0.549 [0.418, 0.695] |
| LLM-qwen8b_D2 | all | airline | 419/826 | 81 | 338 | 0.567 [0.520, 0.621] | 24 | 0.506 [0.445, 0.587] |
| LLM-qwen8b_D2 | all | aime | 0/382 | 0 | 0 | n/a | 0 | n/a |
| LLM-qwen8b_D2 | all | all | 419/1208 | 81 | 338 | 0.567 [0.520, 0.621] | 24 | 0.506 [0.445, 0.587] |
| LLM-qwen8b_D3_instruction->premise | planner | airline | 86/391 | 25 | 61 | 0.529 [0.436, 0.626] | 10 | 0.533 [0.410, 0.676] |
| LLM-qwen8b_D3_instruction->premise | planner | aime | 0/123 | 0 | 0 | n/a | 0 | n/a |
| LLM-qwen8b_D3_instruction->premise | planner | all | 86/514 | 25 | 61 | 0.529 [0.436, 0.626] | 10 | 0.533 [0.410, 0.676] |
| LLM-qwen8b_D3_report->planner | planner | airline | 40/391 | 17 | 23 | 0.448 [0.286, 0.639] | 7 | 0.475 [0.261, 0.693] |
| LLM-qwen8b_D3_report->planner | planner | aime | 0/123 | 0 | 0 | n/a | 0 | n/a |
| LLM-qwen8b_D3_report->planner | planner | all | 40/514 | 17 | 23 | 0.448 [0.286, 0.639] | 7 | 0.475 [0.261, 0.693] |
| Judge_p_fail | planner | airline | 388/391 | 46 | 148 | 0.610 [0.521, 0.698] | 16 | 0.686 [0.567, 0.800] |
| Judge_p_fail | planner | aime | 0/123 | 0 | 0 | n/a | 0 | n/a |
| Judge_p_fail | planner | all | 388/514 | 46 | 148 | 0.610 [0.521, 0.698] | 16 | 0.686 [0.567, 0.800] |
| Judge_p_fail | subagent | airline | 431/435 | 48 | 188 | 0.607 [0.529, 0.680] | 8 | 0.707 [0.605, 0.816] |
| Judge_p_fail | subagent | aime | 0/259 | 0 | 0 | n/a | 0 | n/a |
| Judge_p_fail | subagent | all | 431/694 | 48 | 188 | 0.607 [0.529, 0.680] | 8 | 0.707 [0.605, 0.816] |
| Judge_p_fail | all | airline | 819/826 | 94 | 336 | 0.602 [0.538, 0.665] | 24 | 0.662 [0.577, 0.739] |
| Judge_p_fail | all | aime | 0/382 | 0 | 0 | n/a | 0 | n/a |
| Judge_p_fail | all | all | 819/1208 | 94 | 336 | 0.602 [0.538, 0.665] | 24 | 0.662 [0.577, 0.739] |
| Judge_flag | planner | airline | 388/391 | 46 | 148 | 0.567 [0.491, 0.642] | 16 | 0.601 [0.475, 0.736] |
| Judge_flag | planner | aime | 0/123 | 0 | 0 | n/a | 0 | n/a |
| Judge_flag | planner | all | 388/514 | 46 | 148 | 0.567 [0.491, 0.642] | 16 | 0.601 [0.475, 0.736] |
| Judge_flag | subagent | airline | 431/435 | 48 | 188 | 0.602 [0.529, 0.675] | 8 | 0.644 [0.492, 0.779] |
| Judge_flag | subagent | aime | 0/259 | 0 | 0 | n/a | 0 | n/a |
| Judge_flag | subagent | all | 431/694 | 48 | 188 | 0.602 [0.529, 0.675] | 8 | 0.644 [0.492, 0.779] |
| Judge_flag | all | airline | 819/826 | 94 | 336 | 0.579 [0.520, 0.635] | 24 | 0.589 [0.488, 0.695] |
| Judge_flag | all | aime | 0/382 | 0 | 0 | n/a | 0 | n/a |
| Judge_flag | all | all | 819/1208 | 94 | 336 | 0.579 [0.520, 0.635] | 24 | 0.589 [0.488, 0.695] |

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
| D3 | planner | airline | 33 | 67 | 8 | 3 | 0.727 | 0.242 | 0.364 | 0.045 | 6/13 |
| D3 | planner | aime | 3 | 42 | 0 | 0 | n/a | 0.000 | n/a | 0.000 | n/a |
| D3 | planner | all | 36 | 109 | 8 | 3 | 0.727 | 0.222 | 0.340 | 0.028 | 6/13 |
| LLM_D2 | planner | airline | 44 | 148 | 3 | 10 | 0.231 | 0.068 | 0.105 | 0.068 | 0/16 |
| LLM_D2 | planner | all | 44 | 148 | 3 | 10 | 0.231 | 0.068 | 0.105 | 0.068 | 0/16 |
| LLM_D2 | subagent | airline | 37 | 190 | 17 | 26 | 0.395 | 0.459 | 0.425 | 0.137 | 3/8 |
| LLM_D2 | subagent | all | 37 | 190 | 17 | 26 | 0.395 | 0.459 | 0.425 | 0.137 | 3/8 |
| LLM_D2 | all | airline | 81 | 338 | 20 | 36 | 0.357 | 0.247 | 0.292 | 0.107 | 3/24 |
| LLM_D2 | all | all | 81 | 338 | 20 | 36 | 0.357 | 0.247 | 0.292 | 0.107 | 3/24 |
| LLM-gptoss20b_D2 | planner | airline | 44 | 148 | 23 | 43 | 0.348 | 0.523 | 0.418 | 0.291 | 8/16 |
| LLM-gptoss20b_D2 | planner | all | 44 | 148 | 23 | 43 | 0.348 | 0.523 | 0.418 | 0.291 | 8/16 |
| LLM-gptoss20b_D2 | subagent | airline | 37 | 190 | 17 | 22 | 0.436 | 0.459 | 0.447 | 0.116 | 3/8 |
| LLM-gptoss20b_D2 | subagent | all | 37 | 190 | 17 | 22 | 0.436 | 0.459 | 0.447 | 0.116 | 3/8 |
| LLM-gptoss20b_D2 | all | airline | 81 | 338 | 40 | 65 | 0.381 | 0.494 | 0.430 | 0.192 | 11/24 |
| LLM-gptoss20b_D2 | all | all | 81 | 338 | 40 | 65 | 0.381 | 0.494 | 0.430 | 0.192 | 11/24 |
| LLM-qwen8b_D2 | planner | airline | 44 | 148 | 5 | 9 | 0.357 | 0.114 | 0.172 | 0.061 | 1/16 |
| LLM-qwen8b_D2 | planner | all | 44 | 148 | 5 | 9 | 0.357 | 0.114 | 0.172 | 0.061 | 1/16 |
| LLM-qwen8b_D2 | subagent | airline | 37 | 190 | 15 | 29 | 0.341 | 0.405 | 0.370 | 0.153 | 2/8 |
| LLM-qwen8b_D2 | subagent | all | 37 | 190 | 15 | 29 | 0.341 | 0.405 | 0.370 | 0.153 | 2/8 |
| LLM-qwen8b_D2 | all | airline | 81 | 338 | 20 | 38 | 0.345 | 0.247 | 0.288 | 0.112 | 3/24 |
| LLM-qwen8b_D2 | all | all | 81 | 338 | 20 | 38 | 0.345 | 0.247 | 0.288 | 0.112 | 3/24 |
| Judge_flag | planner | airline | 46 | 148 | 17 | 35 | 0.327 | 0.370 | 0.347 | 0.236 | 7/16 |
| Judge_flag | planner | all | 46 | 148 | 17 | 35 | 0.327 | 0.370 | 0.347 | 0.236 | 7/16 |
| Judge_flag | subagent | airline | 48 | 188 | 32 | 87 | 0.269 | 0.667 | 0.383 | 0.463 | 6/8 |
| Judge_flag | subagent | all | 48 | 188 | 32 | 87 | 0.269 | 0.667 | 0.383 | 0.463 | 6/8 |
| Judge_flag | all | airline | 94 | 336 | 49 | 122 | 0.287 | 0.521 | 0.370 | 0.363 | 13/24 |
| Judge_flag | all | all | 94 | 336 | 49 | 122 | 0.287 | 0.521 | 0.370 | 0.363 | 13/24 |

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
| LLM_D1_1-conf | planner | airline | 8 | 2 | 6 | not computable (success=6, failure=2) | not computable (success=6, failure=2) |
| LLM_D1_1-conf | planner | all | 8 | 2 | 6 | not computable (success=6, failure=2) | not computable (success=6, failure=2) |
| LLM_D1_1-conf | subagent | airline | 10 | 4 | 6 | 0.500 [0.000, 0.958] | 0.208 [0.000, 0.542] |
| LLM_D1_1-conf | subagent | all | 10 | 4 | 6 | 0.500 [0.000, 0.958] | 0.208 [0.000, 0.542] |
| LLM_D1_1-conf | all | airline | 9 | 3 | 6 | 0.611 [0.000, 1.000] | 0.389 [0.000, 0.833] |
| LLM_D1_1-conf | all | all | 9 | 3 | 6 | 0.611 [0.000, 1.000] | 0.389 [0.000, 0.833] |
| LLM_D1_1-p_actual | planner | airline | 8 | 2 | 6 | not computable (success=6, failure=2) | not computable (success=6, failure=2) |
| LLM_D1_1-p_actual | planner | all | 8 | 2 | 6 | not computable (success=6, failure=2) | not computable (success=6, failure=2) |
| LLM_D1_1-p_actual | subagent | airline | 10 | 4 | 6 | 0.583 [0.500, 0.750] | 0.208 [0.000, 0.625] |
| LLM_D1_1-p_actual | subagent | all | 10 | 4 | 6 | 0.583 [0.500, 0.750] | 0.208 [0.000, 0.625] |
| LLM_D1_1-p_actual | all | airline | 9 | 3 | 6 | 0.500 [0.500, 0.500] | 0.778 [0.443, 1.000] |
| LLM_D1_1-p_actual | all | all | 9 | 3 | 6 | 0.500 [0.500, 0.500] | 0.778 [0.443, 1.000] |
| LLM_D2 | planner | airline | 8 | 2 | 6 | not computable (success=6, failure=2) | not computable (success=6, failure=2) |
| LLM_D2 | planner | all | 8 | 2 | 6 | not computable (success=6, failure=2) | not computable (success=6, failure=2) |
| LLM_D2 | subagent | airline | 10 | 4 | 6 | 0.667 [0.500, 0.833] | 0.750 [0.333, 1.000] |
| LLM_D2 | subagent | all | 10 | 4 | 6 | 0.667 [0.500, 0.833] | 0.750 [0.333, 1.000] |
| LLM_D2 | all | airline | 9 | 3 | 6 | 0.583 [0.500, 0.750] | 0.722 [0.333, 1.000] |
| LLM_D2 | all | all | 9 | 3 | 6 | 0.583 [0.500, 0.750] | 0.722 [0.333, 1.000] |
| LLM-gptoss20b_D1_1-conf | planner | airline | 8 | 2 | 6 | not computable (success=6, failure=2) | not computable (success=6, failure=2) |
| LLM-gptoss20b_D1_1-conf | planner | all | 8 | 2 | 6 | not computable (success=6, failure=2) | not computable (success=6, failure=2) |
| LLM-gptoss20b_D1_1-conf | subagent | airline | 9 | 3 | 6 | 0.500 [0.111, 0.833] | 0.333 [0.000, 0.722] |
| LLM-gptoss20b_D1_1-conf | subagent | all | 9 | 3 | 6 | 0.500 [0.111, 0.833] | 0.333 [0.000, 0.722] |
| LLM-gptoss20b_D1_1-conf | all | airline | 8 | 2 | 6 | not computable (success=6, failure=2) | not computable (success=6, failure=2) |
| LLM-gptoss20b_D1_1-conf | all | all | 8 | 2 | 6 | not computable (success=6, failure=2) | not computable (success=6, failure=2) |
| LLM-gptoss20b_D1_1-p_actual | planner | airline | 8 | 2 | 6 | not computable (success=6, failure=2) | not computable (success=6, failure=2) |
| LLM-gptoss20b_D1_1-p_actual | planner | all | 8 | 2 | 6 | not computable (success=6, failure=2) | not computable (success=6, failure=2) |
| LLM-gptoss20b_D1_1-p_actual | subagent | airline | 9 | 3 | 6 | 0.250 [0.000, 0.583] | 0.500 [0.000, 1.000] |
| LLM-gptoss20b_D1_1-p_actual | subagent | all | 9 | 3 | 6 | 0.250 [0.000, 0.583] | 0.500 [0.000, 1.000] |
| LLM-gptoss20b_D1_1-p_actual | all | airline | 8 | 2 | 6 | not computable (success=6, failure=2) | not computable (success=6, failure=2) |
| LLM-gptoss20b_D1_1-p_actual | all | all | 8 | 2 | 6 | not computable (success=6, failure=2) | not computable (success=6, failure=2) |
| LLM-gptoss20b_D2 | planner | airline | 8 | 2 | 6 | not computable (success=6, failure=2) | not computable (success=6, failure=2) |
| LLM-gptoss20b_D2 | planner | all | 8 | 2 | 6 | not computable (success=6, failure=2) | not computable (success=6, failure=2) |
| LLM-gptoss20b_D2 | subagent | airline | 10 | 4 | 6 | 0.458 [0.208, 0.708] | 0.646 [0.249, 1.000] |
| LLM-gptoss20b_D2 | subagent | all | 10 | 4 | 6 | 0.458 [0.208, 0.708] | 0.646 [0.249, 1.000] |
| LLM-gptoss20b_D2 | all | airline | 9 | 3 | 6 | 0.500 [0.500, 0.500] | 0.333 [0.000, 0.722] |
| LLM-gptoss20b_D2 | all | all | 9 | 3 | 6 | 0.500 [0.500, 0.500] | 0.333 [0.000, 0.722] |
| LLM-qwen8b_D1_1-conf | planner | airline | 7 | 2 | 5 | not computable (success=5, failure=2) | not computable (success=5, failure=2) |
| LLM-qwen8b_D1_1-conf | planner | all | 7 | 2 | 5 | not computable (success=5, failure=2) | not computable (success=5, failure=2) |
| LLM-qwen8b_D1_1-conf | subagent | airline | 5 | 3 | 2 | not computable (success=2, failure=3) | not computable (success=2, failure=3) |
| LLM-qwen8b_D1_1-conf | subagent | all | 5 | 3 | 2 | not computable (success=2, failure=3) | not computable (success=2, failure=3) |
| LLM-qwen8b_D1_1-conf | all | airline | 6 | 2 | 4 | not computable (success=4, failure=2) | not computable (success=4, failure=2) |
| LLM-qwen8b_D1_1-conf | all | all | 6 | 2 | 4 | not computable (success=4, failure=2) | not computable (success=4, failure=2) |
| LLM-qwen8b_D1_1-p_actual | planner | airline | 7 | 2 | 5 | not computable (success=5, failure=2) | not computable (success=5, failure=2) |
| LLM-qwen8b_D1_1-p_actual | planner | all | 7 | 2 | 5 | not computable (success=5, failure=2) | not computable (success=5, failure=2) |
| LLM-qwen8b_D1_1-p_actual | subagent | airline | 5 | 3 | 2 | not computable (success=2, failure=3) | not computable (success=2, failure=3) |
| LLM-qwen8b_D1_1-p_actual | subagent | all | 5 | 3 | 2 | not computable (success=2, failure=3) | not computable (success=2, failure=3) |
| LLM-qwen8b_D1_1-p_actual | all | airline | 6 | 2 | 4 | not computable (success=4, failure=2) | not computable (success=4, failure=2) |
| LLM-qwen8b_D1_1-p_actual | all | all | 6 | 2 | 4 | not computable (success=4, failure=2) | not computable (success=4, failure=2) |
| LLM-qwen8b_D2 | planner | airline | 8 | 2 | 6 | not computable (success=6, failure=2) | not computable (success=6, failure=2) |
| LLM-qwen8b_D2 | planner | all | 8 | 2 | 6 | not computable (success=6, failure=2) | not computable (success=6, failure=2) |
| LLM-qwen8b_D2 | subagent | airline | 10 | 4 | 6 | 0.500 [0.500, 0.500] | 0.771 [0.438, 1.000] |
| LLM-qwen8b_D2 | subagent | all | 10 | 4 | 6 | 0.500 [0.500, 0.500] | 0.771 [0.438, 1.000] |
| LLM-qwen8b_D2 | all | airline | 9 | 3 | 6 | 0.500 [0.500, 0.500] | 1.000 [1.000, 1.000] |
| LLM-qwen8b_D2 | all | all | 9 | 3 | 6 | 0.500 [0.500, 0.500] | 1.000 [1.000, 1.000] |
| Judge_p_fail | planner | airline | 31 | 25 | 6 | 0.480 [0.280, 0.687] | 0.533 [0.300, 0.760] |
| Judge_p_fail | planner | all | 31 | 25 | 6 | 0.480 [0.280, 0.687] | 0.533 [0.300, 0.760] |
| Judge_p_fail | subagent | airline | 30 | 24 | 6 | 0.604 [0.364, 0.833] | 0.743 [0.493, 0.931] |
| Judge_p_fail | subagent | all | 30 | 24 | 6 | 0.604 [0.364, 0.833] | 0.743 [0.493, 0.931] |
| Judge_p_fail | all | airline | 31 | 25 | 6 | 0.553 [0.370, 0.720] | 0.780 [0.487, 0.993] |
| Judge_p_fail | all | all | 31 | 25 | 6 | 0.553 [0.370, 0.720] | 0.780 [0.487, 0.993] |
| Judge_flag | planner | airline | 31 | 25 | 6 | 0.500 [0.500, 0.500] | 0.553 [0.307, 0.787] |
| Judge_flag | planner | all | 31 | 25 | 6 | 0.500 [0.500, 0.500] | 0.553 [0.307, 0.787] |
| Judge_flag | subagent | airline | 30 | 24 | 6 | 0.542 [0.417, 0.729] | 0.747 [0.514, 0.924] |
| Judge_flag | subagent | all | 30 | 24 | 6 | 0.542 [0.417, 0.729] | 0.747 [0.514, 0.924] |
| Judge_flag | all | airline | 31 | 25 | 6 | 0.500 [0.500, 0.500] | 0.790 [0.477, 1.000] |
| Judge_flag | all | all | 31 | 25 | 6 | 0.500 [0.500, 0.500] | 0.790 [0.477, 1.000] |

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
| D3 | planner | airline | 24 | 0.333 | 0.333 | 0.667 |
| D3 | planner | aime | 22 | 0.000 | 0.545 | 0.045 |
| D3 | planner | all | 46 | 0.174 | 0.435 | 0.370 |
| D3fid_instruction->premise | planner | airline | 21 | 0.286 | 0.333 | 0.619 |
| D3fid_instruction->premise | planner | aime | 21 | 0.000 | 0.381 | 0.048 |
| D3fid_instruction->premise | planner | all | 42 | 0.143 | 0.357 | 0.333 |
| D3fid_report->planner | planner | airline | 23 | 0.174 | 0.217 | 0.652 |
| D3fid_report->planner | planner | aime | 22 | 0.000 | 0.455 | 0.045 |
| D3fid_report->planner | planner | all | 45 | 0.089 | 0.333 | 0.356 |
| LLM_D1_1-conf | planner | airline | 24 | 0.333 | 0.500 | 0.667 |
| LLM_D1_1-conf | planner | all | 24 | 0.333 | 0.500 | 0.667 |
| LLM_D1_1-conf | subagent | airline | 17 | 0.118 | 0.294 | 0.412 |
| LLM_D1_1-conf | subagent | all | 17 | 0.118 | 0.294 | 0.412 |
| LLM_D1_1-conf | all | airline | 24 | 0.417 | 0.583 | 0.708 |
| LLM_D1_1-conf | all | all | 24 | 0.417 | 0.583 | 0.708 |
| LLM_D1_1-p_actual | planner | airline | 24 | 0.375 | 0.417 | 0.667 |
| LLM_D1_1-p_actual | planner | all | 24 | 0.375 | 0.417 | 0.667 |
| LLM_D1_1-p_actual | subagent | airline | 17 | 0.118 | 0.235 | 0.412 |
| LLM_D1_1-p_actual | subagent | all | 17 | 0.118 | 0.235 | 0.412 |
| LLM_D1_1-p_actual | all | airline | 24 | 0.375 | 0.458 | 0.667 |
| LLM_D1_1-p_actual | all | all | 24 | 0.375 | 0.458 | 0.667 |
| LLM_D2 | planner | airline | 24 | 0.125 | 0.292 | 0.667 |
| LLM_D2 | planner | all | 24 | 0.125 | 0.292 | 0.667 |
| LLM_D2 | subagent | airline | 17 | 0.059 | 0.176 | 0.353 |
| LLM_D2 | subagent | all | 17 | 0.059 | 0.176 | 0.353 |
| LLM_D2 | all | airline | 24 | 0.167 | 0.375 | 0.667 |
| LLM_D2 | all | all | 24 | 0.167 | 0.375 | 0.667 |
| LLM_D3_instruction->premise | planner | airline | 24 | 0.292 | 0.292 | 0.667 |
| LLM_D3_instruction->premise | planner | all | 24 | 0.292 | 0.292 | 0.667 |
| LLM_D3_report->planner | planner | airline | 24 | 0.375 | 0.417 | 0.667 |
| LLM_D3_report->planner | planner | all | 24 | 0.375 | 0.417 | 0.667 |
| LLM-gptoss20b_D1_1-conf | planner | airline | 24 | 0.417 | 0.542 | 0.667 |
| LLM-gptoss20b_D1_1-conf | planner | all | 24 | 0.417 | 0.542 | 0.667 |
| LLM-gptoss20b_D1_1-conf | subagent | airline | 17 | 0.059 | 0.176 | 0.294 |
| LLM-gptoss20b_D1_1-conf | subagent | all | 17 | 0.059 | 0.176 | 0.294 |
| LLM-gptoss20b_D1_1-conf | all | airline | 24 | 0.417 | 0.542 | 0.750 |
| LLM-gptoss20b_D1_1-conf | all | all | 24 | 0.417 | 0.542 | 0.750 |
| LLM-gptoss20b_D1_1-p_actual | planner | airline | 24 | 0.333 | 0.333 | 0.667 |
| LLM-gptoss20b_D1_1-p_actual | planner | all | 24 | 0.333 | 0.333 | 0.667 |
| LLM-gptoss20b_D1_1-p_actual | subagent | airline | 17 | 0.118 | 0.176 | 0.353 |
| LLM-gptoss20b_D1_1-p_actual | subagent | all | 17 | 0.118 | 0.176 | 0.353 |
| LLM-gptoss20b_D1_1-p_actual | all | airline | 24 | 0.375 | 0.417 | 0.750 |
| LLM-gptoss20b_D1_1-p_actual | all | all | 24 | 0.375 | 0.417 | 0.750 |
| LLM-gptoss20b_D2 | planner | airline | 24 | 0.292 | 0.417 | 0.667 |
| LLM-gptoss20b_D2 | planner | all | 24 | 0.292 | 0.417 | 0.667 |
| LLM-gptoss20b_D2 | subagent | airline | 17 | 0.000 | 0.118 | 0.353 |
| LLM-gptoss20b_D2 | subagent | all | 17 | 0.000 | 0.118 | 0.353 |
| LLM-gptoss20b_D2 | all | airline | 24 | 0.292 | 0.417 | 0.625 |
| LLM-gptoss20b_D2 | all | all | 24 | 0.292 | 0.417 | 0.625 |
| LLM-gptoss20b_D3_instruction->premise | planner | airline | 24 | 0.375 | 0.375 | 0.667 |
| LLM-gptoss20b_D3_instruction->premise | planner | all | 24 | 0.375 | 0.375 | 0.667 |
| LLM-gptoss20b_D3_report->planner | planner | airline | 24 | 0.333 | 0.333 | 0.667 |
| LLM-gptoss20b_D3_report->planner | planner | all | 24 | 0.333 | 0.333 | 0.667 |
| LLM-qwen8b_D1_1-conf | planner | airline | 24 | 0.208 | 0.375 | 0.667 |
| LLM-qwen8b_D1_1-conf | planner | all | 24 | 0.208 | 0.375 | 0.667 |
| LLM-qwen8b_D1_1-conf | subagent | airline | 17 | 0.059 | 0.176 | 0.412 |
| LLM-qwen8b_D1_1-conf | subagent | all | 17 | 0.059 | 0.176 | 0.412 |
| LLM-qwen8b_D1_1-conf | all | airline | 24 | 0.208 | 0.417 | 0.667 |
| LLM-qwen8b_D1_1-conf | all | all | 24 | 0.208 | 0.417 | 0.667 |
| LLM-qwen8b_D1_1-p_actual | planner | airline | 24 | 0.250 | 0.292 | 0.667 |
| LLM-qwen8b_D1_1-p_actual | planner | all | 24 | 0.250 | 0.292 | 0.667 |
| LLM-qwen8b_D1_1-p_actual | subagent | airline | 17 | 0.118 | 0.118 | 0.412 |
| LLM-qwen8b_D1_1-p_actual | subagent | all | 17 | 0.118 | 0.118 | 0.412 |
| LLM-qwen8b_D1_1-p_actual | all | airline | 24 | 0.250 | 0.292 | 0.667 |
| LLM-qwen8b_D1_1-p_actual | all | all | 24 | 0.250 | 0.292 | 0.667 |
| LLM-qwen8b_D2 | planner | airline | 24 | 0.167 | 0.333 | 0.667 |
| LLM-qwen8b_D2 | planner | all | 24 | 0.167 | 0.333 | 0.667 |
| LLM-qwen8b_D2 | subagent | airline | 17 | 0.000 | 0.059 | 0.353 |
| LLM-qwen8b_D2 | subagent | all | 17 | 0.000 | 0.059 | 0.353 |
| LLM-qwen8b_D2 | all | airline | 24 | 0.167 | 0.333 | 0.750 |
| LLM-qwen8b_D2 | all | all | 24 | 0.167 | 0.333 | 0.750 |
| LLM-qwen8b_D3_instruction->premise | planner | airline | 22 | 0.227 | 0.227 | 0.636 |
| LLM-qwen8b_D3_instruction->premise | planner | all | 22 | 0.227 | 0.227 | 0.636 |
| LLM-qwen8b_D3_report->planner | planner | airline | 18 | 0.333 | 0.333 | 0.667 |
| LLM-qwen8b_D3_report->planner | planner | all | 18 | 0.333 | 0.333 | 0.667 |
| Judge_p_fail | planner | airline | 24 | 0.167 | 0.167 | 0.667 |
| Judge_p_fail | planner | all | 24 | 0.167 | 0.167 | 0.667 |
| Judge_p_fail | subagent | airline | 24 | 0.000 | 0.125 | 0.208 |
| Judge_p_fail | subagent | all | 24 | 0.000 | 0.125 | 0.208 |
| Judge_p_fail | all | airline | 24 | 0.125 | 0.125 | 0.583 |
| Judge_p_fail | all | all | 24 | 0.125 | 0.125 | 0.583 |
| Judge_flag | planner | airline | 24 | 0.250 | 0.250 | 0.667 |
| Judge_flag | planner | all | 24 | 0.250 | 0.250 | 0.667 |
| Judge_flag | subagent | airline | 24 | 0.000 | 0.250 | 0.208 |
| Judge_flag | subagent | all | 24 | 0.000 | 0.250 | 0.208 |
| Judge_flag | all | airline | 24 | 0.250 | 0.250 | 0.667 |
| Judge_flag | all | all | 24 | 0.250 | 0.250 | 0.667 |

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
| D3 | planner | airline | 1 | 0.045 | 0.242 | 33 | 9/24 | 0.0 |
| D3 | planner | aime | 1e-09 | 0.000 | 0.000 | 3 | 0/23 | n/a |
| D3 | planner | all | 1 | 0.028 | 0.222 | 36 | 9/47 | 0.0 |
| D3fid_instruction->premise | planner | airline | 0.8 | 0.091 | 0.190 | 21 | 1/24 | 0.0 |
| D3fid_instruction->premise | planner | aime | 0.8889 | 0.077 | 0.000 | 3 | 2/23 | 4.5 |
| D3fid_instruction->premise | planner | all | 0.8667 | 0.072 | 0.083 | 24 | 3/47 | 3.0 |
| D3fid_report->planner | planner | airline | 1 | 0.000 | 0.000 | 31 | 0/24 | n/a |
| D3fid_report->planner | planner | aime | 1 | 0.000 | 0.000 | 3 | 0/23 | n/a |
| D3fid_report->planner | planner | all | 1 | 0.000 | 0.000 | 34 | 0/47 | n/a |
| LLM_D1_1-conf | planner | airline | 0.4475 | 0.089 | 0.182 | 44 | 4/24 | 0.0 |
| LLM_D1_1-conf | planner | all | 0.4475 | 0.089 | 0.182 | 44 | 4/47 | 0.0 |
| LLM_D1_1-conf | subagent | airline | 0.461 | 0.097 | 0.111 | 36 | 1/24 | 0.0 |
| LLM_D1_1-conf | subagent | all | 0.461 | 0.097 | 0.111 | 36 | 1/46 | 0.0 |
| LLM_D1_1-conf | all | airline | 0.4288 | 0.099 | 0.163 | 80 | 5/24 | 0.0 |
| LLM_D1_1-conf | all | all | 0.4288 | 0.099 | 0.163 | 80 | 5/47 | 0.0 |
| LLM_D1_1-p_actual | planner | airline | 1 | 0.000 | 0.000 | 44 | 0/24 | n/a |
| LLM_D1_1-p_actual | planner | all | 1 | 0.000 | 0.000 | 44 | 0/47 | n/a |
| LLM_D1_1-p_actual | subagent | airline | 1 | 0.000 | 0.000 | 36 | 0/24 | n/a |
| LLM_D1_1-p_actual | subagent | all | 1 | 0.000 | 0.000 | 36 | 0/46 | n/a |
| LLM_D1_1-p_actual | all | airline | 1 | 0.000 | 0.000 | 80 | 0/24 | n/a |
| LLM_D1_1-p_actual | all | all | 1 | 0.000 | 0.000 | 80 | 0/47 | n/a |
| LLM_D2 | planner | airline | 1 | 0.068 | 0.068 | 44 | 0/24 | n/a |
| LLM_D2 | planner | all | 1 | 0.068 | 0.068 | 44 | 0/47 | n/a |
| LLM_D2 | subagent | airline | 1 | 0.000 | 0.000 | 37 | 0/24 | n/a |
| LLM_D2 | subagent | all | 1 | 0.000 | 0.000 | 37 | 0/46 | n/a |
| LLM_D2 | all | airline | 1 | 0.000 | 0.000 | 81 | 0/24 | n/a |
| LLM_D2 | all | all | 1 | 0.000 | 0.000 | 81 | 0/47 | n/a |
| LLM_D3_instruction->premise | planner | airline | 0.143 | 0.090 | 0.226 | 31 | 2/24 | 0.0 |
| LLM_D3_instruction->premise | planner | all | 0.143 | 0.090 | 0.226 | 31 | 2/47 | 0.0 |
| LLM_D3_report->planner | planner | airline | 1 | 0.000 | 0.000 | 29 | 0/24 | n/a |
| LLM_D3_report->planner | planner | all | 1 | 0.000 | 0.000 | 29 | 0/47 | n/a |
| LLM-gptoss20b_D1_1-conf | planner | airline | 0.562 | 0.095 | 0.114 | 44 | 2/24 | 0.0 |
| LLM-gptoss20b_D1_1-conf | planner | all | 0.562 | 0.095 | 0.114 | 44 | 2/47 | 0.0 |
| LLM-gptoss20b_D1_1-conf | subagent | airline | 0.5002 | 0.097 | 0.114 | 35 | 1/24 | 0.0 |
| LLM-gptoss20b_D1_1-conf | subagent | all | 0.5002 | 0.097 | 0.114 | 35 | 1/46 | 0.0 |
| LLM-gptoss20b_D1_1-conf | all | airline | 0.5185 | 0.093 | 0.114 | 79 | 4/24 | 0.0 |
| LLM-gptoss20b_D1_1-conf | all | all | 0.5185 | 0.093 | 0.114 | 79 | 4/47 | 0.0 |
| LLM-gptoss20b_D1_1-p_actual | planner | airline | 0.9802 | 0.088 | 0.159 | 44 | 5/24 | 0.0 |
| LLM-gptoss20b_D1_1-p_actual | planner | all | 0.9802 | 0.088 | 0.159 | 44 | 5/47 | 0.0 |
| LLM-gptoss20b_D1_1-p_actual | subagent | airline | 0.998 | 0.097 | 0.143 | 35 | 0/24 | n/a |
| LLM-gptoss20b_D1_1-p_actual | subagent | all | 0.998 | 0.097 | 0.143 | 35 | 0/46 | n/a |
| LLM-gptoss20b_D1_1-p_actual | all | airline | 0.99 | 0.099 | 0.114 | 79 | 2/24 | 0.0 |
| LLM-gptoss20b_D1_1-p_actual | all | all | 0.99 | 0.099 | 0.114 | 79 | 2/47 | 0.0 |
| LLM-gptoss20b_D2 | planner | airline | 1 | 0.000 | 0.000 | 44 | 0/24 | n/a |
| LLM-gptoss20b_D2 | planner | all | 1 | 0.000 | 0.000 | 44 | 0/47 | n/a |
| LLM-gptoss20b_D2 | subagent | airline | 1 | 0.000 | 0.000 | 37 | 0/24 | n/a |
| LLM-gptoss20b_D2 | subagent | all | 1 | 0.000 | 0.000 | 37 | 0/46 | n/a |
| LLM-gptoss20b_D2 | all | airline | 1 | 0.000 | 0.000 | 81 | 0/24 | n/a |
| LLM-gptoss20b_D2 | all | all | 1 | 0.000 | 0.000 | 81 | 0/47 | n/a |
| LLM-gptoss20b_D3_instruction->premise | planner | airline | 0.25 | 0.090 | 0.226 | 31 | 5/24 | 0.0 |
| LLM-gptoss20b_D3_instruction->premise | planner | all | 0.25 | 0.090 | 0.226 | 31 | 5/47 | 0.0 |
| LLM-gptoss20b_D3_report->planner | planner | airline | 1 | 0.000 | 0.000 | 30 | 0/24 | n/a |
| LLM-gptoss20b_D3_report->planner | planner | all | 1 | 0.000 | 0.000 | 30 | 0/47 | n/a |
| LLM-qwen8b_D1_1-conf | planner | airline | 0.4053 | 0.094 | 0.073 | 41 | 2/24 | 0.0 |
| LLM-qwen8b_D1_1-conf | planner | all | 0.4053 | 0.094 | 0.073 | 41 | 2/47 | 0.0 |
| LLM-qwen8b_D1_1-conf | subagent | airline | 0.226 | 0.081 | 0.185 | 27 | 1/24 | 0.0 |
| LLM-qwen8b_D1_1-conf | subagent | all | 0.226 | 0.081 | 0.185 | 27 | 1/46 | 0.0 |
| LLM-qwen8b_D1_1-conf | all | airline | 0.3409 | 0.097 | 0.118 | 68 | 3/24 | 0.0 |
| LLM-qwen8b_D1_1-conf | all | all | 0.3409 | 0.097 | 0.118 | 68 | 3/47 | 0.0 |
| LLM-qwen8b_D1_1-p_actual | planner | airline | 1 | 0.000 | 0.000 | 41 | 0/24 | n/a |
| LLM-qwen8b_D1_1-p_actual | planner | all | 1 | 0.000 | 0.000 | 41 | 0/47 | n/a |
| LLM-qwen8b_D1_1-p_actual | subagent | airline | 1 | 0.000 | 0.000 | 27 | 0/24 | n/a |
| LLM-qwen8b_D1_1-p_actual | subagent | all | 1 | 0.000 | 0.000 | 27 | 0/46 | n/a |
| LLM-qwen8b_D1_1-p_actual | all | airline | 1 | 0.000 | 0.000 | 68 | 0/24 | n/a |
| LLM-qwen8b_D1_1-p_actual | all | all | 1 | 0.000 | 0.000 | 68 | 0/47 | n/a |
| LLM-qwen8b_D2 | planner | airline | 1 | 0.061 | 0.114 | 44 | 1/24 | 0.0 |
| LLM-qwen8b_D2 | planner | all | 1 | 0.061 | 0.114 | 44 | 1/47 | 0.0 |
| LLM-qwen8b_D2 | subagent | airline | 1 | 0.000 | 0.000 | 37 | 0/24 | n/a |
| LLM-qwen8b_D2 | subagent | all | 1 | 0.000 | 0.000 | 37 | 0/46 | n/a |
| LLM-qwen8b_D2 | all | airline | 1 | 0.000 | 0.000 | 81 | 0/24 | n/a |
| LLM-qwen8b_D2 | all | all | 1 | 0.000 | 0.000 | 81 | 0/47 | n/a |
| LLM-qwen8b_D3_instruction->premise | planner | airline | 0.25 | 0.098 | 0.160 | 25 | 2/24 | 0.0 |
| LLM-qwen8b_D3_instruction->premise | planner | all | 0.25 | 0.098 | 0.160 | 25 | 2/47 | 0.0 |
| LLM-qwen8b_D3_report->planner | planner | airline | 1 | 0.000 | 0.000 | 17 | 0/24 | n/a |
| LLM-qwen8b_D3_report->planner | planner | all | 1 | 0.000 | 0.000 | 17 | 0/47 | n/a |
| Judge_p_fail | planner | airline | 0.95 | 0.061 | 0.087 | 46 | 9/24 | 10.0 |
| Judge_p_fail | planner | all | 0.95 | 0.061 | 0.087 | 46 | 9/47 | 10.0 |
| Judge_p_fail | subagent | airline | 1 | 0.016 | 0.000 | 48 | 8/24 | 3.5 |
| Judge_p_fail | subagent | all | 1 | 0.016 | 0.000 | 48 | 8/46 | 3.5 |
| Judge_p_fail | all | airline | 1 | 0.012 | 0.000 | 94 | 8/24 | 3.5 |
| Judge_p_fail | all | all | 1 | 0.012 | 0.000 | 94 | 8/47 | 3.5 |
| Judge_flag | planner | airline | 1 | 0.000 | 0.000 | 46 | 0/24 | n/a |
| Judge_flag | planner | all | 1 | 0.000 | 0.000 | 46 | 0/47 | n/a |
| Judge_flag | subagent | airline | 1 | 0.000 | 0.000 | 48 | 0/24 | n/a |
| Judge_flag | subagent | all | 1 | 0.000 | 0.000 | 48 | 0/46 | n/a |
| Judge_flag | all | airline | 1 | 0.000 | 0.000 | 94 | 0/24 | n/a |
| Judge_flag | all | all | 1 | 0.000 | 0.000 | 94 | 0/47 | n/a |

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

Of the 172 labeled error steps (decisive + transient), **0.703** (121/172) are flagged by at least one item at its own 90th-percentile threshold (percentiles taken over that item's scores on all labeled non-aux steps).

Item thresholds: `D1_1-conf`=0.2793, `D1_1-margin`=0.4443, `D1_1-p_actual`=0.2344, `D1_handoff`=0.4819, `D2`=1.0000, `D3`=1.0000, `D3fid_instruction->premise`=0.7500, `D3fid_report->planner`=1.0000, `Judge_flag`=1.0000, `Judge_p_fail`=0.9500, `LLM-gptoss20b_D1_1-conf`=0.5156, `LLM-gptoss20b_D1_1-p_actual`=0.9900, `LLM-gptoss20b_D2`=1.0000, `LLM-gptoss20b_D3_instruction->premise`=0.3333, `LLM-gptoss20b_D3_report->planner`=1.0000, `LLM-qwen8b_D1_1-conf`=0.3258, `LLM-qwen8b_D1_1-p_actual`=1.0000, `LLM-qwen8b_D2`=1.0000, `LLM-qwen8b_D3_instruction->premise`=0.2500, `LLM-qwen8b_D3_report->planner`=1.0000, `LLM_D1_1-conf`=0.4523, `LLM_D1_1-p_actual`=1.0000, `LLM_D2`=1.0000, `LLM_D3_instruction->premise`=0.2000, `LLM_D3_report->planner`=0.9375.

