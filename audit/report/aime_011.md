# Audit report — aime_011

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 1 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["Maximum possible value of M is 7056.", "Remainder when 7056 divided by 1000 is 56.", "Final answer is 56."], "altered": []} | solver report->planner: missing ['Maximum possible value of M is 7056.', 'Remainder when 7056 divided by 1000 is 56.', 'Final answer is 56.'] altered [] |
| 4 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["The integers from 1 to 64 are placed in an 8x8 grid.", "M is the sum of the absolute differences between adjacent cells horizontally and vertically.", "The goal is to find the maximum possible value of M and compute its remainder when divided by 1000.", "Total adjacent pairs = 112.", "Strategy: alternate high and low numbers in a checkerboard pattern."], "altered": []} | verifier report->planner: missing ['The integers from 1 to 64 are placed in an 8x8 grid.', 'M is the sum of the absolute differences between adjacent cells horizontally and vertically.', 'The goal is to find the maximum possible value of M and compute its remainder when divided by 1000.'] altered [] |
| 5 | verifier | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: run_python |

## Per-module summary
```
{
 "D1": {
  "n_scored": 7,
  "method": "stepwise"
 },
 "D2": {
  "n_steps": 7,
  "flagged": 1,
  "missing_tool": 1,
  "fabricated_arg": 0,
  "tool_call_failed": 0
 },
 "D3": {
  "n_handoffs": 4
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D3": 1.0, "D2": "procedural flag (no threshold)"}`