# Audit report — aime_004

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 7 | planner | D1/tool | {"confidence": 0.629, "p_actual": 0.751, "margin": 0.534} | action distribution: solver 0.75, no_tool 0.22, submit_answer 0.03 (actual: solver) |
| 7 | planner | D1/handoff | {"p_delegate": 0.753, "H2": 0.806} | delegate-vs-not split p_delegate=0.75 |
| 8 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=945, numeric=220, numeric=770, numeric=2285, numeric=3175 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 10,
  "method": "stepwise"
 },
 "D3": {
  "tool_calls": 6,
  "utterances": 5,
  "checks": {}
 },
 "D7": {
  "n_handoffs": 6
 },
 "D3_args": {
  "n_steps": 1,
  "n_values": 1,
  "n_ungrounded": 0
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3_args": "any ungrounded value"}`