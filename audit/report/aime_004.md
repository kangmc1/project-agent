# Audit report — aime_004

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 1 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["Expression is a + b + ab where a and b are distinct positive integers.", "We need to count integers n <= 100 that can be expressed as a + b + ab.", "Identity: a + b + ab = (a+1)(b+1) - 1.", "Verification: (a+1)(b+1) = ab + a + b + 1, so subtracting 1 gives ab + a + b.", "For each n <= 100, n+1 must equal (a+1)(b+1)."], "altered": []} | solver report->planner: missing ['Expression is a + b + ab where a and b are distinct positive integers.', 'We need to count integers n <= 100 that can be expressed as a + b + ab.', 'Identity: a + b + ab = (a+1)(b+1) - 1.'] altered [] |
| 4 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["The number of valid pairs (a+1, b+1) such that (a+1)(b+1) <= 101 and a+1 != b+1 is 274.", "Each such pair corresponds to a unique integer x = (a+1)(b+1) - 1 <= 100.", "The number of integers less than or equal to 100 that can be expressed in the form a + b + ab for distinct positive integers a and b is 274.", "Final answer: 274.", "a and b are distinct positive integers."], "altered": []} | verifier report->planner: missing ['The number of valid pairs (a+1, b+1) such that (a+1)(b+1) <= 101 and a+1 != b+1 is 274.', 'Each such pair corresponds to a unique integer x = (a+1)(b+1) - 1 <= 100.', 'The number of integers less than or equal to 100 that can be expressed in the form a + b + ab for distinct positive integers a and b is 274.'] altered [] |
| 7 | planner | D1/tool | {"confidence": 0.629, "p_actual": 0.751, "margin": 0.534} | action distribution: solver 0.75, no_tool 0.22, submit_answer 0.03 (actual: solver) |
| 7 | planner | D1/handoff | {"p_delegate": 0.753, "H2": 0.806} | delegate-vs-not split p_delegate=0.75 |
| 8 | solver | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: run_python |

## Per-module summary
```
{
 "D1": {
  "n_scored": 10,
  "method": "stepwise"
 },
 "D2": {
  "n_steps": 10,
  "flagged": 1,
  "missing_tool": 1,
  "fabricated_arg": 0,
  "tool_call_failed": 0
 },
 "D3": {
  "n_handoffs": 6
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D3": 1.0, "D2": "procedural flag (no threshold)"}`