# Audit report — aime_028

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=4040 |
| 5 | solver | D1/tool | {"confidence": 0.74, "p_actual": 0.884, "margin": 0.767} | action distribution: run_python 0.88, no_tool 0.12, read_file 0.00 (actual: run_python) |
| 5 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=19 |
| 9 | planner | D1/tool | {"confidence": 0.588, "p_actual": 0.76, "margin": 0.628} | action distribution: verifier 0.76, solver 0.13, submit_answer 0.10 (actual: verifier) |
| 9 | planner | D1/handoff | {"p_delegate": 0.892, "H2": 0.493} | delegate-vs-not split p_delegate=0.89 |
| 11 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=2048 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 12,
  "method": "stepwise"
 },
 "D2": {
  "n_utterances": 10,
  "n_na": 4
 },
 "D3": {
  "tool_calls": 9,
  "utterances": 6,
  "checks": {}
 },
 "D7": {
  "n_handoffs": 4
 },
 "D9": {
  "n_steps": 10
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`