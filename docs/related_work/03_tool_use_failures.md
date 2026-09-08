# Survey notes: evaluating & detecting tool-use failures (raw, 2026-09-08)

Legend: Output = grades final answer/end-state; Traj = grades/labels steps inside the trajectory.

## Agent-success benchmarks (Output-style)
- **τ-bench** (Sierra 2024; 2406.12045; MIT). Retail 115 / airline 50 tasks, mock DBs, LLM user sim, policy docs; end-state grading, pass^k. Manual failure analysis: ~50% wrong args/info, ~25% rule violation, ~19% partial compound request.
- **τ²-bench** (2506.07982; MIT; now τ³). Adds telecom (dual-control, user has tools). gpt-4.1 pass^1 74/56/34. Separates reasoning vs communication errors in analysis.
- **BFCL v1–v4** (Berkeley Gorilla). v3 multi-turn 800 entries (missing param / missing function / long context / composite), v4 adds web search, memory, format sensitivity; state-based grading; hallucination/relevance 10% of score. No per-step labels.
- **ToolEmu** (ICLR 2024; 2309.15817). LM-emulated sandbox 311 tools, 144 high-stakes cases; LLM safety evaluator flags unsafe actions in-trajectory (68.8% precision).
- **ToolSandbox** (Apple 2024; 2408.04682). 1,032 scenarios, 34 stateful tools; milestones + minefields → trajectory similarity.
- **NESTFUL** (IBM, EMNLP 2025), **ToolBench/StableToolBench** (2024; GPT-4 API simulator), **ACEBench** (2501.12851; Normal/Special(incomplete, error-param, irrelevant)/Agent), **API-Bank** (2023), **AgentDojo** (NeurIPS 2024; mock email/banking/travel/Slack + ground-truth unsafe-action checks).

## Failure-focused / diagnostic
- **ToolFuzz** (ETH 2025; 2503.04479) fuzzes tool docs → runtime errors; tests tools not agents.
- **ToolBeHonest** (EMNLP 2024; 2406.20015) solvability / missing-tool detection, 700 samples.
- **RelyToolBench / Relign** (SJTU 2024; 2412.04141). Tool hallucination types: tool type, timing, format, content. **The Reasoning Trap** (ACL 2026; 2510.22977): reasoning training causally increases tool hallucination.
- **ToolScan** (Salesforce 2024; 2411.13547). 150 queries, rule-based detection of 7 patterns (insufficient calls, wrong arg value/name/type, repeated calls, wrong fn name, invalid format). **PALADIN** (2509.25238) injects ToolScan-style failures into 50k ToolBench trajectories for recovery training.
- **CRITICTOOL** (2506.13977). 2,740 cases from BFCL v3 / T-Eval with injected errors: internal (tool selection, tool hallucination, param key, param value) + external (timeout, permission, API instability). Scores Reflect/Correct/Retry/Skip-Finish. Evaluates *recovery* given an erroneous step.
- **Tools Fail** (CMU 2024; 2406.19228): silent wrong tool outputs; no code.
- **TRAIL** (Patronus 2025): tool selection/misuse, tool-output misinterpretation, tool definition, timeouts among 20+ categories; best LLM 11% joint. **Holistic Eval** (Deepchecks 2605.14865): span-level decomposition +38% F1 on TRAIL.
- 2026: **ToolMaze** (Baidu; 2606.05806; 2,000 instances, 270 sandboxed tools, perturbations P1–P4 explicit/implicit × transient/permanent; recovery drops ~37% for implicit corruption), **ToolFailBench** (2607.04686; 1,000 single-turn tasks, labels Tool-Skip / Result-Ignore / Output-Fabrication / Unnecessary-Tool-Use via rules + 2 LLM judges), **Real-Time Detection and Repair** (2608.02464; telemetry-only monitors: looping, cascading tool errors, goal drift, fabrication; AUROC 0.872; single-author preprint), **TraceSafe-Bench** (COLM 2026; 2604.07223; 1,000+ trajectories, 12 risk categories, guard detection mid-trajectory), **Benchmarking the Benchmarks** (2607.02577; 18.5% evaluator–human misalignment across BFCL v4 / τ² / MCP benches), MCP-Bench (ICLR 2026), MCPToolBench++.

## Industry practice
- Anthropic "Demystifying evals for AI agents" (Jan 2026): grade outcomes over paths; code graders for required tools/params; LLM judges allowed to say "Unknown".
- Langfuse guide: tool-selection accuracy, schema-validated args, tool error rate, recovery after failed call, loops; cheap code checks on every trace + LLM judge on subset + human review.
- Arize Phoenix: prebuilt judge templates separating tool selection from parameter extraction; trajectory-order and path-convergence evals.

## Gaps
1. No dedicated benchmark for *post-hoc tool-failure detection from logs* at step granularity in multi-turn trajectories (TRAIL closest; ToolFailBench single-turn only).
2. Ignored tool errors / silent corruption under-measured (ToolMaze implicit failures; "Tools Fail" no data).
3. Hallucinated tool outputs appear as a single label; nothing isolates fabricated-vs-real tool returns in multi-turn logs.
4. Detector quality itself unvalidated: judges ≤12% on TRAIL; 18.5% evaluator–human misalignment; ToolFailBench majority-vote without human agreement.
5. Unsafe vs wrong actions studied separately; no unified log-level labelling.
6. Recovery vs detection conflated (CRITICTOOL/ToolMaze/PALADIN score recovery; only 2608.02464 does external detection, unreviewed).
7. Small, sim-heavy data; real API-drift errors rare.

## Reusable (mock tools, public)
τ²-bench (3 domains, mock DBs, JSON trajectories — wrap tools to inject faults), ToolSandbox (34 stateful tools), BFCL v3 multi-turn + CRITICTOOL (2,740 pre-injected erroneous trajectories), ToolFailBench (rule classifier code), ToolMaze (perturbation injector), TRAIL (HF), AgentDojo, StableToolBench virtual API server.
