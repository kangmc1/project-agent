# Audit report — aime_014

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 1 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["184", "189", "492 + 184√5", "5", "903.44"], "altered": ["final_answer"]} | solver report->planner: missing ['184', '189', '492 + 184√5'] altered ['final_answer'] |
| 2 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=800, numeric=92, numeric=616, numeric=308, numeric=184 |
| 3 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=189, numeric=492, numeric=72, numeric=184, numeric=368 |
| 4 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: final_answer=189, numeric=184, numeric=492 |
| 4 | solver | D9 | {"consistency": 0.0} | false equations: {'step_id': 4, 'expr': '492 + 184*sqrt(5) == 903.44'}; {'step_id': 4, 'expr': '184*sqrt(5) == 410.44'} |
| 6 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=984, numeric=700, numeric=497 |
| 7 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: final_answer=497, numeric=700 |
| 9 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=189, numeric=200, numeric=497, numeric=77 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 11,
  "method": "stepwise"
 },
 "D2": {
  "n_utterances": 8,
  "n_na": 4
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
  "n_steps": 8
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`