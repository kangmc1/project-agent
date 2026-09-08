# Audit report — airline_046

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 6 | db_agent | D2 | {"s": 0.0, "unsupported": 1.0} | values not found in any prior tool result: San Francisco (SFO), New York (JFK), May 15th, 2024 |
| 9 | db_agent | D3 | {"checks": ["repeat"], "tool": "search_direct_flight"} | tool search_direct_flight call #5: repeat |
| 15 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["user not found"], "altered": ["final_answer", "verdict"]} | db_agent report->planner: missing ['user not found'] altered ['final_answer', 'verdict'] |
| 16 | db_agent | D3 | {"checks": ["error"], "tool": "get_user_details"} | tool get_user_details call #9: error |
| 17 | planner | D3 | {"checks": ["error", "ignored"], "tool": "db_agent"} | tool db_agent call #10: error, ignored |
| 20 | planner | D1/handoff | {"p_delegate": 0.82, "H2": 0.68} | delegate-vs-not split p_delegate=0.82 |
| 20 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["not_found", "sara_doe_496", "the provided user id was not found in the database."], "altered": ["verdict"]} | db_agent report->planner: missing ['not_found', 'sara_doe_496', 'the provided user id was not found in the database.'] altered ['verdict'] |
| 21 | db_agent | D3 | {"checks": ["error", "repeat"], "tool": "get_user_details"} | tool get_user_details call #12: error, repeat |
| 22 | planner | D3 | {"checks": ["error"], "tool": "db_agent"} | tool db_agent call #13: error |
| 34 | db_agent | D1/tool | {"confidence": 0.775, "p_actual": 0.678, "margin": 0.358} | action distribution: search_direct_flight 0.68, search_onestop_flight 0.32, no_tool 0.00 (actual: search_direct_flight) |
| 39 | db_agent | D3 | {"checks": ["repeat"], "tool": "search_direct_flight"} | tool search_direct_flight call #22: repeat |
| 40 | db_agent | D1/tool | {"confidence": 0.767, "p_actual": 0.632, "margin": 0.264} | action distribution: search_onestop_flight 0.63, no_tool 0.37, transfer_to_human_agents 0.00 (actual: search_onestop_flight) |
| 45 | db_agent | D3 | {"checks": ["repeat"], "tool": "search_direct_flight"} | tool search_direct_flight call #26: repeat |
| 59 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["not found", "sara_doe_496"], "altered": ["user_id", "verdict"]} | db_agent report->planner: missing ['not found', 'sara_doe_496'] altered ['user_id', 'verdict'] |
| 60 | db_agent | D1/tool | {"confidence": 0.635, "p_actual": 0.62, "margin": 0.371} | action distribution: get_user_details 0.62, search_direct_flight 0.25, no_tool 0.07 (actual: get_user_details) |
| 60 | db_agent | D3 | {"checks": ["error", "repeat"], "tool": "get_user_details"} | tool get_user_details call #36: error, repeat |
| 61 | planner | D3 | {"checks": ["error", "ignored"], "tool": "db_agent"} | tool db_agent call #37: error, ignored |

## Per-module summary
```
{
 "D1": {
  "n_scored": 52,
  "method": "stepwise"
 },
 "D2": {
  "n_utterances": 25,
  "n_na": 7
 },
 "D3": {
  "tool_calls": 40,
  "utterances": 4,
  "checks": {
   "repeat": 5,
   "error": 6,
   "ignored": 2
  }
 },
 "D7": {
  "n_handoffs": 24
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`