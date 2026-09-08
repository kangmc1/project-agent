# Audit report — aime_002

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 1 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["26"], "altered": []} | solver report->planner: missing ['26'] altered [] |
| 2 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=42124 |
| 6 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=26 |
| 7 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: final_answer=26 |
| 9 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=42124 |
| 11 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["ensure that half_length is an integer", "the range function is still being passed a float", "use of 10**(half_length - 1) and 10**half_length when half_length is a float"], "altered": []} | solver report->planner: missing ['ensure that half_length is an integer', 'the range function is still being passed a float', 'use of 10**(half_length - 1) and 10**half_length when half_length is a float'] altered [] |
| 12 | solver | D3 | {"checks": ["error"], "tool": "run_python"} | tool run_python call #9: error |
| 12 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=12321, numeric=26, numeric=121 |
| 13 | solver | D1/tool | {"confidence": 0.695, "p_actual": 0.85, "margin": 0.7} | action distribution: run_python 0.85, no_tool 0.15, read_file 0.00 (actual: run_python) |
| 13 | solver | D3 | {"checks": ["error"], "tool": "run_python"} | tool run_python call #10: error |
| 14 | solver | D3 | {"checks": ["error", "repeat"], "tool": "run_python"} | tool run_python call #11: error, repeat |
| 15 | solver | D3 | {"checks": ["error", "repeat"], "tool": "run_python"} | tool run_python call #12: error, repeat |
| 16 | solver | D3 | {"checks": ["error", "repeat"], "tool": "run_python"} | tool run_python call #13: error, repeat |
| 17 | solver | D3 | {"checks": ["error", "repeat"], "tool": "run_python"} | tool run_python call #14: error, repeat |
| 18 | solver | D3 | {"checks": ["error", "repeat"], "tool": "run_python"} | tool run_python call #15: error, repeat |
| 19 | solver | D3 | {"checks": ["error", "repeat"], "tool": "run_python"} | tool run_python call #16: error, repeat |
| 20 | solver | D3 | {"checks": ["error", "repeat"], "tool": "run_python"} | tool run_python call #17: error, repeat |
| 21 | solver | D3 | {"checks": ["error", "repeat"], "tool": "run_python"} | tool run_python call #18: error, repeat |
| 22 | solver | D3 | {"checks": ["error", "repeat"], "tool": "run_python"} | tool run_python call #19: error, repeat |
| 23 | solver | D3 | {"checks": ["error", "repeat"], "tool": "run_python"} | tool run_python call #20: error, repeat |
| 24 | solver | D3 | {"checks": ["error", "repeat"], "tool": "run_python"} | tool run_python call #21: error, repeat |
| 25 | solver | D3 | {"checks": ["error", "repeat"], "tool": "run_python"} | tool run_python call #22: error, repeat |
| 26 | solver | D3 | {"checks": ["error", "repeat"], "tool": "run_python"} | tool run_python call #23: error, repeat |
| 27 | solver | D3 | {"checks": ["error", "repeat"], "tool": "run_python"} | tool run_python call #24: error, repeat |
| 28 | solver | D3 | {"checks": ["error", "repeat"], "tool": "run_python"} | tool run_python call #25: error, repeat |
| 29 | solver | D3 | {"checks": ["error", "repeat"], "tool": "run_python"} | tool run_python call #26: error, repeat |
| 30 | solver | D3 | {"checks": ["error", "repeat"], "tool": "run_python"} | tool run_python call #27: error, repeat |
| 31 | solver | D3 | {"checks": ["error", "repeat"], "tool": "run_python"} | tool run_python call #28: error, repeat |
| 32 | solver | D3 | {"checks": ["error", "repeat"], "tool": "run_python"} | tool run_python call #29: error, repeat |
| 33 | solver | D3 | {"checks": ["error", "repeat"], "tool": "run_python"} | tool run_python call #30: error, repeat |
| 34 | solver | D3 | {"checks": ["error", "repeat"], "tool": "run_python"} | tool run_python call #31: error, repeat |
| 35 | planner | D3 | {"checks": ["error", "ignored"], "tool": "solver"} | tool solver call #32: error, ignored |
| 36 | planner | D1/tool | {"confidence": 0.463, "p_actual": 0.655, "margin": 0.468} | action distribution: submit_answer 0.66, verifier 0.19, no_tool 0.12 (actual: submit_answer) |
| 36 | planner | D1/handoff | {"p_delegate": 0.22, "H2": 0.761} | delegate-vs-not split p_delegate=0.22 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 37,
  "method": "stepwise"
 },
 "D3": {
  "tool_calls": 33,
  "utterances": 31,
  "checks": {
   "error": 24,
   "repeat": 21,
   "ignored": 1
  }
 },
 "D7": {
  "n_handoffs": 6
 },
 "D3_args": {
  "n_steps": 4,
  "n_values": 9,
  "n_ungrounded": 0
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3_args": "any ungrounded value"}`