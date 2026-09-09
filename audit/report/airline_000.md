# Audit report — airline_000

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | planner | D1/handoff | {"p_delegate": 0.148, "H2": 0.605} | delegate-vs-not split p_delegate=0.15 |
| 12 | planner | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": false} | argument never given: respond_to_user.money=204, respond_to_user.money=255, respond_to_user.money=261 |
| 14 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["/case_notes.md", "failed", "hat039", "hat268", "mia_li_123"], "altered": []} | db_agent report->planner: missing ['/case_notes.md', 'failed', 'hat039'] altered [] |
| 15 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": true} | argument never given: book_reservation.user_id=mia_li_123, book_reservation.airport=SFO; call failed: book_reservation returned an error |
| 22 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": true} | argument never given: book_reservation.airport=SFO; call failed: book_reservation returned an error |
| 31 | planner | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": false} | db_agent: re-issued after a failure report (similarity 0.86): 'Find one-stop economy flights from New York to Seattle on May 20th with departure time between 10am ' |
| 39 | planner | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": false} | argument never given: respond_to_user.money=261, respond_to_user.money=255 |
| 42 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": true} | argument never given: book_reservation.airport=SFO; call failed: book_reservation returned an error |
| 43 | db_agent | D1/tool | {"confidence": 0.738, "p_actual": 0.613, "margin": 0.241} | action distribution: write_file 0.61, read_file 0.37, think 0.01 (actual: write_file) |
| 47 | planner | D1/tool | {"confidence": 0.51, "p_actual": 0.692, "margin": 0.494} | action distribution: read_file 0.69, write_file 0.20, db_agent 0.09 (actual: read_file) |
| 47 | planner | D1/handoff | {"p_delegate": 0.098, "H2": 0.464} | delegate-vs-not split p_delegate=0.10 |
| 48 | planner | D1/tool | {"confidence": 0.572, "p_actual": 0.655, "margin": 0.346} | action distribution: db_agent 0.66, respond_to_user 0.31, policy_checker 0.03 (actual: db_agent) |
| 48 | planner | D1/handoff | {"p_delegate": 0.688, "H2": 0.895} | delegate-vs-not split p_delegate=0.69 |
| 49 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: get_reservation_details/get_user_details |
| 57 | planner | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": false} | db_agent: re-issued after a failure report (similarity 0.82): 'Find one-stop economy flights from New York to Seattle on dates near May 20th (e.g., May 19th, May 2' |
| 57 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["4", "before 10am est", "with departure time after 10am est on the requested dates"], "altered": []} | db_agent report->planner: missing ['4', 'before 10am est', 'with departure time after 10am est on the requested dates'] altered [] |
| 70 | planner | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": false} | argument never given: respond_to_user.money=234, respond_to_user.money=242, respond_to_user.money=315, respond_to_user.money=301 |
| 73 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": true} | argument never given: book_reservation.airport=SFO; call failed: book_reservation returned an error |
| 80 | planner | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": false} | argument never given: respond_to_user.money=234, respond_to_user.money=242 |
| 83 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": true} | argument never given: book_reservation.airport=SFO; call failed: book_reservation returned an error |
| 87 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["credit_card_7815826", "failed", "hat218 + hat039", "invalid or missing payment method", "may 18th"], "altered": []} | db_agent report->planner: missing ['credit_card_7815826', 'failed', 'hat218 + hat039'] altered [] |
| 88 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: book_reservation returned an error |
| 92 | planner | D1/tool | {"confidence": 0.633, "p_actual": 0.676, "margin": 0.357} | action distribution: db_agent 0.68, policy_checker 0.32, respond_to_user 0.00 (actual: db_agent) |
| 92 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["investigate further and attempt to resolve the issue", "still failing", "the payment_id parameter", "transfer the case to a human agent for assistance"], "altered": []} | db_agent report->planner: missing ['investigate further and attempt to resolve the issue', 'still failing', 'the payment_id parameter'] altered [] |
| 93 | db_agent | D1/tool | {"confidence": 0.76, "p_actual": 0.778, "margin": 0.604} | action distribution: get_user_details 0.78, get_reservation_details 0.17, update_reservation_flights 0.04 (actual: get_user_details) |
| 94 | db_agent | D1/tool | {"confidence": 0.775, "p_actual": 0.808, "margin": 0.699} | action distribution: book_reservation 0.81, get_reservation_details 0.11, no_tool 0.08 (actual: book_reservation) |
| 94 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: book_reservation returned an error |
| 95 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: book_reservation returned an error |
| 96 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: send_certificate |
| 99 | planner | D1/tool | {"confidence": 0.483, "p_actual": 0.347, "margin": 0.205} | action distribution: no_tool 0.55, respond_to_user 0.35, write_file 0.10 (actual: respond_to_user) |

## Per-module summary
```
{
 "D1": {
  "n_scored": 80,
  "method": "stepwise"
 },
 "D2": {
  "n_steps": 80,
  "flagged": 16,
  "missing_tool": 2,
  "fabricated_arg": 9,
  "tool_call_failed": 8
 },
 "D3": {
  "n_handoffs": 36
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D3": 1.0, "D2": "procedural flag (no threshold)"}`