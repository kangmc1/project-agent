# Audit report — airline_013

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 4 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: money=363 |
| 9 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT102, reservation_id=HAT052, reservation_id=HAT178, reservation_id=HAT281, reservation_id=HAT174 |
| 12 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["cannot be modified under the airline's policy", "modify flight policy: basic economy flights cannot be modified.", "needs to confirm if they want to proceed with the upgrade if allowed", "not_allowed", "permitted but the user must pay the price difference"], "altered": []} | policy_checker report->planner: missing ["cannot be modified under the airline's policy", 'modify flight policy: basic economy flights cannot be modified.', 'needs to confirm if they want to proceed with the upgrade if allowed'] altered [] |
| 13 | policy_checker | D1/tool | {"confidence": 0.652, "p_actual": 0.183, "margin": 0.633} | action distribution: no_tool 0.82, think 0.18, read_file 0.00 (actual: think) |
| 13 | policy_checker | D3 | {"checks": ["empty"], "tool": "think"} | tool think call #7: empty |
| 15 | planner | D3/arguments | {"ungrounded_ratio": 0.286} | argument values never given to the agent: respond_to_user.money=121, respond_to_user.money=71 |
| 18 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #10: repeat |
| 18 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT052, money=121, update_flights= |
| 19 | db_agent | D3 | {"checks": ["error"], "tool": "update_reservation_flights"} | tool update_reservation_flights call #11: error |
| 30 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #19: repeat |
| 31 | db_agent | D3 | {"checks": ["error", "repeat"], "tool": "update_reservation_flights"} | tool update_reservation_flights call #20: error, repeat |

## Per-module summary
```
{
 "D1": {
  "n_scored": 30,
  "method": "stepwise"
 },
 "D3": {
  "tool_calls": 23,
  "utterances": 17,
  "checks": {
   "empty": 1,
   "repeat": 3,
   "error": 2
  }
 },
 "D7": {
  "n_handoffs": 12
 },
 "D3_args": {
  "n_steps": 19,
  "n_values": 100,
  "n_ungrounded": 2
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3_args": "any ungrounded value"}`