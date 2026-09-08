# Audit report — aime_000

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=10, numeric=28 |
| 3 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: final_answer=277 |
| 5 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=10, numeric=28 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 8,
  "method": "stepwise"
 },
 "D3": {
  "tool_calls": 5,
  "utterances": 4,
  "checks": {}
 },
 "D7": {
  "n_handoffs": 4
 },
 "D3_args": {
  "n_steps": 3,
  "n_values": 5,
  "n_ungrounded": 0
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3_args": "any ungrounded value"}`