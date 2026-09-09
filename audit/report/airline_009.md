# Audit report — airline_009

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | planner | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": false} | db_agent: lookup/modification requested without reservation or user id: "Get the sum of the customer's gift card balances and the sum of their certificate balances." |
| 2 | planner | D3/instruction->premise | {"fidelity": 0.0, "missing": ["Sum of the customer's gift card balances", "Sum of the customer's certificate balances"], "altered": []} | db_agent instruction->premise: missing ["Sum of the customer's gift card balances", "Sum of the customer's certificate balances"] altered [] |
| 4 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: send_certificate |
| 5 | planner | D1/tool | {"confidence": 0.661, "p_actual": 0.704, "margin": 0.409} | action distribution: no_tool 0.70, respond_to_user 0.30, db_agent 0.00 (actual: no_tool) |

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