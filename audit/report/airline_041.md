# Audit report — airline_041

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 7 | planner | D1/handoff | {"p_delegate": 0.816, "H2": 0.688} | delegate-vs-not split p_delegate=0.82 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 10,
  "method": "stepwise"
 },
 "D3": {
  "n_steps": 10,
  "flagged": 0,
  "missing_tool": 0,
  "fabricated_arg": 0,
  "tool_error": 0
 },
 "D7": {
  "n_handoffs": 6
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3": "procedural flag (no threshold)"}`