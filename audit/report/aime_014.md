# Audit report — aime_014

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 1 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["184", "189", "492 + 184√5", "5", "903.44"], "altered": ["final_answer"]} | solver report->planner: missing ['184', '189', '492 + 184√5'] altered ['final_answer'] |
| 2 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=800, numeric=92, numeric=616, numeric=308, numeric=184 |
| 3 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=189, numeric=492, numeric=72, numeric=184, numeric=368 |
| 4 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: final_answer=189, numeric=184, numeric=492 |
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
 "D3": {
  "tool_calls": 7,
  "utterances": 6,
  "checks": {}
 },
 "D7": {
  "n_handoffs": 6
 },
 "D3_args": {
  "n_steps": 4,
  "n_values": 7,
  "n_ungrounded": 0
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3_args": "any ungrounded value"}`