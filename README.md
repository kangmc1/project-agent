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
scripts/       serve_qwen32b.sh serve_qwen8b.sh serve_qwen32b_score.sh    # 3 vLLM servers (GPUs 1-4, ports 18001-18003)
               check_server.py (P1 gate)  probe_deepagents.py (P1b gate)  check_docs.py  d1_*.sh (D1 batch scoring)
src/data/      aime.py tau.py tau_user.py        # AIME 2026 loader, tau-bench airline env, raw-httpx user simulator
src/harness/   deepagents_compat.py model.py capture.py tools.py airline.py aime.py validate.py   # graphs + full-observability capture
src/run.py                                        # run one task or a batch
src/audit/     render.py d1.py                    # D1 decision-distribution scoring (scoring server)
               d2_rules.py d2_toolcalls.py d2_instruction.py d2_args.py d2_action.py   # D2 action grounding (code only)
               d3_handoff.py extract.py           # D3 handoff fidelity (8B extractor + set comparison)
               report.py system_report.py         # per-trace reports, system-level aggregate
               judge.py                           # optional LLM-judge baseline (not part of the results)
               unused/d4_judge.py                 # D4 evidence-dependence judge — DESIGN ONLY, not used in results
src/eval/      index.py summarize.py labels.py metrics.py thresholds.py recovery.py
data/          tau_task_ids.json aime_ids.json    # fixed task samples (batch 1 = first 15 of each domain)
runs/          index.csv, <run_id>/summary.md     # raw traces are NOT committed (see .gitignore)
audit/         d1.jsonl d1_check.json d2_toolcalls.jsonl d2_instruction.jsonl d2_args.jsonl d2_action.jsonl
               d3_handoff.jsonl d3_handoff_stats.json report/<run_id>.{json,md} system_report.{md,json}
audit/_removed/  outputs of retired modules (utterance-grounding check, equation-consistency module, D4 8B pilot) — history only
labels/        RUBRIC.md LABELER_PROMPT.md index.csv <run_id>.json   # Claude-annotated step labels (evaluation only)
eval/          metrics.md metrics.csv thresholds.md recovery.png subtags.md
eval/_archive/ pre-D1 metrics snapshot with the old module numbering — history only
```

## Execution graphs (system under test)

```
[τ-bench airline — main]                                       [AIME 2026 — supplementary]
 customer(user_sim) ⇄ planner ─policy_checker─▶ think + policy wiki    planner ─solver───▶ run_python
                          └─db_agent───────▶ 14 DB tools                    └─verifier─▶ run_python (independent re-derivation)
                     shared FS /case_notes.md (subagents append)             submit_answer
```

Subagents are exposed to the planner as **named wrapper tools** (`policy_checker`, `db_agent`, `solver`, `verifier`)
that replicate deepagents' `task` state protocol (copy-in / merge-out), so the handoff decision sits at the tool-name
position where D1 can score it. Executor: Qwen3-32B (vLLM, TP=2, thinking off); the user simulator is the same model over
raw HTTP. Airline is the main experiment; AIME was demoted to supplementary after the results review because the solver
does almost all of the work and the planner makes few real decisions (6 labeled planner errors), so the planner→subagent
decomposition is largely formal there (proposal §4.2.12).

## Auditor modules

`Dn` is the detector-module number; the final numbering follows the order in which the modules appear in the results
(D1 decision, D2 action, D3 handoff; D4 design only).

| module | layer | compared against | judged by | one sentence | code | output |
|---|---|---|---|---|---|---|
| **D1** decision distribution | decision | the executor's own probability distribution over candidate actions (tool names ∪ `no_tool`), re-scored with the same weights | code (no LLM) | how much did the decision waver — `1−p_actual`, `1−confidence` (normalized entropy), `1−margin`, plus a handoff layer (delegate vs not) | `d1.py` | `audit/d1.jsonl` |
| **D2** action grounding | action (tool call) | the record: the planner's instruction and the values the agent was given | code (no LLM) | is this action one the record required and allowed — flag = (1) a tool family the instruction required was never called ∪ (2) an identifier-like argument value was never given to the agent ∪ (3′) the call returned an error (file tools and wrapper rows excluded) | `d2_instruction.py` `d2_args.py` `d2_toolcalls.py` → `d2_action.py` | `audit/d2_action.jsonl` |
| **D3** handoff fidelity | handoff boundary text | the text on the other side of the boundary | 8B extractor + code set comparison | what got lost while handing over — instruction→premise and report→planner atomic-fact fidelity | `d3_handoff.py` | `audit/d3_handoff.jsonl` |
| **D4** evidence dependence — *design only* | utterance | the evidence (tool results + instruction) | external LLM as judge | how much does what was said depend on the evidence — per-claim supported / derived / unsupported / contradicted; an 8B pilot was not adopted (airline AUROC 0.47, flagged-step precision 17%) | `unused/d4_judge.py` | none |

D2 and D4 compare the same record against **actions** and **utterances** respectively; actions are structured JSON and
can be checked by code, utterances are natural language and need an LLM. D2 is evaluated at its flag (precision / recall /
F1 / FPR); AUROC is reported only for comparability, because a 0/1 score's AUROC is fixed at (recall + 1 − FPR)/2.

Outputs: per-trace report `audit/report/<run_id>.{json,md}` (flags with evidence pointers, no fused score) and the
system-level aggregate `audit/system_report.md` (per agent role, per handoff edge, hotspots).

## Reproduce

```bash
# 0. envs: conda `math_infer` (vLLM 0.9.2) for the servers, `agentbench` (py3.11) for everything else
pip install -r requirements.txt                       # inside agentbench
# 1. servers (GPUs 1-4 only)
bash scripts/serve_qwen32b.sh &        # executor  Qwen3-32B TP=2, GPUs 1-2, :18001
bash scripts/serve_qwen8b.sh &         # extractor Qwen3-8B,        GPU 3,   :18002
bash scripts/serve_qwen32b_score.sh &  # D1 scorer Qwen3-32B TP=1, GPU 4,   :18003
export OPENAI_BASE_URL=http://localhost:18001/v1 OPENAI_API_BASE=$OPENAI_BASE_URL OPENAI_API_KEY=dummy
python scripts/check_server.py && python scripts/probe_deepagents.py      # P1 / P1b gates
# 2. data + runs  (EXEC_RECORD_TOKENS=1 by default: run-time logprobs are requested only as the channel that carries
#    the generated token ids — vLLM 0.9.2 has no return_token_ids; D1 never uses the recorded logprob values)
python -m src.data.tau --write && python -m src.data.aime --write
python -m src.run --domain airline --task 0 && python -m src.harness.validate runs/airline_000   # smoke
python -m src.run --batch 1 --parallel 4 --resume      # then --batch 2
# 3. audit
python -m src.audit.d1 --check && python -m src.audit.d1 --all --method stepwise        # D1 (scoring server)
python -m src.audit.d2_toolcalls && python -m src.audit.d2_instruction && python -m src.audit.d2_args && python -m src.audit.d2_action   # D2
python -m src.audit.d3_handoff --stats                                                   # D3 (8B extractor)
python -m src.audit.report && python -m src.audit.system_report
# 4. labels + evaluation
python -m src.eval.index && python -m src.eval.summarize      # then annotate labels/<run_id>.json per labels/RUBRIC.md
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
| D3 handoff fidelity, report→planner | boundary | planner | AUROC 0.59 [0.47, 0.72] / 0.60 | same | weak |
| D3 handoff fidelity, instruction→premise | boundary | planner | AUROC 0.40 [0.25, 0.55] / 0.35 | same | no signal (negative result) |
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
- Models — Qwen3-32B / Qwen3-8B (Apache-2.0), served with vLLM 0.9.2.
- deepagents 0.7.13, langchain 1.4, langgraph 1.2.

## Commit policy

Raw traces (`runs/<id>/steps.jsonl`, `tool_calls.sqlite`, `fs/`) are not committed (size); `runs/index.csv`,
`runs/<id>/summary.md`, `audit/`, `labels/`, `eval/` and all scripts are, so every table can be regenerated from the
committed artefacts, and the raw traces from the scripts.
