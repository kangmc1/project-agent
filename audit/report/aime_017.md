# Audit report — aime_017

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | solver | D2 | {"s": 0.16666666666666666, "unsupported": 0.8333333333333334} | values not found in any prior tool result: from the lower left to the upper right, right along the horizontal segments, up along the vertical segments, diagonally from lower left to upper right, left or down, find the number of such paths N and compute sqrt(N), 1x10 grid of squares |
| 3 | solver | D9 | {"consistency": 0.0} | false equations: {'step_id': 3, 'expr': 'sqrt(20) == 4'} |
| 5 | verifier | D1/tool | {"confidence": 0.692, "p_actual": 0.847, "margin": 0.695} | action distribution: run_python 0.85, no_tool 0.15, write_file 0.00 (actual: run_python) |
| 6 | verifier | D9 | {"consistency": 0.0} | false equations: {'step_id': 6, 'expr': 'sqrt(20) == 4'} |

## Per-module summary
```
{
 "D1": {
  "n_scored": 8,
  "method": "stepwise"
 },
 "D2": {
  "n_utterances": 5,
  "n_na": 0
 },
 "D3": {
  "tool_calls": 5,
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