# Audit report — airline_029

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 4 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["case notes updated", "operation details for finding upcoming flights for single-passenger reservations", "user ID 'amelia_davis_8890'", "reservation ID 'UDMOP1'", "reservation ID '4XGCCM'"], "altered": []} | db_agent report->planner: missing ['case notes updated', 'operation details for finding upcoming flights for single-passenger reservations', "user ID 'amelia_davis_8890'"] altered [] |
| 10 | planner | D1/tool | {"confidence": 0.601, "p_actual": 0.753, "margin": 0.585} | action distribution: respond_to_user 0.75, policy_checker 0.17, db_agent 0.08 (actual: respond_to_user) |
| 10 | planner | D1/handoff | {"p_delegate": 0.247, "H2": 0.807} | delegate-vs-not split p_delegate=0.25 |
| 12 | planner | D1/tool | {"confidence": 0.617, "p_actual": 0.562, "margin": 0.124} | action distribution: db_agent 0.56, policy_checker 0.44, write_file 0.00 (actual: db_agent) |
| 12 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["user ID 'amelia_davis_8890'", "cancellations recorded in shared file `/case_notes.md`"], "altered": ["cancellation of reservation UDMOP1 recorded", "cancellation of reservation 4XGCCM recorded"]} | db_agent report->planner: missing ["user ID 'amelia_davis_8890'", 'cancellations recorded in shared file `/case_notes.md`'] altered ['cancellation of reservation UDMOP1 recorded', 'cancellation of reservation 4XGCCM recorded'] |
| 14 | db_agent | D1/tool | {"confidence": 0.763, "p_actual": 0.622, "margin": 0.245} | action distribution: read_file 0.62, write_file 0.38, think 0.00 (actual: read_file) |

## Per-module summary
```
{
 "D1": {
  "n_scored": 15,
  "method": "stepwise"
 },
 "D2": {
  "n_steps": 15,
  "flagged": 0,
  "missing_tool": 0,
  "fabricated_arg": 0,
  "tool_call_failed": 0
 },
 "D3": {
  "n_handoffs": 4
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D3": 1.0, "D2": "procedural flag (no threshold)"}`