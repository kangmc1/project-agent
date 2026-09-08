# Item scores by label subtag

- generated: 2026-09-09 05:59:37 KST
- `mean` is over the labeled error steps of that subtag where the item has a score; `flagged` is the fraction of those steps at or above the item's 90th-percentile threshold (percentile taken over the item's scores on all labeled non-aux steps).

| subtag | n_steps | item | n_scored | mean | flagged@p90 | threshold |
|---|---|---|---|---|---|---|
| hallucination_like | 69 | D1_1-conf | 69 | 0.1218 | 0.159 | 0.2793 |
| hallucination_like | 69 | D1_1-p_actual | 69 | 0.1076 | 0.145 | 0.2344 |
| hallucination_like | 69 | D1_1-margin | 69 | 0.1763 | 0.145 | 0.4443 |
| hallucination_like | 69 | D1_handoff | 17 | 0.2517 | 0.176 | 0.4819 |
| hallucination_like | 69 | D2_unsupported | 50 | 0.1242 | 0.100 | 0.5667 |
| hallucination_like | 69 | D3_instruction | 16 | 0.3750 | 0.375 | 1.0000 |
| hallucination_like | 69 | D3_unsatisfied | 36 | 0.5000 | 0.500 | 1.0000 |
| hallucination_like | 69 | D7_instruction->premise | 1 | 0.8333 | 1.000 | 0.7500 |
| hallucination_like | 69 | D7_report->planner | 1 | 0.8000 | 0.000 | 1.0000 |
| hallucination_like | 69 | D9_1-consistency | 7 | 0.3474 | 0.143 | 0.9600 |
| handoff_induced | 93 | D1_1-conf | 93 | 0.0988 | 0.151 | 0.2793 |
| handoff_induced | 93 | D1_1-p_actual | 93 | 0.0678 | 0.129 | 0.2344 |
| handoff_induced | 93 | D1_1-margin | 93 | 0.1266 | 0.140 | 0.4443 |
| handoff_induced | 93 | D1_handoff | 82 | 0.1875 | 0.159 | 0.4819 |
| handoff_induced | 93 | D2_unsupported | 5 | 0.1600 | 0.200 | 0.5667 |
| handoff_induced | 93 | D3_instruction | 11 | 0.7273 | 0.727 | 1.0000 |
| handoff_induced | 93 | D3_unsatisfied | 4 | 0.2500 | 0.250 | 1.0000 |
| handoff_induced | 93 | D7_instruction->premise | 38 | 0.3052 | 0.132 | 0.7500 |
| handoff_induced | 93 | D7_report->planner | 62 | 0.6638 | 0.226 | 1.0000 |
| handoff_induced | 93 | D9_1-consistency | 1 | 0.0000 | 0.000 | 0.9600 |
| none | 180 | D1_1-conf | 180 | 0.0614 | 0.083 | 0.2793 |
| none | 180 | D1_1-p_actual | 180 | 0.0719 | 0.111 | 0.2344 |
| none | 180 | D1_1-margin | 180 | 0.0978 | 0.094 | 0.4443 |
| none | 180 | D1_handoff | 16 | 0.0247 | 0.000 | 0.4819 |
| none | 180 | D2_unsupported | 116 | 0.1232 | 0.103 | 0.5667 |
| none | 180 | D3_instruction | 14 | 0.7143 | 0.714 | 1.0000 |
| none | 180 | D3_unsatisfied | 125 | 0.1840 | 0.184 | 1.0000 |
| none | 180 | D7_instruction->premise | 5 | 0.1000 | 0.000 | 0.7500 |
| none | 180 | D7_report->planner | 4 | 0.4934 | 0.000 | 1.0000 |
| none | 180 | D9_1-consistency | 15 | 0.1667 | 0.067 | 0.9600 |
| reasoning_like | 92 | D1_1-conf | 92 | 0.0193 | 0.022 | 0.2793 |
| reasoning_like | 92 | D1_1-p_actual | 92 | 0.0106 | 0.011 | 0.2344 |
| reasoning_like | 92 | D1_1-margin | 92 | 0.0207 | 0.011 | 0.4443 |
| reasoning_like | 92 | D1_handoff | 10 | 0.0789 | 0.100 | 0.4819 |
| reasoning_like | 92 | D2_unsupported | 74 | 0.2412 | 0.162 | 0.5667 |
| reasoning_like | 92 | D3_instruction | 44 | 0.3864 | 0.386 | 1.0000 |
| reasoning_like | 92 | D3_unsatisfied | 78 | 0.6154 | 0.615 | 1.0000 |
| reasoning_like | 92 | D7_instruction->premise | 2 | 0.0000 | 0.000 | 0.7500 |
| reasoning_like | 92 | D7_report->planner | 2 | 0.9130 | 0.500 | 1.0000 |
| reasoning_like | 92 | D9_1-consistency | 24 | 0.3799 | 0.167 | 0.9600 |

