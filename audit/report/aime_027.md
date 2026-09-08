# Audit report — aime_027

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | solver | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: run_python |
| 31 | planner | D1/tool | {"confidence": 0.456, "p_actual": 0.454, "margin": 0.0} | action distribution: solver 0.45, submit_answer 0.45, verifier 0.08 (actual: submit_answer) |
| 31 | planner | D1/handoff | {"p_delegate": 0.533, "H2": 0.997} | delegate-vs-not split p_delegate=0.53 |
| 31 | planner | D3 | {"missing_tool": false, "fabricated_arg": true, "tool_call_failed": false} | argument never given: submit_answer.final_answer=123 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 32,
  "method": "stepwise"
 },
 "D3": {
  "n_steps": 32,
  "flagged": 2,
  "missing_tool": 1,
  "fabricated_arg": 1,
  "tool_call_failed": 0
 },
 "D7": {
  "n_handoffs": 4
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3": "procedural flag (no threshold)"}`