# Stability-based failure detection for multi-agent runs (Coxwave take-home, v3)

An **offline auditor** that reads the full execution record of a planner→subagent system and flags handoff, tool and
"reasoning-stability" failures **without labels or ground truth**, using (1) the executing model's own logprobs over the
finite set of next actions and (2) deterministic record cross-checks. Evaluated on 60 real runs (τ-bench airline ×30,
AIME 2026 ×30) executed with LangChain Deep Agents on a local Qwen3-32B.

- Proposal (Korean): [`docs/proposal.md`](docs/proposal.md) · Slides: `docs/slides.html` (Artifact link below)
- Plan / ADR: `.omc/plans/agent-failure-detection-plan.md` (local) · Timeline: [`docs/notes/timeline.md`](docs/notes/timeline.md)

## What is in the repo

```
scripts/   serve_qwen32b.sh serve_qwen8b.sh serve_qwen32b_score.sh   # 3 vLLM servers (GPUs 1-4)
           check_server.py (P1 gate) probe_deepagents.py (P1b gate) check_docs.py
src/data/  aime.py tau.py tau_user.py           # AIME 2026 loader, tau-bench airline env, raw-httpx user simulator
src/harness/ deepagents_compat.py model.py capture.py tools.py subagents(=compat) airline.py aime.py validate.py
src/run.py                                       # run a task / a batch with full-observability capture
src/audit/ render.py d1.py d3.py d3_rules.py extract.py d2.py d7.py d9.py report.py system_report.py
src/eval/  index.py summarize.py labels.py metrics.py thresholds.py recovery.py
data/      tau_task_ids.json aime_ids.json      # fixed samples (batch1 = first 15 of each)
runs/      index.csv, <run_id>/summary.md        # raw traces are NOT committed (see .gitignore)
audit/     d1.jsonl d1_check.json d3.jsonl d2.jsonl d7.jsonl d9.jsonl report/ system_report.md
labels/    RUBRIC.md index.csv <run_id>.json     # Claude-annotated step-level labels (evaluation only)
eval/      metrics.md thresholds.md recovery.png subtags.md
```

## Execution graphs (system under test)

```
[τ-bench airline]                                            [AIME 2026]
 customer(user_sim) ⇄ planner ─policy_checker─▶ think + policy wiki    planner ─solver───▶ run_python
                          └─db_agent───────▶ 14 DB tools                    └─verifier─▶ run_python (independent)
                     shared FS /case_notes.md (subagents append)             submit_answer
```

Subagents are exposed to the planner as **named wrapper tools** (`policy_checker`, `db_agent`, `solver`, `verifier`)
that replicate deepagents' `task` state protocol (copy-in / merge-out), so the handoff decision sits at the tool-name
position where D1 can score it. Executor: Qwen3-32B (vLLM, TP=2, thinking off). User simulator: same model via raw HTTP.

## Auditor modules

| module | signal | judged by |
|---|---|---|
| D1 confidence | distribution over next actions from the executor's logprobs (definition: forced-prefix `prompt_logprobs`; execution: stepwise `allowed_token_ids`, validated equivalent at the distribution level) — tool layer + handoff layer | code |
| D3 tool-called | does each claim have prior tool evidence; 5 tool-log checks (error / empty / repeat / schema / ignored) | code |
| D2 groundedness | claims extracted by an 8B model, values looked up in prior tool results | extractor + code |
| D7 handoff fidelity | atomic-fact set diff: report→planner quote, instruction→subagent premise | extractor + code |
| D9 equation consistency (AIME) | equations extracted → sympy `parse_expr` sandbox → true/false/unknown | extractor + code |

Outputs: per-trace report `audit/report/<run_id>.{json,md}` (flags + evidence pointers, no fused score) and a
system-level aggregate `audit/system_report.md` (per agent role / handoff edge / hotspots).

## Reproduce

```bash
# 0. envs: conda `math_infer` (vllm 0.9.2) for servers, `agentbench` (py3.11) for everything else
pip install -r requirements.txt                       # inside agentbench
# 1. servers (GPUs 1-4 only)
bash scripts/serve_qwen32b.sh & bash scripts/serve_qwen8b.sh & bash scripts/serve_qwen32b_score.sh &
export OPENAI_BASE_URL=http://localhost:18001/v1 OPENAI_API_BASE=$OPENAI_BASE_URL OPENAI_API_KEY=dummy
python scripts/check_server.py && python scripts/probe_deepagents.py      # P1 / P1b gates
# 2. data + runs
python -m src.data.tau --write && python -m src.data.aime --write
python -m src.run --domain airline --task 0 && python -m src.harness.validate runs/airline_000   # smoke
python -m src.run --batch 1 --parallel 4 --resume      # then --batch 2
# 3. audit
python -m src.audit.d1 --check && python -m src.audit.d1 --all
python -m src.audit.d3 && python -m src.audit.d2 --stats && python -m src.audit.d7 --stats && python -m src.audit.d9 --stats
python -m src.audit.report && python -m src.audit.system_report
# 4. labels + evaluation
python -m src.eval.index && python -m src.eval.summarize      # then annotate labels/<run_id>.json per labels/RUBRIC.md
python -m src.eval.labels --validate
python -m src.eval.metrics && python -m src.eval.thresholds && python -m src.eval.recovery
```

## Data & licenses

- τ-bench (Sierra Research, MIT) — airline domain test tasks, tools, policy wiki.
- AIME 2026 — `MathArena/aime_2026` (Hugging Face).
- Models — Qwen3-32B / Qwen3-8B (Apache-2.0), served with vLLM 0.9.2.
- deepagents 0.7.13, langchain 1.4, langgraph 1.2.

## Results

(filled at M8 — see `eval/metrics.md`)

## Limitations

(filled at M8 — see proposal §4.3)

## Commit policy

Raw traces (`runs/<id>/steps.jsonl`, `tool_calls.sqlite`, `fs/`) are not committed (size); `runs/index.csv`,
`runs/<id>/summary.md`, `audit/`, `labels/`, `eval/` and all scripts are, so every table can be regenerated from the
committed artefacts, and the raw traces from the scripts.
