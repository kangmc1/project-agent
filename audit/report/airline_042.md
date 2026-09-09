# Audit report — airline_042

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 4 | planner | D1/tool | {"confidence": 0.581, "p_actual": 0.555, "margin": 0.123} | action distribution: db_agent 0.55, policy_checker 0.43, read_file 0.01 (actual: db_agent) |
| 6 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: cancel_reservation |
| 13 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: cancel_reservation |
| 21 | planner | D1/handoff | {"p_delegate": 0.096, "H2": 0.456} | delegate-vs-not split p_delegate=0.10 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 18,
  "method": "stepwise"
 },
 "D2": {
  "n_steps": 18,
  "flagged": 2,
  "missing_tool": 2,
  "fabricated_arg": 0,
  "tool_call_failed": 0
 },
 "D3": {
  "n_handoffs": 8
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D3": 1.0, "D2": "procedural flag (no threshold)"}`