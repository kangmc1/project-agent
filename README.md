# 라벨 없는 멀티에이전트 실패 탐지 (Coxwave 직무과제)

orchestrator→subagent 시스템의 실행 기록 전체를 읽고, **정답이나 라벨 없이** 실패를 짚어내는 **오프라인 감사기(auditor)**다.
기록의 층마다 대조 상대와 판정 주체를 달리 둔다. 결정 층은 실행 모델 자신이 유한한 다음 행동 후보에 매긴 확률로(D1),
행동 층은 도구 호출을 기록과 코드로 대조하여(D2), handoff 경계는 두 텍스트를 LLM으로 비교하여(D3) 검사한다.
LangChain Deep Agents 위에서 로컬 Qwen3-32B로 실제 실행한 τ-bench airline 30회로 평가하였다.
그 산출물인 완전 관측 트레이스 30건, 스텝 라벨 이벤트 215건, handoff 손실 정답지 60건은 과제의 네 실패 유형을 모두 라벨한
평가 데이터셋이자 생성 파이프라인으로 함께 제출한다(제안서 §3.5). 같은 하네스로 실행한 AIME 2026 30회는 제안서 부록 C에 있다.
결론은 세 문장이다. orchestrator의 결정 불안정성(D1)은 실패를 예측한다(decisive step AUROC 0.75).
subagent 층은 D1에 보이지 않으며, 대신 정밀도 위주의 행동 근거성 검사(D2, F1 0.54)가 맡는다.
탐지기의 성능은 탐지기 자체보다 어느 역할·어느 층에 붙이는가에 따라 갈린다.

- 제안서 (한국어, 주 제출물): [`docs/proposal.md`](docs/proposal.md)
- 계획 / ADR: `.omc/plans/agent-failure-detection-plan.md` (로컬, 미커밋) · 타임라인: [`docs/notes/timeline.md`](docs/notes/timeline.md)

## 저장소 구성

```
src/harness/   실행 환경: Deep Agents 위의 두 그래프 + 완전 관측 기록
src/audit/     감사기: d1_decision.py, d2_*.py, d3_handoff.py, d4_evidence_judge.py, report.py, system_report.py
src/eval/      라벨 검증과 지표 계산
scripts/       vLLM 서버 스크립트, 게이트 검사
runs/          실행 요약 (원본 trace는 커밋하지 않음)
audit/         감사기 출력과 실행별 리포트
labels/        스텝 라벨과 라벨링 지침 (평가 전용)
eval/          지표 표와 그림
docs/          제안서, 타임라인
```

폐기된 모듈의 출력은 `audit/_removed/`, 옛 번호의 지표 스냅샷은 `eval/_archive/`에 이력으로만 남긴다.

## 실행 그래프 (감사 대상 시스템)

```
[τ-bench airline]
  customer(user_sim) ⇄ orchestrator ─policy_checker─▶ think + 정책 wiki
                                    └─db_agent───────▶ DB 도구 14개
  공유 파일 /case_notes.md (subagent가 덧붙임)
```

subagent는 orchestrator에게 **이름 붙은 wrapper 도구**(`policy_checker`, `db_agent`)로 노출된다. wrapper는
deepagents의 `task` 상태 프로토콜(copy-in / merge-out)을 그대로 따르므로, handoff 결정이 D1이 채점할 수 있는 도구 이름 위치에
놓인다. 실행기는 Qwen3-32B(vLLM, thinking off)이고 사용자 시뮬레이터는 같은 모델을 raw HTTP로 호출한다.
같은 하네스로 실행한 AIME 2026(orchestrator → solver, verifier)은 solver가 일을 거의 다 해 orchestrator→subagent 분해가 형식적이므로
본문에서 빼고 제안서 부록 C에 두었다. 코드, 라벨 파일, 지표 표에서 orchestrator의 역할 이름은 `planner`다.

## 감사기 모듈

`Dn`은 탐지 모듈 번호다. 최종 번호는 결과에 등장하는 순서를 따른다(D1 결정, D2 행동, D3 handoff, D4 발언).

| 모듈 | 층 | 대조 상대 | 판정 주체 | 한 문장 | 코드 | 출력 |
|---|---|---|---|---|---|---|
| **D1** 결정 분포 | 결정 | 실행기 자신의 후보 행동(도구 이름 ∪ `no_tool`) 확률 분포, 같은 가중치로 재채점 | 코드 (LLM 없음) | 결정이 얼마나 흔들렸는가 — `1−p_actual`, `1−confidence`(정규화 엔트로피), `1−margin`, 그리고 handoff 층(위임 여부) | `d1_decision.py` | `audit/d1.jsonl` |
| **D2** 행동 근거성 | 행동 (도구 호출) | 기록: orchestrator의 지시문과 에이전트가 받은 값 | 코드 (LLM 없음) | 이 행동은 기록이 요구하고 허용한 것인가 — flag = (1) 지시문이 요구한 도구 계열을 한 번도 호출하지 않음 ∪ (2) 식별자형 인자 값이 에이전트에게 주어진 적 없음 ∪ (3′) 호출이 오류를 반환함 (파일 도구와 wrapper 행 제외) | `d2_required_calls.py` `d2_argument_grounding.py` `d2_tool_log.py` → `d2_action.py` | `audit/d2_action.jsonl` |
| **D3** handoff 정보 손실 | handoff 경계 텍스트 | 경계 반대편의 텍스트 | LLM 판정기 (gpt-oss-20b)가 두 텍스트를 비교 | 넘기는 과정에서 무엇이 빠지거나 바뀌었는가 — 지시→전제, 보고→orchestrator의 원자 사실 fidelity | `d3_handoff.py` | `audit/d3_handoff.jsonl` |
| **D4** 근거 의존 판정 | 발언 | 근거 (도구 결과 + 지시문) | LLM 판정 (Qwen3-8B / gpt-oss-20b / Qwen3-32B 비교) | 말한 것이 근거에 얼마나 의존하는가 — 주장별 supported / derived / unsupported / contradicted. 세 판정기 모두 우연 수준(airline AUROC 0.47 / 0.55 / 0.50)이라 미채택 | `d4_evidence_judge.py` | `audit/d4_evidence_judge_<judge>.jsonl` |

D2와 D4는 같은 기록을 각각 **행동**과 **발언**에 대조한다. 행동은 구조화된 JSON이라 코드로 검사할 수 있고, 발언은 자연어라
LLM이 필요하다. D3은 자연어 텍스트 둘을 비교하는데, 60개 handoff 정보 손실 정답지에서 LLM 비교가 8B 사실 추출 + 집합 차보다
정답지를 더 잘 따라갔으므로(순위 상관 0.71 vs 0.61, 실질 손실 AUROC 0.74 vs 0.62) LLM이 판정한다. 발언 층의 D4도 LLM 판정이지만
판정기 세 종(8B, 20B, 32B) 모두 우연 수준이라 채택하지 않았다(제안서 §4.2.14). D2는 orchestrator의 위임도
검사한다(식별자 누락, 실패 보고 후 재발행). D2는 flag 기준(정밀도 / 재현율 / F1 / FPR)으로 평가하며, AUROC은 비교 가능성을 위해서만
싣는다. 0/1 점수의 AUROC은 (재현율 + 1 − FPR)/2로 고정되기 때문이다.

출력은 실행별 리포트 `audit/report/<run_id>.{json,md}`(근거 포인터가 달린 flag, 융합 점수 없음)와 시스템 수준 집계
`audit/system_report.md`(에이전트 역할별, handoff 간선별, 핫스팟)다.

## 재현

```bash
# 0. 환경: 서버는 conda `math_infer` (vLLM 0.9.2), 나머지는 전부 `agent_failure_trace` (py3.11)
# 주의: 60회 실행과 D1 채점은 모두 vLLM 0.9.2로 생산하였다. 이후 gpt-oss-20b 비교군 판정기(scripts/serve_gptoss20b.sh)를 띄우기 위해
#       같은 환경을 vLLM 0.11.0(torch 2.8.0+cu128)으로 올렸다. 0.11.0에서 D1을 다시 채점하면 문서화된 재현성 바닥(confidence ~0.005)
#       안에서 값이 움직일 수 있다.
pip install -r requirements.txt                      # agent_failure_trace 안에서
# 1. 서버 (GPU 배치와 포트는 스크립트 안에 있음)
bash scripts/serve_qwen32b.sh &                      # 실행기 Qwen3-32B
bash scripts/serve_gptoss20b.sh &                    # D3 판정기 gpt-oss-20b (vLLM 0.11.0 환경 필요)
bash scripts/serve_qwen8b.sh &                       # Qwen3-8B, 비교군 전용 (fact-set D3, LLM 단독 8B)
bash scripts/serve_qwen32b_score.sh &                # D1 채점기 Qwen3-32B
export OPENAI_BASE_URL=<실행기 서버 url> OPENAI_API_BASE=$OPENAI_BASE_URL OPENAI_API_KEY=dummy
python scripts/check_server.py && python scripts/probe_deepagents.py   # P1 / P1b 게이트
# 2. 데이터 + 실행 (EXEC_RECORD_TOKENS=1 기본: 실행 시 logprob 요청은 생성 토큰 id를 실어 나르는 통로로만 쓴다.
#    vLLM 0.9.2에는 return_token_ids가 없다. D1은 기록된 logprob 값을 쓰지 않는다)
python -m src.data.tau --write && python -m src.data.aime --write
python -m src.run --domain airline --task 0 && python -m src.harness.validate runs/airline_000   # 스모크
python -m src.run --batch 1 --parallel 4 --resume    # 이어서 --batch 2
# 3. 감사
python -m src.audit.d1_decision --check && python -m src.audit.d1_decision --all --method stepwise   # D1 (채점 서버)
python -m src.audit.d2_tool_log && python -m src.audit.d2_required_calls && python -m src.audit.d2_argument_grounding && python -m src.audit.d2_delegation && python -m src.audit.d2_action   # D2
python -m src.audit.d3_handoff --stats               # D3 (gpt-oss-20b 판정기)
LLM_JUDGE_BASE=http://localhost:18004/v1 LLM_JUDGE_MODEL=gptoss20b python -m src.audit.d4_evidence_judge --labeled-only   # D4, 판정기별로 반복 (qwen32b: BASE :18001)
python scripts/eval_d4.py audit/d4_evidence_judge_*.jsonl   # D4 판정기 비교 (제안서 §4.2.14)
python -m src.audit.comparators.d3_factset --stats; python -m src.audit.llm_only all   # 비교군 (선택)
python -m src.audit.report && python -m src.audit.system_report
# 4. 라벨 + 평가
python -m src.eval.index && python -m src.eval.summarize   # 이후 labels/RUBRIC.md에 따라 labels/<run_id>.json 작성
python -m src.eval.labels --validate
python -m src.eval.metrics && python -m src.eval.thresholds && python -m src.eval.recovery
python scripts/check_docs.py --proposal --skeleton --adr
```

## 결과

본 실험 τ-bench airline (30회: 성공 6 / 실패 24; 라벨된 오류 이벤트 215건, decisive step 24개).
라벨은 평가에만 쓰며, 어떤 탐지기도 라벨이나 정답을 입력으로 받지 않는다. 전체 표와 실행 단위 지표는
[`eval/metrics.md`](eval/metrics.md)와 `docs/proposal.md` §4.2에, AIME 2026은 제안서 부록 C에 있다.

| 모듈 | 층 | 역할 | 주 지표 | AUROC 전체 오류 / decisive (비교용) | 판정 |
|---|---|---|---|---|---|
| D1 결정 분포 | 결정 | orchestrator | AUROC 0.63 [0.54, 0.71] / decisive **0.75** [0.61, 0.86] (1 − p_actual) | 좌동 | 작동 |
| D1 결정 분포 | 결정 | subagent | AUROC 0.54 / 0.36 | 좌동 | 신호 없음 |
| D2 행동 근거성 | 행동 | subagent | **F1 0.54** (정밀도 0.62, 재현율 0.48, FPR 0.07) | 0.70 [0.63, 0.78] / 0.59 | 작동 (부분) |
| D2 행동 근거성 | 행동 | orchestrator (위임) | F1 0.35 (정밀도 **0.91**, 재현율 0.22, FPR 0.007); decisive 6/16 | 0.60 / 0.69 | 작동 (고정밀·저재현) |
| D3 handoff 정보 손실, 보고→orchestrator | 경계 | orchestrator | 손실 정답지 대비 순위 상관 0.71, 실질 손실 AUROC 0.74 (n = 30) | 실패 라벨 대비 0.53 / 0.59 (참고) | 계측 성립. 실패 예측은 약함 |
| D3 handoff 정보 손실, 지시→전제 | 경계 | orchestrator | 정답 fidelity 0.97, 손실 거의 없음 (n = 30) | 0.55 / 0.62 (참고) | 손실 없는 경계로 확인 |
| D4 근거 의존 판정 | 발언 | subagent | 판정기 3종 AUROC 0.47 / 0.55 / 0.50, CI 모두 0.5 포함 | 좌동 | 신호 없음. 미채택 |

## 한계

- **주된 근거가 한 도메인 30회 실행이다.** 결론은 τ-bench airline에 기대며, 셀당 decisive 양성이 8–16건이라 부트스트랩 CI가 넓다.
  CI가 겹치는 곳에서는 모듈 간 순위를 주장하지 않는다.
- **라벨을 모델이 달았다.** 라벨러는 실행 요약만 보고 블라인드로 작업한 Claude subagent다. 스팟체크에서 decisive step 일치는 6/6이었지만,
  이벤트 집합 일치(Jaccard 0.56)는 "무엇을 오류로 볼 것인가"에 남는 자유도를 보여준다.
- **발언 / 추론 층이 비어 있다.** "값은 맞는데 결론이 틀린" 오류는 어느 모듈도 잡지 못한다. D4는 8B, 20B, 32B 판정기 모두 우연 수준이라 채택하지 않았다.
- **모델 계열 하나와 완전 관측 로깅 계약.** 실행기, 시뮬레이터, 채점기가 모두 Qwen3다. D1은 모델이 본 입력 그대로와 logprob 접근이
  필요하므로, 출력만 남는 로그로는 D1, D2, D3을 돌릴 수 없다.
- **측정 잡음 바닥.** D1 확률은 bf16 반올림 경로에 따라 confidence 기준 ~0.005 움직인다. 그 아래의 차이는 신호가 아니며,
  라벨 최적 임계값이 그 잡음 수준에 놓인다(제안서 §4.2.6).

## 데이터와 라이선스

- τ-bench (Sierra Research, MIT) — airline 도메인 테스트 과제, 도구, 정책 wiki.
- AIME 2026 — `MathArena/aime_2026` (Hugging Face).
- 모델 — Qwen3-32B / Qwen3-8B (Apache-2.0), openai/gpt-oss-20b (Apache-2.0, D3 판정기). vLLM으로 서빙(실행과 D1 채점은 0.9.2, 이후 0.11.0).
- deepagents 0.7.13, langchain 1.4, langgraph 1.2.

## 커밋 정책

원본 trace(`runs/<id>/steps.jsonl`, `tool_calls.sqlite`, `fs/`)는 용량 때문에 커밋하지 않는다. `runs/index.csv`, `runs/<id>/summary.md`,
`audit/`, `labels/`, `eval/`와 모든 스크립트는 커밋하므로, 모든 표는 커밋된 산출물에서 다시 만들 수 있고 원본 trace는 스크립트로
다시 만들 수 있다.
