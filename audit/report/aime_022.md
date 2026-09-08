# Audit report — aime_022

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | solver | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: run_python |
| 4 | verifier | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: run_python |
| 5 | planner | D1/tool | {"confidence": 0.631, "p_actual": 0.72, "margin": 0.455} | action distribution: solver 0.72, submit_answer 0.26, no_tool 0.01 (actual: solver) |
| 5 | planner | D1/handoff | {"p_delegate": 0.724, "H2": 0.849} | delegate-vs-not split p_delegate=0.72 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 8,
  "method": "stepwise"
 },
 "D2": {
  "n_steps": 8,
  "flagged": 2,
  "missing_tool": 2,
  "fabricated_arg": 0,
  "tool_call_failed": 0
 },
 "D3": {
  "n_handoffs": 6
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D3": 1.0, "D2": "procedural flag (no threshold)"}`