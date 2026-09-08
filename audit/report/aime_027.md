# Audit report — aime_027

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | solver | D2 | {"s": 0.0, "unsupported": 1.0} | values not found in any prior tool result: 5√10, 5√10, 10, 5√10, 5√10, 18, m/n |
| 2 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=10, numeric=100, numeric=25, numeric=18, numeric=225 |
| 4 | verifier | D2 | {"s": 0.0, "unsupported": 1.0} | values not found in any prior tool result: two isosceles triangle faces with side lengths 5√10, 5√10, and 10, two isosceles triangle faces with side lengths 5√10, 5√10, and 18, m/n, where m and n are relatively prime positive integers, to be found |
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

## Per-module summary
```
{
 "D1": {
  "n_scored": 32,
  "method": "stepwise"
 },
 "D2": {
  "n_utterances": 29,
  "n_na": 26
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
 "D9": {
  "n_steps": 28
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`