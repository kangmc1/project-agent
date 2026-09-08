# Audit report — airline_017

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 4 | planner | D1/tool | {"confidence": 0.637, "p_actual": 0.721, "margin": 0.456} | action distribution: db_agent 0.72, respond_to_user 0.27, policy_checker 0.01 (actual: db_agent) |
| 4 | planner | D1/handoff | {"p_delegate": 0.734, "H2": 0.835} | delegate-vs-not split p_delegate=0.73 |
| 13 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT286, reservation_id=HAT112, reservation_id=HAT047, reservation_id=HAT190 |
| 17 | db_agent | D1/tool | {"confidence": 0.477, "p_actual": 0.37, "margin": 0.146} | action distribution: search_direct_flight 0.37, book_reservation 0.22, get_reservation_details 0.22 (actual: search_direct_flight) |
| 17 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT112, reservation_id=HAT047 |
| 17 | db_agent | D3/arguments | {"ungrounded_ratio": 0.333} | argument values never given to the agent: search_direct_flight.date=2024-05-01, search_direct_flight.date=2024-05-01 |
| 18 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT112, reservation_id=HAT047 |
| 18 | db_agent | D3/arguments | {"ungrounded_ratio": 0.333} | argument values never given to the agent: search_onestop_flight.date=2024-05-01, search_onestop_flight.date=2024-05-01 |
| 19 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT112, reservation_id=HAT047 |
| 21 | planner | D1/tool | {"confidence": 0.557, "p_actual": 0.55, "margin": 0.121} | action distribution: read_file 0.55, respond_to_user 0.43, policy_checker 0.01 (actual: read_file) |
| 25 | db_agent | D1/tool | {"confidence": 0.621, "p_actual": 0.409, "margin": 0.019} | action distribution: no_tool 0.43, search_direct_flight 0.41, get_reservation_details 0.15 (actual: search_direct_flight) |
| 25 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT112, reservation_id=HAT047 |
| 26 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT112, reservation_id=HAT047, money=121 |
| 30 | db_agent | D3 | {"checks": ["repeat"], "tool": "search_direct_flight"} | tool search_direct_flight call #22: repeat |
| 30 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: money=100 |
| 31 | db_agent | D3 | {"checks": ["repeat"], "tool": "search_onestop_flight"} | tool search_onestop_flight call #23: repeat |
| 31 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: money=100 |
| 32 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT286, reservation_id=HAT112, reservation_id=HAT047, reservation_id=HAT190, money=120 |
| 36 | db_agent | D1/tool | {"confidence": 0.69, "p_actual": 0.419, "margin": 0.119} | action distribution: get_reservation_details 0.54, calculate 0.42, think 0.02 (actual: calculate) |
| 36 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT112, reservation_id=HAT047 |
| 37 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT112, reservation_id=HAT047 |
| 41 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: money=100 |
| 43 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT286, reservation_id=HAT112, reservation_id=HAT047, reservation_id=HAT190, money=938 |
| 47 | db_agent | D1/tool | {"confidence": 0.734, "p_actual": 0.674, "margin": 0.377} | action distribution: get_reservation_details 0.67, search_direct_flight 0.30, search_onestop_flight 0.02 (actual: get_reservation_details) |
| 47 | db_agent | D3 | {"checks": ["error"], "tool": "get_reservation_details"} | tool get_reservation_details call #35: error |
| 48 | planner | D3 | {"checks": ["error", "ignored"], "tool": "db_agent"} | tool db_agent call #36: error, ignored |
| 52 | db_agent | D3 | {"checks": ["error"], "tool": "get_user_details"} | tool get_user_details call #38: error |
| 52 | db_agent | D3/arguments | {"ungrounded_ratio": 1.0} | argument values never given to the agent: get_user_details.user_id=liam_khan_123 |
| 59 | db_agent | D3 | {"checks": ["repeat"], "tool": "read_file"} | tool read_file call #43: repeat |
| 62 | planner | D1/tool | {"confidence": 0.471, "p_actual": 0.559, "margin": 0.22} | action distribution: db_agent 0.56, respond_to_user 0.34, write_file 0.10 (actual: db_agent) |
| 62 | planner | D1/handoff | {"p_delegate": 0.559, "H2": 0.99} | delegate-vs-not split p_delegate=0.56 |
| 63 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #46: repeat |
| 64 | db_agent | D1/tool | {"confidence": 0.752, "p_actual": 0.554, "margin": 0.11} | action distribution: search_direct_flight 0.55, no_tool 0.44, update_reservation_flights 0.00 (actual: search_direct_flight) |
| 65 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT112, reservation_id=HAT131 |
| 67 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT082, reservation_id=HAT121, reservation_id=HAT011, reservation_id=HAT278, reservation_id=HAT258 |
| 68 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: update_passengers= |
| 71 | planner | D3 | {"satisfied": false} | claims without prior tool evidence: money=440 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 59,
  "method": "stepwise"
 },
 "D3": {
  "tool_calls": 52,
  "utterances": 27,
  "checks": {
   "repeat": 4,
   "error": 3,
   "ignored": 1
  }
 },
 "D7": {
  "n_handoffs": 22
 },
 "D3_args": {
  "n_steps": 35,
  "n_values": 148,
  "n_ungrounded": 5
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3_args": "any ungrounded value"}`