# Audit report — aime_021

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | solver | D3 | {"checks": ["error"], "tool": "run_python"} | tool run_python call #1: error |
| 2 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=39, numeric=1089, numeric=33 |
| 4 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: final_answer=74, numeric=39 |
| 5 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["(x - 4)^2 + (1/2x^2 - 4x - 33)^2 = r^2", "0", "2y = x^2 - 8x + 12", "39", "4"], "altered": []} | verifier report->planner: missing ['(x - 4)^2 + (1/2x^2 - 4x - 33)^2 = r^2', '0', '2y = x^2 - 8x + 12'] altered [] |
| 6 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=39 |
| 7 | verifier | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #5: repeat |
| 9 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=39 |
| 10 | planner | D7/instruction->premise | {"fidelity": 0.0, "missing": ["4", "equation_of_parabola equation_of_circle discriminant_condition_for_tangency solving_system_of_equations"], "altered": []} | solver instruction->premise: missing ['4', 'equation_of_parabola equation_of_circle discriminant_condition_for_tangency solving_system_of_equations'] altered [] |
| 10 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["0", "1/2", "2r - 1 = 0", "r", "r = 0.5"], "altered": ["final_answer"]} | solver report->planner: missing ['0', '1/2', '2r - 1 = 0'] altered ['final_answer'] |

## Per-module summary
```
{
 "D1": {
  "n_scored": 14,
  "method": "stepwise"
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
 "D3_args": {
  "n_steps": 3,
  "n_values": 3,
  "n_ungrounded": 0
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3_args": "any ungrounded value"}`