# Audit report — airline_048

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 4 | db_agent | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_error": false} | required but never called: search_direct_flight/search_onestop_flight |
| 5 | planner | D1/handoff | {"p_delegate": 0.269, "H2": 0.84} | delegate-vs-not split p_delegate=0.27 |
| 17 | db_agent | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_error": false} | required but never called: search_direct_flight/search_onestop_flight |

## Per-module summary
```
{
 "D1": {
  "n_scored": 19,
  "method": "stepwise"
 },
 "D3": {
  "n_steps": 19,
  "flagged": 2,
  "missing_tool": 2,
  "fabricated_arg": 0,
  "tool_error": 0
 },
 "D7": {
  "n_handoffs": 10
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3": "procedural flag (no threshold)"}`