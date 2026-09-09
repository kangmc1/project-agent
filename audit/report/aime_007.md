# Audit report — aime_007

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 1 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["N=276"], "altered": []} | solver report->planner: missing ['N=276'] altered [] |
| 4 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["The total number of permutations of the set A that satisfy the condition π^6(a) = a for all a ∈ A is 391.", "FINAL ANSWER: 391"], "altered": []} | verifier report->planner: missing ['The total number of permutations of the set A that satisfy the condition π^6(a) = a for all a ∈ A is 391.', 'FINAL ANSWER: 391'] altered [] |

## Per-module summary
```
{
 "D1": {
  "n_scored": 11,
  "method": "stepwise"
 },
 "D2": {
  "n_steps": 11,
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