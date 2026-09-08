# Audit report — airline_004

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 4 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["0", "1", "161", "2024-05-24", "2024-05-25"], "altered": ["reservation_id"]} | db_agent report->planner: missing ['0', '1', '161'] altered ['reservation_id'] |
| 7 | db_agent | D1/tool | {"confidence": 0.644, "p_actual": 0.646, "margin": 0.461} | action distribution: get_reservation_details 0.65, write_file 0.18, read_file 0.11 (actual: get_reservation_details) |
| 13 | planner | D1/tool | {"confidence": 0.636, "p_actual": 0.677, "margin": 0.357} | action distribution: respond_to_user 0.68, db_agent 0.32, read_file 0.00 (actual: respond_to_user) |
| 13 | planner | D1/handoff | {"p_delegate": 0.32, "H2": 0.904} | delegate-vs-not split p_delegate=0.32 |
| 27 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: update_reservation_baggages returned an error |

## Per-module summary
```
{
 "D1": {
  "n_scored": 26,
  "method": "stepwise"
 },
 "D3": {
  "n_steps": 26,
  "flagged": 1,
  "missing_tool": 0,
  "fabricated_arg": 0,
  "tool_call_failed": 1
 },
 "D7": {
  "n_handoffs": 8
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3": "procedural flag (no threshold)"}`