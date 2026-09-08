# 에이전트 시스템의 handoff 안정성: 압축·인수인계 경계에서 정보가 깨지는 정도를 수치화하는 벤치마크와 파이프라인

> 제출용 본문 초안 (v0.1, 2026-09-08 15:50). [ ] 표시는 실험 결과 대기.

## 0. 한 장 요약
- **문제**: 에이전트 시스템은 문맥이 유일한 상태이고, 긴 작업일수록 문맥을 압축하고 다른 에이전트에 넘긴다. 이 경계에서 제약과 사실이 빠지거나 추측이 사실로 굳고, 원본이 사라져 복구되지 않는다. 실제 실패 기록(TraceElephant, Magentic-One 91 run)에서 재계획 압축 75건 중 59건이 이미 틀어진 상태를 요약에 굳혀 넘겼고, 2026년 프로덕션 사고(OpenClaw 받은편지함 삭제)의 원인도 compaction에서의 제약 소실이었다.
- **기존 탐지의 한계**: LLM judge는 궤적 하나를 읽고 "이상한가"를 묻는다. 스텝 위치 특정 11~33%, false success AUROC 0.65, 프로덕션 결함 23개 중 0개 포착, 정상 궤적 42~50% 과잉 탐지. 탐지기 자체를 믿을 수 없다는 것이 문제의 일부다.
- **제안**: 탐지기의 정확도를 묻는 대신 **시스템의 handoff 안정성**을 잰다. 검증 가능한 의무(제약·사실·미확인·금지)를 심어 두고 K번의 압축·handoff를 통과시켜 생존 곡선을 그린다. 정답을 우리가 심었으므로 판정은 judge가 아니라 항목 대조로 충분하다. 개입 변수는 handoff 포맷(자유 서술 vs 구조화 JSON with `unverified`)과 경계 검사기 유무.
- **평가**: (A) 자연 발생 근거 — 실제 압축 경계 75건에 사람 라벨, (B) 통제 주입 — 실제 fact sheet에 소실/약화/변조 112건, (C) 스트레스 테스트 — K-hop 체인 생존 곡선 × 포맷 × 검사기, (D) 보조 — 행동 분산 기반 불확실성과 결정적 실수의 상관.
- **기대효과**: 관측 제품에 "이 시스템은 handoff N번까지 안전하다"는 숫자와, 경계에서 무엇이 사라졌는지 보여 주는 계기판을 제공. 로그 계약(경계 전후 문맥, 도구 원시 출력, 행동 영수증)을 제품 요구사항으로 도출.

## 1. 배경 (Background)

### 1.1 현재의 에이전트 시스템은 어떻게 작동하는가
(`design/04_simple_framing.md` §1) 루프 / 문맥이 유일한 상태 / 압축·외부 메모리·분할 / 도구 결과는 신뢰 불가 텍스트 / 산업 배치에서 병렬·분할이 늘수록 압축과 메시지 교환이 는다(Anthropic Research 3~5 서브에이전트, Claude Code 95% auto-compact, Copilot Studio 30~40 도구 초과 시 분할; `related_work/08`).

### 1.2 무엇이 고장 나는가 (네 증거원 교차)
(`design/03_problem_landscape.md`) P1 오류 누적, P2 미검증 진행·false success, P3 관측 오독·도구 오용, P4 압축·handoff 상태 소실, P5 무단·파괴적 행동, P6 인젝션, P7 멀티에이전트 증폭.
- 우리 자체 분류(TraceElephant 220건): 추론 25%, 도구 오용 19%, 검증 13%, 계획 11%, 환경 10%, 환각 10%, 관찰 9%, 조정·handoff 3% (`results/traceelephant_failure_types.json`).
- 그러나 같은 데이터의 재계획 압축 75건 중 59건이 틀어진 상태를 요약에 굳힘 → handoff는 오류의 **출발점**이 아니라 **굳히고 퍼뜨리는 통로**. 실무 사고(OpenClaw, Meta)와 통제 실험(압축 시 blocker 100% 비활성)이 같은 메커니즘.

### 1.3 기존 기술로 탐지되는 것과 안 되는 것
(`design/04_simple_framing.md` §3~4) 형식·인자 오류·최종 실패는 잡힘. 과정상 결함(D1 false success, D2 압축 소실, D3 초반 오류, D4 근거 없는 주장)은 judge가 주된 도구이나 신뢰도 낮음(D5). 프로덕션 로그는 입력이 없음(D6).

### 1.4 연구 세부 주제와 차별점
- **주제**: 압축·handoff 경계에서의 정보 훼손을 "시스템 안정성"으로 수치화하는 벤치마크·파이프라인.
- **차별점(3차 검증된 문장만)**: (i) 실제 궤적의 압축 경계를 이벤트 단위로 정의·추출(TraceElephant는 스텝만 라벨), (ii) 판정을 judge에 맡기지 않고 심어 둔 의무의 생존으로 측정(정답 by construction), (iii) 생존을 hop 수의 함수로 보고 handoff 포맷·검사기의 효과를 같은 축에서 비교, (iv) 송신/수신 책임과 "송신자가 인지했는가"를 구분. 가장 가까운 연구(Bound-Handoff: 프라이버시 마커, Constraint Weakening: 안전 차단 조건, AgentAsk: 수학/코드 메시지 결함)는 합성·단일 hop·특정 도메인에 머묾.

## 2. 기존 연구 (Related Work)
(`related_work/00`, `06`, `07` 요약)
- 실패 귀속 벤치마크: Who&When(ICML 2025), TRAIL, AgentRx(EMNLP 2026), AgentProcessBench(KDD 2026), TraceElephant(ACL 2026; 입력까지 기록, 오케스트레이터 기인 19~29%), Who&When Pro, LongRCA.
- handoff·압축: AgentAsk(edge-level 824), Handoff Debt, Bound-Handoff(EMNLP 2026), Constraint Weakening, Routed Graph Handoff(EMNLP 2026), MasDrift. MAST(NeurIPS 2025)의 "대화 기록 손실·정보 은폐" 모드.
- 눈덩이·전파: Snowballing hallucination(ACL 2024), Lost in multi-turn(2025), Spark to Fire, Scaling Agent Systems(17.2배), AgentProp-Bench(p≈0.62).
- 탐지기 신뢰도: REFLECT, AgentJudgeBench, BabelJudge, trajectory-judge, OpenClawBench(정의만, 결과 없음), AFTraj/CatchBench(prefix).
- 산업: OpenAI Agents SDK handoff(기본 전체 기록, nest로 압축), A2A, Copilot Studio, Cognition의 반론.

## 3. 제안 (Methodology & Benchmark Proposal)

### 3.1 정의
handoff h = (S, R, t, C_S, A, I_R, B_R) (`design/02_handoff_definition.md`). 유형 H1 지시(공유 기록), H2 지시(새 문맥), H3 압축(reset), H4 반환, H5 화자 선택. 본 연구의 본체는 **H3**(정보 비대칭 완전, 원본 폐기) — 산업의 H2와 구조 동일.
의무 o ∈ O(C_S): constraint / verified_fact / open_question / goal / prohibition. 생존 ∈ {preserved, weakened, absent, corrupted}. (`design/01_schema.md`)

### 3.2 안정성 지표 (D5의 답)
- 심어 둔 의무 집합 O₀에 대해 hop k 이후 생존율 S(k) = |{o : surv(o, A_k) = preserved}| / |O₀|.
- **handoff 안정성** = S(k) 곡선과 반감 hop k½(S(k½)=0.5). 승격율 = 미확인 항목이 verified로 바뀐 비율. 비용 = 토큰/지연.
- 판정: 심어 둔 항목의 존재는 문자열·임베딩·함의 판정으로 확인(닫힌 질문). judge의 열린 판단 불필요 → D5 우회.

### 3.3 개입 변수
- **handoff 포맷** (D2): (a) 자유 서술 요약, (b) 구조화 JSON — 키: constraints[], verified_facts[], open_questions[], prohibitions[], goal; 값 없으면 `"unverified"`/`"extraction_failed"` 명시.
- **경계 검사기** (D2 탐지): 압축 직전 O 추출 → 압축 후 항목 생존 판정 → 소실·약화·변조 시 복구(재삽입). 규칙층(항목 존재) + 소형 함의 판정 + judge(잔여).
- (보조) **행동 분산 불확실성** (D3): 같은 문맥에서 다음 행동 k회 샘플 → 도구·인자 클러스터 분산. 결정적 실수 스텝과의 상관.

### 3.3b 폐쇄형 멀티에이전트 워크플로우 (스트레스 테스트의 본체, 2026-09-08 17:40 확정)
- 역할: Orchestrator(계획·지시·압축·최종 답) / Researcher(문맥에서 사실·조건 추출, 없으면 "UNAVAILABLE") / Executor(구체 값으로 행동 초안, 없으면 "MISSING") / Verifier(제약·금지·사실 대조, APPROVE|REVISE). 모두 같은 Qwen3-8B, 시스템 프롬프트만 다름.
- **행동 = 다음 에이전트 선택**(4지선다) + 에이전트별 행동 유형(유한) + 대상·지시문. 행동 분포는 샘플링이 아니라 **guided-choice 첫 토큰 logprobs**로 한 번에 읽고 엔트로피를 기록(D3의 답: 행동 공간이 유한하므로 가능). 상태만 보고 잰 분포(정책 불확실성)와 짧은 평가문 뒤의 실제 결정을 분리 기록.
- 경계: 지시 handoff(가시성 shared=대화록 전체 | summary=상태 요약만), 반환 handoff(보고), 압축(대화록 단어 수 > 예산 시, free | json, 가드 유무).
- 폐쇄형(closed-book): 도구·world 없음. 정보는 초기 대화록에 모두 주어지고, 측정 대상은 "주어진 정보가 역할 경계와 압축을 거치며 얼마나 살아남는가". 관측 오류·환경 실패는 재현하지 않으므로 측정값은 전달 손실의 하한. 실제 발생 근거는 A층(TraceElephant)이 담당.
- 측정: 압축마다 심어 둔 의무의 생존·승격·소실(규칙 매처), 최종 답의 제약 보존·금지 위반(부정어 인식)·날조 값(초기 문맥에 없는 숫자형 토큰), Verifier의 REVISE/APPROVE, 라운드별 행동 엔트로피, 토큰.
- 예비 실행(파리 여행 시나리오, 8 라운드, 예산 600): Executor→Researcher→Executor→Verifier(REVISE)→…; 압축 3회 각 0.75 보존; 최종 답 보존 0.50, 날조 값 3개(가짜 예약번호 포함); 정책 엔트로피 1.5~1.9비트.

### 3.4 파이프라인
1. 추출기: TraceElephant run → H1 1,228 / H3 75 이벤트 (`src/agent_handoff/data/traceelephant.py`)
2. 주입기: 실제 fact sheet 항목 소실/약화/변조 + 대조군 (`injection/facts.py`)
3. 체인 시뮬레이터: K-hop 압축 (`chain/telephone.py`) × 포맷 × 검사기
4. 검사기: D0 규칙 / D1 holistic judge / D2 계약 검사기 (`detectors/`)
5. 라벨링 도구: db 기반 검수 페이지 (`scripts/review_template.html`)
6. 로그 계약(D6): 경계 전후 문맥, 도구 호출+원시 결과, 행동 선언+영수증(D1).

## 4. 결과 및 평가 (Evaluation & Expected Impact)

### 4.1 평가 설계
| 층 | 데이터 | 질문 | 지표 |
|---|---|---|---|
| A 자연 | H3 75건(사람 gold 20 + silver) | 실제 압축에서 무엇이 얼마나 사라지나, 송신자가 알고 있었나 | 항목별 생존 분포, 승격율, recognized 비율 |
| B 주입 | 112건(drop/weaken/corrupt/none) | 검사기가 정답 확실한 누락을 잡나, 정상에서 오탐하나 | op별 재현율, 대조군 오탐률 |
| C 스트레스(체인) | 합성 시나리오 × K=8 hop × 예산{80,150,300} × {free,json} × {가드 무,유} | 압축 반복 시 생존 곡선이 포맷·검사기로 얼마나 달라지나 | S(k), k½, 승격율, 토큰 |
| C' 워크플로우 | 합성 시나리오 × 가시성{shared,summary} × {free,json} × {가드 무,유}, 8 라운드 | 역할 분업·경계를 거친 최종 답에서 무엇이 살아남고 무엇이 지어지는가 | 최종 보존율, 승격, 금지 위반, 날조 수, Verifier REVISE율, 행동 엔트로피 |
| D 보조 | H1 결정적 실수 스텝 vs 대조 스텝 | 행동 분산이 실수를 가리키나 | AUROC |

### 4.2 예비 결과 (2026-09-08 15:40 기준)
- A: 재계획 75건 중 결정적 실수 위치 before_reset 59 / at_summary 2 / after 14.
- B: **judge 기반 검사기의 한계** — D2(계약 검사기, Qwen3-8B) 재현율 drop 2/30, weaken 6/30, corrupt 7/22; 대조군 30건 중 23건 오탐. D1(holistic) drop 4/30, weaken 4/30, corrupt 2/22; 대조군 30/30 오탐. → 열린 추출·판정에 기대는 탐지기는 정답이 있는 누락조차 못 잡고 정상에서 울린다. **본 제안이 judge를 부품으로 강등하고 심어 둔 항목 대조로 가는 근거.** [ ] 항목 매칭 방식 재검토 후 확정
- C: 3-hop 예비 실행에서 생존 4/4 유지(예산 150단어) — [ ] K=8, 예산 {80,150,300}, 포맷 2종, 검사기 유무로 본 실험
- D (TraceElephant): (i) 자유 텍스트 지시를 8회 샘플링해 군집 불일치도를 잰 방식은 AUROC 0.47 — 행동이 고정되지 않은 측정이라 D3의 시험이 아니며, 거의 모든 결정이 최대 불일치로 나와 변별력이 없음을 확인. 고정된 화자 선택의 샘플 불일치도 평균 0.03 — 샘플링으로는 작은 확률을 관측할 수 없음. (ii) **고정 행동(4 에이전트) + guided-choice logprobs**로 분포를 읽는 공정한 시험(`scripts/run_uncertainty_fixed.py`, 오케스트레이터의 실제 입력 프롬프트 사용, 실수 39 vs 대조 40): 엔트로피 평균 0.72 vs 0.66비트, AUROC **0.54**; 실제 선택된 에이전트에 준 확률(p_actual) 0.48 vs 0.52, AUROC 0.54. 약한 신호. 단, 판단 모델(Qwen3-8B)이 실제 결정 모델(GPT-4o)과 달라 대리 정책이며, 결정적 실수의 다수가 화자 선택이 아니라 지시 내용·후속 행동에 있음(§1.2 분류: 조정 3%). 워크플로우 그리드(같은 모델이 결정하고 행동)에서 라운드 엔트로피 vs 이후 손실을 다시 본다. 워크플로우 그리드에서는 라운드별 정책 엔트로피 vs 이후 손실을 보고.

### 4.3 한계
합성 체인은 실제 실패 분포와 다름(A층으로 보완); 의무 추출은 LLM에 의존(구조화 포맷이 이를 줄임); 데이터는 Magentic-One 한 시스템(Captain-Agent·Who&When으로 확장 가능); 사람 라벨 20건은 파일럿; P5·P6은 탐지가 아니라 아키텍처 강제의 영역.

### 4.4 기대효과
- 제품: "이 에이전트 구성은 handoff N번, 압축 예산 M단어까지 의무 생존 90%"라는 **안정성 등급**; 경계에서 사라진 항목을 보여 주는 대시보드; 로그 계약이 SDK 요구사항. Align AI의 로드맵(실시간 이상 탐지)을 세션 KPI에서 경계 단위로 내리는 구체안.
- 엔터프라이즈: 에이전트 수·압축 정책 변경 전에 안정성 곡선으로 회귀 테스트; 사람 개입 지점을 경계로 특정.
- 연구: 정답 by construction으로 탐지기 신뢰도 문제를 우회하는 평가 설계; H2(새 문맥 위임)로의 직접 확장.

## 부록
- 조사 기록: `related_work/`, 3차 검증 `06`·`07`
- 이 과제 수행 중의 handoff: 서브에이전트 위임 15회, 그중 2차 검증의 과대 보고를 3차 정독으로 잡음(반환 handoff의 R3 사례)
