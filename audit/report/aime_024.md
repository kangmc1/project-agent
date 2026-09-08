# Audit report — aime_024

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 1 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["111"], "altered": ["final_answer"]} | solver report->planner: missing ['111'] altered ['final_answer'] |
| 2 | solver | D1/tool | {"confidence": 0.527, "p_actual": 0.365, "margin": 0.271} | action distribution: no_tool 0.64, run_python 0.36, write_file 0.00 (actual: run_python) |
| 2 | solver | D2 | {"s": 0.07692307692307693, "unsupported": 0.9230769230769231} | values not found in any prior tool result: S = 1/9 + 1/99 + 1/999 + 1/9999 + ..., 1/(10^n - 1), floor(10^100 S) mod 1000, a_n = 1/(10^n - 1), S = sum_{n=1}^infty 1/(10^n - 1) |
| 2 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=99, numeric=99999, numeric=9999, numeric=999 |
| 3 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: final_answer=111 |
| 5 | verifier | D1/tool | {"confidence": 0.645, "p_actual": 0.806, "margin": 0.612} | action distribution: run_python 0.81, no_tool 0.19, read_file 0.00 (actual: run_python) |
| 5 | verifier | D2 | {"s": 0.0, "unsupported": 1.0} | values not found in any prior tool result: 1/9 + 1/99 + 1/999 + 1/9999 + \cdots, 1/(10^n - 1), number of digits in the denominator, \sum_{n=1}^\infty 1/(10^n - 1), find the remainder when the greatest integer less than or equal to 10^{100} S is divided by 1000 |
| 5 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=99, numeric=9999, numeric=999 |
| 7 | planner | D1/handoff | {"p_delegate": 0.818, "H2": 0.685} | delegate-vs-not split p_delegate=0.82 |
| 8 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=9999, numeric=999 |
| 9 | solver | D1/tool | {"confidence": 0.502, "p_actual": 0.539, "margin": 0.079} | action distribution: run_python 0.54, no_tool 0.46, write_file 0.00 (actual: run_python) |
| 9 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #6: repeat |
| 9 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=999, numeric=9999 |
| 10 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #7: repeat |
| 10 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=999, numeric=9999 |
| 11 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #8: repeat |
| 11 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=999, numeric=9999 |
| 12 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=999, numeric=9999 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 14,
  "method": "stepwise"
 },
 "D2": {
  "n_utterances": 10,
  "n_na": 0
 },
 "D3": {
  "tool_calls": 10,
  "utterances": 9,
  "checks": {
   "repeat": 3
  }
 },
 "D7": {
  "n_handoffs": 6
 },
 "D9": {
  "n_steps": 10
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`