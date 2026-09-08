# Audit report — aime_030

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 1 | planner | D7/instruction->premise | {"fidelity": 0.0, "missing": ["108", "find the number of ordered 7-tuples (a_1 a_2 a_3 ... a_7) having the following properties: - a_k ∈ {123} for all k. - a_1+a_2+a_3+a_4+a_5+a_6+a_7 is a multiple of 3. - a_1a_2 a_4 + a_2a_3a_5 + a_3a_4 a_6 + a_4 a_5 a_7 + a_5 a_6 a_1 + a_6 a_7 a_2 + a_7 a_1 a_3 is a multiple of 3.", "let f(n) be the number of n-tuples (a_1 a_2 ... a_n) with a_k ∈ {123} such that the sum is divisible by 3. let g(n) be the number of n-tuples such that the sum is congruent to 1 mod 3. let h(n) be the number of n-tuples such that the sum is congruent to 2 mod 3. then f(n) = g(n) = h(n) = 3^{n-1} for n ≥ 1. using generating functions and modular arithmetic the total number of valid 7-tuples is 108."], "altered": ["final_answer"]} | solver instruction->premise: missing ['108', 'find the number of ordered 7-tuples (a_1 a_2 a_3 ... a_7) having the following properties: - a_k ∈ {123} for all k. - a_1+a_2+a_3+a_4+a_5+a_6+a_7 is a multiple of 3. - a_1a_2 a_4 + a_2a_3a_5 + a_3a_4 a_6 + a_4 a_5 a_7 + a_5 a_6 a_1 + a_6 a_7 a_2 + a_7 a_1 a_3 is a multiple of 3.', 'let f(n) be the number of n-tuples (a_1 a_2 ... a_n) with a_k ∈ {123} such that the sum is divisible by 3. let g(n) be the number of n-tuples such that the sum is congruent to 1 mod 3. let h(n) be the number of n-tuples such that the sum is congruent to 2 mod 3. then f(n) = g(n) = h(n) = 3^{n-1} for n ≥ 1. using generating functions and modular arithmetic the total number of valid 7-tuples is 108.'] altered ['final_answer'] |
| 1 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["393"], "altered": ["final_answer"]} | solver report->planner: missing ['393'] altered ['final_answer'] |
| 4 | planner | D7/instruction->premise | {"fidelity": 0.0, "missing": ["108", "find the number of ordered 7-tuples (a_1 a_2 a_3 ... a_7) having the following properties: - a_k ∈ {123} for all k. - a_1+a_2+a_3+a_4+a_5+a_6+a_7 is a multiple of 3. - a_1a_2 a_4 + a_2a_3a_5 + a_3a_4 a_6 + a_4 a_5 a_7 + a_5 a_6 a_1 + a_6 a_7 a_2 + a_7 a_1 a_3 is a multiple of 3.", "let f(n) be the number of n-tuples (a_1 a_2 ... a_n) with a_k ∈ {123} such that the sum is divisible by 3. let g(n) be the number of n-tuples such that the sum is congruent to 1 mod 3. let h(n) be the number of n-tuples such that the sum is congruent to 2 mod 3. then f(n) = g(n) = h(n) = 3^{n-1} for n ≥ 1. using generating functions and modular arithmetic the total number of valid 7-tuples is 108."], "altered": []} | verifier instruction->premise: missing ['108', 'find the number of ordered 7-tuples (a_1 a_2 a_3 ... a_7) having the following properties: - a_k ∈ {123} for all k. - a_1+a_2+a_3+a_4+a_5+a_6+a_7 is a multiple of 3. - a_1a_2 a_4 + a_2a_3a_5 + a_3a_4 a_6 + a_4 a_5 a_7 + a_5 a_6 a_1 + a_6 a_7 a_2 + a_7 a_1 a_3 is a multiple of 3.', 'let f(n) be the number of n-tuples (a_1 a_2 ... a_n) with a_k ∈ {123} such that the sum is divisible by 3. let g(n) be the number of n-tuples such that the sum is congruent to 1 mod 3. let h(n) be the number of n-tuples such that the sum is congruent to 2 mod 3. then f(n) = g(n) = h(n) = 3^{n-1} for n ≥ 1. using generating functions and modular arithmetic the total number of valid 7-tuples is 108.'] altered [] |

## Per-module summary
```
{
 "D1": {
  "n_scored": 8,
  "method": "stepwise"
 },
 "D3": {
  "n_steps": 8,
  "flagged": 0,
  "missing_tool": 0,
  "fabricated_arg": 0,
  "tool_call_failed": 0
 },
 "D7": {
  "n_handoffs": 4
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D7": 1.0, "D3": "procedural flag (no threshold)"}`