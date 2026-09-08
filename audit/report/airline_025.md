# Audit report — airline_025

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 7 | db_agent | D3 | {"checks": ["error", "ignored"], "tool": "read_file"} | tool read_file call #4: error, ignored |
| 10 | planner | D1/handoff | {"p_delegate": 0.269, "H2": 0.839} | delegate-vs-not split p_delegate=0.27 |
| 10 | planner | D3 | {"checks": ["repeat"], "tool": "read_file"} | tool read_file call #7: repeat |
| 12 | policy_checker | D3 | {"satisfied": false} | claims without prior tool evidence: cancel= |
| 13 | planner | D1/tool | {"confidence": 0.535, "p_actual": 0.48, "margin": 0.0} | action distribution: db_agent 0.48, respond_to_user 0.48, read_file 0.04 (actual: db_agent) |
| 13 | planner | D1/handoff | {"p_delegate": 0.48, "H2": 0.999} | delegate-vs-not split p_delegate=0.48 |
| 14 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #9: repeat |
| 17 | policy_checker | D3 | {"satisfied": false} | claims without prior tool evidence: date=2024-05-15, cancel= |
| 21 | policy_checker | D1/tool | {"confidence": 0.462, "p_actual": 0.559, "margin": 0.131} | action distribution: think 0.56, no_tool 0.43, read_file 0.01 (actual: think) |
| 21 | policy_checker | D3 | {"checks": ["empty"], "tool": "think"} | tool think call #13: empty |
| 22 | policy_checker | D3 | {"satisfied": false} | claims without prior tool evidence: cancel= |
| 27 | db_agent | D1/tool | {"confidence": 0.757, "p_actual": 0.553, "margin": 0.107} | action distribution: search_onestop_flight 0.55, no_tool 0.45, search_direct_flight 0.00 (actual: search_onestop_flight) |
| 27 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT023 |
| 28 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT083, reservation_id=HAT011, money=314 |
| 31 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["booking_failed", "booking_operation_failed", "hat011", "hat083", "sara_doe_496"], "altered": ["final_answer", "user_id", "verdict"]} | db_agent report->planner: missing ['booking_failed', 'booking_operation_failed', 'hat011'] altered ['final_answer', 'user_id', 'verdict'] |
| 32 | db_agent | D3 | {"checks": ["error"], "tool": "book_reservation"} | tool book_reservation call #20: error |
| 32 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: money=314 |
| 32 | db_agent | D3/arguments | {"ungrounded_ratio": 0.111} | argument values never given to the agent: book_reservation.user_id=sara_doe_496 |
| 33 | planner | D3 | {"checks": ["error", "ignored"], "tool": "db_agent"} | tool db_agent call #21: error, ignored |
| 33 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: user_id=sara_doe_496 |
| 37 | db_agent | D3 | {"checks": ["error"], "tool": "book_reservation"} | tool book_reservation call #23: error |
| 41 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["could you please provide the date for the flight?", "the `book_reservation` function failed because the required parameter `date` was not provided."], "altered": []} | db_agent report->planner: missing ['could you please provide the date for the flight?', 'the `book_reservation` function failed because the required parameter `date` was not provided.'] altered [] |
| 42 | db_agent | D3 | {"checks": ["error", "repeat"], "tool": "book_reservation"} | tool book_reservation call #26: error, repeat |
| 43 | planner | D3 | {"checks": ["repeat"], "tool": "db_agent"} | tool db_agent call #27: repeat |
| 45 | planner | D3 | {"checks": ["repeat"], "tool": "respond_to_user"} | tool respond_to_user call #28: repeat |
| 46 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["aarav_ahmed_6699", "amount parameter", "successfully transferred to a human agent"], "altered": []} | db_agent report->planner: missing ['aarav_ahmed_6699', 'amount parameter', 'successfully transferred to a human agent'] altered [] |
| 47 | db_agent | D3 | {"checks": ["error"], "tool": "book_reservation"} | tool book_reservation call #29: error |
| 48 | db_agent | D3 | {"checks": ["error"], "tool": "book_reservation"} | tool book_reservation call #30: error |
| 49 | db_agent | D3 | {"checks": ["error", "repeat"], "tool": "book_reservation"} | tool book_reservation call #31: error, repeat |
| 52 | planner | D3 | {"checks": ["repeat"], "tool": "db_agent"} | tool db_agent call #34: repeat |

## Per-module summary
```
{
 "D1": {
  "n_scored": 46,
  "method": "stepwise"
 },
 "D3": {
  "tool_calls": 35,
  "utterances": 23,
  "checks": {
   "error": 8,
   "ignored": 2,
   "repeat": 7,
   "empty": 1
  }
 },
 "D7": {
  "n_handoffs": 20
 },
 "D3_args": {
  "n_steps": 22,
  "n_values": 94,
  "n_ungrounded": 1
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3_args": "any ungrounded value"}`