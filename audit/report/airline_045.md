# Audit report — airline_045

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 4 | planner | D1/handoff | {"p_delegate": 0.731, "H2": 0.84} | delegate-vs-not split p_delegate=0.73 |
| 5 | db_agent | D1/tool | {"confidence": 0.512, "p_actual": 0.276, "margin": 0.172} | action distribution: no_tool 0.45, get_user_details 0.28, list_all_airports 0.13 (actual: get_user_details) |
| 5 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": true} | argument never given: get_user_details.user_id=sara_doe_496; call failed: get_user_details returned an error |
| 9 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["3", "given_id", "no_matching_reservation_found", "search_for_reservation"], "altered": ["verdict"]} | db_agent report->planner: missing ['3', 'given_id', 'no_matching_reservation_found'] altered ['verdict'] |
| 10 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": true} | argument never given: get_user_details.user_id=sara_doe_496; call failed: get_user_details returned an error |
| 17 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: get_reservation_details/get_user_details |
| 20 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["operation failed to locate a reservation.", "user not found with the provided details."], "altered": []} | db_agent report->planner: missing ['operation failed to locate a reservation.', 'user not found with the provided details.'] altered [] |
| 21 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": true} | argument never given: get_user_details.user_id=sara_doe_496; call failed: get_user_details returned an error |
| 26 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": true} | argument never given: get_user_details.user_id=sara_doe_496; call failed: get_user_details returned an error |
| 30 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["delta_user_123", "no_further_action_can_be_taken", "user_not_found"], "altered": ["verdict"]} | db_agent report->planner: missing ['delta_user_123', 'no_further_action_can_be_taken', 'user_not_found'] altered ['verdict'] |
| 31 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": true} | argument never given: get_user_details.user_id=delta_user_123; call failed: get_user_details returned an error |
| 38 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: get_reservation_details/get_user_details |
| 43 | db_agent | D1/tool | {"confidence": 0.766, "p_actual": 0.626, "margin": 0.252} | action distribution: search_onestop_flight 0.63, no_tool 0.37, transfer_to_human_agents 0.00 (actual: search_onestop_flight) |
| 44 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: get_reservation_details/get_user_details |
| 48 | db_agent | D1/tool | {"confidence": 0.777, "p_actual": 0.787, "margin": 0.612} | action distribution: search_direct_flight 0.79, get_reservation_details 0.17, no_tool 0.03 (actual: search_direct_flight) |
| 49 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: get_reservation_details/get_user_details |
| 52 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["8jx2wo", "could not be found", "no details were retrieved for the requested reservation."], "altered": ["final_answer", "verdict"]} | db_agent report->planner: missing ['8jx2wo', 'could not be found', 'no details were retrieved for the requested reservation.'] altered ['final_answer', 'verdict'] |
| 53 | db_agent | D1/tool | {"confidence": 0.719, "p_actual": 0.549, "margin": 0.119} | action distribution: get_reservation_details 0.55, search_direct_flight 0.43, book_reservation 0.01 (actual: get_reservation_details) |
| 53 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": true} | argument never given: get_reservation_details.reservation_id=8JX2WO; call failed: get_reservation_details returned an error |
| 60 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: get_user_details returned an error |
| 65 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: get_user_details returned an error |
| 69 | planner | D1/tool | {"confidence": 0.657, "p_actual": 0.698, "margin": 0.397} | action distribution: respond_to_user 0.70, no_tool 0.30, write_file 0.00 (actual: respond_to_user) |

## Per-module summary
```
{
 "D1": {
  "n_scored": 54,
  "method": "stepwise"
 },
 "D2": {
  "n_steps": 54,
  "flagged": 12,
  "missing_tool": 4,
  "fabricated_arg": 6,
  "tool_call_failed": 8
 },
 "D3": {
  "n_handoffs": 24
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D3": 1.0, "D2": "procedural flag (no threshold)"}`