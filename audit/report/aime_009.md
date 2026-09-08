# Audit report — aime_009

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 1 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["1", "900", "900/1", "901"], "altered": ["final_answer", "m_plus_n"]} | solver report->planner: missing ['1', '900', '900/1'] altered ['final_answer', 'm_plus_n'] |
| 2 | solver | D2 | {"s": 0.15384615384615385, "unsupported": 0.8461538461538461} | values not found in any prior tool result: rolls the die and places the sticker labeled 1 on the top face, then rolls again and places sticker 2 on the top face, continuing this process, If the die lands with a sticker already on the top face, the new sticker covers the old one, Number of favorable outcomes, Number of outcomes where all even-numbered stickers are visible, exactly one face is left blank at the end |
| 7 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=19, numeric=10, numeric=16, numeric=14, numeric=11 |
| 8 | planner | D1/tool | {"confidence": 0.522, "p_actual": 0.613, "margin": 0.285} | action distribution: solver 0.61, submit_answer 0.33, verifier 0.05 (actual: solver) |
| 8 | planner | D1/handoff | {"p_delegate": 0.664, "H2": 0.921} | delegate-vs-not split p_delegate=0.66 |
| 9 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=27 |
| 10 | solver | D2 | {"s": 0.4444444444444444, "unsupported": 0.5555555555555556} | values not found in any prior tool result: binom(6, 3), 1/3!, 3^3, 90/90, 1 + 1 |
| 10 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #7: repeat |
| 10 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=27 |
| 11 | solver | D2 | {"s": 0.4444444444444444, "unsupported": 0.5555555555555556} | values not found in any prior tool result: binom(6, 3), 1/3!, 3^3, 90/90, 1 + 1 |
| 11 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #8: repeat |
| 11 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=27 |
| 12 | solver | D1/tool | {"confidence": 0.741, "p_actual": 0.884, "margin": 0.768} | action distribution: run_python 0.88, no_tool 0.12, read_file 0.00 (actual: run_python) |
| 12 | solver | D2 | {"s": 0.4444444444444444, "unsupported": 0.5555555555555556} | values not found in any prior tool result: binom(6, 3), 1/3!, 3^3, 90/90, 1 + 1 |
| 12 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #9: repeat |
| 12 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=27 |
| 13 | solver | D2 | {"s": 0.4444444444444444, "unsupported": 0.5555555555555556} | values not found in any prior tool result: binom(6, 3), 1/3!, 3^3, 90/90, 1 + 1 |
| 13 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #10: repeat |
| 13 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=27 |
| 14 | solver | D2 | {"s": 0.4444444444444444, "unsupported": 0.5555555555555556} | values not found in any prior tool result: binom(6, 3), 1/3!, 3^3, 90/90, 1 + 1 |
| 14 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #11: repeat |
| 14 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=27 |
| 15 | solver | D2 | {"s": 0.4444444444444444, "unsupported": 0.5555555555555556} | values not found in any prior tool result: binom(6, 3), 1/3!, 3^3, 90/90, 1 + 1 |
| 15 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #12: repeat |
| 15 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=27 |
| 16 | solver | D2 | {"s": 0.4444444444444444, "unsupported": 0.5555555555555556} | values not found in any prior tool result: binom(6, 3), 1/3!, 3^3, 90/90, 1 + 1 |
| 16 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #13: repeat |
| 16 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=27 |
| 17 | solver | D2 | {"s": 0.4444444444444444, "unsupported": 0.5555555555555556} | values not found in any prior tool result: binom(6, 3), 1/3!, 3^3, 90/90, 1 + 1 |
| 17 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #14: repeat |
| 17 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=27 |
| 18 | solver | D2 | {"s": 0.4444444444444444, "unsupported": 0.5555555555555556} | values not found in any prior tool result: binom(6, 3), 1/3!, 3^3, 90/90, 1 + 1 |
| 18 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #15: repeat |
| 18 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=27 |
| 19 | solver | D2 | {"s": 0.4444444444444444, "unsupported": 0.5555555555555556} | values not found in any prior tool result: binom(6, 3), 1/3!, 3^3, 90/90, 1 + 1 |
| 19 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #16: repeat |
| 19 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=27 |
| 20 | solver | D2 | {"s": 0.4444444444444444, "unsupported": 0.5555555555555556} | values not found in any prior tool result: binom(6, 3), 1/3!, 3^3, 90/90, 1 + 1 |
| 20 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #17: repeat |
| 20 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=27 |
| 21 | solver | D2 | {"s": 0.4444444444444444, "unsupported": 0.5555555555555556} | values not found in any prior tool result: binom(6, 3), 1/3!, 3^3, 90/90, 1 + 1 |
| 21 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #18: repeat |
| 21 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=27 |
| 22 | solver | D2 | {"s": 0.4444444444444444, "unsupported": 0.5555555555555556} | values not found in any prior tool result: binom(6, 3), 1/3!, 3^3, 90/90, 1 + 1 |
| 22 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #19: repeat |
| 22 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=27 |
| 23 | solver | D2 | {"s": 0.4444444444444444, "unsupported": 0.5555555555555556} | values not found in any prior tool result: binom(6, 3), 1/3!, 3^3, 90/90, 1 + 1 |
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
 "D2": {
  "n_utterances": 22,
  "n_na": 0
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
 "D9": {
  "n_steps": 22
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`