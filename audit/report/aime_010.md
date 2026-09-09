# Audit report — aime_010

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 1 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["Circumradius R = 8.125", "Hexagon AA'CC'BB' is formed by triangle ABC and its rotated image A'B'C' about circumcenter", "Distances from vertices to center remain same under rotation", "Hexagon consists of triangle ABC, triangle A'B'C', quadrilaterals AA'C'C, CC'B'B, BB'A'A", "Rotation is by 90°"], "altered": []} | solver report->planner: missing ['Circumradius R = 8.125', "Hexagon AA'CC'BB' is formed by triangle ABC and its rotated image A'B'C' about circumcenter", 'Distances from vertices to center remain same under rotation'] altered [] |

## Per-module summary
```
{
 "D1": {
  "n_scored": 10,
  "method": "stepwise"
 },
 "D2": {
  "n_steps": 10,
  "flagged": 0,
  "missing_tool": 0,
  "fabricated_arg": 0,
  "tool_call_failed": 0
 },
 "D3": {
  "n_handoffs": 4
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D3": 1.0, "D2": "procedural flag (no threshold)"}`