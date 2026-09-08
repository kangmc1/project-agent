# Audit report — aime_009

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 1 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["1", "900", "900/1", "901"], "altered": ["final_answer", "m_plus_n"]} | solver report->planner: missing ['1', '900', '900/1'] altered ['final_answer', 'm_plus_n'] |
| 7 | verifier | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: run_python |
| 8 | planner | D1/tool | {"confidence": 0.522, "p_actual": 0.613, "margin": 0.285} | action distribution: solver 0.61, submit_answer 0.33, verifier 0.05 (actual: solver) |
| 8 | planner | D1/handoff | {"p_delegate": 0.664, "H2": 0.921} | delegate-vs-not split p_delegate=0.66 |
| 12 | solver | D1/tool | {"confidence": 0.741, "p_actual": 0.884, "margin": 0.768} | action distribution: run_python 0.88, no_tool 0.12, read_file 0.00 (actual: run_python) |

## Per-module summary
```
{
 "D1": {
  "n_scored": 26,
  "method": "stepwise"
 },
 "D3": {
  "n_steps": 26,
  "flagged": 1,
  "missing_tool": 1,
  "fabricated_arg": 0,
  "tool_call_failed": 0
 },
 "D7": {
  "n_handoffs": 6
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3": "procedural flag (no threshold)"}`