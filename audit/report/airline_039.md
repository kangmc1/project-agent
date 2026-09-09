# Audit report — airline_039

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["h8q05l", "successfully retrieved and recorded in the case notes"], "altered": []} | db_agent report->planner: missing ['h8q05l', 'successfully retrieved and recorded in the case notes'] altered [] |
| 4 | db_agent | D1/tool | {"confidence": 0.736, "p_actual": 0.689, "margin": 0.423} | action distribution: write_file 0.69, no_tool 0.27, read_file 0.04 (actual: write_file) |
| 6 | planner | D1/tool | {"confidence": 0.64, "p_actual": 0.759, "margin": 0.541} | action distribution: read_file 0.76, policy_checker 0.22, respond_to_user 0.02 (actual: read_file) |
| 6 | planner | D1/handoff | {"p_delegate": 0.218, "H2": 0.756} | delegate-vs-not split p_delegate=0.22 |
| 11 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["cancellation", "h8q05l", "harper kovacs"], "altered": []} | db_agent report->planner: missing ['cancellation', 'h8q05l', 'harper kovacs'] altered [] |
| 12 | db_agent | D1/tool | {"confidence": 0.778, "p_actual": 0.679, "margin": 0.358} | action distribution: cancel_reservation 0.68, get_reservation_details 0.32, no_tool 0.00 (actual: cancel_reservation) |
| 13 | db_agent | D1/tool | {"confidence": 0.721, "p_actual": 0.702, "margin": 0.479} | action distribution: write_file 0.70, no_tool 0.22, read_file 0.07 (actual: write_file) |
| 15 | planner | D1/tool | {"confidence": 0.553, "p_actual": 0.648, "margin": 0.342} | action distribution: read_file 0.65, respond_to_user 0.31, write_file 0.04 (actual: read_file) |

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
  "n_handoffs": 6
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D3": 1.0, "D2": "procedural flag (no threshold)"}`