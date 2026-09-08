# Audit report — airline_026

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 4 | planner | D1/tool | {"confidence": 0.615, "p_actual": 0.562, "margin": 0.124} | action distribution: db_agent 0.56, policy_checker 0.44, read_file 0.00 (actual: db_agent) |
| 10 | planner | D1/tool | {"confidence": 0.552, "p_actual": 0.643, "margin": 0.339} | action distribution: policy_checker 0.64, db_agent 0.30, respond_to_user 0.05 (actual: policy_checker) |
| 18 | db_agent | D1/tool | {"confidence": 0.772, "p_actual": 0.821, "margin": 0.704} | action distribution: search_direct_flight 0.82, calculate 0.12, search_onestop_flight 0.04 (actual: search_direct_flight) |
| 21 | db_agent | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_error": false} | required but never called: calculate |
| 26 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": true, "tool_error": true} | argument never given: update_reservation_flights.user_id=credit_card_7334 |
| 27 | db_agent | D1/tool | {"confidence": 0.759, "p_actual": 0.394, "margin": 0.211} | action distribution: no_tool 0.60, get_user_details 0.39, transfer_to_human_agents 0.00 (actual: get_user_details) |
| 29 | db_agent | D1/tool | {"confidence": 0.687, "p_actual": 0.266, "margin": 0.367} | action distribution: no_tool 0.63, read_file 0.27, write_file 0.10 (actual: read_file) |

## Per-module summary
```
{
 "D1": {
  "n_scored": 28,
  "method": "stepwise"
 },
 "D3": {
  "n_steps": 28,
  "flagged": 2,
  "missing_tool": 1,
  "fabricated_arg": 1,
  "tool_error": 1
 },
 "D7": {
  "n_handoffs": 10
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3": "procedural flag (no threshold)"}`