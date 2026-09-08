# Audit report — aime_025

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=200, numeric=10, numeric=16, numeric=14, numeric=11 |
| 4 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=200, numeric=40000, numeric=225, numeric=360000, numeric=50625 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 7,
  "method": "stepwise"
 },
 "D2": {
  "n_utterances": 4,
  "n_na": 0
 },
 "D3": {
  "tool_calls": 4,
  "utterances": 3,
  "checks": {}
 },
 "D7": {
  "n_handoffs": 4
 },
 "D9": {
  "n_steps": 3
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`