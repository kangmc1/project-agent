# Audit report — airline_019

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["successfully retrieved and recorded in the case notes", "va5sgq"], "altered": []} | db_agent report->planner: missing ['successfully retrieved and recorded in the case notes', 'va5sgq'] altered [] |
| 4 | db_agent | D1/tool | {"confidence": 0.626, "p_actual": 0.471, "margin": 0.185} | action distribution: read_file 0.47, write_file 0.29, no_tool 0.24 (actual: read_file) |
| 6 | db_agent | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_error": false} | required but never called: search_direct_flight/search_onestop_flight |
| 8 | planner | D1/tool | {"confidence": 0.64, "p_actual": 0.656, "margin": 0.312} | action distribution: no_tool 0.66, respond_to_user 0.34, policy_checker 0.00 (actual: no_tool) |

## Per-module summary
```
{
 "D1": {
  "n_scored": 7,
  "method": "stepwise"
 },
 "D3": {
  "n_steps": 7,
  "flagged": 1,
  "missing_tool": 1,
  "fabricated_arg": 0,
  "tool_error": 1
 },
 "D7": {
  "n_handoffs": 2
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3": "procedural flag (no threshold)"}`