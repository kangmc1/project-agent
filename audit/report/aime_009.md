# Audit report — aime_009

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 1 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["p = 900/1", "m = 900", "n = 1", "m+n = 901", "FINAL ANSWER: 901"], "altered": []} | solver report->planner: missing ['p = 900/1', 'm = 900', 'n = 1'] altered [] |
| 6 | planner | D3/report->planner | {"fidelity": 0.0, "missing": ["Joanne places stickers 1 through 6 on a die, one at a time, by rolling the die and placing the sticker on the top face.", "If the top face already has a sticker, the new sticker covers the old one.", "All even-numbered stickers (2, 4, 6) are visible on the die at the end.", "We are to find the conditional probability p that exactly one face is left blank at the end, given that all even-numbered stickers are visible.", "The final answer should be in the form m/n, where m and n are relatively prime, and we are to find m + n."], "altered": []} | verifier report->planner: missing ['Joanne places stickers 1 through 6 on a die, one at a time, by rolling the die and placing the sticker on the top face.', 'If the top face already has a sticker, the new sticker covers the old one.', 'All even-numbered stickers (2, 4, 6) are visible on the die at the end.'] altered [] |
| 7 | verifier | D2 | {"missing_tool": true, "fabricated_arg": false, "tool_call_failed": false} | required but never called: run_python |
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
 "D2": {
  "n_steps": 26,
  "flagged": 1,
  "missing_tool": 1,
  "fabricated_arg": 0,
  "tool_call_failed": 0
 },
 "D3": {
  "n_handoffs": 6
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D3": 1.0, "D2": "procedural flag (no threshold)"}`