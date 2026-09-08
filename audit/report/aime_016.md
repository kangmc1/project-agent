# Audit report — aime_016

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 1 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["32"], "altered": []} | solver report->planner: missing ['32'] altered [] |
| 2 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=10, numeric=24, numeric=34, numeric=20, numeric=30 |
| 3 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: final_answer=32 |
| 5 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=24, numeric=34 |

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
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3_args": "any ungrounded value"}`