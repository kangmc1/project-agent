# Audit report — aime_019

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=999, numeric=72, numeric=1000, numeric=10 |
| 4 | verifier | D2 | {"s": 0.4444444444444444, "unsupported": 0.5555555555555556} | values not found in any prior tool result: positive integer n, value of n viewed in base b, where b is the least integer greater than the greatest digit in n, less than 1000, 123, 4 |
| 4 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=58, numeric=999, numeric=16, numeric=123, numeric=72 |

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
  "n_steps": 4
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`