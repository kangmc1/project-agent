# Audit report — airline_046

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 5 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": true, "tool_error": false} | argument never given: search_direct_flight.date=2024-05-15 |
| 6 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": true, "tool_error": false} | argument never given: search_onestop_flight.date=2024-05-15 |
| 9 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": true, "tool_error": false} | argument never given: search_direct_flight.date=2024-05-15 |
| 15 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["user not found"], "altered": ["final_answer", "verdict"]} | db_agent report->planner: missing ['user not found'] altered ['final_answer', 'verdict'] |
| 16 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": true, "tool_error": true} | argument never given: get_user_details.user_id=sara_doe_496 |
| 20 | planner | D1/handoff | {"p_delegate": 0.82, "H2": 0.68} | delegate-vs-not split p_delegate=0.82 |
| 20 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["not_found", "sara_doe_496", "the provided user id was not found in the database."], "altered": ["verdict"]} | db_agent report->planner: missing ['not_found', 'sara_doe_496', 'the provided user id was not found in the database.'] altered ['verdict'] |
| 21 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": true, "tool_error": true} | argument never given: get_user_details.user_id=sara_doe_496 |
| 22 | db_agent | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_error": true} | required but never called: search_direct_flight/search_onestop_flight |
| 26 | db_agent | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_error": false} | required but never called: search_direct_flight/search_onestop_flight |
| 30 | db_agent | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_error": false} | required but never called: search_direct_flight/search_onestop_flight |
| 34 | db_agent | D1/tool | {"confidence": 0.775, "p_actual": 0.678, "margin": 0.358} | action distribution: search_direct_flight 0.68, search_onestop_flight 0.32, no_tool 0.00 (actual: search_direct_flight) |
| 34 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": true, "tool_error": false} | argument never given: search_direct_flight.date=2024-04-08 |
| 39 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": true, "tool_error": false} | argument never given: search_direct_flight.date=2024-04-08 |
| 40 | db_agent | D1/tool | {"confidence": 0.767, "p_actual": 0.632, "margin": 0.264} | action distribution: search_onestop_flight 0.63, no_tool 0.37, transfer_to_human_agents 0.00 (actual: search_onestop_flight) |
| 40 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": true, "tool_error": false} | argument never given: search_onestop_flight.date=2024-04-08 |
| 41 | db_agent | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_error": false} | required but never called: get_reservation_details/get_user_details |
| 46 | db_agent | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_error": false} | required but never called: get_reservation_details/get_user_details |
| 51 | db_agent | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_error": false} | required but never called: get_reservation_details/get_user_details |
| 55 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": true, "tool_error": false} | argument never given: search_direct_flight.date=2024-04-05, search_direct_flight.date=2024-04-05 |
| 59 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["not found", "sara_doe_496"], "altered": ["user_id", "verdict"]} | db_agent report->planner: missing ['not found', 'sara_doe_496'] altered ['user_id', 'verdict'] |
| 60 | db_agent | D1/tool | {"confidence": 0.635, "p_actual": 0.62, "margin": 0.371} | action distribution: get_user_details 0.62, search_direct_flight 0.25, no_tool 0.07 (actual: get_user_details) |
| 60 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": true, "tool_error": true} | argument never given: get_user_details.user_id=sara_doe_496 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 52,
  "method": "stepwise"
 },
 "D3": {
  "n_steps": 52,
  "flagged": 16,
  "missing_tool": 6,
  "fabricated_arg": 10,
  "tool_error": 6
 },
 "D7": {
  "n_handoffs": 24
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3": "procedural flag (no threshold)"}`