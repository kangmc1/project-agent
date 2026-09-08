# Audit report — aime_008

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 13 | planner | D1/tool | {"confidence": 0.619, "p_actual": 0.725, "margin": 0.485} | action distribution: run_python 0.72, submit_answer 0.24, write_file 0.01 (actual: run_python) |
| 14 | planner | D1/tool | {"confidence": 0.4, "p_actual": 0.24, "margin": 0.354} | action distribution: no_tool 0.59, submit_answer 0.24, solver 0.11 (actual: submit_answer) |
| 14 | planner | D1/handoff | {"p_delegate": 0.155, "H2": 0.623} | delegate-vs-not split p_delegate=0.16 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 15,
  "method": "stepwise"
 },
 "D2": {
  "n_steps": 15,
  "flagged": 0,
  "missing_tool": 0,
  "fabricated_arg": 0,
  "tool_call_failed": 0
 },
 "D3": {
  "n_handoffs": 6
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D3": 1.0, "D2": "procedural flag (no threshold)"}`