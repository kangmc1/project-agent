# Audit report — airline_013

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 4 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: money=363 |
| 9 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT102, reservation_id=HAT052, reservation_id=HAT178, reservation_id=HAT281, reservation_id=HAT174 |
| 12 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["cannot be modified under the airline's policy", "modify flight policy: basic economy flights cannot be modified.", "needs to confirm if they want to proceed with the upgrade if allowed", "not_allowed", "permitted but the user must pay the price difference"], "altered": []} | policy_checker report->planner: missing ["cannot be modified under the airline's policy", 'modify flight policy: basic economy flights cannot be modified.', 'needs to confirm if they want to proceed with the upgrade if allowed'] altered [] |
| 13 | policy_checker | D1/tool | {"confidence": 0.652, "p_actual": 0.183, "margin": 0.633} | action distribution: no_tool 0.82, think 0.18, read_file 0.00 (actual: think) |
| 13 | policy_checker | D3 | {"checks": ["empty"], "tool": "think"} | tool think call #7: empty |
| 18 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #10: repeat |
| 18 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT052, money=121, update_flights= |
| 19 | db_agent | D2 | {"s": 0.3333333333333333, "unsupported": 0.6666666666666667} | values not found in any prior tool result: HAT030 (LAX to ORD), HAT223 (ORD to ATL), HAT252 (ATL to DFW), HAT124 (DFW to LAX), Gift Card (ID: gift_card_4643416), 0 (0 non-free), HAT252 (ATL to LAS) |
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
 "D2": {
  "n_utterances": 19,
  "n_na": 2
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
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`