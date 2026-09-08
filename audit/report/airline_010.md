# Audit report — airline_010

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 7 | planner | D1/tool | {"confidence": 0.604, "p_actual": 0.56, "margin": 0.124} | action distribution: respond_to_user 0.56, policy_checker 0.44, db_agent 0.00 (actual: respond_to_user) |
| 7 | planner | D1/handoff | {"p_delegate": 0.438, "H2": 0.989} | delegate-vs-not split p_delegate=0.44 |
| 15 | db_agent | D3/arguments | {"ungrounded_ratio": 0.333} | argument values never given to the agent: search_direct_flight.airport=LAX, search_direct_flight.airport=SFO, search_direct_flight.airport=SEA, search_direct_flight.airport=PDX |
| 16 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT041 |
| 16 | db_agent | D3/arguments | {"ungrounded_ratio": 0.167} | argument values never given to the agent: search_direct_flight.airport=SFO, search_direct_flight.airport=PDX |
| 17 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT083, reservation_id=HAT023, reservation_id=HAT069 |
| 18 | db_agent | D3 | {"checks": ["error", "ignored"], "tool": "read_file"} | tool read_file call #19: error, ignored |
| 18 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT276, reservation_id=HAT100, reservation_id=HAT041, reservation_id=HAT012, reservation_id=HAT069 |
| 20 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT276, reservation_id=HAT069, money=106 |
| 24 | db_agent | D3 | {"checks": ["error"], "tool": "book_reservation"} | tool book_reservation call #23: error |
| 24 | db_agent | D3/arguments | {"ungrounded_ratio": 0.273} | argument values never given to the agent: book_reservation.user_id=sara_doe_496, book_reservation.user_id=gift_card_12345, book_reservation.user_id=gift_card_67890 |
| 25 | planner | D3 | {"checks": ["error", "ignored"], "tool": "db_agent"} | tool db_agent call #24: error, ignored |
| 25 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: user_id=sara_doe_496 |
| 29 | db_agent | D1/tool | {"confidence": 0.723, "p_actual": 0.551, "margin": 0.122} | action distribution: book_reservation 0.55, get_user_details 0.43, no_tool 0.02 (actual: book_reservation) |
| 29 | db_agent | D3 | {"checks": ["error"], "tool": "book_reservation"} | tool book_reservation call #26: error |
| 29 | db_agent | D3/arguments | {"ungrounded_ratio": 0.182} | argument values never given to the agent: book_reservation.user_id=gift_card_12345, book_reservation.user_id=gift_card_67890 |
| 30 | planner | D3 | {"checks": ["error", "ignored"], "tool": "db_agent"} | tool db_agent call #27: error, ignored |
| 31 | planner | D1/handoff | {"p_delegate": 0.78, "H2": 0.761} | delegate-vs-not split p_delegate=0.78 |
| 32 | db_agent | D1/tool | {"confidence": 0.683, "p_actual": 0.353, "margin": 0.227} | action distribution: get_reservation_details 0.58, search_direct_flight 0.35, no_tool 0.06 (actual: search_direct_flight) |
| 32 | db_agent | D3 | {"checks": ["repeat"], "tool": "search_direct_flight"} | tool search_direct_flight call #28: repeat |
| 32 | db_agent | D3 | {"checks": ["repeat"], "tool": "search_direct_flight"} | tool search_direct_flight call #29: repeat |
| 34 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["error related to the `flight_number` parameter", "failed", "hat069", "hat276"], "altered": ["flight_number_1"]} | db_agent report->planner: missing ['error related to the `flight_number` parameter', 'failed', 'hat069'] altered ['flight_number_1'] |
| 35 | db_agent | D1/tool | {"confidence": 0.723, "p_actual": 0.551, "margin": 0.122} | action distribution: book_reservation 0.55, get_user_details 0.43, no_tool 0.02 (actual: book_reservation) |
| 35 | db_agent | D3 | {"checks": ["error", "repeat"], "tool": "book_reservation"} | tool book_reservation call #31: error, repeat |
| 35 | db_agent | D3/arguments | {"ungrounded_ratio": 0.182} | argument values never given to the agent: book_reservation.user_id=gift_card_12345, book_reservation.user_id=gift_card_67890 |
| 36 | planner | D3 | {"checks": ["error", "repeat", "ignored"], "tool": "db_agent"} | tool db_agent call #32: error, repeat, ignored |
| 37 | planner | D1/tool | {"confidence": 0.454, "p_actual": 0.544, "margin": 0.214} | action distribution: respond_to_user 0.54, policy_checker 0.33, db_agent 0.12 (actual: respond_to_user) |
| 37 | planner | D1/handoff | {"p_delegate": 0.452, "H2": 0.993} | delegate-vs-not split p_delegate=0.45 |
| 40 | db_agent | D3 | {"checks": ["repeat"], "tool": "search_direct_flight"} | tool search_direct_flight call #34: repeat |
| 40 | db_agent | D3 | {"checks": ["repeat"], "tool": "search_direct_flight"} | tool search_direct_flight call #35: repeat |
| 40 | db_agent | D3 | {"checks": ["repeat"], "tool": "search_direct_flight"} | tool search_direct_flight call #36: repeat |
| 40 | db_agent | D3 | {"checks": ["repeat"], "tool": "search_direct_flight"} | tool search_direct_flight call #37: repeat |
| 40 | db_agent | D3 | {"checks": ["repeat"], "tool": "search_direct_flight"} | tool search_direct_flight call #38: repeat |
| 40 | db_agent | D3 | {"checks": ["repeat"], "tool": "search_direct_flight"} | tool search_direct_flight call #39: repeat |
| 40 | db_agent | D3/arguments | {"ungrounded_ratio": 0.333} | argument values never given to the agent: search_direct_flight.airport=LAX, search_direct_flight.airport=SFO, search_direct_flight.airport=SEA, search_direct_flight.airport=LAX, search_direct_flight.airport=SFO |
| 41 | db_agent | D3 | {"checks": ["repeat"], "tool": "search_direct_flight"} | tool search_direct_flight call #40: repeat |
| 41 | db_agent | D3 | {"checks": ["repeat"], "tool": "search_direct_flight"} | tool search_direct_flight call #41: repeat |
| 41 | db_agent | D3 | {"checks": ["repeat"], "tool": "search_direct_flight"} | tool search_direct_flight call #42: repeat |
| 41 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT023, reservation_id=HAT083, reservation_id=HAT041 |
| 42 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT100, reservation_id=HAT041, reservation_id=HAT012, reservation_id=HAT089, reservation_id=HAT228 |
| 45 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["error related to the `flight_number` parameter", "failed", "hat012", "hat041"], "altered": []} | db_agent report->planner: missing ['error related to the `flight_number` parameter', 'failed', 'hat012'] altered [] |
| 46 | db_agent | D1/tool | {"confidence": 0.677, "p_actual": 0.624, "margin": 0.33} | action distribution: book_reservation 0.62, get_user_details 0.29, no_tool 0.06 (actual: book_reservation) |
| 46 | db_agent | D3 | {"checks": ["error"], "tool": "book_reservation"} | tool book_reservation call #45: error |
| 46 | db_agent | D3/arguments | {"ungrounded_ratio": 0.182} | argument values never given to the agent: book_reservation.user_id=gift_card_12345, book_reservation.user_id=gift_card_67890 |
| 47 | planner | D3 | {"checks": ["error", "ignored"], "tool": "db_agent"} | tool db_agent call #46: error, ignored |

## Per-module summary
```
{
 "D1": {
  "n_scored": 42,
  "method": "stepwise"
 },
 "D3": {
  "tool_calls": 48,
  "utterances": 20,
  "checks": {
   "error": 9,
   "ignored": 5,
   "repeat": 13
  }
 },
 "D7": {
  "n_handoffs": 18
 },
 "D3_args": {
  "n_steps": 23,
  "n_values": 149,
  "n_ungrounded": 21
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3_args": "any ungrounded value"}`