# Audit report — airline_017

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 4 | planner | D1/tool | {"confidence": 0.637, "p_actual": 0.721, "margin": 0.456} | action distribution: db_agent 0.72, respond_to_user 0.27, policy_checker 0.01 (actual: db_agent) |
| 4 | planner | D1/handoff | {"p_delegate": 0.734, "H2": 0.835} | delegate-vs-not split p_delegate=0.73 |
| 7 | db_agent | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_error": false} | required but never called: get_reservation_details/get_user_details |
| 17 | db_agent | D1/tool | {"confidence": 0.477, "p_actual": 0.37, "margin": 0.146} | action distribution: search_direct_flight 0.37, book_reservation 0.22, get_reservation_details 0.22 (actual: search_direct_flight) |
| 17 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": true, "tool_error": false} | argument never given: search_direct_flight.date=2024-05-01, search_direct_flight.date=2024-05-01 |
| 18 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": true, "tool_error": false} | argument never given: search_onestop_flight.date=2024-05-01, search_onestop_flight.date=2024-05-01 |
| 20 | db_agent | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_error": false} | required but never called: calculate |
| 21 | planner | D1/tool | {"confidence": 0.557, "p_actual": 0.55, "margin": 0.121} | action distribution: read_file 0.55, respond_to_user 0.43, policy_checker 0.01 (actual: read_file) |
| 25 | db_agent | D1/tool | {"confidence": 0.621, "p_actual": 0.409, "margin": 0.019} | action distribution: no_tool 0.43, search_direct_flight 0.41, get_reservation_details 0.15 (actual: search_direct_flight) |
| 26 | db_agent | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_error": false} | required but never called: calculate |
| 36 | db_agent | D1/tool | {"confidence": 0.69, "p_actual": 0.419, "margin": 0.119} | action distribution: get_reservation_details 0.54, calculate 0.42, think 0.02 (actual: calculate) |
| 47 | db_agent | D1/tool | {"confidence": 0.734, "p_actual": 0.674, "margin": 0.377} | action distribution: get_reservation_details 0.67, search_direct_flight 0.30, search_onestop_flight 0.02 (actual: get_reservation_details) |
| 47 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": false, "tool_error": true} | tool get_reservation_details returned an error |
| 48 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": false, "tool_error": true} | tool db_agent returned an error |
| 52 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": true, "tool_error": true} | argument never given: get_user_details.user_id=liam_khan_123; tool get_user_details returned an error |
| 53 | db_agent | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_error": false} | required but never called: search_direct_flight/search_onestop_flight |
| 61 | db_agent | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_error": false} | required but never called: search_direct_flight/search_onestop_flight |
| 62 | planner | D1/tool | {"confidence": 0.471, "p_actual": 0.559, "margin": 0.22} | action distribution: db_agent 0.56, respond_to_user 0.34, write_file 0.10 (actual: db_agent) |
| 62 | planner | D1/handoff | {"p_delegate": 0.559, "H2": 0.99} | delegate-vs-not split p_delegate=0.56 |
| 64 | db_agent | D1/tool | {"confidence": 0.752, "p_actual": 0.554, "margin": 0.11} | action distribution: search_direct_flight 0.55, no_tool 0.44, update_reservation_flights 0.00 (actual: search_direct_flight) |

## Per-module summary
```
{
 "D1": {
  "n_scored": 59,
  "method": "stepwise"
 },
 "D3": {
  "n_steps": 59,
  "flagged": 10,
  "missing_tool": 5,
  "fabricated_arg": 3,
  "tool_error": 3
 },
 "D7": {
  "n_handoffs": 22
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3": "procedural flag (no threshold)"}`