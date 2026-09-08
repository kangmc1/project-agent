# Survey notes: error/failure detection benchmarks for agent trajectories (raw, 2026-09-08)

Source: automated literature sweep, verified against arXiv/GitHub/HF pages unless flagged.

## Core works (2025)
- **TRAIL** (Patronus AI; arXiv 2505.08638; HF `PatronusAI/TRAIL`, MIT). 148 OpenTelemetry traces (118 GAIA via multi-agent deep research, 31 SWE-bench Lite single-agent), 841 errors, 1,987 spans. Manual, 4 experts, 30–40 min/trace. Taxonomy 3 groups: Reasoning (hallucination text/tool, poor retrieval, tool-output misinterpretation, tool-selection error, formatting, instruction non-compliance…), System execution (tool def, env, rate-limit, auth, timeout…), Planning/coordination (context handling, resource abuse, goal deviation, task orchestration). Task: span localization + category + impact. Gemini-2.5-Pro 18.3% joint (GAIA), 5.0% (SWE).
- **AgentErrorTaxonomy / AgentErrorBench / AgentDebug** (Zhu et al., UIUC; arXiv 2509.25370; github ulab-uiuc/AgentDebug). 200 failed single-agent trajectories (ALFWorld 100, WebShop 50, GAIA 50), 10 annotators, κ=0.55. 5 modules × 16 types (Memory, Reflection, Planning, Action, System). Task: root-cause step + module + type. Best baseline 0.3% all-correct / 28% step; AgentDebug 24.3% / 45%.
- **AgentIssue-Bench** (NeurIPS 2025; arXiv 2505.20749). Framework *code bugs*, not trajectories. 50 reproducible tasks from 201 issues.
- **Who&When** (ICML 2025; arXiv 2505.00212). Multi-agent only. 184 logs; who + step; best 55% agent / 8.8% step (hand-crafted).
- **Who&When Pro** (2026; arXiv 2607.09996; HF `Leoxx/whowhen_pro`). 12,326 failed trajectories, 26 benchmarks, single+multi, labels via *warm-start injection* (replay success prefix, inject one error). 18 modes / 6 categories (perception, reasoning, planning, action, verification, coordination). GPT-5.4: 72.3% step acc but 15.3% mode F1.
- **Agent-as-a-Judge / DevAI** (ICML 2025; arXiv 2410.10934). Judges requirement satisfaction; no failure taxonomy.
- **TRAJECT-Bench** (arXiv 2510.04550). Tool trajectory quality metrics (selection, args, order); no annotated error set.
- **AgentBoard** (NeurIPS 2024). Progress rate; no failure annotation.
- **τ-bench / τ²-bench** ships `auto_error_identification.py` (LLM labels fault author + 4 agent fault types: wrong tool, wrong argument, goal partially completed, other). No human-labelled release.

## 2026 single-agent trajectory benchmarks
- **AgentRx** (Microsoft; EMNLP Findings 2026; arXiv 2602.02475; HF `microsoft/AgentRx`, CC-BY-4.0). 170 failed trajectories (τ-bench retail 39, Flash 42, Magentic-One 44, RelWork 45), κ=0.89. 9 categories: instruction/plan adherence, invented information, invalid invocation, tool-output misinterpretation, intent-plan misalignment, under-specified intent, intent not supported, guardrails triggered, system failure. Task: first-unrecoverable-step + category. Judge-only 29.9–80.2% → AgentRx (invariant checking) 42.7–82.5%.
- **AgentProcessBench** (RUC/Tsinghua; arXiv 2603.14465). 1,000 trajectories / 8,509 steps (HotpotQA, GAIA, BFCL, τ²), κ=0.767, ternary step labels. Best Gemini-3-Flash-Thinking 81.6% StepAcc / 65.8% FirstErrAcc. No type taxonomy.
- **TELBench / DRIFT** (NJU; arXiv 2606.02060; HF `NJU-LINK/TELBench`). 1,000 deep-research trajectories, 11,950 spans; 18 faults / 6 families × 8 stages. Claude-Sonnet-4.6 F1 21.9% → DRIFT 54.9%.
- **TrajDebug / TrajErrBench** (Tsinghua; arXiv 2608.06346). 486 trajectories (τ², SWE-Bench Pro); critical vs benign ("error lifecycle"). Release pending.
- **LHATA** (Huawei; arXiv 2608.06909). 1,300+ tool-use trajectories, component attribution incl. attack chains; Hit@1 0.537.
- **AgentLens-Bench** (arXiv 2605.12925). 1,815 OpenHands trajectories; "lucky pass" taxonomy (10.7% of passes). Release pending.
- **trajectory-judge** (Utrecht; arXiv 2609.00038). 400 synthetic support-desk trajectories, 6 injected fault types; outcome-only judges catch 45% of silent faults.
- Adjacent: **False Success** (arXiv 2606.09863; judges AUROC ≤0.65 on τ²/AppWorld), SWE-PRM (2509.02360), Holistic Eval (Deepchecks, 2605.14865).

## Taxonomy / survey papers
MAST (NeurIPS 2025), "Model or Harness?" (2607.28802; 41 modes on component edges), Failure Modes in LLM Systems (2511.19933), Evaluation & Benchmarking of LLM Agents survey (2507.21504), MAS attribution survey (2605.14892), AgentAtlas (2605.20530).

## Gaps observed
1. No cross-dataset taxonomy alignment (TRAIL 20 / AgentErrorBench 16 / AgentRx 9 / TELBench 18 / Who&When Pro 18); judge transfer across taxonomies untested.
2. Natural vs injected failures never compared on the same tasks; sim-to-real gap for judges unmeasured (trajectory-judge admits injected faults are "cleaner").
3. Critical-vs-benign error distinction under-labelled (only TrajDebug unreleased, AgentProcessBench neutral label).
4. Successful-but-flawed trajectories nearly absent → judges never evaluated for false positives on successes at scale (TRAIL has 4 clean traces).
5. Inter-annotator agreement on *type* labels low/unreported (κ=0.55 AgentErrorBench).
6. Coding-agent single-agent step-level labels thin.
7. Detection under truncated/partial context (online monitoring) untested; all benchmarks are full post-hoc traces.
8. No small-model / scaling results for detection except AgenTracer-8B and trajectory-judge (14B).

## Reusable seed data
AgentErrorBench (200, MIT, GDrive), AgentRx (170, HF), AgentProcessBench (1,000 / 8,509 step labels), TELBench (1,000), TRAIL (148, OTel spans), Who&When Pro (12k, single-agent subset), τ²-bench + auto_error_identification.
