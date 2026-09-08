# Audit report — aime_023

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=10000, numeric=475, numeric=425, numeric=125, numeric=100 |
| 3 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["(2x + y)/2", "125:6", "2x + y", "6/125(2x + y)", "ai + ic + y"], "altered": []} | verifier report->planner: missing ['(2x + y)/2', '125:6', '2x + y'] altered [] |
| 4 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=125 |
| 5 | planner | D1/tool | {"confidence": 0.623, "p_actual": 0.673, "margin": 0.355} | action distribution: solver 0.67, submit_answer 0.32, verifier 0.01 (actual: solver) |
| 5 | planner | D1/handoff | {"p_delegate": 0.682, "H2": 0.903} | delegate-vs-not split p_delegate=0.68 |
| 5 | planner | D7/instruction->premise | {"fidelity": 0.0, "missing": ["incomplete", "missing", "re-solve the aime problem with the objection from the verifier: the solution is incomplete and lacks a clear derivation of the incenter distances and the final answer. please provide a complete solution with the final integer answer and the key equations used."], "altered": []} | solver instruction->premise: missing ['incomplete', 'missing', 're-solve the aime problem with the objection from the verifier: the solution is incomplete and lacks a clear derivation of the incenter distances and the final answer. please provide a complete solution with the final integer answer and the key equations used.'] altered [] |
| 6 | solver | D1/tool | {"confidence": 0.749, "p_actual": 0.889, "margin": 0.778} | action distribution: run_python 0.89, no_tool 0.11, write_file 0.00 (actual: run_python) |
| 6 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=289, numeric=150, numeric=225, numeric=15, numeric=256 |
| 7 | solver | D3 | {"checks": ["error"], "tool": "run_python"} | tool run_python call #4: error |
| 7 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=45, numeric=35 |
| 8 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #5: repeat |
| 9 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #6: repeat |
| 10 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #7: repeat |
| 11 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #8: repeat |
| 12 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #9: repeat |
| 13 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #10: repeat |
| 14 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #11: repeat |
| 15 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #12: repeat |
| 16 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #13: repeat |
| 17 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #14: repeat |
| 18 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #15: repeat |
| 19 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #16: repeat |
| 20 | solver | D1/tool | {"confidence": 0.543, "p_actual": 0.67, "margin": 0.341} | action distribution: run_python 0.67, no_tool 0.33, read_file 0.00 (actual: run_python) |
| 20 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #17: repeat |
| 21 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #18: repeat |
| 22 | solver | D1/tool | {"confidence": 0.513, "p_actual": 0.404, "margin": 0.193} | action distribution: no_tool 0.60, run_python 0.40, read_file 0.00 (actual: run_python) |
| 22 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #19: repeat |
| 23 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #20: repeat |
| 24 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #21: repeat |
| 25 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #22: repeat |
| 26 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #23: repeat |
| 27 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #24: repeat |
| 28 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #25: repeat |
| 29 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #26: repeat |
| 30 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #27: repeat |
| 31 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #28: repeat |
| 32 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #29: repeat |
| 33 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #30: repeat |
| 34 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #31: repeat |
| 35 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #32: repeat |
| 36 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #33: repeat |
| 37 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #34: repeat |
| 38 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #35: repeat |
| 39 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #36: repeat |
| 40 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #37: repeat |
| 41 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #38: repeat |
| 42 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #39: repeat |
| 43 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #40: repeat |
| 44 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #41: repeat |
| 45 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #42: repeat |
| 46 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #43: repeat |
| 47 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #44: repeat |
| 48 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #45: repeat |
| 49 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #46: repeat |
| 50 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #47: repeat |
| 51 | planner | D3 | {"checks": ["error", "ignored"], "tool": "solver"} | tool solver call #48: error, ignored |

## Per-module summary
```
{
 "D1": {
  "n_scored": 53,
  "method": "stepwise"
 },
 "D3": {
  "tool_calls": 49,
  "utterances": 48,
  "checks": {
   "error": 2,
   "repeat": 43,
   "ignored": 1
  }
 },
 "D7": {
  "n_handoffs": 6
 },
 "D3_args": {
  "n_steps": 3,
  "n_values": 3,
  "n_ungrounded": 0
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3_args": "any ungrounded value"}`