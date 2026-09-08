# Audit report — airline_013

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 12 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["cannot be modified under the airline's policy", "modify flight policy: basic economy flights cannot be modified.", "needs to confirm if they want to proceed with the upgrade if allowed", "not_allowed", "permitted but the user must pay the price difference"], "altered": []} | policy_checker report->planner: missing ["cannot be modified under the airline's policy", 'modify flight policy: basic economy flights cannot be modified.', 'needs to confirm if they want to proceed with the upgrade if allowed'] altered [] |
| 13 | policy_checker | D1/tool | {"confidence": 0.652, "p_actual": 0.183, "margin": 0.633} | action distribution: no_tool 0.82, think 0.18, read_file 0.00 (actual: think) |
| 15 | planner | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": false} | argument never given: respond_to_user.money=121, respond_to_user.money=71 |
| 19 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: update_reservation_flights returned an error |
| 23 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: calculate |
| 31 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: update_reservation_flights returned an error |
| 33 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: search_direct_flight/search_onestop_flight/book_reservation/calculate, calculate |

## Per-module summary
```
{
 "D1": {
  "n_scored": 30,
  "method": "stepwise"
 },
 "D2": {
  "n_steps": 30,
  "flagged": 5,
  "missing_tool": 2,
  "fabricated_arg": 1,
  "tool_call_failed": 2
 },
 "D3": {
  "n_handoffs": 12
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D3": 1.0, "D2": "procedural flag (no threshold)"}`