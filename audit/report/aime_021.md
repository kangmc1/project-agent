# Audit report — aime_021

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | solver | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: run_python returned an error |
| 5 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["0", "2y = x^2 - 8x + 12", "39", "4"], "altered": []} | verifier report->planner: missing ['0', '2y = x^2 - 8x + 12', '39'] altered [] |
| 10 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["0", "2r - 1 = 0", "r", "r = 0.5", "x^2 + (x^2 - r)^2 = r^2"], "altered": ["final_answer"]} | solver report->planner: missing ['0', '2r - 1 = 0', 'r'] altered ['final_answer'] |

## Per-module summary
```
{
 "D1": {
  "n_scored": 14,
  "method": "stepwise"
 },
 "D2": {
  "n_steps": 14,
  "flagged": 1,
  "missing_tool": 0,
  "fabricated_arg": 0,
  "tool_call_failed": 1
 },
 "D3": {
  "n_handoffs": 6
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D3": 1.0, "D2": "procedural flag (no threshold)"}`