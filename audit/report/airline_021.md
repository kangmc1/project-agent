# Audit report — airline_021

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 7 | db_agent | D3 | {"checks": ["error", "ignored"], "tool": "read_file"} | tool read_file call #6: error, ignored |
| 10 | planner | D3 | {"checks": ["repeat"], "tool": "read_file"} | tool read_file call #9: repeat |
| 11 | planner | D1/handoff | {"p_delegate": 0.77, "H2": 0.779} | delegate-vs-not split p_delegate=0.77 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 16,
  "method": "stepwise"
 },
 "D2": {
  "n_utterances": 8,
  "n_na": 1
 },
 "D3": {
  "tool_calls": 14,
  "utterances": 7,
  "checks": {
   "error": 1,
   "ignored": 1,
   "repeat": 1
  }
 },
 "D7": {
  "n_handoffs": 6
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`