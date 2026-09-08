# Audit report — aime_018

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=45, numeric=16, numeric=14, numeric=2026, numeric=20 |
| 4 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=2022, numeric=45, numeric=10, numeric=506, numeric=2020 |
| 5 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: final_answer=506 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 6,
  "method": "stepwise"
 },
 "D3": {
  "tool_calls": 3,
  "utterances": 3,
  "checks": {}
 },
 "D7": {
  "n_handoffs": 4
 },
 "D3_args": {
  "n_steps": 2,
  "n_values": 2,
  "n_ungrounded": 0
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3_args": "any ungrounded value"}`