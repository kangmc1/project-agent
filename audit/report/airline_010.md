# Audit report — airline_010

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 7 | planner | D1/tool | {"confidence": 0.604, "p_actual": 0.56, "margin": 0.124} | action distribution: respond_to_user 0.56, policy_checker 0.44, db_agent 0.00 (actual: respond_to_user) |
| 7 | planner | D1/handoff | {"p_delegate": 0.438, "H2": 0.989} | delegate-vs-not split p_delegate=0.44 |
| 15 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": false} | argument never given: search_direct_flight.airport=LAX, search_direct_flight.airport=SFO, search_direct_flight.airport=SEA, search_direct_flight.airport=PDX |
| 16 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": false} | argument never given: search_direct_flight.airport=SFO, search_direct_flight.airport=PDX |
| 24 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": true} | argument never given: book_reservation.user_id=sara_doe_496, book_reservation.user_id=gift_card_12345, book_reservation.user_id=gift_card_67890; call failed: book_reservation returned an error |
| 29 | db_agent | D1/tool | {"confidence": 0.723, "p_actual": 0.551, "margin": 0.122} | action distribution: book_reservation 0.55, get_user_details 0.43, no_tool 0.02 (actual: book_reservation) |
| 29 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": true} | argument never given: book_reservation.user_id=gift_card_12345, book_reservation.user_id=gift_card_67890; call failed: book_reservation returned an error |
| 31 | planner | D1/handoff | {"p_delegate": 0.78, "H2": 0.761} | delegate-vs-not split p_delegate=0.78 |
| 32 | db_agent | D1/tool | {"confidence": 0.683, "p_actual": 0.353, "margin": 0.227} | action distribution: get_reservation_details 0.58, search_direct_flight 0.35, no_tool 0.06 (actual: search_direct_flight) |
| 34 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["error related to the `flight_number` parameter", "failed", "hat069", "hat276"], "altered": ["flight_number_1"]} | db_agent report->planner: missing ['error related to the `flight_number` parameter', 'failed', 'hat069'] altered ['flight_number_1'] |
| 35 | db_agent | D1/tool | {"confidence": 0.723, "p_actual": 0.551, "margin": 0.122} | action distribution: book_reservation 0.55, get_user_details 0.43, no_tool 0.02 (actual: book_reservation) |
| 35 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": true} | argument never given: book_reservation.user_id=gift_card_12345, book_reservation.user_id=gift_card_67890; call failed: book_reservation returned an error |
| 37 | planner | D1/tool | {"confidence": 0.454, "p_actual": 0.544, "margin": 0.214} | action distribution: respond_to_user 0.54, policy_checker 0.33, db_agent 0.12 (actual: respond_to_user) |
| 37 | planner | D1/handoff | {"p_delegate": 0.452, "H2": 0.993} | delegate-vs-not split p_delegate=0.45 |
| 40 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": false} | argument never given: search_direct_flight.airport=LAX, search_direct_flight.airport=SFO, search_direct_flight.airport=SEA, search_direct_flight.airport=LAX |
| 45 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["error related to the `flight_number` parameter", "failed", "hat012", "hat041"], "altered": []} | db_agent report->planner: missing ['error related to the `flight_number` parameter', 'failed', 'hat012'] altered [] |
| 46 | db_agent | D1/tool | {"confidence": 0.677, "p_actual": 0.624, "margin": 0.33} | action distribution: book_reservation 0.62, get_user_details 0.29, no_tool 0.06 (actual: book_reservation) |
| 46 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": true} | argument never given: book_reservation.user_id=gift_card_12345, book_reservation.user_id=gift_card_67890; call failed: book_reservation returned an error |

## Per-module summary
```
{
 "D1": {
  "n_scored": 42,
  "method": "stepwise"
 },
 "D3": {
  "n_steps": 42,
  "flagged": 7,
  "missing_tool": 0,
  "fabricated_arg": 7,
  "tool_call_failed": 4
 },
 "D7": {
  "n_handoffs": 18
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3": "procedural flag (no threshold)"}`