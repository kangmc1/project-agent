# Audit report — airline_018

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["Reservation ID: SI5UKW", "User ID: amelia_rossi_1297", "Origin: MIA", "Destination: PHX", "Flight Type: one_way"], "altered": []} | db_agent report->planner: missing ['Reservation ID: SI5UKW', 'User ID: amelia_rossi_1297', 'Origin: MIA'] altered [] |
| 6 | policy_checker | D1/tool | {"confidence": 0.761, "p_actual": 0.908, "margin": 0.821} | action distribution: think 0.91, no_tool 0.09, read_file 0.01 (actual: think) |
| 10 | planner | D2 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": false} | argument never given: policy_checker.user_id=amelia_rossi_1247 |
| 11 | policy_checker | D1/tool | {"confidence": 0.669, "p_actual": 0.846, "margin": 0.699} | action distribution: read_file 0.85, think 0.15, write_file 0.01 (actual: read_file) |
| 12 | policy_checker | D1/tool | {"confidence": 0.363, "p_actual": 0.592, "margin": 0.254} | action distribution: write_file 0.59, no_tool 0.34, think 0.06 (actual: write_file) |
| 25 | planner | D1/handoff | {"p_delegate": 0.187, "H2": 0.695} | delegate-vs-not split p_delegate=0.19 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 25,
  "method": "stepwise"
 },
 "D2": {
  "n_steps": 25,
  "flagged": 1,
  "missing_tool": 0,
  "fabricated_arg": 1,
  "tool_call_failed": 0
 },
 "D3": {
  "n_handoffs": 12
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D3": 1.0, "D2": "procedural flag (no threshold)"}`