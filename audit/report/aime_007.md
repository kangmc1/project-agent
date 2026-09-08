# Audit report — aime_007

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 1 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["276"], "altered": []} | solver report->planner: missing ['276'] altered [] |
| 2 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=10 |
| 4 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["391"], "altered": []} | verifier report->planner: missing ['391'] altered [] |
| 5 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=10 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 11,
  "method": "stepwise"
 },
 "D2": {
  "n_utterances": 7,
  "n_na": 0
 },
 "D3": {
  "tool_calls": 7,
  "utterances": 6,
  "checks": {}
 },
 "D7": {
  "n_handoffs": 6
 },
 "D9": {
  "n_steps": 7
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`