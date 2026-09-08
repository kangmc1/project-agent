# Audit report — airline_002

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 4 | planner | D1/handoff | {"p_delegate": 0.852, "H2": 0.605} | delegate-vs-not split p_delegate=0.85 |
| 12 | db_agent | D3 | {"missing_tool": false, "fabricated_arg": false, "tool_error": true} | tool read_file returned an error |
| 15 | planner | D1/tool | {"confidence": 0.431, "p_actual": 0.656, "margin": 0.51} | action distribution: respond_to_user 0.66, write_file 0.15, db_agent 0.15 (actual: respond_to_user) |
| 15 | planner | D1/handoff | {"p_delegate": 0.188, "H2": 0.698} | delegate-vs-not split p_delegate=0.19 |
| 19 | db_agent | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_error": false} | required but never called: search_direct_flight/search_onestop_flight/book_reservation/calculate |
| 20 | planner | D1/tool | {"confidence": 0.399, "p_actual": 0.443, "margin": 0.098} | action distribution: db_agent 0.44, respond_to_user 0.34, policy_checker 0.21 (actual: db_agent) |
| 20 | planner | D1/handoff | {"p_delegate": 0.652, "H2": 0.932} | delegate-vs-not split p_delegate=0.65 |
| 20 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["/case_notes.md", "successfully appended"], "altered": []} | db_agent report->planner: missing ['/case_notes.md', 'successfully appended'] altered [] |
| 22 | db_agent | D1/tool | {"confidence": 0.708, "p_actual": 0.36, "margin": 0.231} | action distribution: no_tool 0.59, write_file 0.36, read_file 0.05 (actual: write_file) |
| 23 | db_agent | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_error": false} | required but never called: search_direct_flight/search_onestop_flight/book_reservation/calculate |
| 24 | planner | D1/tool | {"confidence": 0.52, "p_actual": 0.594, "margin": 0.233} | action distribution: respond_to_user 0.59, read_file 0.36, policy_checker 0.03 (actual: respond_to_user) |
| 28 | db_agent | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_error": false} | required but never called: search_direct_flight/search_onestop_flight/book_reservation/calculate |
| 31 | planner | D1/tool | {"confidence": 0.504, "p_actual": 0.574, "margin": 0.226} | action distribution: policy_checker 0.57, db_agent 0.35, respond_to_user 0.08 (actual: policy_checker) |
| 32 | policy_checker | D1/tool | {"confidence": 0.327, "p_actual": 0.637, "margin": 0.403} | action distribution: read_file 0.64, think 0.23, no_tool 0.12 (actual: read_file) |
| 40 | db_agent | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_error": false} | required but never called: search_direct_flight/search_onestop_flight/book_reservation/calculate |
| 43 | planner | D1/handoff | {"p_delegate": 0.814, "H2": 0.692} | delegate-vs-not split p_delegate=0.81 |
| 45 | db_agent | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_error": false} | required but never called: search_direct_flight/search_onestop_flight/book_reservation/calculate |
| 48 | planner | D1/tool | {"confidence": 0.547, "p_actual": 0.484, "margin": 0.0} | action distribution: policy_checker 0.48, respond_to_user 0.48, db_agent 0.03 (actual: policy_checker) |
| 48 | planner | D1/handoff | {"p_delegate": 0.515, "H2": 0.999} | delegate-vs-not split p_delegate=0.52 |
| 54 | db_agent | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_error": false} | required but never called: search_direct_flight/search_onestop_flight/book_reservation/calculate |
| 59 | db_agent | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_error": true} | required but never called: search_direct_flight/search_onestop_flight/book_reservation/calculate; tool db_agent returned an error |
| 63 | policy_checker | D1/tool | {"confidence": 0.731, "p_actual": 0.896, "margin": 0.801} | action distribution: think 0.90, read_file 0.09, no_tool 0.01 (actual: think) |

## Per-module summary
```
{
 "D1": {
  "n_scored": 55,
  "method": "stepwise"
 },
 "D3": {
  "n_steps": 55,
  "flagged": 8,
  "missing_tool": 7,
  "fabricated_arg": 0,
  "tool_error": 2
 },
 "D7": {
  "n_handoffs": 22
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3": "procedural flag (no threshold)"}`