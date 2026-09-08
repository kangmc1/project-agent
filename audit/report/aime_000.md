# Audit report — aime_000

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | solver | D2 | {"s": 0.0, "unsupported": 1.0} | values not found in any prior tool result: r + 2, r + 9, t - 1, t - 2, m/n |
| 2 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=10, numeric=28 |
| 3 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: final_answer=277 |
| 5 | verifier | D2 | {"s": 0.4, "unsupported": 0.6} | values not found in any prior tool result: x + 2, x + 9, t - 1, t - 2, m/n |
| 5 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=10, numeric=28 |
| 5 | verifier | D9 | {"consistency": 0.06666666666666667} | false equations: {'step_id': 5, 'expr': 'x * t == (x + 2) * (t - 1)'}; {'step_id': 5, 'expr': 'x * t == (x + 9) * (t - 2)'}; {'step_id': 5, 'expr': 'x == 2 * t - 2'} |

## Per-module summary
```
{
 "D1": {
  "n_scored": 8,
  "method": "stepwise"
 },
 "D2": {
  "n_utterances": 5,
  "n_na": 0
 },
 "D3": {
  "tool_calls": 5,
  "utterances": 4,
  "checks": {}
 },
 "D7": {
  "n_handoffs": 4
 },
 "D9": {
  "n_steps": 5
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`