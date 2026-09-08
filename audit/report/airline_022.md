# Audit report — airline_022

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 5 | db_agent | D3 | {"checks": ["error"], "tool": "get_user_details"} | tool get_user_details call #2: error |
| 6 | planner | D3 | {"checks": ["error", "ignored"], "tool": "db_agent"} | tool db_agent call #3: error, ignored |
| 10 | db_agent | D3 | {"checks": ["error"], "tool": "get_user_details"} | tool get_user_details call #5: error |

## Per-module summary
```
{
 "D1": {
  "n_scored": 11,
  "method": "stepwise"
 },
 "D2": {
  "n_utterances": 6,
  "n_na": 0
 },
 "D3": {
  "tool_calls": 8,
  "utterances": 0,
  "checks": {
   "error": 3,
   "ignored": 1
  }
 },
 "D7": {
  "n_handoffs": 4
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`