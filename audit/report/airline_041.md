# Audit report — airline_041

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 6 | policy_checker | D3 | {"satisfied": false} | claims without prior tool evidence: cancel= |
| 7 | planner | D1/handoff | {"p_delegate": 0.816, "H2": 0.688} | delegate-vs-not split p_delegate=0.82 |
| 12 | planner | D3 | {"satisfied": false} | claims without prior tool evidence: book= |

## Per-module summary
```
{
 "D1": {
  "n_scored": 10,
  "method": "stepwise"
 },
 "D2": {
  "n_utterances": 6,
  "n_na": 0
 },
 "D3": {
  "tool_calls": 6,
  "utterances": 6,
  "checks": {}
 },
 "D7": {
  "n_handoffs": 6
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`