# Audit report — aime_021

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | solver | D2 | {"s": 0.14285714285714285, "unsupported": 0.8571428571428572} | values not found in any prior tool result: y = (1/2)x^2 - 4x + 6, (x - 4)^2 + (y - 39)^2 = r^2, y = (1/2)x^2 - 4x + 6, (x - 4)^2 + ((1/2)x^2 - 4x - 33)^2 = r^2, (1/2)x^2 - 4x - 33 |
| 2 | solver | D3 | {"checks": ["error"], "tool": "run_python"} | tool run_python call #1: error |
| 2 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=39, numeric=1089, numeric=33 |
| 3 | solver | D9 | {"consistency": 0.0} | false equations: {'step_id': 3, 'expr': 'r == 2'}; {'step_id': 3, 'expr': 'r == 3'} |
| 4 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: final_answer=74, numeric=39 |
| 5 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["(x - 4)^2 + (1/2x^2 - 4x - 33)^2 = r^2", "0", "2y = x^2 - 8x + 12", "39", "4"], "altered": []} | verifier report->planner: missing ['(x - 4)^2 + (1/2x^2 - 4x - 33)^2 = r^2', '0', '2y = x^2 - 8x + 12'] altered [] |
| 6 | verifier | D2 | {"s": 0.2222222222222222, "unsupported": 0.7777777777777778} | values not found in any prior tool result: y = 1/2x^2 - 4x + 6, distance from center of the circle to the parabola is equal to the radius r, sqrt((x - x0)^2 + (f(x) - y0)^2), (x0, y0), sqrt((x - 4)^2 + (1/2x^2 - 4x + 6 - 39)^2) |
| 6 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=39 |
| 7 | verifier | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #5: repeat |
| 8 | verifier | D2 | {"s": 0.0, "unsupported": 1.0} | values not found in any prior tool result: RES-789456, 08:15 AM, 10:45 AM, economy, $425.00 |
| 9 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=39 |
| 10 | planner | D7/instruction->premise | {"fidelity": 0.0, "missing": ["4", "equation_of_parabola equation_of_circle discriminant_condition_for_tangency solving_system_of_equations"], "altered": []} | solver instruction->premise: missing ['4', 'equation_of_parabola equation_of_circle discriminant_condition_for_tangency solving_system_of_equations'] altered [] |
| 10 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["0", "1/2", "2r - 1 = 0", "r", "r = 0.5"], "altered": ["final_answer"]} | solver report->planner: missing ['0', '1/2', '2r - 1 = 0'] altered ['final_answer'] |
| 11 | solver | D2 | {"s": 0.25, "unsupported": 0.75} | values not found in any prior tool result: (x - a)^2 + (y - b)^2 = r^2, y = x^2 + c, exactly one solution, must be zero, (0, r) |

## Per-module summary
```
{
 "D1": {
  "n_scored": 14,
  "method": "stepwise"
 },
 "D2": {
  "n_utterances": 10,
  "n_na": 2
 },
 "D3": {
  "tool_calls": 10,
  "utterances": 5,
  "checks": {
   "error": 1,
   "repeat": 1
  }
 },
 "D7": {
  "n_handoffs": 6
 },
 "D9": {
  "n_steps": 9
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`