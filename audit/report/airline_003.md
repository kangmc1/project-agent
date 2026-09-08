# Audit report — airline_003

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 4 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["flight from houston to denver on may 27th", "successfully recorded"], "altered": []} | db_agent report->planner: missing ['flight from houston to denver on may 27th', 'successfully recorded'] altered [] |
| 6 | db_agent | D2 | {"s": 0.3333333333333333, "unsupported": 0.6666666666666667} | values not found in any prior tool result: ['OI5L9G', 'AQLBTL', 'KA7I60', 'I57WUD', 'OBUT9V', '4BMN53', 'Q0ZF0J'], Find reservation details for a flight from Houston to Denver on May 27th |
| 7 | db_agent | D1/tool | {"confidence": 0.699, "p_actual": 0.377, "margin": 0.194} | action distribution: no_tool 0.57, write_file 0.38, read_file 0.05 (actual: write_file) |
| 10 | planner | D1/handoff | {"p_delegate": 0.851, "H2": 0.608} | delegate-vs-not split p_delegate=0.85 |
| 10 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["2024-05-15 15:00:00 est", "modify_flight_add_checked_bag", "need_info", "unknown"], "altered": ["reservation_id"]} | policy_checker report->planner: missing ['2024-05-15 15:00:00 est', 'modify_flight_add_checked_bag', 'need_info'] altered ['reservation_id'] |
| 11 | policy_checker | D1/tool | {"confidence": 0.502, "p_actual": 0.37, "margin": 0.255} | action distribution: no_tool 0.62, think 0.37, read_file 0.01 (actual: think) |
| 11 | policy_checker | D3 | {"checks": ["empty"], "tool": "think"} | tool think call #13: empty |
| 11 | policy_checker | D3 | {"satisfied": false} | claims without prior tool evidence: date=2024-05-15 |
| 12 | policy_checker | D3 | {"satisfied": false} | claims without prior tool evidence: date=2024-05-15 |
| 17 | planner | D1/tool | {"confidence": 0.454, "p_actual": 0.568, "margin": 0.3} | action distribution: respond_to_user 0.57, db_agent 0.27, read_file 0.16 (actual: respond_to_user) |
| 17 | planner | D1/handoff | {"p_delegate": 0.268, "H2": 0.839} | delegate-vs-not split p_delegate=0.27 |
| 20 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #18: repeat |
| 22 | db_agent | D3 | {"checks": ["error"], "tool": "update_reservation_flights"} | tool update_reservation_flights call #20: error |
| 22 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=HAT175, reservation_id=HAT290, update_baggages= |
| 23 | db_agent | D3 | {"checks": ["error"], "tool": "update_reservation_flights"} | tool update_reservation_flights call #21: error |
| 25 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["04:00", "1", "13:00", "changes have been recorded in the case notes", "den"], "altered": []} | db_agent report->planner: missing ['04:00', '1', '13:00'] altered [] |
| 26 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #23: repeat |
| 29 | db_agent | D1/tool | {"confidence": 0.537, "p_actual": 0.372, "margin": 0.056} | action distribution: write_file 0.37, no_tool 0.32, read_file 0.18 (actual: write_file) |
| 31 | planner | D1/tool | {"confidence": 0.566, "p_actual": 0.549, "margin": 0.12} | action distribution: read_file 0.55, respond_to_user 0.43, no_tool 0.02 (actual: read_file) |
| 31 | planner | D3 | {"checks": ["repeat"], "tool": "read_file"} | tool read_file call #28: repeat |

## Per-module summary
```
{
 "D1": {
  "n_scored": 29,
  "method": "stepwise"
 },
 "D2": {
  "n_utterances": 18,
  "n_na": 2
 },
 "D3": {
  "tool_calls": 29,
  "utterances": 16,
  "checks": {
   "empty": 1,
   "repeat": 3,
   "error": 2
  }
 },
 "D7": {
  "n_handoffs": 10
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`