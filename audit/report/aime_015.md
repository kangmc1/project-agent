# Audit report — aime_015

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 1 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["50101"], "altered": []} | solver report->planner: missing ['50101'] altered [] |
| 2 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=60, numeric=120, numeric=16, numeric=40, numeric=100 |
| 3 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=100 |
| 6 | verifier | D1/tool | {"confidence": 0.536, "p_actual": 0.343, "margin": 0.314} | action distribution: no_tool 0.66, run_python 0.34, write_file 0.00 (actual: run_python) |
| 9 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=60, numeric=120, numeric=16, numeric=40, numeric=12 |
| 10 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=60, numeric=20 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 12,
  "method": "stepwise"
 },
 "D3": {
  "tool_calls": 8,
  "utterances": 6,
  "checks": {}
 },
 "D7": {
  "n_handoffs": 6
 },
 "D3_args": {
  "n_steps": 4,
  "n_values": 16,
  "n_ungrounded": 0
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3_args": "any ungrounded value"}`