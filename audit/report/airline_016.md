# Audit report — airline_016

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | planner | D1/tool | {"confidence": 0.647, "p_actual": 0.724, "margin": 0.458} | action distribution: respond_to_user 0.72, db_agent 0.27, read_file 0.01 (actual: respond_to_user) |
| 2 | planner | D1/handoff | {"p_delegate": 0.267, "H2": 0.837} | delegate-vs-not split p_delegate=0.27 |
| 5 | db_agent | D3 | {"checks": ["error"], "tool": "get_user_details"} | tool get_user_details call #2: error |
| 5 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT039, flight_no=HAT039 |
| 6 | db_agent | D1/tool | {"confidence": 0.561, "p_actual": 0.104, "margin": 0.523} | action distribution: no_tool 0.63, transfer_to_human_agents 0.10, book_reservation 0.10 (actual: get_reservation_details) |
| 6 | db_agent | D3 | {"checks": ["error"], "tool": "get_reservation_details"} | tool get_reservation_details call #3: error |
| 7 | planner | D3 | {"checks": ["error", "ignored"], "tool": "db_agent"} | tool db_agent call #4: error, ignored |
| 11 | db_agent | D3 | {"checks": ["error"], "tool": "get_reservation_details"} | tool get_reservation_details call #6: error |
| 12 | db_agent | D1/tool | {"confidence": 0.722, "p_actual": 0.676, "margin": 0.409} | action distribution: write_file 0.68, no_tool 0.27, transfer_to_human_agents 0.06 (actual: write_file) |
| 13 | planner | D3 | {"checks": ["error", "ignored"], "tool": "db_agent"} | tool db_agent call #8: error, ignored |
| 14 | planner | D1/tool | {"confidence": 0.535, "p_actual": 0.592, "margin": 0.233} | action distribution: respond_to_user 0.59, read_file 0.36, write_file 0.05 (actual: respond_to_user) |
| 22 | db_agent | D3 | {"checks": ["error", "repeat"], "tool": "get_user_details"} | tool get_user_details call #13: error, repeat |
| 23 | planner | D3 | {"checks": ["error", "ignored"], "tool": "db_agent"} | tool db_agent call #14: error, ignored |
| 29 | planner | D1/tool | {"confidence": 0.646, "p_actual": 0.673, "margin": 0.346} | action distribution: respond_to_user 0.67, no_tool 0.33, read_file 0.00 (actual: respond_to_user) |

## Per-module summary
```
{
 "D1": {
  "n_scored": 23,
  "method": "stepwise"
 },
 "D2": {
  "n_utterances": 11,
  "n_na": 2
 },
 "D3": {
  "tool_calls": 18,
  "utterances": 8,
  "checks": {
   "error": 7,
   "ignored": 3,
   "repeat": 1
  }
 },
 "D7": {
  "n_handoffs": 8
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`