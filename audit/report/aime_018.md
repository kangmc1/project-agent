# Audit report — aime_018

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=45, numeric=16, numeric=14, numeric=2026, numeric=20 |
| 4 | verifier | D2 | {"s": 0.25, "unsupported": 0.75} | values not found in any prior tool result: 90°, 90°, 45°, 45°, 14√2 |
| 4 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=2022, numeric=45, numeric=10, numeric=506, numeric=2020 |
| 5 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: final_answer=506 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 6,
  "method": "stepwise"
 },
 "D2": {
  "n_utterances": 4,
  "n_na": 1
 },
 "D3": {
  "tool_calls": 3,
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