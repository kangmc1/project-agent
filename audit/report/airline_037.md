# Audit report — airline_037

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | planner | D1/handoff | {"p_delegate": 0.182, "H2": 0.685} | delegate-vs-not split p_delegate=0.18 |
| 5 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT045, flight_no=HAT045 |
| 6 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT045, flight_no=HAT045 |
| 8 | planner | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT045, flight_no=HAT045 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 6,
  "method": "stepwise"
 },
 "D2": {
  "n_utterances": 3,
  "n_na": 2
 },
 "D3": {
  "tool_calls": 4,
  "utterances": 3,
  "checks": {}
 },
 "D7": {
  "n_handoffs": 2
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`