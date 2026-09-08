# Audit report — aime_003

| step | agent | module | signal | evidence |
|---|---|---|---|---|

## Per-module summary
```
{
 "D1": {
  "n_scored": 5,
  "method": "stepwise"
 },
 "D3": {
  "n_steps": 5,
  "flagged": 0,
  "missing_tool": 0,
  "fabricated_arg": 0,
  "tool_call_failed": 0
 },
 "D7": {
  "n_handoffs": 2
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3": "procedural flag (no threshold)"}`