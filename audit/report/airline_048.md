# Audit report — airline_048

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 4 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: money=306 |
| 5 | planner | D1/handoff | {"p_delegate": 0.269, "H2": 0.84} | delegate-vs-not split p_delegate=0.27 |
| 23 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT102, reservation_id=HAT093, reservation_id=HAT229, reservation_id=HAT147, reservation_id=HAT131 |
| 24 | planner | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT102, reservation_id=HAT093, reservation_id=HAT229, reservation_id=HAT147, reservation_id=HAT131 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 19,
  "method": "stepwise"
 },
 "D2": {
  "n_utterances": 10,
  "n_na": 3
 },
 "D3": {
  "tool_calls": 15,
  "utterances": 6,
  "checks": {}
 },
 "D7": {
  "n_handoffs": 10
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`