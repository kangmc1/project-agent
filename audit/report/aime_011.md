# Audit report — aime_011

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 4 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["112", "1280", "1_to_64", "800", "8x8"], "altered": []} | verifier report->planner: missing ['112', '1280', '1_to_64'] altered [] |
| 5 | verifier | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: run_python |

## Per-module summary
```
{
 "D1": {
  "n_scored": 7,
  "method": "stepwise"
 },
 "D3": {
  "n_steps": 7,
  "flagged": 1,
  "missing_tool": 1,
  "fabricated_arg": 0,
  "tool_call_failed": 0
 },
 "D7": {
  "n_handoffs": 4
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3": "procedural flag (no threshold)"}`