# Audit report — aime_017

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 1 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["Grid consists of 10 squares in a row, each with a diagonal from lower left to upper right.", "Bug starts at lower left corner (A) and ends at upper right corner (B).", "Bug moves along line segments, never traversing the same segment twice and never moving from right to left along a horizontal or diagonal segment.", "Goal: find number of such paths N and compute sqrt(N).", "Allowed moves: right along horizontal, up along vertical, diagonally from lower left to upper right."], "altered": []} | solver report->planner: missing ['Grid consists of 10 squares in a row, each with a diagonal from lower left to upper right.', 'Bug starts at lower left corner (A) and ends at upper right corner (B).', 'Bug moves along line segments, never traversing the same segment twice and never moving from right to left along a horizontal or diagonal segment.'] altered [] |
| 4 | planner | D3/instruction->premise | {"fidelity": 0.0, "missing": ["Problem type: AIME", "Grid: 10 squares in a row", "Each square has a diagonal from lower left to upper right", "Bug moves along line segments from vertex to vertex", "Bug never traverses same segment twice"], "altered": []} | verifier instruction->premise: missing ['Problem type: AIME', 'Grid: 10 squares in a row', 'Each square has a diagonal from lower left to upper right'] altered [] |
| 4 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["Grid consists of 10 squares in a row.", "Each square has a diagonal from lower left to upper right.", "Bug starts at lower left corner (A).", "Bug must reach upper right corner (B).", "Bug can only move along line segments (horizontal, vertical, or diagonal)."], "altered": []} | verifier report->planner: missing ['Grid consists of 10 squares in a row.', 'Each square has a diagonal from lower left to upper right.', 'Bug starts at lower left corner (A).'] altered [] |
| 5 | verifier | D1/tool | {"confidence": 0.692, "p_actual": 0.847, "margin": 0.695} | action distribution: run_python 0.85, no_tool 0.15, write_file 0.00 (actual: run_python) |

## Per-module summary
```
{
 "D1": {
  "n_scored": 8,
  "method": "stepwise"
 },
 "D2": {
  "n_steps": 8,
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