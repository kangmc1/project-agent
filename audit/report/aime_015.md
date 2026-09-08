# Audit report — aime_015

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 1 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["50101"], "altered": []} | solver report->planner: missing ['50101'] altered [] |
| 2 | solver | D2 | {"s": 0.16666666666666666, "unsupported": 0.8333333333333334} | values not found in any prior tool result: 10 x 10, 100, (a - 2) x (b - 2), 12, 100 |
| 2 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=60, numeric=120, numeric=16, numeric=40, numeric=100 |
| 3 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=100 |
| 5 | verifier | D2 | {"s": 0.38461538461538464, "unsupported": 0.6153846153846154} | values not found in any prior tool result: 2n × 2n, the 2a + 2b - 4 cells surrounding an (a - 2) × (b - 2) rectangle, (a - 2) × (b - 2), 2 ≤ a, b ≤ 2n, 10 × 10 |
| 6 | verifier | D1/tool | {"confidence": 0.536, "p_actual": 0.343, "margin": 0.314} | action distribution: no_tool 0.66, run_python 0.34, write_file 0.00 (actual: run_python) |
| 9 | solver | D2 | {"s": 0.2857142857142857, "unsupported": 0.7142857142857143} | values not found in any prior tool result: 10 × 10, (a - 2) × (b - 2), 12, 4 × 4, 60 |
| 9 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=60, numeric=120, numeric=16, numeric=40, numeric=12 |
| 10 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=60, numeric=20 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 12,
  "method": "stepwise"
 },
 "D2": {
  "n_utterances": 9,
  "n_na": 2
 },
 "D3": {
  "tool_calls": 8,
  "utterances": 6,
  "checks": {}
 },
 "D7": {
  "n_handoffs": 6
 },
 "D9": {
  "n_steps": 8
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`