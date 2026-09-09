# Audit report — aime_024

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 1 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["The computation was executed successfully.", "The integer part of 10^100 S is computed.", "The remainder when this integer is divided by 1000 is determined.", "The remainder when the greatest integer less than or equal to 10^100 S is divided by 1000 is 111.", "FINAL ANSWER: 111"], "altered": []} | solver report->planner: missing ['The computation was executed successfully.', 'The integer part of 10^100 S is computed.', 'The remainder when this integer is divided by 1000 is determined.'] altered [] |
| 2 | solver | D1/tool | {"confidence": 0.527, "p_actual": 0.365, "margin": 0.271} | action distribution: no_tool 0.64, run_python 0.36, write_file 0.00 (actual: run_python) |
| 5 | verifier | D1/tool | {"confidence": 0.645, "p_actual": 0.806, "margin": 0.612} | action distribution: run_python 0.81, no_tool 0.19, read_file 0.00 (actual: run_python) |
| 7 | planner | D1/handoff | {"p_delegate": 0.818, "H2": 0.685} | delegate-vs-not split p_delegate=0.82 |
| 9 | solver | D1/tool | {"confidence": 0.502, "p_actual": 0.539, "margin": 0.079} | action distribution: run_python 0.54, no_tool 0.46, write_file 0.00 (actual: run_python) |

## Per-module summary
```
{
 "D1": {
  "n_scored": 14,
  "method": "stepwise"
 },
 "D2": {
  "n_steps": 14,
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