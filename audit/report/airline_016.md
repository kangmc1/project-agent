# Audit report — airline_016

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | planner | D1/tool | {"confidence": 0.647, "p_actual": 0.724, "margin": 0.458} | action distribution: respond_to_user 0.72, db_agent 0.27, read_file 0.01 (actual: respond_to_user) |
| 2 | planner | D1/handoff | {"p_delegate": 0.267, "H2": 0.837} | delegate-vs-not split p_delegate=0.27 |
| 5 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": true, "tool_error": true} | argument never given: get_user_details.user_id=ethan_martin_123; tool get_user_details returned an error |
| 6 | db_agent | D1/tool | {"confidence": 0.561, "p_actual": 0.104, "margin": 0.523} | action distribution: no_tool 0.63, transfer_to_human_agents 0.10, book_reservation 0.10 (actual: get_reservation_details) |
| 6 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": false, "tool_error": true} | tool get_reservation_details returned an error |
| 7 | db_agent | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_error": true} | required but never called: search_direct_flight/search_onestop_flight; tool db_agent returned an error |
| 11 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": false, "tool_error": true} | tool get_reservation_details returned an error |
| 12 | db_agent | D1/tool | {"confidence": 0.722, "p_actual": 0.676, "margin": 0.409} | action distribution: write_file 0.68, no_tool 0.27, transfer_to_human_agents 0.06 (actual: write_file) |
| 13 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": false, "tool_error": true} | tool db_agent returned an error |
| 14 | planner | D1/tool | {"confidence": 0.535, "p_actual": 0.592, "margin": 0.233} | action distribution: respond_to_user 0.59, read_file 0.36, write_file 0.05 (actual: respond_to_user) |
| 18 | db_agent | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_error": false} | required but never called: search_direct_flight/search_onestop_flight |
| 22 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": true, "tool_error": true} | argument never given: get_user_details.user_id=ethan_martin_123; tool get_user_details returned an error |
| 23 | db_agent | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_error": true} | required but never called: search_direct_flight/search_onestop_flight; tool db_agent returned an error |
| 29 | planner | D1/tool | {"confidence": 0.646, "p_actual": 0.673, "margin": 0.346} | action distribution: respond_to_user 0.67, no_tool 0.33, read_file 0.00 (actual: respond_to_user) |

## Per-module summary
```
{
 "D1": {
  "n_scored": 23,
  "method": "stepwise"
 },
 "D3": {
  "n_steps": 23,
  "flagged": 8,
  "missing_tool": 3,
  "fabricated_arg": 2,
  "tool_error": 7
 },
 "D7": {
  "n_handoffs": 8
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3": "procedural flag (no threshold)"}`