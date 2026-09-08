# Audit report — aime_012

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 1 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["1", "6", "6/1", "7"], "altered": ["final_answer"]} | solver report->planner: missing ['1', '6', '6/1'] altered ['final_answer'] |
| 2 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=39, numeric=16, numeric=24, numeric=72, numeric=12 |
| 4 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["-2_3", "0", "1", "2", "3"], "altered": ["final_answer"]} | verifier report->planner: missing ['-2_3', '0', '1'] altered ['final_answer'] |
| 5 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=10, numeric=40, numeric=32, numeric=72, numeric=832 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 7,
  "method": "stepwise"
 },
 "D3": {
  "tool_calls": 4,
  "utterances": 3,
  "checks": {}
 },
 "D7": {
  "n_handoffs": 4
 },
 "D3_args": {
  "n_steps": 3,
  "n_values": 3,
  "n_ungrounded": 0
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3_args": "any ungrounded value"}`