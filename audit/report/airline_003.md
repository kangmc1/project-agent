# Audit report — airline_003

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 4 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["flight from houston to denver on may 27th", "successfully recorded"], "altered": []} | db_agent report->planner: missing ['flight from houston to denver on may 27th', 'successfully recorded'] altered [] |
| 7 | db_agent | D1/tool | {"confidence": 0.699, "p_actual": 0.377, "margin": 0.194} | action distribution: no_tool 0.57, write_file 0.38, read_file 0.05 (actual: write_file) |
| 10 | planner | D1/handoff | {"p_delegate": 0.851, "H2": 0.608} | delegate-vs-not split p_delegate=0.85 |
| 10 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["2024-05-15 15:00:00 est", "need_info", "unknown"], "altered": ["reservation_id"]} | policy_checker report->planner: missing ['2024-05-15 15:00:00 est', 'need_info', 'unknown'] altered ['reservation_id'] |
| 11 | policy_checker | D1/tool | {"confidence": 0.502, "p_actual": 0.37, "margin": 0.255} | action distribution: no_tool 0.62, think 0.37, read_file 0.01 (actual: think) |
| 15 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["gift card", "modify flight and baggage policy clauses; need reservation id cabin class and reservation type to determine eligibility for modification and baggage allowance", "need_info", "no membership tier"], "altered": []} | policy_checker report->planner: missing ['gift card', 'modify flight and baggage policy clauses; need reservation id cabin class and reservation type to determine eligibility for modification and baggage allowance', 'need_info'] altered [] |
| 17 | planner | D1/tool | {"confidence": 0.454, "p_actual": 0.568, "margin": 0.3} | action distribution: respond_to_user 0.57, db_agent 0.27, read_file 0.16 (actual: respond_to_user) |
| 17 | planner | D1/handoff | {"p_delegate": 0.268, "H2": 0.839} | delegate-vs-not split p_delegate=0.27 |
| 22 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: update_reservation_flights returned an error |
| 23 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: update_reservation_flights returned an error |
| 24 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: update_reservation_baggages |
| 25 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["04:00", "1", "13:00", "changes have been recorded in the case notes", "den"], "altered": []} | db_agent report->planner: missing ['04:00', '1', '13:00'] altered [] |
| 29 | db_agent | D1/tool | {"confidence": 0.537, "p_actual": 0.372, "margin": 0.056} | action distribution: write_file 0.37, no_tool 0.32, read_file 0.18 (actual: write_file) |
| 31 | planner | D1/tool | {"confidence": 0.566, "p_actual": 0.549, "margin": 0.12} | action distribution: read_file 0.55, respond_to_user 0.43, no_tool 0.02 (actual: read_file) |

## Per-module summary
```
{
 "D1": {
  "n_scored": 29,
  "method": "stepwise"
 },
 "D2": {
  "n_steps": 29,
  "flagged": 3,
  "missing_tool": 1,
  "fabricated_arg": 0,
  "tool_call_failed": 2
 },
 "D3": {
  "n_handoffs": 10
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D3": 1.0, "D2": "procedural flag (no threshold)"}`