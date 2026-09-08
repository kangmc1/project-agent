# Audit report — aime_006

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 1 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["441"], "altered": ["final_answer"]} | solver report->planner: missing ['441'] altered ['final_answer'] |
| 2 | solver | D2 | {"s": 0.11764705882352941, "unsupported": 0.8823529411764706} | values not found in any prior tool result: x^{\log_{2026}x} = (26x)^{20}, \log_{2026}(x^{\log_{2026}x}) = \log_{2026}((26x)^{20}), (\log_{2026}x)^2 = 20 \log_{2026}(26x), (\log_{2026}x)^2 = 20 (\log_{2026}26 + \log_{2026}x), y^2 = 20 (\log_{2026}26 + y) |
| 2 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=1013, numeric=10, numeric=2026, numeric=100, numeric=80 |
| 5 | verifier | D2 | {"s": 0.058823529411764705, "unsupported": 0.9411764705882353} | values not found in any prior tool result: x^{\log_{2026}x} = (26x)^{20}, \log_{2026}(x^{\log_{2026}x}) = \log_{2026}((26x)^{20}), (\log_{2026}x)(\log_{2026}x) = 20 \log_{2026}(26x), (\log_{2026}x)^2 = 20 (\log_{2026}26 + \log_{2026}x), y = \log_{2026}x |
| 5 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=1013, numeric=10, numeric=100, numeric=80, numeric=400 |

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
  "n_steps": 4
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`