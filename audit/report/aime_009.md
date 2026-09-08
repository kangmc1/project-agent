# Audit report — aime_009

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 1 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["1", "900", "900/1", "901"], "altered": ["final_answer", "m_plus_n"]} | solver report->planner: missing ['1', '900', '900/1'] altered ['final_answer', 'm_plus_n'] |
| 7 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=19, numeric=10, numeric=16, numeric=14, numeric=11 |
| 8 | planner | D1/tool | {"confidence": 0.522, "p_actual": 0.613, "margin": 0.285} | action distribution: solver 0.61, submit_answer 0.33, verifier 0.05 (actual: solver) |
| 8 | planner | D1/handoff | {"p_delegate": 0.664, "H2": 0.921} | delegate-vs-not split p_delegate=0.66 |
| 9 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=27 |
| 10 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #7: repeat |
| 10 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=27 |
| 11 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #8: repeat |
| 11 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=27 |
| 12 | solver | D1/tool | {"confidence": 0.741, "p_actual": 0.884, "margin": 0.768} | action distribution: run_python 0.88, no_tool 0.12, read_file 0.00 (actual: run_python) |
| 12 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #9: repeat |
| 12 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=27 |
| 13 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #10: repeat |
| 13 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=27 |
| 14 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #11: repeat |
| 14 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=27 |
| 15 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #12: repeat |
| 15 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=27 |
| 16 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #13: repeat |
| 16 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=27 |
| 17 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #14: repeat |
| 17 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=27 |
| 18 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #15: repeat |
| 18 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=27 |
| 19 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #16: repeat |
| 19 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=27 |
| 20 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #17: repeat |
| 20 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=27 |
| 21 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #18: repeat |
| 21 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=27 |
| 22 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #19: repeat |
| 22 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=27 |
| 23 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #20: repeat |
| 23 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=27 |
| 24 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=27 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 26,
  "method": "stepwise"
 },
 "D3": {
  "tool_calls": 22,
  "utterances": 20,
  "checks": {
   "repeat": 14
  }
 },
 "D7": {
  "n_handoffs": 6
 },
 "D3_args": {
  "n_steps": 1,
  "n_values": 1,
  "n_ungrounded": 0
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3_args": "any ungrounded value"}`