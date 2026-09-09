# Audit report — aime_023

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | solver | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: run_python |
| 3 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["Triangle ABC is isosceles with AB = BC.", "I is the incenter of triangle ABC.", "The perimeters of triangle ABC and triangle AIC are in the ratio 125:6.", "All sides of both triangles have integer lengths.", "We are to find the minimum possible value of AB."], "altered": []} | verifier report->planner: missing ['Triangle ABC is isosceles with AB = BC.', 'I is the incenter of triangle ABC.', 'The perimeters of triangle ABC and triangle AIC are in the ratio 125:6.'] altered [] |
| 4 | verifier | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: run_python |
| 5 | planner | D1/tool | {"confidence": 0.623, "p_actual": 0.673, "margin": 0.355} | action distribution: solver 0.67, submit_answer 0.32, verifier 0.01 (actual: solver) |
| 5 | planner | D1/handoff | {"p_delegate": 0.682, "H2": 0.903} | delegate-vs-not split p_delegate=0.68 |
| 5 | planner | D3/instruction->premise | {"fidelity": 0.0, "missing": ["The problem is an AIME problem.", "The solution is incomplete.", "The solution lacks a clear derivation of the incenter distances.", "The solution lacks the final answer.", "The request is to provide a complete solution with the final integer answer and key equations used."], "altered": []} | solver instruction->premise: missing ['The problem is an AIME problem.', 'The solution is incomplete.', 'The solution lacks a clear derivation of the incenter distances.'] altered [] |
| 5 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["The system of equations has been solved.", "a = 30", "b = 40", "c = 80", "These side lengths do not form a valid triangle because the product inside the square root in Heron's formula is negative."], "altered": []} | solver report->planner: missing ['The system of equations has been solved.', 'a = 30', 'b = 40'] altered [] |
| 6 | solver | D1/tool | {"confidence": 0.749, "p_actual": 0.889, "margin": 0.778} | action distribution: run_python 0.89, no_tool 0.11, write_file 0.00 (actual: run_python) |
| 7 | solver | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: run_python returned an error |
| 20 | solver | D1/tool | {"confidence": 0.543, "p_actual": 0.67, "margin": 0.341} | action distribution: run_python 0.67, no_tool 0.33, read_file 0.00 (actual: run_python) |
| 22 | solver | D1/tool | {"confidence": 0.513, "p_actual": 0.404, "margin": 0.193} | action distribution: no_tool 0.60, run_python 0.40, read_file 0.00 (actual: run_python) |

## Per-module summary
```
{
 "D1": {
  "n_scored": 53,
  "method": "stepwise"
 },
 "D2": {
  "n_steps": 53,
  "flagged": 3,
  "missing_tool": 2,
  "fabricated_arg": 0,
  "tool_call_failed": 1
 },
 "D3": {
  "n_handoffs": 6
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D3": 1.0, "D2": "procedural flag (no threshold)"}`