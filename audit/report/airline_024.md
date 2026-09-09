# Audit report — airline_024

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | planner | D1/tool | {"confidence": 0.629, "p_actual": 0.622, "margin": 0.245} | action distribution: db_agent 0.62, respond_to_user 0.38, no_tool 0.00 (actual: db_agent) |
| 2 | planner | D1/handoff | {"p_delegate": 0.622, "H2": 0.956} | delegate-vs-not split p_delegate=0.62 |
| 7 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["need_info"], "altered": []} | policy_checker report->planner: missing ['need_info'] altered [] |
| 11 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["hxdubj", "verified booking code association", "yara_garcia_1905"], "altered": []} | db_agent report->planner: missing ['hxdubj', 'verified booking code association', 'yara_garcia_1905'] altered [] |
| 19 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["/case_notes.md", "could not proceed", "successfully written"], "altered": []} | db_agent report->planner: missing ['/case_notes.md', 'could not proceed', 'successfully written'] altered [] |
| 20 | db_agent | D1/tool | {"confidence": 0.65, "p_actual": 0.553, "margin": 0.217} | action distribution: get_reservation_details 0.55, calculate 0.34, no_tool 0.09 (actual: get_reservation_details) |
| 20 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: get_reservation_details returned an error; call failed: get_reservation_details returned an error |
| 23 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: search_direct_flight/search_onestop_flight/book_reservation/calculate, update_reservation_baggages, calculate |
| 24 | planner | D1/tool | {"confidence": 0.581, "p_actual": 0.495, "margin": 0.0} | action distribution: db_agent 0.49, respond_to_user 0.49, no_tool 0.01 (actual: respond_to_user) |
| 24 | planner | D1/handoff | {"p_delegate": 0.496, "H2": 1.0} | delegate-vs-not split p_delegate=0.50 |
| 30 | planner | D1/handoff | {"p_delegate": 0.904, "H2": 0.456} | delegate-vs-not split p_delegate=0.90 |
| 32 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: search_direct_flight/search_onestop_flight/book_reservation/calculate, update_reservation_baggages, calculate |
| 35 | planner | D1/tool | {"confidence": 0.649, "p_actual": 0.679, "margin": 0.358} | action distribution: db_agent 0.68, policy_checker 0.32, no_tool 0.00 (actual: db_agent) |
| 39 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: update_reservation_baggages returned an error |
| 40 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: calculate |
| 41 | planner | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": false} | argument never given: respond_to_user.money=539 |
| 44 | policy_checker | D1/tool | {"confidence": 0.624, "p_actual": 0.835, "margin": 0.69} | action distribution: write_file 0.83, think 0.15, read_file 0.02 (actual: write_file) |
| 48 | planner | D1/tool | {"confidence": 0.566, "p_actual": 0.726, "margin": 0.543} | action distribution: respond_to_user 0.73, policy_checker 0.18, db_agent 0.09 (actual: respond_to_user) |
| 48 | planner | D1/handoff | {"p_delegate": 0.27, "H2": 0.842} | delegate-vs-not split p_delegate=0.27 |
| 50 | planner | D1/tool | {"confidence": 0.589, "p_actual": 0.614, "margin": 0.242} | action distribution: respond_to_user 0.61, db_agent 0.37, no_tool 0.01 (actual: respond_to_user) |
| 50 | planner | D1/handoff | {"p_delegate": 0.374, "H2": 0.954} | delegate-vs-not split p_delegate=0.37 |
| 52 | planner | D1/tool | {"confidence": 0.48, "p_actual": 0.724, "margin": 0.598} | action distribution: respond_to_user 0.72, write_file 0.13, no_tool 0.08 (actual: respond_to_user) |
| 54 | planner | D1/tool | {"confidence": 0.605, "p_actual": 0.749, "margin": 0.556} | action distribution: no_tool 0.75, respond_to_user 0.19, write_file 0.06 (actual: no_tool) |

## Per-module summary
```
{
 "D1": {
  "n_scored": 43,
  "method": "stepwise"
 },
 "D2": {
  "n_steps": 43,
  "flagged": 6,
  "missing_tool": 3,
  "fabricated_arg": 1,
  "tool_call_failed": 2
 },
 "D3": {
  "n_handoffs": 18
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D3": 1.0, "D2": "procedural flag (no threshold)"}`