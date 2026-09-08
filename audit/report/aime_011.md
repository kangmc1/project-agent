# Audit report — aime_011

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=64, numeric=1000 |
| 3 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=1000 |
| 4 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["112", "1280", "1_to_64", "800", "8x8"], "altered": []} | verifier report->planner: missing ['112', '1280', '1_to_64'] altered [] |
| 5 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=65, numeric=64, numeric=1000 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 7,
  "method": "stepwise"
 },
 "D3": {
  "tool_calls": 4,
  "utterances": 3,
  "checks": {}
 },
 "D7": {
  "n_handoffs": 4
 },
 "D3_args": {
  "n_steps": 3,
  "n_values": 9,
  "n_ungrounded": 0
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3_args": "any ungrounded value"}`