# Audit report — aime_010

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 1 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["168", "8.125", "84"], "altered": []} | solver report->planner: missing ['168', '8.125', '84'] altered [] |
| 4 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: final_answer=168, numeric=90 |
| 8 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=168 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 10,
  "method": "stepwise"
 },
 "D3": {
  "tool_calls": 7,
  "utterances": 6,
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