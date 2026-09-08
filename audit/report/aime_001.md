# Audit report — aime_001

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | solver | D1/tool | {"confidence": 0.554, "p_actual": 0.692, "margin": 0.383} | action distribution: run_python 0.69, no_tool 0.31, read_file 0.00 (actual: run_python) |
| 2 | solver | D2 | {"s": 0.2, "unsupported": 0.8} | values not found in any prior tool result: m/n miles, 252 + 25, p miles per hour, p + 2 miles per hour, p + 9 miles per hour |
| 2 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=10, numeric=28, numeric=14, numeric=18 |
| 3 | solver | D2 | {"s": 0.0625, "unsupported": 0.9375} | values not found in any prior tool result: $1,234.50, 10:15 AM, economy, RES277, 2023-12-15 |
| 5 | verifier | D2 | {"s": 0.42857142857142855, "unsupported": 0.5714285714285714} | values not found in any prior tool result: x + 2, x + 9, t - 1, t - 2, m/n |
| 5 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=10, numeric=28 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 7,
  "method": "stepwise"
 },
 "D2": {
  "n_utterances": 5,
  "n_na": 0
 },
 "D3": {
  "tool_calls": 4,
  "utterances": 4,
  "checks": {}
 },
 "D7": {
  "n_handoffs": 4
 },
 "D9": {
  "n_steps": 5
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`