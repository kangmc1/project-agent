# Audit report — airline_035

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | planner | D1/tool | {"confidence": 0.561, "p_actual": 0.653, "margin": 0.345} | action distribution: db_agent 0.65, policy_checker 0.31, respond_to_user 0.03 (actual: db_agent) |
| 8 | planner | D1/tool | {"confidence": 0.394, "p_actual": 0.244, "margin": 0.297} | action distribution: no_tool 0.54, write_file 0.24, respond_to_user 0.19 (actual: write_file) |

## Per-module summary
```
{
 "D1": {
  "n_scored": 7,
  "method": "stepwise"
 },
 "D3": {
  "n_steps": 7,
  "flagged": 0,
  "missing_tool": 0,
  "fabricated_arg": 0,
  "tool_error": 0
 },
 "D7": {
  "n_handoffs": 2
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3": "procedural flag (no threshold)"}`