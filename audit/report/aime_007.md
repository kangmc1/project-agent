# Audit report — aime_007

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 1 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["276"], "altered": []} | solver report->planner: missing ['276'] altered [] |
| 4 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["391"], "altered": []} | verifier report->planner: missing ['391'] altered [] |

## Per-module summary
```
{
 "D1": {
  "n_scored": 11,
  "method": "stepwise"
 },
 "D3": {
  "n_steps": 11,
  "flagged": 0,
  "missing_tool": 0,
  "fabricated_arg": 0,
  "tool_call_failed": 0
 },
 "D7": {
  "n_handoffs": 6
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3": "procedural flag (no threshold)"}`