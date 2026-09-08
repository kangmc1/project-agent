# Audit report — aime_010

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 1 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["168", "8.125", "84"], "altered": []} | solver report->planner: missing ['168', '8.125', '84'] altered [] |
| 4 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: final_answer=168, numeric=90 |
| 7 | verifier | D2 | {"s": 0.3333333333333333, "unsupported": 0.6666666666666667} | values not found in any prior tool result: 13 \cdot 14 \cdot 15, 4 \cdot 84 |
| 8 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=168 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 10,
  "method": "stepwise"
 },
 "D2": {
  "n_utterances": 7,
  "n_na": 0
 },
 "D3": {
  "tool_calls": 7,
  "utterances": 6,
  "checks": {}
 },
 "D7": {
  "n_handoffs": 4
 },
 "D9": {
  "n_steps": 7
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`