# Audit report — aime_008

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 1 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["472392", "1000", "392"], "altered": []} | solver report->planner: missing ['472392', '1000', '392'] altered [] |
| 10 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["Prime factorization of 17017 is 7 × 11 × 13 × 17.", "17017^17 has prime factorization 7^17 × 11^17 × 13^17 × 17^17.", "Any positive divisor d of 17017^17 can be written as d = 7^a × 11^b × 13^c × 17^d with 0 ≤ a,b,c,d ≤ 17.", "We are to count the number of such divisors d ≡ 5 mod 12.", "7^a mod 12 cycles with period 2: values 7,1."], "altered": []} | solver report->planner: missing ['Prime factorization of 17017 is 7 × 11 × 13 × 17.', '17017^17 has prime factorization 7^17 × 11^17 × 13^17 × 17^17.', 'Any positive divisor d of 17017^17 can be written as d = 7^a × 11^b × 13^c × 17^d with 0 ≤ a,b,c,d ≤ 17.'] altered [] |
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