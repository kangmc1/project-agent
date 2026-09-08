# Audit report — airline_042

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 4 | planner | D1/tool | {"confidence": 0.581, "p_actual": 0.555, "margin": 0.123} | action distribution: db_agent 0.55, policy_checker 0.43, read_file 0.01 (actual: db_agent) |
| 6 | db_agent | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_error": false} | required but never called: cancel_reservation, search_direct_flight/search_onestop_flight |
| 7 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["5 to 7 business days", "cancellations are allowed only if travel insurance is bought and the condition is met", "eligible for a refund if travel insurance is purchased and cancellation is due to health reasons", "need_info"], "altered": []} | policy_checker report->planner: missing ['5 to 7 business days', 'cancellations are allowed only if travel insurance is bought and the condition is met', 'eligible for a refund if travel insurance is purchased and cancellation is due to health reasons'] altered [] |
| 11 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["3rk2t9", "cannot proceed with a refund as there is no travel insurance linked to this reservation.", "n/a", "not linked"], "altered": []} | db_agent report->planner: missing ['3rk2t9', 'cannot proceed with a refund as there is no travel insurance linked to this reservation.', 'n/a'] altered [] |
| 13 | db_agent | D3 | {"missing_tool": true, "fabricated_arg": false, "tool_error": false} | required but never called: cancel_reservation |
| 21 | planner | D1/handoff | {"p_delegate": 0.096, "H2": 0.456} | delegate-vs-not split p_delegate=0.10 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 18,
  "method": "stepwise"
 },
 "D3": {
  "n_steps": 18,
  "flagged": 2,
  "missing_tool": 2,
  "fabricated_arg": 0,
  "tool_error": 0
 },
 "D7": {
  "n_handoffs": 8
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3": "procedural flag (no threshold)"}`