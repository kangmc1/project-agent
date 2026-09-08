# Survey notes: hallucination & reasoning-error detection, text → agents (raw, 2026-09-08)

✱ = detail not verified.

## Text-level hallucination benchmarks
- **HaluEval** (EMNLP 2023; 2305.11747) ~35k samples, response-level; ChatGPT detects 58–72%. **HaluEval 2.0** (ACL 2024; 2401.03205) 8,770 questions, fact-level via GPT-4 extraction+judgement.
- **RAGTruth** (ACL 2024; 2401.00396) ~18k RAG responses, human word-level spans + type/intensity; fine-tuned Llama-2-13B ≈ GPT-4.
- **FaithBench** (NAACL 2025; 2410.13210) 660 summaries, 11 annotators; best detector ≈58% balanced acc.
- **FActScore** (EMNLP 2023), **SAFE/LongFact** (NeurIPS 2024; search-verified atomic facts), **LLM-Oasis** (81k pairs), **SelfCheckGPT** (EMNLP 2023; sampling consistency).

## Reasoning-error (step-level) datasets
- **PRM800K** (OpenAI; 800k human step labels, MATH), **Math-Shepherd** (445k MC-rollout labels), **ProcessBench** (Qwen; 3,400 cases, earliest erroneous step; o1-mini F1 87.9, best PRM 56.5 → PRMs generalize poorly), **BIG-Bench Mistake** (2,186 CoT traces, first-mistake; GPT-4 52.9%), **REVEAL** (ACL 2024; 3,360 steps; relevance/attribution/logic; CC-BY-ND), **GRACE** (EMNLP 2026; 2606.16151; step faithfulness-to-context ✱).

## Agent-specific hallucination
- **Survey "LLM-based Agents Suffer from Hallucinations"** (2509.18970): taxonomy reasoning / execution (tool selection, calling) / perception / memory / communication; 18 causes; detector families language/retrieval/execution/simulation/ensemble; detection "remains relatively limited".
- **MIRAGE-Bench** (Berkeley 2025; 2507.21017): actions unfaithful to instruction / history / observation; snapshots from WebArena, TheAgentCompany, SWE-Bench, OSWorld, τ-Bench; risk-aware judge 89.5% agreement; GPT-4o hallucinates 33.9%.
- **AgentHallu** (2026; 2601.06818): 693 trajectories, 7 frameworks, 5 categories / 14 subtypes; step attribution + causal explanation; best 41.1% step; tool-use hallucination subset 11.6%.
- **AgentProcessBench** (2603.14465): 1,000 tool-augmented trajectories, 8,509 human step labels (+1/0/−1); Gemini-3-Flash-Thinking 81.6/65.8; Qwen3-30B-A3B 68.5/52.0.
- **TrajAD / TrajBench** (2602.06443): 60k+ synthetic perturb-and-complete trajectories, 3 anomaly types; trained verifier 81.8 macro-F1 vs Qwen3-8B zero-shot.
- **AgentProp-Bench** (2604.16706; single-author ✱): 14,750 traces; substring judge κ=0.049 vs GPT-4o-mini judge κ=0.567; param-level errors → wrong answer p≈0.62.
- **Tool Receipts** (2603.10060 ✱): HMAC-signed tool receipts cross-checked against claims; 94.2% fabricated-tool-reference detection.
- Unfaithful CoT: Anthropic "Reasoning models don't always say what they think" (2505.05410; hint verbalization <20%); **Gaming the Judge** (2601.14691): rewriting reasoning text only raises judge false positives up to 90%.

## Detection methods
- Semantic entropy (Nature 2024) + **SEPs** hidden-state probes (2406.15927); entity-level streaming probes (2509.03531; AUC 0.90 vs 0.71 SE).
- NLI/grounding classifiers: **MiniCheck** (EMNLP 2024; 770M ≈ GPT-4 on LLM-AggreFact), **LettuceDetect** (2502.17125; ModernBERT token classifier on RAGTruth, 79.2 F1), HHEM-2.
- LLM-as-judge with rubrics (SAFE, MIRAGE risk-aware prompts) — fragile (κ≈0.57; adversarial reasoning text).
- Agent PRMs: **AgentPRM/InversePRM** (CMU 2502.10325; ALFWorld), **AgentPRM promise+progress** (WWW 2026; 2511.08325). Score *progress*, not error.

## Gaps
1. Sample-consistency / entropy methods don't transfer to trajectories (non-replayable env state); no SE/SEP AUROC on agent steps reported.
2. Grounding classifiers (MiniCheck/LettuceDetect) could check claims vs tool observations but no benchmark evaluates that; AgentHallu tool-use step acc only 11.6%.
3. Step-level datasets for tool agents are small/young; none ship hidden states or per-step logprobs of the acting model.
4. PRMs measure progress not hallucination; binary labels misclassify exploration (why AgentProcessBench added neutral).
5. Judges are the labelling backbone yet fragile (κ≈0.57; FaithBench ~58%; Gaming the Judge FP up to 90%; CoT unfaithful).
6. Error propagation measured (p≈0.62) but detectors evaluated per-step, not on cascade prevention.
7. Several 2026 single-author preprints need scrutiny before citation.

## Reusable with an open 8B model
Data: AgentProcessBench (human step labels, public), RAGTruth + LettuceDetect (span baseline in minutes), ProcessBench (control task), MIRAGE-Bench snapshots (Apache-2.0), Who&When.
Methods: (i) hidden-state linear probe on Qwen3-8B per step (SEP recipe), (ii) MiniCheck-7B / LettuceDetect NLI between claimed result and raw tool observation, (iii) 8B judge with risk-aware prompt calibrated on AgentProcessBench, (iv) SE over resampled single-step actions from snapshots.
