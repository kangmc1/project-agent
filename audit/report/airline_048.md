# Audit report — airline_048

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 5 | planner | D1/handoff | {"p_delegate": 0.269, "H2": 0.84} | delegate-vs-not split p_delegate=0.27 |
| 16 | planner | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": false} | db_agent: lookup/modification requested without reservation or user id: 'Search for available flights for the new dates (two days later than the original) for the same route (ORD to LAS round t' |
| 17 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: search_direct_flight/search_onestop_flight |

## Per-module summary
```
{
 "D1": {
  "n_scored": 19,
  "method": "stepwise"
 },
 "D2": {
  "n_steps": 19,
  "flagged": 2,
  "missing_tool": 1,
  "fabricated_arg": 0,
  "tool_call_failed": 0
 },
 "D3": {
  "n_handoffs": 10
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D3": 1.0, "D2": "procedural flag (no threshold)"}`