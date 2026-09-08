# Audit report — aime_002

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 1 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["26"], "altered": []} | solver report->planner: missing ['26'] altered [] |
| 11 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["ensure that half_length is an integer", "the range function is still being passed a float", "use of 10**(half_length - 1) and 10**half_length when half_length is a float"], "altered": []} | solver report->planner: missing ['ensure that half_length is an integer', 'the range function is still being passed a float', 'use of 10**(half_length - 1) and 10**half_length when half_length is a float'] altered [] |
| 12 | solver | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: run_python returned an error |
| 13 | solver | D1/tool | {"confidence": 0.695, "p_actual": 0.85, "margin": 0.7} | action distribution: run_python 0.85, no_tool 0.15, read_file 0.00 (actual: run_python) |
| 13 | solver | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: run_python returned an error |
| 14 | solver | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: run_python returned an error |
| 15 | solver | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: run_python returned an error |
| 16 | solver | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: run_python returned an error |
| 17 | solver | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: run_python returned an error |
| 18 | solver | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: run_python returned an error |
| 19 | solver | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: run_python returned an error |
| 20 | solver | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: run_python returned an error |
| 21 | solver | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: run_python returned an error |
| 22 | solver | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: run_python returned an error |
| 23 | solver | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: run_python returned an error |
| 24 | solver | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: run_python returned an error |
| 25 | solver | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: run_python returned an error |
| 26 | solver | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: run_python returned an error |
| 27 | solver | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: run_python returned an error |
| 28 | solver | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: run_python returned an error |
| 29 | solver | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: run_python returned an error |
| 30 | solver | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: run_python returned an error |
| 31 | solver | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: run_python returned an error |
| 32 | solver | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: run_python returned an error |
| 33 | solver | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: run_python returned an error |
| 34 | solver | D2 | {"missing_tool": false, "fabricated_arg": false, "tool_call_failed": true} | call failed: run_python returned an error |
| 36 | planner | D1/tool | {"confidence": 0.463, "p_actual": 0.655, "margin": 0.468} | action distribution: submit_answer 0.66, verifier 0.19, no_tool 0.12 (actual: submit_answer) |
| 36 | planner | D1/handoff | {"p_delegate": 0.22, "H2": 0.761} | delegate-vs-not split p_delegate=0.22 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 37,
  "method": "stepwise"
 },
 "D2": {
  "n_steps": 37,
  "flagged": 23,
  "missing_tool": 0,
  "fabricated_arg": 0,
  "tool_call_failed": 23
 },
 "D3": {
  "n_handoffs": 6
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D3": 1.0, "D2": "procedural flag (no threshold)"}`