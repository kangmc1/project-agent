# Audit report — aime_027

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=10, numeric=100, numeric=25, numeric=18, numeric=225 |
| 4 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=10, numeric=176, numeric=100, numeric=74, numeric=18 |
| 5 | verifier | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #3: repeat |
| 6 | verifier | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #4: repeat |
| 7 | verifier | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #5: repeat |
| 8 | verifier | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #6: repeat |
| 9 | verifier | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #7: repeat |
| 10 | verifier | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #8: repeat |
| 11 | verifier | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #9: repeat |
| 12 | verifier | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #10: repeat |
| 13 | verifier | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #11: repeat |
| 14 | verifier | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #12: repeat |
| 15 | verifier | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #13: repeat |
| 16 | verifier | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #14: repeat |
| 17 | verifier | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #15: repeat |
| 18 | verifier | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #16: repeat |
| 19 | verifier | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #17: repeat |
| 20 | verifier | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #18: repeat |
| 21 | verifier | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #19: repeat |
| 22 | verifier | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #20: repeat |
| 23 | verifier | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #21: repeat |
| 24 | verifier | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #22: repeat |
| 25 | verifier | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #23: repeat |
| 26 | verifier | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #24: repeat |
| 27 | verifier | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #25: repeat |
| 28 | verifier | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #26: repeat |
| 29 | verifier | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #27: repeat |
| 31 | planner | D1/tool | {"confidence": 0.456, "p_actual": 0.454, "margin": 0.0} | action distribution: solver 0.45, submit_answer 0.45, verifier 0.08 (actual: submit_answer) |
| 31 | planner | D1/handoff | {"p_delegate": 0.533, "H2": 0.997} | delegate-vs-not split p_delegate=0.53 |
| 31 | planner | D3/arguments | {"ungrounded_ratio": 1.0} | argument values never given to the agent: submit_answer.final_answer=123 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 32,
  "method": "stepwise"
 },
 "D3": {
  "tool_calls": 29,
  "utterances": 2,
  "checks": {
   "repeat": 25
  }
 },
 "D7": {
  "n_handoffs": 4
 },
 "D3_args": {
  "n_steps": 3,
  "n_values": 7,
  "n_ungrounded": 1
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3_args": "any ungrounded value"}`