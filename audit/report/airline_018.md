# Audit report — airline_018

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 6 | policy_checker | D1/tool | {"confidence": 0.761, "p_actual": 0.908, "margin": 0.821} | action distribution: think 0.91, no_tool 0.09, read_file 0.01 (actual: think) |
| 6 | policy_checker | D3 | {"checks": ["empty"], "tool": "think"} | tool think call #3: empty |
| 6 | policy_checker | D3 | {"satisfied": false} | claims without prior tool evidence: date=2024-05-15 |
| 11 | policy_checker | D1/tool | {"confidence": 0.669, "p_actual": 0.846, "margin": 0.699} | action distribution: read_file 0.85, think 0.15, write_file 0.01 (actual: read_file) |
| 11 | policy_checker | D3 | {"checks": ["error", "ignored"], "tool": "read_file"} | tool read_file call #6: error, ignored |
| 11 | policy_checker | D3 | {"satisfied": false} | claims without prior tool evidence: user_id=amelia_rossi_1247, date=2024-05-15, cancel= |
| 12 | policy_checker | D1/tool | {"confidence": 0.363, "p_actual": 0.592, "margin": 0.254} | action distribution: write_file 0.59, no_tool 0.34, think 0.06 (actual: write_file) |
| 13 | policy_checker | D3 | {"satisfied": false} | claims without prior tool evidence: user_id=amelia_rossi_1247, date=2024-05-15, cancel= |
| 15 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #9: repeat |
| 18 | policy_checker | D3 | {"satisfied": false} | claims without prior tool evidence: user_id=amelia_rossi_1247, date=2024-05-15, cancel= |
| 22 | policy_checker | D3 | {"satisfied": false} | claims without prior tool evidence: date=2024-05-15, cancel= |
| 25 | planner | D1/handoff | {"p_delegate": 0.187, "H2": 0.695} | delegate-vs-not split p_delegate=0.19 |
| 26 | planner | D3 | {"checks": ["error"], "tool": "respond_to_user"} | tool respond_to_user call #15: error |

## Per-module summary
```
{
 "D1": {
  "n_scored": 25,
  "method": "stepwise"
 },
 "D2": {
  "n_utterances": 11,
  "n_na": 1
 },
 "D3": {
  "tool_calls": 18,
  "utterances": 9,
  "checks": {
   "empty": 1,
   "error": 2,
   "ignored": 1,
   "repeat": 1
  }
 },
 "D7": {
  "n_handoffs": 12
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`