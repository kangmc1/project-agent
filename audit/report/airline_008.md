# Audit report — airline_008

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | planner | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": false} | db_agent: lookup/modification requested without reservation or user id: "Retrieve the sum of the customer's gift card balances and the sum of their certificate balances." |
| 4 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: send_certificate |

## Per-module summary
```
{
 "D1": {
  "n_scored": 4,
  "method": "stepwise"
 },
 "D2": {
  "n_steps": 4,
  "flagged": 2,
  "missing_tool": 1,
  "fabricated_arg": 0,
  "tool_call_failed": 0
 },
 "D3": {
  "n_handoffs": 2
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D3": 1.0, "D2": "procedural flag (no threshold)"}`