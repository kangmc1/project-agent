# Audit report — airline_032

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 12 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_user_details"} | tool get_user_details call #8: repeat |
| 13 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #9: repeat |
| 14 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #10: repeat |
| 16 | planner | D1/tool | {"confidence": 0.649, "p_actual": 0.679, "margin": 0.358} | action distribution: db_agent 0.68, respond_to_user 0.32, no_tool 0.00 (actual: db_agent) |
| 16 | planner | D1/handoff | {"p_delegate": 0.679, "H2": 0.905} | delegate-vs-not split p_delegate=0.68 |
| 17 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_user_details"} | tool get_user_details call #12: repeat |
| 18 | db_agent | D2 | {"s": 0.3333333333333333, "unsupported": 0.6666666666666667} | values not found in any prior tool result: ['NM1VX1', 'KC18K6', 'S61CZX', 'H8Q05L', 'WUNA5K'], Check each reservation for flights on May 10 |
| 18 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #13: repeat |
| 19 | db_agent | D2 | {"s": 0.3333333333333333, "unsupported": 0.6666666666666667} | values not found in any prior tool result: 'NM1VX1', 1 of 5 reservations checked |
| 19 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #14: repeat |
| 20 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #15: repeat |
| 21 | db_agent | D2 | {"s": 0.3333333333333333, "unsupported": 0.6666666666666667} | values not found in any prior tool result: 'S61CZX', 3 of 5 reservations checked |
| 21 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #16: repeat |
| 23 | db_agent | D1/tool | {"confidence": 0.718, "p_actual": 0.714, "margin": 0.51} | action distribution: write_file 0.71, read_file 0.20, no_tool 0.07 (actual: write_file) |
| 26 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #20: repeat |
| 30 | planner | D1/handoff | {"p_delegate": 0.191, "H2": 0.704} | delegate-vs-not split p_delegate=0.19 |
| 33 | policy_checker | D3 | {"checks": ["empty"], "tool": "think"} | tool think call #25: empty |
| 39 | policy_checker | D3 | {"satisfied": false} | claims without prior tool evidence: date=2024-05-15 |
| 40 | planner | D1/handoff | {"p_delegate": 0.182, "H2": 0.685} | delegate-vs-not split p_delegate=0.18 |
| 43 | db_agent | D1/tool | {"confidence": 0.694, "p_actual": 0.543, "margin": 0.12} | action distribution: search_direct_flight 0.54, book_reservation 0.42, calculate 0.02 (actual: search_direct_flight) |
| 46 | planner | D1/handoff | {"p_delegate": 0.818, "H2": 0.685} | delegate-vs-not split p_delegate=0.82 |
| 47 | db_agent | D3 | {"checks": ["error"], "tool": "get_reservation_details"} | tool get_reservation_details call #34: error |
| 48 | db_agent | D3 | {"checks": ["repeat"], "tool": "search_direct_flight"} | tool search_direct_flight call #35: repeat |
| 49 | planner | D3 | {"checks": ["error", "ignored"], "tool": "db_agent"} | tool db_agent call #36: error, ignored |
| 54 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT139, reservation_id=HAT289 |
| 58 | db_agent | D3 | {"checks": ["error"], "tool": "book_reservation"} | tool book_reservation call #41: error |
| 59 | db_agent | D1/tool | {"confidence": 0.651, "p_actual": 0.574, "margin": 0.226} | action distribution: think 0.57, transfer_to_human_agents 0.35, no_tool 0.05 (actual: think) |
| 59 | db_agent | D3 | {"checks": ["empty"], "tool": "think"} | tool think call #42: empty |
| 59 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: user_id=sophia_silva_123 |
| 60 | db_agent | D3 | {"checks": ["error"], "tool": "get_user_details"} | tool get_user_details call #43: error |
| 61 | planner | D3 | {"checks": ["error", "ignored"], "tool": "db_agent"} | tool db_agent call #44: error, ignored |
| 65 | db_agent | D1/tool | {"confidence": 0.659, "p_actual": 0.508, "margin": 0.112} | action distribution: search_direct_flight 0.51, book_reservation 0.40, calculate 0.09 (actual: search_direct_flight) |
| 65 | db_agent | D3 | {"checks": ["repeat"], "tool": "search_direct_flight"} | tool search_direct_flight call #46: repeat |
| 67 | planner | D1/handoff | {"p_delegate": 0.27, "H2": 0.842} | delegate-vs-not split p_delegate=0.27 |
| 70 | db_agent | D3 | {"checks": ["repeat"], "tool": "search_direct_flight"} | tool search_direct_flight call #49: repeat |
| 71 | db_agent | D3 | {"checks": ["error"], "tool": "book_reservation"} | tool book_reservation call #50: error |
| 71 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT139, money=322 |
| 72 | db_agent | D3 | {"checks": ["error"], "tool": "book_reservation"} | tool book_reservation call #51: error |
| 73 | db_agent | D3 | {"checks": ["error", "repeat"], "tool": "book_reservation"} | tool book_reservation call #52: error, repeat |
| 75 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["payment_id", "required parameter `payment_id` was missing"], "altered": []} | db_agent report->planner: missing ['payment_id', 'required parameter `payment_id` was missing'] altered [] |
| 76 | db_agent | D1/tool | {"confidence": 0.639, "p_actual": 0.591, "margin": 0.312} | action distribution: book_reservation 0.59, calculate 0.28, search_direct_flight 0.10 (actual: book_reservation) |
| 76 | db_agent | D3 | {"checks": ["error"], "tool": "book_reservation"} | tool book_reservation call #54: error |
| 86 | planner | D1/tool | {"confidence": 0.61, "p_actual": 0.465, "margin": 0.069} | action distribution: no_tool 0.53, respond_to_user 0.46, write_file 0.00 (actual: respond_to_user) |

## Per-module summary
```
{
 "D1": {
  "n_scored": 75,
  "method": "stepwise"
 },
 "D2": {
  "n_utterances": 48,
  "n_na": 4
 },
 "D3": {
  "tool_calls": 60,
  "utterances": 45,
  "checks": {
   "repeat": 13,
   "empty": 2,
   "error": 9,
   "ignored": 2
  }
 },
 "D7": {
  "n_handoffs": 28
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`