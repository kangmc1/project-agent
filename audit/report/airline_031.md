# Audit report — airline_031

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | planner | D1/handoff | {"p_delegate": 0.119, "H2": 0.528} | delegate-vs-not split p_delegate=0.12 |
| 7 | db_agent | D1/tool | {"confidence": 0.765, "p_actual": 0.616, "margin": 0.233} | action distribution: get_reservation_details 0.62, no_tool 0.38, cancel_reservation 0.00 (actual: get_reservation_details) |
| 15 | planner | D1/tool | {"confidence": 0.625, "p_actual": 0.779, "margin": 0.605} | action distribution: respond_to_user 0.78, write_file 0.17, policy_checker 0.04 (actual: respond_to_user) |
| 21 | policy_checker | D1/tool | {"confidence": 0.703, "p_actual": 0.873, "margin": 0.755} | action distribution: write_file 0.87, think 0.12, no_tool 0.01 (actual: write_file) |
| 27 | db_agent | D1/tool | {"confidence": 0.762, "p_actual": 0.6, "margin": 0.2} | action distribution: get_reservation_details 0.60, no_tool 0.40, book_reservation 0.00 (actual: get_reservation_details) |
| 32 | policy_checker | D1/tool | {"confidence": 0.26, "p_actual": 0.454, "margin": 0.075} | action distribution: think 0.45, no_tool 0.38, read_file 0.17 (actual: think) |
| 33 | policy_checker | D1/tool | {"confidence": 0.236, "p_actual": 0.47, "margin": 0.164} | action distribution: think 0.47, no_tool 0.31, read_file 0.22 (actual: think) |
| 34 | policy_checker | D1/tool | {"confidence": 0.353, "p_actual": 0.522, "margin": 0.115} | action distribution: write_file 0.52, think 0.41, read_file 0.07 (actual: write_file) |
| 40 | policy_checker | D1/tool | {"confidence": 0.506, "p_actual": 0.776, "margin": 0.603} | action distribution: think 0.78, write_file 0.17, no_tool 0.03 (actual: think) |
| 46 | planner | D1/handoff | {"p_delegate": 0.776, "H2": 0.767} | delegate-vs-not split p_delegate=0.78 |
| 48 | planner | D1/handoff | {"p_delegate": 0.223, "H2": 0.765} | delegate-vs-not split p_delegate=0.22 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 48,
  "method": "stepwise"
 },
 "D3": {
  "n_steps": 48,
  "flagged": 0,
  "missing_tool": 0,
  "fabricated_arg": 0,
  "tool_error": 1
 },
 "D7": {
  "n_handoffs": 22
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3": "procedural flag (no threshold)"}`