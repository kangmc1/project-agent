# Survey notes: multi-agent failures, handoff, attribution (raw, 2026-09-08)

Source: automated literature sweep (WebSearch/arXiv), verified against arXiv/GitHub pages unless marked [unverified].

## A. Taxonomies / failure studies
- **MAST** (Cemri et al., UC Berkeley; arXiv 2503.13657; NeurIPS 2025). 1,642 traces, 7 frameworks, 8 benchmarks. 14 failure modes / 3 categories (system design; inter-agent misalignment; task verification). Handoff-ish modes: loss of conversation history 2.8%, information withholding 0.85%, ignored other agent's input 1.9%. Per-trace labels, no step localization, no explicit "handoff" mode. Data: HF `mcemri/MAST-Data`.
- **Science of Scaling Agent Systems** (Kim et al., Google/MIT; arXiv 2512.08296). Independent agents amplify errors 17.2x vs single agent; centralized 4.4x.
- **From Spark to Fire** (Xie et al.; arXiv 2603.04474). Single injected error cascades across 6 MAS frameworks.
- **MultiAgentBench/MARBLE** (Zhu et al., ACL 2025; arXiv 2503.01935). Collaboration benchmark, no failure annotations.

## B. Failure attribution (who / when)
- **Who&When** (Zhang et al., ICML 2025; arXiv 2505.00212). 184 failure logs (CaptainAgent, Magentic-One) on GAIA/AssistantBench; human who/when/why. Best 53.5% agent / 14.2% step. HF `Kevin355/Who_and_When` (MIT).
- Follow-ups: AgenTracer (2509.03312; TracerTraj 2,000+ injected/counterfactual; 8B RL model 69.6%/42.9%), RAFFLES (2509.06822), A2P (2509.10401), DoVer (Microsoft, 2512.06749; argues single-step attribution often ill-posed), StepFinder (KDD 2026), SAFARI (2606.24626), Adaptive Influence Graphs (2608.24361), EDGE (EMNLP 2026, 2609.01360).
- New benchmarks 2026: **MP-Bench** (2603.25001; 289 logs, only 16.2% steps unanimous → ranked labels), **TraceElephant** (ACL 2026, 2604.22708; 220 full traces, orchestrators cause 18–29% of failures; full trace vs partial +76% step acc), **Who&When Pro** (2607.09996; 12,326 injected trajectories, 26 benchmarks, 18 error modes incl. coordination; acc 94%→50% beyond 12K tokens), **LongRCA** (2608.15242; 1,140 natural failures, median 145 steps; baseline 13.2%), **AgentRx** (Microsoft, 2602.02475; 115 single-agent traces, 10-category taxonomy, invariant checking +23.6% localization), **TRAIL** (Patronus, 2505.08638; 148 OTel traces, 841 span errors, Gemini-2.5-pro ~11%), **TELBench/DRIFT** (2606.02060).

## C. Handoff / delegation / communication
- **Handoff Debt** (arXiv 2606.02875). 181 handoff points on SWE-bench Verified, 724 takeover runs; measures rediscovery cost (events/tokens) under 4 handoff views. Closest to a handoff-quality benchmark. Code: github.com/anjilab/agent-handoff-debt.
- **Routed Graph Handoff** (EMNLP 2026, 2608.25277). NL delegation messages eat 40–60% of tokens; typed graph vs NL routing.
- **EntCollabBench** (2605.08761) failure areas: delegation, context transfer, parameter grounding, workflow closure. [size unverified]
- **MasDrift** (2608.07556). Authorization drift across delegation.
- Protocols: OpenAI Agents SDK handoffs (`transfer_to_X`, `input_filter`), Google A2A — only security evals exist (2505.12490 etc.). No A2A handoff-quality benchmark.

## Gaps observed
1. No benchmark labels *handoff events* as such; handoff loss smeared across MAST modes.
2. Context loss measured as cost (Handoff Debt), never as *which facts were dropped* and whether they caused failure.
3. Attribution accuracy collapses with trace length; handoffs are where traces get summarized/truncated — untested interaction.
4. Injected vs natural failures diverge (AG vs HC gap everywhere); injected sets rarely inject handoff-type faults.
5. Single-label attribution ill-posed; handoff failures are two-party (sender omitted vs receiver ignored) — no dual-responsibility labels.
6. Protocol-level handoffs (OpenAI SDK, A2A, LangGraph, CrewAI) have zero public failure datasets.
7. Production handoffs discard inputs by design (input_filter, A2A tasks) — attribution under filtered handoffs unstudied.
8. Delegation *instruction quality* → downstream failure link unstudied.

## Reusable data (2-day scope)
Who&When (184, MIT), TraceElephant (220, CC BY 4.0, full traces), MAST-Data (1,642), MP-Bench (289), Who&When Pro (12k), Handoff Debt (181 handoff points), TRAIL, AgentRx.
