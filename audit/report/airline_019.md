# Audit report — airline_019

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["reservation ID VA5SGQ", "reservation details successfully retrieved", "reservation details recorded in case notes"], "altered": []} | db_agent report->planner: missing ['reservation ID VA5SGQ', 'reservation details successfully retrieved', 'reservation details recorded in case notes'] altered [] |
| 4 | db_agent | D1/tool | {"confidence": 0.626, "p_actual": 0.471, "margin": 0.185} | action distribution: read_file 0.47, write_file 0.29, no_tool 0.24 (actual: read_file) |
| 8 | planner | D1/tool | {"confidence": 0.64, "p_actual": 0.656, "margin": 0.312} | action distribution: no_tool 0.66, respond_to_user 0.34, policy_checker 0.00 (actual: no_tool) |

## Per-module summary
```
{
 "D1": {
  "n_scored": 7,
  "method": "stepwise"
 },
 "D2": {
  "n_steps": 7,
  "flagged": 0,
  "missing_tool": 0,
  "fabricated_arg": 0,
  "tool_call_failed": 0
 },
 "D3": {
  "n_handoffs": 2
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D3": 1.0, "D2": "procedural flag (no threshold)"}`