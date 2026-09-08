# Audit report — aime_020

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | solver | D2 | {"s": 0.21052631578947367, "unsupported": 0.7894736842105263} | values not found in any prior tool result: exactly 4 red marbles, exactly 5 red marbles, find the sum of the five least values of $ n $, hypergeometric distribution, $ P(k) = \frac{\binom{r}{k} \binom{b}{7-k}}{\binom{n}{7}} $ |
| 2 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=12 |
| 3 | solver | D1/tool | {"confidence": 0.754, "p_actual": 0.895, "margin": 0.79} | action distribution: no_tool 0.89, run_python 0.10, read_file 0.00 (actual: no_tool) |
| 3 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: final_answer=205, numeric=46, numeric=41, numeric=31, numeric=36 |
| 5 | verifier | D2 | {"s": 0.05555555555555555, "unsupported": 0.9444444444444444} | values not found in any prior tool result: each either red or blue, equals the probability of drawing exactly 5 red marbles, the sum of the five least values of $ n $, given by the hypergeometric distribution, $ P(4) $ |
| 5 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=120, numeric=24, numeric=12, numeric=240, numeric=144 |
| 6 | verifier | D1/tool | {"confidence": 0.676, "p_actual": 0.836, "margin": 0.672} | action distribution: no_tool 0.84, run_python 0.16, read_file 0.00 (actual: no_tool) |
| 6 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: final_answer=360, numeric=32, numeric=112, numeric=92, numeric=72 |
| 7 | planner | D1/tool | {"confidence": 0.612, "p_actual": 0.608, "margin": 0.22} | action distribution: solver 0.61, no_tool 0.39, submit_answer 0.00 (actual: solver) |
| 7 | planner | D1/handoff | {"p_delegate": 0.608, "H2": 0.966} | delegate-vs-not split p_delegate=0.61 |
| 7 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["15 = (r - 4) * (b - 2)", "15 = (r - 4) * (n - r - 2)", "32 52 72 92 112", "360", "4"], "altered": []} | solver report->planner: missing ['15 = (r - 4) * (b - 2)', '15 = (r - 4) * (n - r - 2)', '32 52 72 92 112'] altered [] |
| 8 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=32, numeric=112, numeric=92, numeric=72, numeric=52 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 10,
  "method": "stepwise"
 },
 "D2": {
  "n_utterances": 6,
  "n_na": 0
 },
 "D3": {
  "tool_calls": 6,
  "utterances": 5,
  "checks": {}
 },
 "D7": {
  "n_handoffs": 6
 },
 "D9": {
  "n_steps": 6
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`