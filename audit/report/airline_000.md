# Audit report — airline_000

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | planner | D1/handoff | {"p_delegate": 0.148, "H2": 0.605} | delegate-vs-not split p_delegate=0.15 |
| 6 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT083, reservation_id=HAT069 |
| 11 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT039, reservation_id=HAT218, reservation_id=HAT136, reservation_id=HAT268 |
| 12 | planner | D3/arguments | {"ungrounded_ratio": 0.273} | argument values never given to the agent: respond_to_user.money=204, respond_to_user.money=255, respond_to_user.money=261 |
| 14 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["/case_notes.md", "failed", "hat039", "hat268", "mia_li_123"], "altered": []} | db_agent report->planner: missing ['/case_notes.md', 'failed', 'hat039'] altered [] |
| 15 | db_agent | D3 | {"checks": ["error"], "tool": "book_reservation"} | tool book_reservation call #8: error |
| 15 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: user_id=mia_li_123 |
| 15 | db_agent | D3/arguments | {"ungrounded_ratio": 0.25} | argument values never given to the agent: book_reservation.user_id=mia_li_123, book_reservation.airport=SFO |
| 16 | db_agent | D3 | {"checks": ["error"], "tool": "read_file"} | tool read_file call #9: error |
| 16 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: user_id=mia_li_123 |
| 18 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: user_id=mia_li_123 |
| 22 | db_agent | D3 | {"checks": ["error"], "tool": "book_reservation"} | tool book_reservation call #13: error |
| 22 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: user_id=mia_li_3668 |
| 22 | db_agent | D3/arguments | {"ungrounded_ratio": 0.143} | argument values never given to the agent: book_reservation.airport=SFO |
| 23 | planner | D3 | {"checks": ["error", "ignored"], "tool": "db_agent"} | tool db_agent call #14: error, ignored |
| 23 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: user_id=mia_li_3668 |
| 32 | db_agent | D3 | {"checks": ["repeat"], "tool": "search_onestop_flight"} | tool search_onestop_flight call #19: repeat |
| 37 | db_agent | D3 | {"checks": ["repeat"], "tool": "search_onestop_flight"} | tool search_onestop_flight call #22: repeat |
| 38 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT218, reservation_id=HAT136 |
| 39 | planner | D3/arguments | {"ungrounded_ratio": 0.25} | argument values never given to the agent: respond_to_user.money=261, respond_to_user.money=255 |
| 42 | db_agent | D3 | {"checks": ["error"], "tool": "book_reservation"} | tool book_reservation call #25: error |
| 42 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: user_id=mia_li_3668 |
| 42 | db_agent | D3/arguments | {"ungrounded_ratio": 0.125} | argument values never given to the agent: book_reservation.airport=SFO |
| 43 | db_agent | D1/tool | {"confidence": 0.738, "p_actual": 0.613, "margin": 0.241} | action distribution: write_file 0.61, read_file 0.37, think 0.01 (actual: write_file) |
| 44 | planner | D3 | {"checks": ["error", "ignored"], "tool": "db_agent"} | tool db_agent call #27: error, ignored |
| 44 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: user_id=mia_li_3668 |
| 47 | planner | D1/tool | {"confidence": 0.51, "p_actual": 0.692, "margin": 0.494} | action distribution: read_file 0.69, write_file 0.20, db_agent 0.09 (actual: read_file) |
| 47 | planner | D1/handoff | {"p_delegate": 0.098, "H2": 0.464} | delegate-vs-not split p_delegate=0.10 |
| 47 | planner | D3 | {"checks": ["error", "ignored"], "tool": "read_file"} | tool read_file call #29: error, ignored |
| 48 | planner | D1/tool | {"confidence": 0.572, "p_actual": 0.655, "margin": 0.346} | action distribution: db_agent 0.66, respond_to_user 0.31, policy_checker 0.03 (actual: db_agent) |
| 48 | planner | D1/handoff | {"p_delegate": 0.688, "H2": 0.895} | delegate-vs-not split p_delegate=0.69 |
| 53 | db_agent | D3 | {"checks": ["repeat"], "tool": "search_onestop_flight"} | tool search_onestop_flight call #32: repeat |
| 57 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["4", "before 10am est", "with departure time after 10am est on the requested dates"], "altered": []} | db_agent report->planner: missing ['4', 'before 10am est', 'with departure time after 10am est on the requested dates'] altered [] |
| 63 | db_agent | D3 | {"checks": ["repeat"], "tool": "search_onestop_flight"} | tool search_onestop_flight call #39: repeat |
| 69 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT218 |
| 70 | planner | D3/arguments | {"ungrounded_ratio": 0.4} | argument values never given to the agent: respond_to_user.money=234, respond_to_user.money=242, respond_to_user.money=315, respond_to_user.money=301 |
| 73 | db_agent | D3 | {"checks": ["error"], "tool": "book_reservation"} | tool book_reservation call #46: error |
| 73 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: user_id=mia_li_3668 |
| 73 | db_agent | D3/arguments | {"ungrounded_ratio": 0.125} | argument values never given to the agent: book_reservation.airport=SFO |
| 74 | planner | D3 | {"checks": ["error", "ignored"], "tool": "db_agent"} | tool db_agent call #47: error, ignored |
| 74 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: user_id=mia_li_3668 |
| 78 | db_agent | D3 | {"checks": ["repeat"], "tool": "search_onestop_flight"} | tool search_onestop_flight call #49: repeat |
| 79 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT218 |
| 80 | planner | D3/arguments | {"ungrounded_ratio": 0.25} | argument values never given to the agent: respond_to_user.money=234, respond_to_user.money=242 |
| 83 | db_agent | D3 | {"checks": ["error", "repeat"], "tool": "book_reservation"} | tool book_reservation call #52: error, repeat |
| 83 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: user_id=mia_li_3668 |
| 83 | db_agent | D3/arguments | {"ungrounded_ratio": 0.125} | argument values never given to the agent: book_reservation.airport=SFO |
| 84 | planner | D3 | {"checks": ["error", "repeat", "ignored"], "tool": "db_agent"} | tool db_agent call #53: error, repeat, ignored |
| 84 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: user_id=mia_li_3668 |
| 87 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["credit_card_7815826", "failed", "hat218 + hat039", "invalid or missing payment method", "may 18th"], "altered": []} | db_agent report->planner: missing ['credit_card_7815826', 'failed', 'hat218 + hat039'] altered [] |
| 88 | db_agent | D3 | {"checks": ["error"], "tool": "book_reservation"} | tool book_reservation call #55: error |
| 88 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: user_id=mia_li_3668 |
| 89 | planner | D3 | {"checks": ["error", "ignored"], "tool": "db_agent"} | tool db_agent call #56: error, ignored |
| 89 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: user_id=mia_li_3668 |
| 92 | planner | D1/tool | {"confidence": 0.633, "p_actual": 0.676, "margin": 0.357} | action distribution: db_agent 0.68, policy_checker 0.32, respond_to_user 0.00 (actual: db_agent) |
| 92 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["investigate further and attempt to resolve the issue", "still failing", "the payment_id parameter", "transfer the case to a human agent for assistance"], "altered": []} | db_agent report->planner: missing ['investigate further and attempt to resolve the issue', 'still failing', 'the payment_id parameter'] altered [] |
| 93 | db_agent | D1/tool | {"confidence": 0.76, "p_actual": 0.778, "margin": 0.604} | action distribution: get_user_details 0.78, get_reservation_details 0.17, update_reservation_flights 0.04 (actual: get_user_details) |
| 94 | db_agent | D1/tool | {"confidence": 0.775, "p_actual": 0.808, "margin": 0.699} | action distribution: book_reservation 0.81, get_reservation_details 0.11, no_tool 0.08 (actual: book_reservation) |
| 94 | db_agent | D3 | {"checks": ["error"], "tool": "book_reservation"} | tool book_reservation call #59: error |
| 95 | db_agent | D3 | {"checks": ["error", "schema"], "tool": "book_reservation"} | tool book_reservation call #60: error, schema; schema: ['unknown:payment_id'] |
| 99 | planner | D1/tool | {"confidence": 0.483, "p_actual": 0.347, "margin": 0.205} | action distribution: no_tool 0.55, respond_to_user 0.35, write_file 0.10 (actual: respond_to_user) |

## Per-module summary
```
{
 "D1": {
  "n_scored": 80,
  "method": "stepwise"
 },
 "D3": {
  "tool_calls": 63,
  "utterances": 29,
  "checks": {
   "error": 15,
   "ignored": 6,
   "repeat": 7,
   "schema": 1
  }
 },
 "D7": {
  "n_handoffs": 36
 },
 "D3_args": {
  "n_steps": 36,
  "n_values": 192,
  "n_ungrounded": 17
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3_args": "any ungrounded value"}`