# Audit report — airline_046

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 5 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": false} | argument never given: search_direct_flight.date=2024-05-15 |
| 6 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": false} | argument never given: search_onestop_flight.date=2024-05-15 |
| 9 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": false} | argument never given: search_direct_flight.date=2024-05-15 |
| 15 | planner | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": false} | db_agent: lookup/modification requested without reservation or user id: 'Find the last reservation with three passengers.' |
| 16 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": true} | argument never given: get_user_details.user_id=sara_doe_496; call failed: get_user_details returned an error |
| 20 | planner | D1/handoff | {"p_delegate": 0.82, "H2": 0.68} | delegate-vs-not split p_delegate=0.82 |
| 21 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": true} | argument never given: get_user_details.user_id=sara_doe_496; call failed: get_user_details returned an error |
| 22 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: search_direct_flight/search_onestop_flight |
| 25 | planner | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": false} | db_agent: lookup/modification requested without reservation or user id: 'Search for recent delayed flights with three passengers without a specific user ID.' |
| 26 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: search_direct_flight/search_onestop_flight |
| 30 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: search_direct_flight/search_onestop_flight |
| 33 | planner | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": false} | db_agent: re-issued after a failure report (similarity 0.90): 'Search for a delayed flight from SFO to JFK on the 8th of last month with three passengers.' |
| 34 | db_agent | D1/tool | {"confidence": 0.775, "p_actual": 0.678, "margin": 0.358} | action distribution: search_direct_flight 0.68, search_onestop_flight 0.32, no_tool 0.00 (actual: search_direct_flight) |
| 34 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": false} | argument never given: search_direct_flight.date=2024-04-08 |
| 38 | planner | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": false} | db_agent: lookup/modification requested without reservation or user id: 'Search for a delayed flight from SFO to JFK on the 8th of last month with three passengers and retrieve the reservation '; db_agent: re-issued after a failure report (similarity 0.83): 'Search for a delayed flight from SFO to JFK on the 8th of last month with three passengers and retri' |
| 38 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["No one-stop flights were found for the specified date and route."], "altered": []} | db_agent report->planner: missing ['No one-stop flights were found for the specified date and route.'] altered [] |
| 39 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": false} | argument never given: search_direct_flight.date=2024-04-08 |
| 40 | db_agent | D1/tool | {"confidence": 0.767, "p_actual": 0.632, "margin": 0.264} | action distribution: search_onestop_flight 0.63, no_tool 0.37, transfer_to_human_agents 0.00 (actual: search_onestop_flight) |
| 40 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": false} | argument never given: search_onestop_flight.date=2024-04-08 |
| 41 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: get_reservation_details/get_user_details |
| 44 | planner | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": false} | db_agent: lookup/modification requested without reservation or user id: 'Search for flight DL142 operated by Delta from SFO to JFK on April 8th and retrieve the reservation details for three pa' |
| 46 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: get_reservation_details/get_user_details |
| 49 | planner | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": false} | db_agent: lookup/modification requested without reservation or user id: 'Search for flight DL142 operated by Delta from SFO to LGA on April 8th and retrieve the reservation details for three pa'; db_agent: re-issued after a failure report (similarity 0.98): 'Search for flight DL142 operated by Delta from SFO to LGA on April 8th and retrieve the reservation ' |
| 51 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: get_reservation_details/get_user_details |
| 55 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": false} | argument never given: search_direct_flight.date=2024-04-05, search_direct_flight.date=2024-04-05 |
| 59 | planner | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": false} | db_agent: lookup/modification requested without reservation or user id: 'Search for a Delta reservation with three passengers, including a passenger named Sarah, for a morning flight from SFO t' |
| 60 | db_agent | D1/tool | {"confidence": 0.635, "p_actual": 0.62, "margin": 0.371} | action distribution: get_user_details 0.62, search_direct_flight 0.25, no_tool 0.07 (actual: get_user_details) |
| 60 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": true} | argument never given: get_user_details.user_id=sara_doe_496; call failed: get_user_details returned an error |

## Per-module summary
```
{
 "D1": {
  "n_scored": 52,
  "method": "stepwise"
 },
 "D2": {
  "n_steps": 52,
  "flagged": 23,
  "missing_tool": 6,
  "fabricated_arg": 10,
  "tool_call_failed": 3
 },
 "D3": {
  "n_handoffs": 24
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D3": 1.0, "D2": "procedural flag (no threshold)"}`