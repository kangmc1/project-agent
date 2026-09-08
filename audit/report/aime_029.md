# Audit report — aime_029

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | solver | D1/tool | {"confidence": 0.741, "p_actual": 0.884, "margin": 0.768} | action distribution: run_python 0.88, no_tool 0.12, write_file 0.00 (actual: run_python) |

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
  "n_steps": 1,
  "n_values": 1,
  "n_ungrounded": 0
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3_args": "any ungrounded value"}`