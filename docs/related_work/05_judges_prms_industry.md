# Survey notes: judges, PRMs, online monitoring, industry products (raw, 2026-09-08)

## A. Research
**Trajectory judges**: Agent-as-a-Judge (ICML 2025; 90.4% human alignment on DevAI vs 60.4% LLM-judge; code-gen only), AgentRewardBench (2504.08942; 1,302 expert-labelled web trajectories, 12 judges, none best everywhere), TRAIL (frontier ≤11% joint), Who&When (53.5%/14.2%), MAST (o1 annotator κ=0.77 vs human 0.88), **AgentProcessBench** (KDD'26; Qwen3-8B 60.4% StepAcc / 57.2% first-error; Qwen3-4B 55.9%; Gemini-3-Flash-Thinking 81.6%).

**PRMs / critics**: AgentPRM promise+progress (2511.08325; RL-oriented), **AgenTracer-8B** (2509.03312; Qwen3-8B + RL → 63.8% agent / 20.7% step on Who&When vs base 39.5%/3.5%, beats Gemini-2.5-Pro), SeekJudge-9B (2607.23263; AgentRewardBench F1 74.7), CRATE (2608.20797; step consequence reasoning then aggregation), **Intervention Paradox** (Writer, 2602.03338; 0.6B critic AUROC 0.936 yet mid-trajectory interventions regress up to 26pp).

**Judge reliability on agent traces (2026)**: Time to Reflect (2605.19196; 14 judges <55% on research-agent eval; fine-grained beats holistic by >30pp), Catching One in Five (2606.10315; production judge caught 2/9 systematic problems; misses cross-turn state), trajectory-judge (2609.00038; outcome-only 14B judge catches 45% silent faults with 33% FP; step-view 76.6% recall, 0 FP), AgentProp-Bench (judge κ=0.567 vs human 0.835), BabelJudge (2606.22329; order-swap consistency collapses).
**Bias/calibration**: position bias (2406.07791), CALM 12 bias types (2410.02736), self-preference via perplexity (2410.21819).
**Small fine-tuned judges**: Prometheus 2, GLIDER (3.8B), Selene-1-Mini (8B) — none benchmarked on trajectories.
**Cost vs accuracy**: Trust-or-Escalate (ICLR 2025; 2407.18370; 7B first, escalate on low confidence, 78.5% cost saving with >80% agreement guarantee); ensembling + criteria injection +13.5pp, small models gain most (2604.13717).
**Online monitoring**: PrefixGuard (2605.06455; prefix-risk AUPRC 0.90 WebArena / 0.71 τ² / 0.55 Terminal; "observability ceiling"), Real-Time Detection and Repair (2608.02464; ESN+CUSUM ~200µs/step, AUROC 0.872, no cross-deploy transfer), AgentTelemetry (2608.14680), When Errors Become Narratives (2606.14589; "fail-plausible" silent failures caught by humans not monitors).

## B. Industry
- LangSmith: trajectory match (strict/unordered/subset/superset), LLM-judge trajectory evaluator, online rules. No taxonomy, no accuracy.
- Langfuse: observation-level evals (Feb 2026), managed catalog (hallucination, relevance, toxicity), trajectory/tool checks in code. No taxonomy, no accuracy.
- Arize Phoenix/AX: trace-level judge over ordered tool calls; tool-calling / parameter-extraction / planning / path-convergence evaluators. No accuracy.
- Galileo: Luna-2 3B/8B judges ($0.02/M tokens, ~152ms, self-reported F1 0.95 on unspecified data); metrics Tool Selection Quality, Action Advancement/Completion, Agent Flow, Tool Error.
- Patronus Percival (May 2025): agent-as-a-judge, 20+ modes (reasoning / system / planning-coordination), span-level localization, OTel. No Percival-on-TRAIL score published.
- Braintrust, W&B Weave, Datadog LLM Observability: span/trace scorers; Datadog managed evals incl. Tool Selection, Tool Argument Correctness, Goal Completeness. No accuracy evidence.
- **Coxwave Align AI**: "Google Analytics for Gen-AI conversational products". SDK ingestion, semantic search, Analytics Copilot, dashboards, cohorts. Metrics: session engagement, response quality, satisfaction signals, topic clustering, retention, escalation patterns, goal completion. Pro $599/mo; on-prem; SOC2/GDPR. Jan 2026 $5M pre-Series A: today "user analytics and feedback-driven evaluation"; roadmap "track agent behavior in real time, detect anomalies, support rapid intervention" (guardrails / agent verification). Granularity session/message; no public evidence of tool-call/step-level trace support (unverified; docs JS-rendered). No accuracy evidence.

## Gaps
1. Outcome/turn-level judges miss silent faults (45% recall, 33% FP) and cross-turn state defects.
2. No vendor publishes judge accuracy vs human labels; research shows frontier judges at 11–55%.
3. Fragmented taxonomies (Percival 20+, MAST 14, Datadog ~10, Align none); no vendor reports on public benchmarks.
4. "Real-time" in products = async sampled LLM-judge; research monitors run per-step with false-alarm budgets.
5. Detection ≠ prevention; interventions can regress.
6. No bias calibration exposed by products.
7. Small fine-tuned judges not benchmarked on trajectories; trajectory-specific RL/SFT is what closes the gap.
8. Conversation analytics (Align AI) stops at session KPIs; step-level failure localization absent.

## Qwen3-8B as judge, 2-day scope
Anchors: 60.4% step / 57.2% first-error on AgentProcessBench; 39.5%/3.5% on Who&When zero-shot. Realistic: per-step structured prompts (not holistic), rule prefilters for system errors, 3–5-sample self-consistency (+~13pp), calibration on 50–100 labelled traces, position-swap consistency. Expect ~55–65% step accuracy zero-shot, coarse classes better; do not expect reliable step localization (<20%). LoRA SFT on 1–2k pairs feasible in hours but gains unverified.
