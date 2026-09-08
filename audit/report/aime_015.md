# Audit report — aime_015

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 1 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["50101"], "altered": []} | solver report->planner: missing ['50101'] altered [] |
| 6 | verifier | D1/tool | {"confidence": 0.536, "p_actual": 0.343, "margin": 0.314} | action distribution: no_tool 0.66, run_python 0.34, write_file 0.00 (actual: run_python) |

## Per-module summary
```
{
 "D1": {
  "n_scored": 12,
  "method": "stepwise"
 },
 "D2": {
  "n_steps": 12,
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