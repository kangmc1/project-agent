# Audit report — aime_022

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | solver | D2 | {"s": 0.25, "unsupported": 0.75} | values not found in any prior tool result: 1/3, 1/3, 1/3, m/n |
| 5 | planner | D1/tool | {"confidence": 0.631, "p_actual": 0.72, "margin": 0.455} | action distribution: solver 0.72, submit_answer 0.26, no_tool 0.01 (actual: solver) |
| 5 | planner | D1/handoff | {"p_delegate": 0.724, "H2": 0.849} | delegate-vs-not split p_delegate=0.72 |
| 6 | solver | D2 | {"s": 0.0, "unsupported": 1.0} | values not found in any prior tool result: 2/6, 1/3, 2/6, 1/3, 2/6 |
| 7 | planner | D3 | {"checks": ["repeat"], "tool": "solver"} | tool solver call #4: repeat |

## Per-module summary
```
{
 "D1": {
  "n_scored": 8,
  "method": "stepwise"
 },
 "D2": {
  "n_utterances": 5,
  "n_na": 0
 },
 "D3": {
  "tool_calls": 4,
  "utterances": 1,
  "checks": {
   "repeat": 1
  }
 },
 "D7": {
  "n_handoffs": 6
 },
 "D9": {
  "n_steps": 5
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`