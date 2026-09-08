# Audit report — airline_042

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 4 | planner | D1/tool | {"confidence": 0.581, "p_actual": 0.555, "margin": 0.123} | action distribution: db_agent 0.55, policy_checker 0.43, read_file 0.01 (actual: db_agent) |
| 7 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["5 to 7 business days", "cancellations are allowed only if travel insurance is bought and the condition is met", "eligible for a refund if travel insurance is purchased and cancellation is due to health reasons", "need_info"], "altered": []} | policy_checker report->planner: missing ['5 to 7 business days', 'cancellations are allowed only if travel insurance is bought and the condition is met', 'eligible for a refund if travel insurance is purchased and cancellation is due to health reasons'] altered [] |
| 8 | policy_checker | D3 | {"satisfied": false} | claims without prior tool evidence: cancel= |
| 11 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["3rk2t9", "cannot proceed with a refund as there is no travel insurance linked to this reservation.", "n/a", "not linked"], "altered": []} | db_agent report->planner: missing ['3rk2t9', 'cannot proceed with a refund as there is no travel insurance linked to this reservation.', 'n/a'] altered [] |
| 12 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #6: repeat |
| 17 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #9: repeat |
| 21 | planner | D1/handoff | {"p_delegate": 0.096, "H2": 0.456} | delegate-vs-not split p_delegate=0.10 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 18,
  "method": "stepwise"
 },
 "D2": {
  "n_utterances": 8,
  "n_na": 0
 },
 "D3": {
  "tool_calls": 13,
  "utterances": 8,
  "checks": {
   "repeat": 2
  }
 },
 "D7": {
  "n_handoffs": 8
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`