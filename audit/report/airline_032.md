# Audit report — airline_032

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 16 | planner | D1/tool | {"confidence": 0.649, "p_actual": 0.679, "margin": 0.358} | action distribution: db_agent 0.68, respond_to_user 0.32, no_tool 0.00 (actual: db_agent) |
| 16 | planner | D1/handoff | {"p_delegate": 0.679, "H2": 0.905} | delegate-vs-not split p_delegate=0.68 |
| 23 | db_agent | D1/tool | {"confidence": 0.718, "p_actual": 0.714, "margin": 0.51} | action distribution: write_file 0.71, read_file 0.20, no_tool 0.07 (actual: write_file) |
| 29 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: get_user_details |
| 30 | planner | D1/handoff | {"p_delegate": 0.191, "H2": 0.704} | delegate-vs-not split p_delegate=0.19 |
| 40 | planner | D1/handoff | {"p_delegate": 0.182, "H2": 0.685} | delegate-vs-not split p_delegate=0.18 |
| 43 | db_agent | D1/tool | {"confidence": 0.694, "p_actual": 0.543, "margin": 0.12} | action distribution: search_direct_flight 0.54, book_reservation 0.42, calculate 0.02 (actual: search_direct_flight) |
| 45 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: calculate |
| 46 | planner | D1/handoff | {"p_delegate": 0.818, "H2": 0.685} | delegate-vs-not split p_delegate=0.82 |
| 47 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: get_reservation_details returned an error |
| 58 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": true} | argument never given: book_reservation.user_id=sophia_silva_123, book_reservation.airport=SFO, book_reservation.airport=JFK; call failed: book_reservation returned an error |
| 59 | db_agent | D1/tool | {"confidence": 0.651, "p_actual": 0.574, "margin": 0.226} | action distribution: think 0.57, transfer_to_human_agents 0.35, no_tool 0.05 (actual: think) |
| 60 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": true} | argument never given: get_user_details.user_id=sophia_silva_123; call failed: get_user_details returned an error |
| 61 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: calculate |
| 65 | db_agent | D1/tool | {"confidence": 0.659, "p_actual": 0.508, "margin": 0.112} | action distribution: search_direct_flight 0.51, book_reservation 0.40, calculate 0.09 (actual: search_direct_flight) |
| 66 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: book_reservation, calculate |
| 67 | planner | D1/handoff | {"p_delegate": 0.27, "H2": 0.842} | delegate-vs-not split p_delegate=0.27 |
| 71 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: book_reservation returned an error |
| 72 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: book_reservation returned an error |
| 73 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: book_reservation returned an error |
| 74 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: calculate |
| 75 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["payment_id", "required parameter `payment_id` was missing"], "altered": []} | db_agent report->planner: missing ['payment_id', 'required parameter `payment_id` was missing'] altered [] |
| 76 | db_agent | D1/tool | {"confidence": 0.639, "p_actual": 0.591, "margin": 0.312} | action distribution: book_reservation 0.59, calculate 0.28, search_direct_flight 0.10 (actual: book_reservation) |
| 76 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: book_reservation returned an error |
| 77 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: calculate |
| 86 | planner | D1/tool | {"confidence": 0.61, "p_actual": 0.465, "margin": 0.069} | action distribution: no_tool 0.53, respond_to_user 0.46, write_file 0.00 (actual: respond_to_user) |

## Per-module summary
```
{
 "D1": {
  "n_scored": 75,
  "method": "stepwise"
 },
 "D2": {
  "n_steps": 75,
  "flagged": 13,
  "missing_tool": 6,
  "fabricated_arg": 2,
  "tool_call_failed": 7
 },
 "D3": {
  "n_handoffs": 28
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D3": 1.0, "D2": "procedural flag (no threshold)"}`