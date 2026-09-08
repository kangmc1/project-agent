# Audit report — aime_003

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | solver | D2 | {"s": 0.35714285714285715, "unsupported": 0.6428571428571428} | values not found in any prior tool result: the set of points P on the disk such that a sphere of radius 42 can be placed at P and lie entirely within the hemisphere, find the ratio of the area of T to the area of the disk, expressed as p/q, where p and q are relatively prime positive integers, and compute p+q, origin, 42 units, 158 |
| 2 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=200, numeric=158, numeric=42 |
| 4 | solver | D2 | {"s": 0.3333333333333333, "unsupported": 0.6666666666666667} | values not found in any prior tool result: 10:15 AM, 1:45 PM, economy, XK9872, $8120.50 |
| 5 | planner | D2 | {"s": 0.2, "unsupported": 0.8} | values not found in any prior tool result: $1250.00, 08:45 AM, 11:15 AM, economy, $625.00 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 5,
  "method": "stepwise"
 },
 "D2": {
  "n_utterances": 4,
  "n_na": 0
 },
 "D3": {
  "tool_calls": 3,
  "utterances": 3,
  "checks": {}
 },
 "D7": {
  "n_handoffs": 2
 },
 "D9": {
  "n_steps": 3
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`