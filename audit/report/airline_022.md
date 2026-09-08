# Audit report — airline_022

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 5 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": true, "tool_error": true} | argument never given: get_user_details.user_id=rossi_123 |
| 6 | db_agent | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_error": true} | required but never called: search_direct_flight/search_onestop_flight |
| 10 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": true, "tool_error": true} | argument never given: get_user_details.user_id=ivan_rossi |
| 12 | db_agent | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_error": false} | required but never called: search_direct_flight/search_onestop_flight |

## Per-module summary
```
{
 "D1": {
  "n_scored": 11,
  "method": "stepwise"
 },
 "D3": {
  "n_steps": 11,
  "flagged": 4,
  "missing_tool": 2,
  "fabricated_arg": 2,
  "tool_error": 3
 },
 "D7": {
  "n_handoffs": 4
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3": "procedural flag (no threshold)"}`