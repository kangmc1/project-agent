# Audit report — airline_030

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 10 | planner | D1/handoff | {"p_delegate": 0.121, "H2": 0.531} | delegate-vs-not split p_delegate=0.12 |
| 12 | planner | D1/tool | {"confidence": 0.534, "p_actual": 0.685, "margin": 0.488} | action distribution: policy_checker 0.68, db_agent 0.20, respond_to_user 0.12 (actual: policy_checker) |
| 12 | planner | D1/handoff | {"p_delegate": 0.881, "H2": 0.528} | delegate-vs-not split p_delegate=0.88 |
| 13 | policy_checker | D1/tool | {"confidence": 0.673, "p_actual": 0.84, "margin": 0.683} | action distribution: think 0.84, no_tool 0.16, read_file 0.00 (actual: think) |
| 13 | policy_checker | D3 | {"checks": ["empty"], "tool": "think"} | tool think call #13: empty |
| 13 | policy_checker | D3 | {"satisfied": false} | claims without prior tool evidence: date=2024-05-15, cancel= |
| 14 | policy_checker | D1/tool | {"confidence": 0.068, "p_actual": 0.404, "margin": 0.159} | action distribution: think 0.40, read_file 0.25, write_file 0.25 (actual: think) |
| 14 | policy_checker | D3 | {"checks": ["empty"], "tool": "think"} | tool think call #14: empty |
| 14 | policy_checker | D3 | {"satisfied": false} | claims without prior tool evidence: date=2024-05-15, cancel= |
| 15 | policy_checker | D3 | {"satisfied": false} | claims without prior tool evidence: date=2024-05-15, cancel= |
| 17 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #16: repeat |
| 20 | policy_checker | D3 | {"satisfied": false} | claims without prior tool evidence: date=2024-05-15, cancel= |
| 24 | planner | D2 | {"s": 0.0, "unsupported": 1.0} | values not found in any prior tool result: flights on May 17, 2024 (JFK-ORD-PHL) |

## Per-module summary
```
{
 "D1": {
  "n_scored": 20,
  "method": "stepwise"
 },
 "D2": {
  "n_utterances": 12,
  "n_na": 0
 },
 "D3": {
  "tool_calls": 20,
  "utterances": 12,
  "checks": {
   "empty": 2,
   "repeat": 1
  }
 },
 "D7": {
  "n_handoffs": 10
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`