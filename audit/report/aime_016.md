# Audit report — aime_016

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 1 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["32"], "altered": []} | solver report->planner: missing ['32'] altered [] |
| 2 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=10, numeric=24, numeric=34, numeric=20, numeric=30 |
| 2 | solver | D9 | {"consistency": 0.0} | false equations: {'step_id': 2, 'expr': 'a_10 == 4 + 9*-1'}; {'step_id': 2, 'expr': 'a_10 == 4 + 9*2'}; {'step_id': 2, 'expr': 'a_10 == 4 + 9*-2'} |
| 3 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: final_answer=32 |
| 5 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=24, numeric=34 |
| 5 | verifier | D9 | {"consistency": 0.06666666666666667} | false equations: {'step_id': 5, 'expr': 'd == 5'}; {'step_id': 5, 'expr': 'd == 2'}; {'step_id': 5, 'expr': 'd == 1'} |

## Per-module summary
```
{
 "D1": {
  "n_scored": 7,
  "method": "stepwise"
 },
 "D2": {
  "n_utterances": 5,
  "n_na": 0
 },
 "D3": {
  "tool_calls": 4,
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