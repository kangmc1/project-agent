# Stability-based failure detection for multi-agent runs (Coxwave take-home)

An **offline auditor** that reads the full execution record of a planner→subagent system and flags failures
**without labels or ground truth**. It combines (1) the executing model's own probabilities over the finite set of next
actions and (2) deterministic cross-checks of actions and handoff text against the record. Evaluated on 60 real runs
executed with LangChain Deep Agents on a local Qwen3-32B: τ-bench airline ×30 (main experiment) and AIME 2026 ×30
(supplementary). Finding, in three sentences: planner decision instability (D1) predicts failure (decisive-step AUROC 0.75);
the subagent layer is not visible to D1 and is covered instead by a precision-oriented action-grounding check (D2, F1 0.54);
detector performance is decided less by the detector than by which role and layer it is attached to.

- Proposal (Korean, the primary deliverable): [`docs/proposal.md`](docs/proposal.md)
- Plan / ADR: `.omc/plans/agent-failure-detection-plan.md` (local, not committed) · Timeline: [`docs/notes/timeline.md`](docs/notes/timeline.md)

## What is in the repo

```
scripts/ serve_qwen32b.sh serve_qwen32b_score.sh serve_gptoss20b.sh serve_qwen8b.sh # vLLM servers: executor, D1 scorer, D3 judge, 8B (comparators only)
 check_server.py (P1 gate) probe_deepagents.py (P1b gate) check_docs.py d1_*.sh (D1 batch scoring)
src/data/ aime.py tau.py tau_user.py # AIME 2026 loader, tau-bench airline env, raw-httpx user simulator
src/harness/ deepagents_compat.py model.py capture.py tools.py airline.py aime.py validate.py # graphs + full-observability capture
src/run.py # run one task or a batch
src/audit/ render.py d1.py # D1 decision-distribution scoring (scoring server)
 d2_rules.py d2_tool_log.py d2_required_calls.py d2_argument_grounding.py d2_delegation.py d2_action.py # D2 action grounding (code only; subagent + planner conditions)
 d3_handoff.py llm_only.py # D3 handoff information loss (LLM direct comparison, gpt-oss-20b); LLM-only comparators
 comparators/d3_factset.py extract.py # retired D3 route (Qwen3-8B fact extraction + set diff), kept as a comparator
 report.py system_report.py # per-trace reports, system-level aggregate
 judge.py # optional LLM-judge baseline (not part of the results)
 unused/d4_evidence_judge.py # D4 evidence-dependence judge — DESIGN ONLY, not used in results
src/eval/ index.py summarize.py labels.py metrics.py thresholds.py recovery.py
data/ tau_task_ids.json aime_ids.json # fixed task samples (batch 1 = first 15 of each domain)
runs/ index.csv, <run_id>/summary.md # raw traces are NOT committed (see.gitignore)
audit/ d1.jsonl d1_check.json d2_tool_log.jsonl d2_required_calls.jsonl d2_argument_grounding.jsonl d2_action.jsonl
 d3_handoff.jsonl d3_handoff_stats.json report/<run_id>.{json,md} system_report.{md,json}
audit/_removed/ outputs of retired modules (utterance-grounding check, equation-consistency module, D4 8B pilot) — history only
labels/ RUBRIC.md LABELER_PROMPT.md index.csv <run_id>.json # Claude-annotated step labels (evaluation only)
eval/ metrics.md metrics.csv thresholds.md recovery.png subtags.md
eval/_archive/ pre-D1 metrics snapshot with the old module numbering — history only
```

## Execution graphs (system under test)

```
[τ-bench airline — main] [AIME 2026 — supplementary]
 customer(user_sim) ⇄ planner ─policy_checker─▶ think + policy wiki planner ─solver───▶ run_python
 └─db_agent───────▶ 14 DB tools └─verifier─▶ run_python (independent re-derivation)
 shared FS /case_notes.md (subagents append) submit_answer
```

Subagents are exposed to the planner as **named wrapper tools** (`policy_checker`, `db_agent`, `solver`, `verifier`)
that replicate deepagents' `task` state protocol (copy-in / merge-out), so the handoff decision sits at the tool-name
position where D1 can score it. Executor: Qwen3-32B (vLLM,, thinking off); the user simulator is the same model over
raw HTTP. Airline is the main experiment; AIME was demoted to supplementary after the results review because the solver
does almost all of the work and the planner makes few real decisions (6 labeled planner errors), so the planner→subagent
decomposition is largely formal there (proposal §4.2.12).

## Auditor modules

`Dn` is the detector-module number; the final numbering follows the order in which the modules appear in the results
(D1 decision, D2 action, D3 handoff; D4 design only).

| module | layer | compared against | judged by | one sentence | code | output |
|---|---|---|---|---|---|---|
| **D1** decision distribution | decision | the executor's own probability distribution over candidate actions (tool names ∪ `no_tool`), re-scored with the same weights | code (no LLM) | how much did the decision waver — `1−p_actual`, `1−confidence` (normalized entropy), `1−margin`, plus a handoff layer (delegate vs not) | `d1_decision.py` | `audit/d1.jsonl` |
| **D2** action grounding | action (tool call) | the record: the planner's instruction and the values the agent was given | code (no LLM) | is this action one the record required and allowed — flag = (1) a tool family the instruction required was never called ∪ (2) an identifier-like argument value was never given to the agent ∪ (3′) the call returned an error (file tools and wrapper rows excluded) | `d2_required_calls.py` `d2_argument_grounding.py` `d2_tool_log.py` → `d2_action.py` | `audit/d2_action.jsonl` |
| **D3** handoff information loss | handoff boundary text | the text on the other side of the boundary | LLM judge (gpt-oss-20b) comparing the two texts | what got lost or altered while handing over — instruction→premise and report→planner atomic-fact fidelity | `d3_handoff.py` | `audit/d3_handoff.jsonl` |
| **D4** evidence dependence — *design only* | utterance | the evidence (tool results + instruction) | external LLM as judge | how much does what was said depend on the evidence — per-claim supported / derived / unsupported / contradicted; an 8B pilot was not adopted (airline AUROC 0.47, flagged-step precision 17%) | `unused/d4_evidence_judge.py` | none |

D2 and D4 compare the same record against **actions** and **utterances** respectively; actions are structured JSON and
can be checked by code, utterances are natural language and need an LLM. D3 compares two natural-language texts, and on a
60-handoff information-loss gold the LLM comparison tracked the gold better than 8B fact extraction + set diff (rank corr.
0.71 vs 0.61, material-loss AUROC 0.74 vs 0.62), so D3 is the one module judged by an LLM. D2 also checks the planner's
delegations (missing identifiers; re-issuing after a failure report). D2 is evaluated at its flag (precision / recall /
F1 / FPR); AUROC is reported only for comparability, because a 0/1 score's AUROC is fixed at (recall + 1 − FPR)/2.

Outputs: per-trace report `audit/report/<run_id>.{json,md}` (flags with evidence pointers, no fused score) and the
system-level aggregate `audit/system_report.md` (per agent role, per handoff edge, hotspots).

## Reproduce

```bash
# 0. envs: conda `math_infer` (vLLM 0.9.2) for the servers, `agent_failure_trace` (py3.11) for everything else
# NOTE: all 60 runs and all D1 scoring were produced with vLLM 0.9.2. The same env was later upgraded to vLLM 0.11.0
# (torch 2.8.0+cu128) to serve the gpt-oss-20b comparator judge (scripts/serve_gptoss20b.sh); re-scoring D1 under
# 0.11.0 may move values within the documented reproducibility floor (~0.005 confidence).
pip install -r requirements.txt # inside agent_failure_trace
# 1. servers (device placement and ports live in the scripts)
bash scripts/serve_qwen32b.sh & # executor Qwen3-32B
bash scripts/serve_gptoss20b.sh & # D3 judge gpt-oss-20b (requires the vLLM 0.11.0 env)
bash scripts/serve_qwen8b.sh & # Qwen3-8B, only for the comparators (fact-set D3, LLM-only 8B)
bash scripts/serve_qwen32b_score.sh & # D1 scorer Qwen3-32B
export OPENAI_BASE_URL=<executor server url> OPENAI_API_BASE=$OPENAI_BASE_URL OPENAI_API_KEY=dummy
python scripts/check_server.py && python scripts/probe_deepagents.py # P1 / P1b gates
# 2. data + runs (EXEC_RECORD_TOKENS=1 by default: run-time logprobs are requested only as the channel that carries
# the generated token ids — vLLM 0.9.2 has no return_token_ids; D1 never uses the recorded logprob values)
python -m src.data.tau --write && python -m src.data.aime --write
python -m src.run --domain airline --task 0 && python -m src.harness.validate runs/airline_000 # smoke
python -m src.run --batch 1 --parallel 4 --resume # then --batch 2
# 3. audit
python -m src.audit.d1_decision --check && python -m src.audit.d1_decision --all --method stepwise # D1 (scoring server)
python -m src.audit.d2_tool_log && python -m src.audit.d2_required_calls && python -m src.audit.d2_argument_grounding && python -m src.audit.d2_delegation && python -m src.audit.d2_action # D2
python -m src.audit.d3_handoff --stats # D3 (gpt-oss-20b judge)
python -m src.audit.comparators.d3_factset --stats; python -m src.audit.llm_only all # comparators (optional)
python -m src.audit.report && python -m src.audit.system_report
# 4. labels + evaluation
python -m src.eval.index && python -m src.eval.summarize # then annotate labels/<run_id>.json per labels/RUBRIC.md
python -m src.eval.labels --validate
python -m src.eval.metrics && python -m src.eval.thresholds && python -m src.eval.recovery
python scripts/check_docs.py --proposal --skeleton --adr
```

## Results

Main experiment, τ-bench airline (30 runs: 6 success / 24 failure; 215 labeled error events, 24 decisive steps).
Labels are used for evaluation only; no detector receives labels or ground truth. Full tables, trace-level metrics and
the AIME supplementary section are in [`eval/metrics.md`](eval/metrics.md) and `docs/proposal.md` §4.2.

| module | layer | role | primary metric | AUROC all errors / decisive (for comparison) | verdict |
|---|---|---|---|---|---|
| D1 decision distribution | decision | planner | AUROC 0.63 [0.54, 0.71] / decisive **0.75** [0.61, 0.86] (1 − p_actual) | same | works |
| D1 decision distribution | decision | subagent | AUROC 0.54 / 0.36 | same | no signal |
| D2 action grounding | action | subagent | **F1 0.54** (precision 0.62, recall 0.48, FPR 0.07) | 0.70 [0.63, 0.78] / 0.59 | works (partial) |
| D2 action grounding | action | planner (delegations) | F1 0.35 (precision **0.91**, recall 0.22, FPR 0.007); decisive 6/16 | 0.60 / 0.69 | works (high precision, low recall) |
| D3 handoff information loss, report→planner | boundary | planner | vs loss gold: rank corr. 0.71, material-loss AUROC 0.74 (n = 30) | vs failure labels 0.53 / 0.59 (reference) | measures loss; weak as a failure predictor |
| D3 handoff information loss, instruction→premise | boundary | planner | gold fidelity 0.97 — almost no loss on this boundary (n = 30) | 0.55 / 0.62 (reference) | boundary confirmed lossless |
| D4 evidence dependence | utterance | subagent | design only, no result | – | not used |

AIME 2026 (supplementary): D1 planner all-errors AUROC 0.73 [0.46, 0.96] on 6 positives (not judgeable); D2 subagent
precision 0.91, recall 0.42, F1 0.57, AUROC 0.67 [0.60, 0.74].

## Limitations

- **Main evidence is one domain and 30 runs.** Conclusions rest on τ-bench airline; per-cell decisive positives are 8–16,
 so bootstrap CIs are wide and no ranking between modules is claimed where CIs overlap.
- **Labels are model-made.** Annotators were Claude subagents working blind from run summaries; decisive-step agreement on
 a spot check was 6/6, but event-set agreement (Jaccard 0.56) shows how much freedom "what counts as an error" leaves.
- **The utterance / reasoning layer is uncovered.** "Values right, conclusion wrong" errors are caught by no module; D4 is
 a design only and its 8B pilot was not adopted.
- **One model family and a full-observability logging contract.** Executor, simulator and scorer are all Qwen3; D1 needs
 the exact inputs the model saw plus logprob access, so output-only logs cannot run D1, D2 or D3.
- **Measurement noise floor.** D1 probabilities move by ~0.005 confidence with bf16 rounding paths; differences below that
 are not signal, and label-optimal thresholds sit at that noise level (proposal §4.2.6).

## Data & licenses

- τ-bench (Sierra Research, MIT) — airline domain test tasks, tools, policy wiki.
- AIME 2026 — `MathArena/aime_2026` (Hugging Face).
- Models — Qwen3-32B / Qwen3-8B (Apache-2.0) and openai/gpt-oss-20b (Apache-2.0, D3 judge), served with vLLM (0.9.2 for runs and D1 scoring, 0.11.0 afterwards).
- deepagents 0.7.13, langchain 1.4, langgraph 1.2.

## Commit policy

Raw traces (`runs/<id>/steps.jsonl`, `tool_calls.sqlite`, `fs/`) are not committed (size); `runs/index.csv`,
`runs/<id>/summary.md`, `audit/`, `labels/`, `eval/` and all scripts are, so every table can be regenerated from the
committed artefacts, and the raw traces from the scripts.
