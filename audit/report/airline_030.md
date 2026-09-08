# Audit report — airline_030

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 10 | planner | D1/handoff | {"p_delegate": 0.121, "H2": 0.531} | delegate-vs-not split p_delegate=0.12 |
| 12 | planner | D1/tool | {"confidence": 0.534, "p_actual": 0.685, "margin": 0.488} | action distribution: policy_checker 0.68, db_agent 0.20, respond_to_user 0.12 (actual: policy_checker) |
| 12 | planner | D1/handoff | {"p_delegate": 0.881, "H2": 0.528} | delegate-vs-not split p_delegate=0.88 |
| 13 | policy_checker | D1/tool | {"confidence": 0.673, "p_actual": 0.84, "margin": 0.683} | action distribution: think 0.84, no_tool 0.16, read_file 0.00 (actual: think) |
| 14 | policy_checker | D1/tool | {"confidence": 0.068, "p_actual": 0.404, "margin": 0.159} | action distribution: think 0.40, read_file 0.25, write_file 0.25 (actual: think) |

## Per-module summary
```
{
 "D1": {
  "n_scored": 20,
  "method": "stepwise"
 },
 "D2": {
  "n_steps": 20,
  "flagged": 0,
  "missing_tool": 0,
  "fabricated_arg": 0,
  "tool_call_failed": 0
 },
 "D3": {
  "n_handoffs": 10
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D3": 1.0, "D2": "procedural flag (no threshold)"}`