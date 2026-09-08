# Audit report — airline_008

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 4 | db_agent | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_error": false} | required but never called: send_certificate |

## Per-module summary
```
{
 "D1": {
  "n_scored": 4,
  "method": "stepwise"
 },
 "D3": {
  "n_steps": 4,
  "flagged": 1,
  "missing_tool": 1,
  "fabricated_arg": 0,
  "tool_error": 0
 },
 "D7": {
  "n_handoffs": 2
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3": "procedural flag (no threshold)"}`