# Item scores by label subtag

- generated: 2026-09-09 06:41:15 KST
- `mean` is over the labeled error steps of that subtag where the item has a score; `flagged` is the fraction of those steps at or above the item's 90th-percentile threshold (percentile taken over the item's scores on all labeled non-aux steps).

| subtag | n_steps | item | n_scored | mean | flagged@p90 | threshold |
|---|---|---|---|---|---|---|
| hallucination_like | 69 | D1_1-conf | 69 | 0.1218 | 0.159 | 0.2793 |
| hallucination_like | 69 | D1_1-p_actual | 69 | 0.1076 | 0.145 | 0.2344 |
| hallucination_like | 69 | D1_1-margin | 69 | 0.1763 | 0.145 | 0.4443 |
| hallucination_like | 69 | D1_handoff | 17 | 0.2517 | 0.176 | 0.4819 |
| hallucination_like | 69 | D3 | 69 | 0.5072 | 0.507 | 1.0000 |
| hallucination_like | 69 | D7_instruction->premise | 1 | 0.8333 | 1.000 | 0.7500 |
| hallucination_like | 69 | D7_report->planner | 1 | 0.8000 | 0.000 | 1.0000 |
| handoff_induced | 93 | D1_1-conf | 93 | 0.0988 | 0.151 | 0.2793 |
| handoff_induced | 93 | D1_1-p_actual | 93 | 0.0678 | 0.129 | 0.2344 |
| handoff_induced | 93 | D1_1-margin | 93 | 0.1266 | 0.140 | 0.4443 |
| handoff_induced | 93 | D1_handoff | 82 | 0.1875 | 0.159 | 0.4819 |
| handoff_induced | 93 | D3 | 93 | 0.1290 | 0.129 | 1.0000 |
| handoff_induced | 93 | D7_instruction->premise | 38 | 0.3052 | 0.132 | 0.7500 |
| handoff_induced | 93 | D7_report->planner | 62 | 0.6638 | 0.226 | 1.0000 |
| none | 180 | D1_1-conf | 180 | 0.0614 | 0.083 | 0.2793 |
| none | 180 | D1_1-p_actual | 180 | 0.0719 | 0.111 | 0.2344 |
| none | 180 | D1_1-margin | 180 | 0.0978 | 0.094 | 0.4443 |
| none | 180 | D1_handoff | 16 | 0.0247 | 0.000 | 0.4819 |
| none | 180 | D3 | 180 | 0.3111 | 0.311 | 1.0000 |
| none | 180 | D7_instruction->premise | 5 | 0.1000 | 0.000 | 0.7500 |
| none | 180 | D7_report->planner | 4 | 0.4934 | 0.000 | 1.0000 |
| reasoning_like | 92 | D1_1-conf | 92 | 0.0193 | 0.022 | 0.2793 |
| reasoning_like | 92 | D1_1-p_actual | 92 | 0.0106 | 0.011 | 0.2344 |
| reasoning_like | 92 | D1_1-margin | 92 | 0.0207 | 0.011 | 0.4443 |
| reasoning_like | 92 | D1_handoff | 10 | 0.0789 | 0.100 | 0.4819 |
| reasoning_like | 92 | D3 | 92 | 0.2174 | 0.217 | 1.0000 |
| reasoning_like | 92 | D7_instruction->premise | 2 | 0.0000 | 0.000 | 0.7500 |
| reasoning_like | 92 | D7_report->planner | 2 | 0.9130 | 0.500 | 1.0000 |

