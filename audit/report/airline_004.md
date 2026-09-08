# Audit report — airline_004

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 4 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["0", "1", "161", "2024-05-24", "2024-05-25"], "altered": ["reservation_id"]} | db_agent report->planner: missing ['0', '1', '161'] altered ['reservation_id'] |
| 7 | db_agent | D1/tool | {"confidence": 0.644, "p_actual": 0.646, "margin": 0.461} | action distribution: get_reservation_details 0.65, write_file 0.18, read_file 0.11 (actual: get_reservation_details) |
| 13 | planner | D1/tool | {"confidence": 0.636, "p_actual": 0.677, "margin": 0.357} | action distribution: respond_to_user 0.68, db_agent 0.32, read_file 0.00 (actual: respond_to_user) |
| 13 | planner | D1/handoff | {"p_delegate": 0.32, "H2": 0.904} | delegate-vs-not split p_delegate=0.32 |
| 16 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_user_details"} | tool get_user_details call #10: repeat |
| 17 | db_agent | D2 | {"s": 0.0, "unsupported": 1.0} | values not found in any prior tool result: ['UM3OG5', '5RJ7UH', 'FQ8APE', 'QKRY03'], Filter reservations with flights from New York to Chicago |
| 17 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #11: repeat |
| 17 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #12: repeat |
| 17 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #13: repeat |
| 17 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #14: repeat |
| 26 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #19: repeat |
| 27 | db_agent | D3 | {"checks": ["error"], "tool": "update_reservation_baggages"} | tool update_reservation_baggages call #21: error |

## Per-module summary
```
{
 "D1": {
  "n_scored": 26,
  "method": "stepwise"
 },
 "D2": {
  "n_utterances": 14,
  "n_na": 1
 },
 "D3": {
  "tool_calls": 25,
  "utterances": 13,
  "checks": {
   "repeat": 6,
   "error": 1
  }
 },
 "D7": {
  "n_handoffs": 8
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`