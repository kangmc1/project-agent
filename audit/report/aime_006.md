# Audit report — aime_006

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 1 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["441"], "altered": ["final_answer"]} | solver report->planner: missing ['441'] altered ['final_answer'] |
| 2 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=1013, numeric=10, numeric=2026, numeric=100, numeric=80 |
| 5 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=1013, numeric=10, numeric=100, numeric=80, numeric=400 |

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
  "n_steps": 1,
  "n_values": 1,
  "n_ungrounded": 0
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3_args": "any ungrounded value"}`