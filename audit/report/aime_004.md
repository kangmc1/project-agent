# Audit report — aime_004

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 7 | planner | D1/tool | {"confidence": 0.629, "p_actual": 0.751, "margin": 0.534} | action distribution: solver 0.75, no_tool 0.22, submit_answer 0.03 (actual: solver) |
| 7 | planner | D1/handoff | {"p_delegate": 0.753, "H2": 0.806} | delegate-vs-not split p_delegate=0.75 |
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