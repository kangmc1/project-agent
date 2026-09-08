# Audit report — aime_026

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | solver | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_error": false} | required but never called: run_python |
| 3 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["10000", "1425", "1436", "16", "25"], "altered": []} | verifier report->planner: missing ['10000', '1425', '1436'] altered [] |

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