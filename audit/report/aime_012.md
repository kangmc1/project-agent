# Audit report — aime_012

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 1 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["1", "6", "6/1", "7"], "altered": ["final_answer"]} | solver report->planner: missing ['1', '6', '6/1'] altered ['final_answer'] |
| 4 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["-2_3", "0", "1", "2", "3"], "altered": ["final_answer"]} | verifier report->planner: missing ['-2_3', '0', '1'] altered ['final_answer'] |
| 5 | verifier | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: run_python |

## Per-module summary
```
{
 "D1": {
  "n_scored": 7,
  "method": "stepwise"
 },
 "D2": {
  "n_steps": 7,
  "flagged": 1,
  "missing_tool": 1,
  "fabricated_arg": 0,
  "tool_call_failed": 0
 },
 "D3": {
  "n_handoffs": 4
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D3": 1.0, "D2": "procedural flag (no threshold)"}`