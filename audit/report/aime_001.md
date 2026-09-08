# Audit report — aime_001

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | solver | D1/tool | {"confidence": 0.554, "p_actual": 0.692, "margin": 0.383} | action distribution: run_python 0.69, no_tool 0.31, read_file 0.00 (actual: run_python) |
| 2 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=10, numeric=28, numeric=14, numeric=18 |
| 5 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=10, numeric=28 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 7,
  "method": "stepwise"
 },
 "D3": {
  "tool_calls": 4,
  "utterances": 4,
  "checks": {}
 },
 "D7": {
  "n_handoffs": 4
 },
 "D3_args": {
  "n_steps": 2,
  "n_values": 4,
  "n_ungrounded": 0
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3_args": "any ungrounded value"}`