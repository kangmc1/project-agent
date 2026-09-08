# Audit report — aime_024

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 1 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["111"], "altered": ["final_answer"]} | solver report->planner: missing ['111'] altered ['final_answer'] |
| 2 | solver | D1/tool | {"confidence": 0.527, "p_actual": 0.365, "margin": 0.271} | action distribution: no_tool 0.64, run_python 0.36, write_file 0.00 (actual: run_python) |
| 2 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=99, numeric=99999, numeric=9999, numeric=999 |
| 3 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: final_answer=111 |
| 5 | verifier | D1/tool | {"confidence": 0.645, "p_actual": 0.806, "margin": 0.612} | action distribution: run_python 0.81, no_tool 0.19, read_file 0.00 (actual: run_python) |
| 5 | verifier | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=99, numeric=9999, numeric=999 |
| 7 | planner | D1/handoff | {"p_delegate": 0.818, "H2": 0.685} | delegate-vs-not split p_delegate=0.82 |
| 8 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=9999, numeric=999 |
| 9 | solver | D1/tool | {"confidence": 0.502, "p_actual": 0.539, "margin": 0.079} | action distribution: run_python 0.54, no_tool 0.46, write_file 0.00 (actual: run_python) |
| 9 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #6: repeat |
| 9 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=999, numeric=9999 |
| 10 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #7: repeat |
| 10 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=999, numeric=9999 |
| 11 | solver | D3 | {"checks": ["repeat"], "tool": "run_python"} | tool run_python call #8: repeat |
| 11 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=999, numeric=9999 |
| 12 | solver | D3 | {"satisfied": false} | claims without prior tool evidence: numeric=999, numeric=9999 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 14,
  "method": "stepwise"
 },
 "D3": {
  "tool_calls": 10,
  "utterances": 9,
  "checks": {
   "repeat": 3
  }
 },
 "D7": {
  "n_handoffs": 6
 },
 "D3_args": {
  "n_steps": 4,
  "n_values": 7,
  "n_ungrounded": 0
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3_args": "any ungrounded value"}`