# Audit report — airline_019

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["successfully retrieved and recorded in the case notes", "va5sgq"], "altered": []} | db_agent report->planner: missing ['successfully retrieved and recorded in the case notes', 'va5sgq'] altered [] |
| 4 | db_agent | D1/tool | {"confidence": 0.626, "p_actual": 0.471, "margin": 0.185} | action distribution: read_file 0.47, write_file 0.29, no_tool 0.24 (actual: read_file) |
| 4 | db_agent | D3 | {"checks": ["error", "ignored"], "tool": "read_file"} | tool read_file call #2: error, ignored |
| 7 | planner | D3 | {"checks": ["repeat"], "tool": "read_file"} | tool read_file call #5: repeat |
| 8 | planner | D1/tool | {"confidence": 0.64, "p_actual": 0.656, "margin": 0.312} | action distribution: no_tool 0.66, respond_to_user 0.34, policy_checker 0.00 (actual: no_tool) |

## Per-module summary
```
{
 "D1": {
  "n_scored": 7,
  "method": "stepwise"
 },
 "D2": {
  "n_utterances": 4,
  "n_na": 1
 },
 "D3": {
  "tool_calls": 5,
  "utterances": 3,
  "checks": {
   "error": 1,
   "ignored": 1,
   "repeat": 1
  }
 },
 "D7": {
  "n_handoffs": 2
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`