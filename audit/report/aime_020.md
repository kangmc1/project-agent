# Audit report — aime_020

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 3 | solver | D1/tool | {"confidence": 0.754, "p_actual": 0.895, "margin": 0.79} | action distribution: no_tool 0.89, run_python 0.10, read_file 0.00 (actual: no_tool) |
| 6 | verifier | D1/tool | {"confidence": 0.676, "p_actual": 0.836, "margin": 0.672} | action distribution: no_tool 0.84, run_python 0.16, read_file 0.00 (actual: no_tool) |
| 7 | planner | D1/tool | {"confidence": 0.612, "p_actual": 0.608, "margin": 0.22} | action distribution: solver 0.61, no_tool 0.39, submit_answer 0.00 (actual: solver) |
| 7 | planner | D1/handoff | {"p_delegate": 0.608, "H2": 0.966} | delegate-vs-not split p_delegate=0.61 |
| 7 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["15 = (r - 4) * (b - 2)", "15 = (r - 4) * (n - r - 2)", "32 52 72 92 112", "360", "4"], "altered": []} | solver report->planner: missing ['15 = (r - 4) * (b - 2)', '15 = (r - 4) * (n - r - 2)', '32 52 72 92 112'] altered [] |
| 8 | solver | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_error": false} | required but never called: run_python |

## Per-module summary
```
{
 "D1": {
  "n_scored": 10,
  "method": "stepwise"
 },
 "D3": {
  "n_steps": 10,
  "flagged": 1,
  "missing_tool": 1,
  "fabricated_arg": 0,
  "tool_error": 0
 },
 "D7": {
  "n_handoffs": 6
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3": "procedural flag (no threshold)"}`