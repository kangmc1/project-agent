# Audit report — airline_002

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 4 | planner | D1/handoff | {"p_delegate": 0.852, "H2": 0.605} | delegate-vs-not split p_delegate=0.85 |
| 7 | db_agent | D2 | {"s": 0.0, "unsupported": 1.0} | values not found in any prior tool result: next step: Check next reservation 'LQ940Q' |
| 12 | db_agent | D3 | {"checks": ["error", "ignored"], "tool": "read_file"} | tool read_file call #9: error, ignored |
| 15 | planner | D1/tool | {"confidence": 0.431, "p_actual": 0.656, "margin": 0.51} | action distribution: respond_to_user 0.66, write_file 0.15, db_agent 0.15 (actual: respond_to_user) |
| 15 | planner | D1/handoff | {"p_delegate": 0.188, "H2": 0.698} | delegate-vs-not split p_delegate=0.19 |
| 18 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #13: repeat |
| 18 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #14: repeat |
| 18 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #15: repeat |
| 18 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #16: repeat |
| 18 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #17: repeat |
| 20 | planner | D1/tool | {"confidence": 0.399, "p_actual": 0.443, "margin": 0.098} | action distribution: db_agent 0.44, respond_to_user 0.34, policy_checker 0.21 (actual: db_agent) |
| 20 | planner | D1/handoff | {"p_delegate": 0.652, "H2": 0.932} | delegate-vs-not split p_delegate=0.65 |
| 20 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["/case_notes.md", "successfully appended"], "altered": []} | db_agent report->planner: missing ['/case_notes.md', 'successfully appended'] altered [] |
| 21 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #19: repeat |
| 21 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #20: repeat |
| 21 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #21: repeat |
| 21 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #22: repeat |
| 21 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #23: repeat |
| 22 | db_agent | D1/tool | {"confidence": 0.708, "p_actual": 0.36, "margin": 0.231} | action distribution: no_tool 0.59, write_file 0.36, read_file 0.05 (actual: write_file) |
| 22 | db_agent | D2 | {"s": 0.0, "unsupported": 1.0} | values not found in any prior tool result: MCO to BOS (HAT028) - Economy class price: $1859, BOS to CLT (HAT277) - Economy class price: $1679, DEN to PHL (HAT080) - Economy class price: $537, PHL to DEN (HAT076) - Economy class price: $996, DEN to MIA (HAT255) - Economy class price: $1440 |
| 24 | planner | D1/tool | {"confidence": 0.52, "p_actual": 0.594, "margin": 0.233} | action distribution: respond_to_user 0.59, read_file 0.36, policy_checker 0.03 (actual: respond_to_user) |
| 27 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #27: repeat |
| 27 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #28: repeat |
| 27 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #29: repeat |
| 27 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #30: repeat |
| 27 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #31: repeat |
| 31 | planner | D1/tool | {"confidence": 0.504, "p_actual": 0.574, "margin": 0.226} | action distribution: policy_checker 0.57, db_agent 0.35, respond_to_user 0.08 (actual: policy_checker) |
| 32 | policy_checker | D1/tool | {"confidence": 0.327, "p_actual": 0.637, "margin": 0.403} | action distribution: read_file 0.64, think 0.23, no_tool 0.12 (actual: read_file) |
| 32 | policy_checker | D3 | {"checks": ["repeat"], "tool": "read_file"} | tool read_file call #34: repeat |
| 39 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #38: repeat |
| 39 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #39: repeat |
| 39 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #40: repeat |
| 39 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #41: repeat |
| 39 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #42: repeat |
| 43 | planner | D1/handoff | {"p_delegate": 0.814, "H2": 0.692} | delegate-vs-not split p_delegate=0.81 |
| 44 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #45: repeat |
| 44 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #46: repeat |
| 44 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #47: repeat |
| 44 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #48: repeat |
| 44 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #49: repeat |
| 48 | planner | D1/tool | {"confidence": 0.547, "p_actual": 0.484, "margin": 0.0} | action distribution: policy_checker 0.48, respond_to_user 0.48, db_agent 0.03 (actual: policy_checker) |
| 48 | planner | D1/handoff | {"p_delegate": 0.515, "H2": 0.999} | delegate-vs-not split p_delegate=0.52 |
| 49 | policy_checker | D3 | {"satisfied": false} | claims without prior tool evidence: date=2024-05-15 |
| 53 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #54: repeat |
| 53 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #55: repeat |
| 53 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #56: repeat |
| 53 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #57: repeat |
| 53 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #58: repeat |
| 56 | planner | D3 | {"checks": ["error", "ignored"], "tool": "respond_to_user"} | tool respond_to_user call #60: error, ignored |
| 58 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #61: repeat |
| 58 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #62: repeat |
| 58 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #63: repeat |
| 58 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #64: repeat |
| 58 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #65: repeat |
| 59 | planner | D3 | {"checks": ["error", "ignored"], "tool": "db_agent"} | tool db_agent call #66: error, ignored |
| 63 | policy_checker | D1/tool | {"confidence": 0.731, "p_actual": 0.896, "margin": 0.801} | action distribution: think 0.90, read_file 0.09, no_tool 0.01 (actual: think) |
| 63 | policy_checker | D3 | {"checks": ["empty"], "tool": "think"} | tool think call #68: empty |
| 63 | policy_checker | D3 | {"satisfied": false} | claims without prior tool evidence: date=2024-05-15 |
| 64 | policy_checker | D3 | {"satisfied": false} | claims without prior tool evidence: date=2024-05-15, cancel= |

## Per-module summary
```
{
 "D1": {
  "n_scored": 55,
  "method": "stepwise"
 },
 "D2": {
  "n_utterances": 31,
  "n_na": 9
 },
 "D3": {
  "tool_calls": 71,
  "utterances": 28,
  "checks": {
   "error": 3,
   "ignored": 3,
   "repeat": 36,
   "empty": 1
  }
 },
 "D7": {
  "n_handoffs": 22
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`