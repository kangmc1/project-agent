# Audit report — aime_017

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 5 | verifier | D1/tool | {"confidence": 0.692, "p_actual": 0.847, "margin": 0.695} | action distribution: run_python 0.85, no_tool 0.15, write_file 0.00 (actual: run_python) |

## Per-module summary
```
{
 "D1": {
  "n_scored": 8,
  "method": "stepwise"
 },
 "D3": {
  "tool_calls": 5,
  "utterances": 4,
  "checks": {}
 },
 "D7": {
  "n_handoffs": 4
 },
 "D3_args": {
  "n_steps": 3,
  "n_values": 3,
  "n_ungrounded": 0
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3_args": "any ungrounded value"}`