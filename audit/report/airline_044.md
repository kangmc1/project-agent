# Audit report — airline_044

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 5 | planner | D1/tool | {"confidence": 0.604, "p_actual": 0.669, "margin": 0.353} | action distribution: respond_to_user 0.67, policy_checker 0.32, read_file 0.01 (actual: respond_to_user) |
| 5 | planner | D1/handoff | {"p_delegate": 0.318, "H2": 0.902} | delegate-vs-not split p_delegate=0.32 |
| 9 | planner | D1/handoff | {"p_delegate": 0.182, "H2": 0.685} | delegate-vs-not split p_delegate=0.18 |
| 15 | planner | D1/tool | {"confidence": 0.641, "p_actual": 0.758, "margin": 0.546} | action distribution: write_file 0.76, no_tool 0.21, respond_to_user 0.03 (actual: write_file) |

## Per-module summary
```
{
 "D1": {
  "n_scored": 12,
  "method": "stepwise"
 },
 "D3": {
  "tool_calls": 8,
  "utterances": 2,
  "checks": {}
 },
 "D7": {
  "n_handoffs": 6
 },
 "D3_args": {
  "n_steps": 3,
  "n_values": 3,
  "n_ungrounded": 0
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3_args": "any ungrounded value"}`