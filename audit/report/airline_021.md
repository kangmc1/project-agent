# Audit report — airline_021

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 4 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["daiki_lee_6144", "jfk", "look up reservation details", "may 17th"], "altered": []} | db_agent report->planner: missing ['daiki_lee_6144', 'jfk', 'look up reservation details'] altered [] |
| 11 | planner | D1/handoff | {"p_delegate": 0.77, "H2": 0.779} | delegate-vs-not split p_delegate=0.77 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 16,
  "method": "stepwise"
 },
 "D2": {
  "n_steps": 16,
  "flagged": 0,
  "missing_tool": 0,
  "fabricated_arg": 0,
  "tool_call_failed": 0
 },
 "D3": {
  "n_handoffs": 6
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D3": 1.0, "D2": "procedural flag (no threshold)"}`