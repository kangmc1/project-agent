# Audit report — aime_028

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 5 | solver | D1/tool | {"confidence": 0.74, "p_actual": 0.884, "margin": 0.767} | action distribution: run_python 0.88, no_tool 0.12, read_file 0.00 (actual: run_python) |
| 9 | planner | D1/tool | {"confidence": 0.588, "p_actual": 0.76, "margin": 0.628} | action distribution: verifier 0.76, solver 0.13, submit_answer 0.10 (actual: verifier) |
| 9 | planner | D1/handoff | {"p_delegate": 0.892, "H2": 0.493} | delegate-vs-not split p_delegate=0.89 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 12,
  "method": "stepwise"
 },
 "D3": {
  "n_steps": 12,
  "flagged": 0,
  "missing_tool": 0,
  "fabricated_arg": 0,
  "tool_call_failed": 0
 },
 "D7": {
  "n_handoffs": 4
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3": "procedural flag (no threshold)"}`