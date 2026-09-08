# Audit report — airline_029

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 4 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["4xgccm", "amelia_davis_8890", "udmop1"], "altered": []} | db_agent report->planner: missing ['4xgccm', 'amelia_davis_8890', 'udmop1'] altered [] |
| 8 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: update_passengers= |
| 10 | planner | D1/tool | {"confidence": 0.601, "p_actual": 0.753, "margin": 0.585} | action distribution: respond_to_user 0.75, policy_checker 0.17, db_agent 0.08 (actual: respond_to_user) |
| 10 | planner | D1/handoff | {"p_delegate": 0.247, "H2": 0.807} | delegate-vs-not split p_delegate=0.25 |
| 12 | planner | D1/tool | {"confidence": 0.617, "p_actual": 0.562, "margin": 0.124} | action distribution: db_agent 0.56, policy_checker 0.44, write_file 0.00 (actual: db_agent) |
| 14 | db_agent | D1/tool | {"confidence": 0.763, "p_actual": 0.622, "margin": 0.245} | action distribution: read_file 0.62, write_file 0.38, think 0.00 (actual: read_file) |
| 14 | db_agent | D3 | {"checks": ["repeat"], "tool": "read_file"} | tool read_file call #16: repeat |

## Per-module summary
```
{
 "D1": {
  "n_scored": 15,
  "method": "stepwise"
 },
 "D3": {
  "tool_calls": 19,
  "utterances": 8,
  "checks": {
   "repeat": 1
  }
 },
 "D7": {
  "n_handoffs": 4
 },
 "D3_args": {
  "n_steps": 7,
  "n_values": 18,
  "n_ungrounded": 0
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3_args": "any ungrounded value"}`