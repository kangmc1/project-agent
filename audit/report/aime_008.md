# Audit report — aime_008

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | solver | D2 | {"s": 0.4, "unsupported": 0.6} | values not found in any prior tool result: 17017^17, number of positive integer divisors of 17017^17, compute the remainder when this count is divided by 1000 |
| 2 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=12, numeric=1000 |
| 3 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=81, numeric=12 |
| 7 | verifier | D2 | {"s": 0.3333333333333333, "unsupported": 0.6666666666666667} | values not found in any prior tool result: 17017^17, remainder when this count is divided by 1000, 17017^k for 0 ≤ k ≤ 17, 17017^k ≡ 5 (mod 12) |
| 7 | verifier | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #5: repeat |
| 7 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=12 |
| 11 | solver | D2 | {"s": 0.0, "unsupported": 1.0} | values not found in any prior tool result: 7 * 11 * 13 * 17 |
| 11 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #8: repeat |
| 12 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=49, numeric=25, numeric=121 |
| 13 | planner | D1/tool | {"confidence": 0.619, "p_actual": 0.725, "margin": 0.485} | action distribution: run_python 0.72, submit_answer 0.24, write_file 0.01 (actual: run_python) |
| 14 | planner | D1/tool | {"confidence": 0.4, "p_actual": 0.24, "margin": 0.354} | action distribution: no_tool 0.59, submit_answer 0.24, solver 0.11 (actual: submit_answer) |
| 14 | planner | D1/handoff | {"p_delegate": 0.155, "H2": 0.623} | delegate-vs-not split p_delegate=0.16 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 15,
  "method": "stepwise"
 },
 "D2": {
  "n_utterances": 11,
  "n_na": 3
 },
 "D3": {
  "tool_calls": 10,
  "utterances": 10,
  "checks": {
   "repeat": 2
  }
 },
 "D7": {
  "n_handoffs": 6
 },
 "D9": {
  "n_steps": 6
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`