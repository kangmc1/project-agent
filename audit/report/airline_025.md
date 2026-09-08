# Audit report — airline_025

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 10 | planner | D1/handoff | {"p_delegate": 0.269, "H2": 0.839} | delegate-vs-not split p_delegate=0.27 |
| 13 | planner | D1/tool | {"confidence": 0.535, "p_actual": 0.48, "margin": 0.0} | action distribution: db_agent 0.48, respond_to_user 0.48, read_file 0.04 (actual: db_agent) |
| 13 | planner | D1/handoff | {"p_delegate": 0.48, "H2": 0.999} | delegate-vs-not split p_delegate=0.48 |
| 21 | policy_checker | D1/tool | {"confidence": 0.462, "p_actual": 0.559, "margin": 0.131} | action distribution: think 0.56, no_tool 0.43, read_file 0.01 (actual: think) |
| 27 | db_agent | D1/tool | {"confidence": 0.757, "p_actual": 0.553, "margin": 0.107} | action distribution: search_onestop_flight 0.55, no_tool 0.45, search_direct_flight 0.00 (actual: search_onestop_flight) |
| 31 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["booking_failed", "booking_operation_failed", "hat011", "hat083", "sara_doe_496"], "altered": ["final_answer", "user_id", "verdict"]} | db_agent report->planner: missing ['booking_failed', 'booking_operation_failed', 'hat011'] altered ['final_answer', 'user_id', 'verdict'] |
| 32 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": true} | argument never given: book_reservation.user_id=sara_doe_496; call failed: book_reservation returned an error |
| 33 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: calculate |
| 37 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: book_reservation returned an error |
| 38 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: calculate |
| 41 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["could you please provide the date for the flight?", "the `book_reservation` function failed because the required parameter `date` was not provided."], "altered": []} | db_agent report->planner: missing ['could you please provide the date for the flight?', 'the `book_reservation` function failed because the required parameter `date` was not provided.'] altered [] |
| 42 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: book_reservation returned an error |
| 43 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: calculate |
| 46 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["aarav_ahmed_6699", "amount parameter", "successfully transferred to a human agent"], "altered": []} | db_agent report->planner: missing ['aarav_ahmed_6699', 'amount parameter', 'successfully transferred to a human agent'] altered [] |
| 47 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: book_reservation returned an error |
| 48 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: book_reservation returned an error |
| 49 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: book_reservation returned an error |
| 52 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: calculate |

## Per-module summary
```
{
 "D1": {
  "n_scored": 46,
  "method": "stepwise"
 },
 "D2": {
  "n_steps": 46,
  "flagged": 10,
  "missing_tool": 4,
  "fabricated_arg": 1,
  "tool_call_failed": 6
 },
 "D3": {
  "n_handoffs": 20
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D3": 1.0, "D2": "procedural flag (no threshold)"}`