# Audit report — airline_037

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | planner | D1/handoff | {"p_delegate": 0.182, "H2": 0.685} | delegate-vs-not split p_delegate=0.18 |
| 6 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: get_reservation_details/get_user_details |

## Per-module summary
```
{
 "D1": {
  "n_scored": 6,
  "method": "stepwise"
 },
 "D2": {
  "n_steps": 6,
  "flagged": 1,
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