# Audit report — airline_045

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 4 | planner | D1/handoff | {"p_delegate": 0.731, "H2": 0.84} | delegate-vs-not split p_delegate=0.73 |
| 4 | planner | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": false} | db_agent: lookup/modification requested without reservation or user id: 'Find the last reservation made by the customer and return its ID and details.' |
| 4 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["sara_doe_496"], "altered": ["user_id"]} | db_agent report->planner: missing ['sara_doe_496'] altered ['user_id'] |
| 5 | db_agent | D1/tool | {"confidence": 0.512, "p_actual": 0.276, "margin": 0.172} | action distribution: no_tool 0.45, get_user_details 0.28, list_all_airports 0.13 (actual: get_user_details) |
| 5 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": true} | argument never given: get_user_details.user_id=sara_doe_496; call failed: get_user_details returned an error |
| 9 | planner | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": false} | db_agent: lookup/modification requested without reservation or user id: "Search for a reservation with 3 passengers that matches the customer's description and return its ID and details." |
| 9 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["3"], "altered": ["verdict"]} | db_agent report->planner: missing ['3'] altered ['verdict'] |
| 10 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": true} | argument never given: get_user_details.user_id=sara_doe_496; call failed: get_user_details returned an error |
| 16 | planner | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": false} | db_agent: lookup/modification requested without reservation or user id: "Search for a reservation with 2 passengers that matches the customer's description and return its ID and details."; db_agent: re-issued after a failure report (similarity 0.99): "Search for a reservation with 2 passengers that matches the customer's description and return its ID" |
| 17 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: get_reservation_details/get_user_details |
| 20 | planner | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": false} | db_agent: lookup/modification requested without reservation or user id: "Search for a reservation with 3 passengers that matches the customer's description and return its ID and details." |
| 20 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["operation failed to locate a reservation.", "user not found with the provided details."], "altered": []} | db_agent report->planner: missing ['operation failed to locate a reservation.', 'user not found with the provided details.'] altered [] |
| 21 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": true} | argument never given: get_user_details.user_id=sara_doe_496; call failed: get_user_details returned an error |
| 25 | planner | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": false} | db_agent: lookup/modification requested without reservation or user id: 'Search for a reservation with 3 passengers, traveling from Chicago to Miami around mid-October, and return its ID and de' |
| 26 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": true} | argument never given: get_user_details.user_id=sara_doe_496; call failed: get_user_details returned an error |
| 30 | planner | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": false} | db_agent: lookup/modification requested without reservation or user id: 'Search for a Delta reservation with 3 passengers, traveling from Chicago to Miami around mid-October, and return its ID '; db_agent: re-issued after a failure report (similarity 0.98): 'Search for a Delta reservation with 3 passengers, traveling from Chicago to Miami around mid-October' |
| 30 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["delta_user_123"], "altered": ["verdict"]} | db_agent report->planner: missing ['delta_user_123'] altered ['verdict'] |
| 31 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": true} | argument never given: get_user_details.user_id=delta_user_123; call failed: get_user_details returned an error |
| 35 | planner | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": false} | db_agent: lookup/modification requested without reservation or user id: 'Search for a Delta reservation with 3 passengers, traveling from Chicago to Miami on October 15th on flight Delta 452, a'; db_agent: re-issued after a failure report (similarity 0.88): 'Search for a Delta reservation with 3 passengers, traveling from Chicago to Miami on October 15th on' |
| 38 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: get_reservation_details/get_user_details |
| 41 | planner | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": false} | db_agent: lookup/modification requested without reservation or user id: 'Search for a Delta reservation with 3 passengers, traveling from Chicago to Miami on October 16th on flight Delta 452, a'; db_agent: re-issued after a failure report (similarity 0.99): 'Search for a Delta reservation with 3 passengers, traveling from Chicago to Miami on October 16th on' |
| 43 | db_agent | D1/tool | {"confidence": 0.766, "p_actual": 0.626, "margin": 0.252} | action distribution: search_onestop_flight 0.63, no_tool 0.37, transfer_to_human_agents 0.00 (actual: search_onestop_flight) |
| 44 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: get_reservation_details/get_user_details |
| 47 | planner | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": false} | db_agent: lookup/modification requested without reservation or user id: 'Search for a Delta reservation with 3 passengers, traveling from Chicago to Miami on mid-October on flight Delta 457, an'; db_agent: re-issued after a failure report (similarity 0.96): 'Search for a Delta reservation with 3 passengers, traveling from Chicago to Miami on mid-October on ' |
| 48 | db_agent | D1/tool | {"confidence": 0.777, "p_actual": 0.787, "margin": 0.612} | action distribution: search_direct_flight 0.79, get_reservation_details 0.17, no_tool 0.03 (actual: search_direct_flight) |
| 49 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: get_reservation_details/get_user_details |
| 52 | planner | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": false} | db_agent: lookup/modification requested without reservation or user id: 'Search for a United reservation with 3 passengers, traveling from Chicago to Miami in mid-October on flight United 123, '; db_agent: re-issued after a failure report (similarity 0.91): 'Search for a United reservation with 3 passengers, traveling from Chicago to Miami in mid-October on' |
| 52 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["8jx2wo", "could not be found", "no details were retrieved for the requested reservation."], "altered": ["final_answer", "verdict"]} | db_agent report->planner: missing ['8jx2wo', 'could not be found', 'no details were retrieved for the requested reservation.'] altered ['final_answer', 'verdict'] |
| 53 | db_agent | D1/tool | {"confidence": 0.719, "p_actual": 0.549, "margin": 0.119} | action distribution: get_reservation_details 0.55, search_direct_flight 0.43, book_reservation 0.01 (actual: get_reservation_details) |
| 53 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": true} | argument never given: get_reservation_details.reservation_id=8JX2WO; call failed: get_reservation_details returned an error |
| 60 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: get_user_details returned an error |
| 64 | planner | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": false} | db_agent: lookup/modification requested without reservation or user id: 'Retrieve the reservation history for the email address noahmuller9847@example.com and return the details.'; db_agent: re-issued after a failure report (similarity 0.99): 'Retrieve the reservation history for the email address noahmuller9847@example.com and return the det' |
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
  "flagged": 23,
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