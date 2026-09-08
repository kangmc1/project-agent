# Audit report — airline_006

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 4 | planner | D7/instruction->premise | {"fidelity": 0.0, "missing": ["john doe", "res123456"], "altered": []} | db_agent instruction->premise: missing ['john doe', 'res123456'] altered [] |
| 5 | db_agent | D1/tool | {"confidence": 0.754, "p_actual": 0.789, "margin": 0.652} | action distribution: get_user_details 0.79, get_reservation_details 0.14, search_direct_flight 0.06 (actual: get_user_details) |
| 5 | db_agent | D3 | {"checks": ["error"], "tool": "get_user_details"} | tool get_user_details call #2: error |
| 5 | db_agent | D3/arguments | {"ungrounded_ratio": 1.0} | argument values never given to the agent: get_user_details.user_id=sara_doe_496 |
| 6 | planner | D3 | {"checks": ["error", "ignored"], "tool": "db_agent"} | tool db_agent call #3: error, ignored |
| 10 | db_agent | D3 | {"checks": ["error"], "tool": "get_user_details"} | tool get_user_details call #5: error |
| 10 | db_agent | D3/arguments | {"ungrounded_ratio": 1.0} | argument values never given to the agent: get_user_details.user_id=aarav_garcia_123 |
| 11 | planner | D3 | {"checks": ["error", "ignored"], "tool": "db_agent"} | tool db_agent call #6: error, ignored |
| 14 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["aarav garcia", "april 5th", "atl", "could not be found", "could not be located"], "altered": ["final_answer", "verdict"]} | db_agent report->planner: missing ['aarav garcia', 'april 5th', 'atl'] altered ['final_answer', 'verdict'] |
| 15 | db_agent | D3 | {"checks": ["error", "repeat"], "tool": "get_user_details"} | tool get_user_details call #8: error, repeat |
| 15 | db_agent | D3/arguments | {"ungrounded_ratio": 1.0} | argument values never given to the agent: get_user_details.user_id=aarav_garcia_123 |
| 19 | planner | D1/tool | {"confidence": 0.565, "p_actual": 0.654, "margin": 0.345} | action distribution: db_agent 0.65, respond_to_user 0.31, policy_checker 0.03 (actual: db_agent) |
| 19 | planner | D1/handoff | {"p_delegate": 0.686, "H2": 0.897} | delegate-vs-not split p_delegate=0.69 |
| 20 | db_agent | D1/tool | {"confidence": 0.746, "p_actual": 0.617, "margin": 0.243} | action distribution: get_user_details 0.62, search_direct_flight 0.37, think 0.01 (actual: get_user_details) |
| 20 | db_agent | D3 | {"checks": ["error", "repeat"], "tool": "get_user_details"} | tool get_user_details call #11: error, repeat |
| 20 | db_agent | D3/arguments | {"ungrounded_ratio": 1.0} | argument values never given to the agent: get_user_details.user_id=aarav_garcia_123 |
| 25 | db_agent | D3 | {"checks": ["error", "repeat"], "tool": "get_user_details"} | tool get_user_details call #14: error, repeat |
| 25 | db_agent | D3/arguments | {"ungrounded_ratio": 1.0} | argument values never given to the agent: get_user_details.user_id=aarav_garcia_123 |
| 37 | planner | D3 | {"satisfied": false} | claims without prior tool evidence: refund= |

## Per-module summary
```
{
 "D1": {
  "n_scored": 27,
  "method": "stepwise"
 },
 "D3": {
  "tool_calls": 20,
  "utterances": 2,
  "checks": {
   "error": 7,
   "ignored": 2,
   "repeat": 3
  }
 },
 "D7": {
  "n_handoffs": 12
 },
 "D3_args": {
  "n_steps": 5,
  "n_values": 5,
  "n_ungrounded": 5
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3_args": "any ungrounded value"}`