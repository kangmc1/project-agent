# Audit report — aime_026

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=800, numeric=176, numeric=6400, numeric=10000, numeric=6144 |
| 3 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["10000", "1425", "1436", "16", "25"], "altered": []} | verifier report->planner: missing ['10000', '1425', '1436'] altered [] |
| 4 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=1425, numeric=16, numeric=625, numeric=396, numeric=25 |
| 5 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=1425, numeric=16, numeric=625, numeric=396, numeric=25 |
| 7 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=20 |
| 8 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=889, numeric=529, numeric=600, numeric=709, numeric=769 |

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