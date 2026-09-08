# Audit report — aime_013

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=501 |
| 3 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #2: repeat |
| 3 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=501 |
| 4 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #3: repeat |
| 4 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=11, numeric=501 |
| 5 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #4: repeat |
| 5 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=14, numeric=12, numeric=13, numeric=501 |
| 6 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #5: repeat |
| 6 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=16, numeric=15, numeric=501, numeric=17 |
| 7 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=19, numeric=18, numeric=20, numeric=501 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 11,
  "method": "stepwise"
 },
 "D3": {
  "tool_calls": 8,
  "utterances": 8,
  "checks": {
   "repeat": 4
  }
 },
 "D7": {
  "n_handoffs": 4
 },
 "D3_args": {
  "n_steps": 2,
  "n_values": 6,
  "n_ungrounded": 0
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3_args": "any ungrounded value"}`