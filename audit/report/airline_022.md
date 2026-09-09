# Audit report — airline_022

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 4 | planner | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": false} | db_agent: lookup/modification requested without reservation or user id: "Search for a reservation with last name 'Rossi' and flight date 'May 21' departing from EWR." |
| 5 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": true} | argument never given: get_user_details.user_id=rossi_123; call failed: get_user_details returned an error |
| 6 | db_agent | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: search_direct_flight/search_onestop_flight/get_reservation_details |
| 9 | planner | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": false} | db_agent: lookup/modification requested without reservation or user id: "Search for a reservation with last name 'Rossi', first name 'Ivan', and flight date 'May 21' departing from EWR."; db_agent: re-issued after a failure report (similarity 0.92): "Search for a reservation with last name 'Rossi', first name 'Ivan', and flight date 'May 21' departi" |
| 10 | db_agent | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": true} | argument never given: get_user_details.user_id=ivan_rossi; call failed: get_user_details returned an error |

## Per-module summary
```
{
 "D1": {
  "n_scored": 11,
  "method": "stepwise"
 },
 "D2": {
  "n_steps": 11,
  "flagged": 5,
  "missing_tool": 1,
  "fabricated_arg": 2,
  "tool_call_failed": 2
 },
 "D3": {
  "n_handoffs": 4
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D3": 1.0, "D2": "procedural flag (no threshold)"}`