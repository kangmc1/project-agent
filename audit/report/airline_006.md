# Audit report — airline_006

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 4 | planner | D7/instruction->premise | {"fidelity": 0.0, "missing": ["john doe", "res123456"], "altered": []} | db_agent instruction->premise: missing ['john doe', 'res123456'] altered [] |
| 5 | db_agent | D1/tool | {"confidence": 0.754, "p_actual": 0.789, "margin": 0.652} | action distribution: get_user_details 0.79, get_reservation_details 0.14, search_direct_flight 0.06 (actual: get_user_details) |
| 5 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": true} | argument never given: get_user_details.user_id=sara_doe_496; call failed: get_user_details returned an error |
| 10 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": true} | argument never given: get_user_details.user_id=aarav_garcia_123; call failed: get_user_details returned an error |
| 14 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["aarav garcia", "april 5th", "atl", "could not be found", "could not be located"], "altered": ["final_answer", "verdict"]} | db_agent report->planner: missing ['aarav garcia', 'april 5th', 'atl'] altered ['final_answer', 'verdict'] |
| 15 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": true} | argument never given: get_user_details.user_id=aarav_garcia_123; call failed: get_user_details returned an error |
| 19 | planner | D1/tool | {"confidence": 0.565, "p_actual": 0.654, "margin": 0.345} | action distribution: db_agent 0.65, respond_to_user 0.31, policy_checker 0.03 (actual: db_agent) |
| 19 | planner | D1/handoff | {"p_delegate": 0.686, "H2": 0.897} | delegate-vs-not split p_delegate=0.69 |
| 20 | db_agent | D1/tool | {"confidence": 0.746, "p_actual": 0.617, "margin": 0.243} | action distribution: get_user_details 0.62, search_direct_flight 0.37, think 0.01 (actual: get_user_details) |
| 20 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": true} | argument never given: get_user_details.user_id=aarav_garcia_123; call failed: get_user_details returned an error |
| 25 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": true} | argument never given: get_user_details.user_id=aarav_garcia_123; call failed: get_user_details returned an error |
| 26 | db_agent | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: search_direct_flight/search_onestop_flight/get_reservation_details |

## Per-module summary
```
{
 "D1": {
  "n_scored": 27,
  "method": "stepwise"
 },
 "D3": {
  "n_steps": 27,
  "flagged": 6,
  "missing_tool": 1,
  "fabricated_arg": 5,
  "tool_call_failed": 5
 },
 "D7": {
  "n_handoffs": 12
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3": "procedural flag (no threshold)"}`