# 빈틈(G1~G8) 재검증 결과 (2026-09-08, 반대 입장 조사)

각 빈틈에 대해 "이미 채운 연구"를 적극적으로 찾은 뒤 판정. 판정 = 유지 / 부분 해소 / 해소.

## G1 — 주입 실패 vs 자연 실패 (sim-to-real gap)
**판정: 부분 해소(약함). "아무도 비교하지 않았다"는 강한 표현은 틀림. 유용한 형태는 살아 있음.**
- 반증 1: Real-Time Detection and Repair (2608.02464, 단독 저자). 같은 환경에서 통계적 모니터(ESN+CUSUM)가 주입 실패 AUROC 0.745–0.885, 자연 실패 11건에서는 within-organic AUROC 0.31–0.42 → 전이 실패를 직접 보고. 단 n=11, LLM judge 아님, temperature shift 교란.
- 반증 2: Trajectory Guard (2601.00516): 합성 이상으로 학습 → Who&When/RAS-Eval 실데이터에서 recall만 보고(정상 샘플 없음), 태스크 비매칭.
- 반증 3: ErrorProbe (2604.17658): 같은 모델의 TracerTraj-합성 34.6% vs Who&When-Algo 58.7% vs Hand 27.6% 보고하나 매칭 분석 없음.
- 미해결 확인: Who&When Pro(주입만), AgenTracer(소스별 ablation 없음), TrajBench(합성만), TraceElephant/TELBench(자연만). Who&When의 AG/HC 분할은 둘 다 자연 실패.
- **남는 것**: LLM 기반 궤적 judge / 학습형 localizer에 대해, *매칭된 태스크·샘플링 조건*에서 주입 vs 자연 실패의 정확도 차이를 충분한 표본(자연 실패 ≥ ~100)으로 측정한 연구 없음. 주입 라벨로 학습 → 자연 실패 step localization 전이도 태스크 분포 통제 하에 미측정.
- 확신: 중상. 미확인: 2606.10315, 2604.16706, 2601.06818 전문.

## G2 — 정상 궤적에 대한 오탐
**판정: outcome-level judge는 부분 해소 / step-level 탐지·귀속은 유지.**
- 반증 1: OpenClawBench (2605.29253): 자연 이상, 정상 ~85%(anomaly 14.7%), 정상 테스트 ~2,258개; fine-tuned detector precision 0.660, zero-shot detector는 42–50% over-flag. 가장 강한 반증.
- 반증 2: Benchmarking LLM Judges for Mobile Agent Evaluation (2608.11434): 931 궤적(성공 492), precision 73.3–92.3%, FP/FN 명시.
- 반증 3: AgentRewardBench (1,302, 성공 라벨, precision 보고), AutoMonitor-Bench (2601.05752; 1,505 benign 쌍, FAR 보고), Real-Time Detection(healthy 1,825 에피소드), trajectory-judge(정상 100), AgentChaosBench(no-fault 25).
- 미해결 확인: AgentProcessBench는 성공 궤적 ~472개 포함하나 StepAcc/FirstErrAcc만 보고(정상 스텝 precision/FP 없음). TELBench: 성공 궤적 36.9%에 오류 있다고만. TraceElephant/Who&When/Pro/TracerTraj는 실패만 수록. 귀속 벤치마크에 "결정적 오류 없음" 클래스 없음.
- **남는 것**: step-level 실패 localizer / 귀속 방법이 정상 궤적을 받았을 때 culprit step을 얼마나 지어내는지(>1,000 정상 궤적, step-level negative)를 보고한 연구 없음.
- 확신: outcome 부분 높음, step-level 중간.

## G5 — 온라인/prefix 탐지 벤치마크 + 오경보 예산
**판정: 해소 (2026-08 기준, 조사의 "공개 벤치마크 없음"은 시대에 뒤짐).**
- 반증 1: **AgentForesight / AFTraj-2K** (2605.08715; HF `ZBox008003/AFTraj`, CC BY 4.0; code MIT). "각 스텝에서 auditor는 현재 prefix만 보고 continue/alarm". 2,276 멀티에이전트 궤적, safe/unsafe 쌍, 결정적 오류 스텝 라벨. 지표: False Alarm Rate, Step-Acc, Exact-F1, Step Shift; "deployable region" FAR ≤20% & Step-Acc ≥50% 정의. AgentForesight-7B 2.4% FAR / 59.5% Step-Acc vs DeepSeek-V4-Pro 43.2% / 54.0%. 라벨은 LLM 합의(사람 검증 아님), 지연/비용 지표 없음.
- 반증 2: **CatchBench** (2608.22808; github yzhao062/catchbench, MIT). 실제 run의 25/50/75/100% prefix에서 탐지기 채점(SWE-Gym 376, τ-bench 660), prefix별 ROC-AUC + TPR@5%FPR, 72개 엔트리. 25% prefix에서 0.742 AUC(SWE-Gym); τ-bench는 0.70 미달.
- 반증 3: Real-Time Detection(2608.02464)이 데이터 공개: HF `sunnydubey1111/agent-trajectory-sentinel`, 3,581 에피소드, onset step 라벨, <1ms/step.
- **남는 것**: (i) 탐지 지연/연산 비용을 FAR·lead time과 함께 보고하는 벤치마크 없음, (ii) *요약/절단된 컨텍스트*에서의 탐지 미평가(CatchBench는 절단 없는 growing prefix), (iii) AFTraj 라벨은 LLM 합의이고 멀티에이전트만, (iv) 단일 에이전트 프로덕션 궤적에서 alarm timing vs correctness 분리 없음. "비동기 샘플링 judge를 실시간이라 부르는 제품" 주장은 여전히 미검증.
- 확신: 높음(공개 아티팩트 3개 확인). 미확인: ATBench(604 궤적) 내용.

## G6 — judge 자체의 신뢰도 프로토콜
**판정: 부분 해소 — 조사보다 훨씬 많이 채워졌으나, 5개 차원을 한 번에 다루는 표준 프로토콜은 없음.**
- 반증 1: **REFLECT** (2605.19196): 연구 에이전트 궤적 메타평가, 472 인스턴스(κ=0.86), judge 13개; holistic vs fine-grained 민감도(+30pt), order-swap 설계, Best-of-N 신뢰도. 최고 47.5%. 코드 미확인.
- 반증 2: **AgentJudgeBench** (ServiceNow, 2608.26623; HF `ServiceNow-AI/AgentJudgeBench`): 3,808 인스턴스, judge 6개; self-preference(GPT-5.4 자기 생성물 +0.172), CoT/온도 민감도, rubric +6.5pp; 사람 일치 92.7%(단일 주석자 120). position bias/order-swap 없음.
- 반증 3: **BabelJudge** (2606.22329): position/verbosity bias, order inconsistency, 궤적 길이 편향 툴킷; Qwen2.5-7B만 대규모 테스트.
- 반증 4: AgentLens(2607.06624; order-swap, judge 간 23% 불일치, 18% self-preference ✱), MobileJudgeBench(2608.11434; 931 사람 라벨), trajectory-judge(calibration 보고), AgentProp-Bench(κ 0.567), Benchmarking the Benchmarks(18.5% 불일치).
- 벤더: Galileo Luna-2(2602.18583) 0.95 acc/152ms는 자체 데이터. Patronus는 TRAIL을 냈지만 Percival의 TRAIL 점수 없음. Arize/LangSmith/Braintrust/Datadog 수치 없음 → **벤더 절반은 유지**.
- **남는 것**: position bias, self-preference, order-swap, step-wise vs holistic, confidence calibration(ECE)을 *같은 judge 집합·같은 사람 라벨 궤적*에서 한꺼번에 보고하는 재사용 가능한 프로토콜 없음. 기존은 도메인별 분산, 소규모(≤472–3,808), 단일 주석자/LLM 합의 라벨. 궤적 판정의 calibration curve(ECE) 보고 없음. 상용 평가기의 공개 벤치마크 정확도 공개 없음.
- 확신: 중상.

## G3 — handoff를 1급 라벨로
**판정: 부분 해소 — "handoff 전용 실패 유형 없음", "컨텍스트 유실은 비용으로만 측정"은 틀림. 이중 책임 라벨 절은 대체로 살아 있음.**
- 반증 1: **AgentAsk** (2510.07593, v2 2026-01): MAS 로그 824개를 *edge-level*(에이전트 간 메시지 단위)로 주석. Data Gap 29.1% / Referential Drift 27.3% / Signal Corruption 36.8% / Capability Gap 6.8%, Fleiss κ 0.84. 송신 edge에 오류 귀속. 한계: 수학/코드 MAS만, 수신자 측 라벨 없음, 사실 단위 drop 추적 없음, 공개 여부 불명.
- 반증 2: **Bound-Handoff** (2608.29028, 2026-08-29): 36 시나리오 × 4 handoff surface × 5 조건 = 720셀; 명제 단위로 boundary marker/operational fact 생존(preserved/paraphrased/weakened/absent, κ 0.74) → 하류 누출과 연결. 공개. "어떤 사실이 떨어졌고 위반을 유발했는가"를 측정 → "비용으로만" 절 반박.
- 반증 3: **Constraint Weakening** (2608.24569): 1,772 합성 에피소드; upstream 미탐지 vs 변환 손실 vs executor 오류 분리 → 사실상 sender/receiver 분리; 필드 단위 보존 라벨.
- 반증 4: MasDrift(제약 유실 첫 handoff 위치), LongRCA(handoff 지시 vs 이후 이탈 루팅 규칙), EntCollabBench(위임 실패 3종), Model or Harness?(peer/subagent delegation failure + fault side), IEEE DataPort A2A/MCP(58 runs, dropped_context/incorrect_delegation 주입, 유료), 벤더 rubric(FutureAGI; 데이터 없음).
- **남는 것**: *실제(비합성·비주입)* 멀티에이전트 궤적에서 각 handoff에 (a) wrong recipient / stale state / conflicting instructions / receiver-ignored를 포함한 handoff 전용 실패 유형, (b) 송신 누락 vs 수신 무시 이중 책임 라벨, (c) 떨어진 사실·제약 목록 + 각 drop이 하류 실패를 유발했는지의 인과 라벨을 모두 붙인 공개 벤치마크 없음. AgentAsk는 (a)를 메시지 내용 결함에 한해 수학/코드 MAS에서, Bound-Handoff/Constraint Weakening은 (c)와 부분 (b)를 안전 경계 중심 합성 환경에서만 제공.
- 확신: 원 표현이 과했다는 점 높음; AgentAsk 세부는 중간. 미확인: OpenAI Agents SDK / LangSmith handoff grader.

## G4 — 분류체계 비호환, 교차 전이
**판정: 유지 (부분 반례 2개).**
- 반례 1: AgentRx(2602.02475)가 MAST 궤적 1,022개에 자기 탐지기를 "generalization stress test"로 실행하며 9개 라벨 중 4개가 MAST에 없다고 명시. 카테고리별 정확도는 미보고(MAST에 step gold 없음).
- 반례 2: Holistic Evaluation(2605.14865)이 LLM 매퍼로 자기 스키마→TRAIL 카테고리 변환(+38% F1), TRAIL 주석 결함(카테고리 중첩) 문서화. 단방향.
- 그 외: EDGE(TRAIL+MAST, 각자 native taxonomy), SAFARI(Who&When+TRAIL, step 위치만), ErrorProbe(둘 다 MAST), Who&When Pro(18 modes, MAST/TRAIL 매핑 없음). 서베이/AgentAtlas/OTel GenAI conventions(v1.42.0)/OpenInference는 span 속성만 표준화, 실패 라벨 아님.
- **남는 것**: TRAIL·MAST·AgentErrorTaxonomy·AgentRx·Who&When Pro·TELBench·AgentHallu 간 many-to-many crosswalk 공개, 같은 궤적 집합을 2개 이상 taxonomy로 재주석해 라벨 일치도 측정, 한 taxonomy로 학습/프롬프트한 탐지기의 다른 taxonomy 카테고리 정확도 보고 — 모두 없음.
- 확신: 중상. 미확인: ErrorAtlas, AgentCompass, 2605.03310 §7.5.

## G7 — RAG grounding 분류기를 도구 관측에 적용
**판정: 부분 해소 — "도구 출력에 평가된 적 없음"은 이제 틀림; "멀티턴 에이전트 궤적"은 유지.**
- 반증 1: **Kovács et al., Beyond Document Grounding** (2607.00895, 2026-07-01; LettuceDetect 팀). 도구 출력 subset 11,365개(테스트 실패, grep, git, 패키지 매니저 출력) + SWE-bench 코드 에이전트 subset 18,524개. Tool-output span-F1: LettuceDetect-Qwen-2B 0.719, off-the-shelf LettuceDetect-large 0.17, zero-shot LLM judge ≤0.22. MiniCheck-7B F1 0.67, HHEM-2.1 0.63, Granite-Guardian 0.66, Lynx-8B 0.61. 저자 명시: 라벨 대부분 합성 주입, 최종 답 검증이지 전체 궤적 아님, 관측 1개 컨텍스트.
- 반증 2: **Trajel** (IBM/Columbia, 2605.24219): 225 전문가 주석 TAO 궤적(κ 0.456), NLI 스타일 탐지기(premise=궤적 이력) F1 0.563 / AUC 0.689 vs LLM judge F1 0.855. MiniCheck/HHEM/LettuceDetect 언급 없음.
- 반증 3: AgentLTL(2607.02599; 정규식/AST로 답의 엔티티가 이전 도구 출력에 있는지), AgentProp-Bench(substring κ 0.049 vs judge 0.567).
- LLM judge만 있는 것 확인: TRAIL, AgentRx("Invention of New Information", "Misinterpretation of Tool Output"), AgentHallu, ToolFailBench("NLI/grounding classifier 없음" 명시).
- **남는 것**: off-the-shelf grounding 분류기를 *멀티턴·다중 호출 궤적 안의 원시 도구 관측*에 대해 *사람 라벨* 날조/오해석 오류로 평가한 연구 없음(TRAIL, AgentRx, ToolFailBench, Trajel 어디에도 NLI baseline 없음). premise 선택(어느 관측을 붙일지)과 관측 길이 스케일링도 미연구.
- 확신: 높음. 미확인: Trajel 부록의 NLI 체크포인트.

## G8 — Align AI와 벤더 정확도 공개
**판정: Align AI 부분은 유지; "어떤 벤더도 공개 벤치마크 정확도를 안 낸다"는 틀림.**
- Align AI: Python SDK 문서(docs.tryalign.ai/python-sdk.html)는 identify_user / open_session / create_message(role, content) / feedback만 노출 — tool call, span, step, agent, handoff 필드 없음. GitHub SDK 최종 갱신 Python 2024-11 / Node 2025-05. 2026-01 Pre-Series A 보도: 에이전트 검증 시장 "진입", 실시간 행동 추적·이상 탐지 예정 — 출시 기능/스키마/정확도 없음. blog·changelog 404, PyPI 렌더 실패 → 비공개 2026 릴리스 가능성 있음.
- 벤더 반증: **Deepchecks** Holistic Evaluation (2605.14865, 저자 15명): TRAIL GAIA joint 0.616(cat-F1 0.547, loc 0.823), SWE 0.638. **FutureAGI** AgentCompass (2509.14647): TRAIL GAIA joint 0.239. 둘 다 arXiv 논문이고 제품 SKU와 직접 연결은 없음.
- 미공개 확인: Patronus(Percival의 TRAIL 점수 없음), Galileo(Luna-2 0.95 F1, 데이터셋 미명시), Noveum(비공개 trace, Claude 라벨), Arize/LangSmith/Braintrust/Maxim/Confident AI 없음.
- **남는 것**: Align AI는 세션/메시지 단위 분석 제품이며 tool-call 수집 스키마·탐지 정확도 공개 없음(로드맵만). 벤더 중 Deepchecks·FutureAGI만 TRAIL에서 사람 라벨 대비 정확도 공개; AgentRewardBench/AgentProcessBench/MAST/AgentRx에 보고한 벤더 없음; 도구 출력 날조/오해석 정확도를 공개한 벤더 없음.
- 확신: SDK/벤더 높음; Align AI 2026 상태 중간.

---

## 종합 판정표

| # | 원래 주장 | 판정 | 살아남은 정밀 서술 |
|---|---|---|---|
| G1 | 주입 vs 자연 실패 비교 없음 | 부분 해소(약) | LLM judge/localizer에 대해 *매칭 태스크*, 자연 실패 ≥100 규모 비교 없음 |
| G2 | 정상 궤적 오탐 평가 없음 | outcome 부분 해소 / step 유지 | step-level localizer가 정상 궤적에서 culprit step을 지어내는 비율 미보고 |
| G3 | handoff 1급 라벨 없음 | 부분 해소 | *실제* 궤적 + 유형 + 송신/수신 이중 책임 + drop 인과 라벨의 조합 없음 |
| G4 | taxonomy 비호환, 전이 미연구 | 유지 | crosswalk·재주석 일치도·교차 taxonomy 정확도 모두 없음 |
| G5 | prefix/온라인 벤치마크 없음 | 해소 | 지연·비용 동시 보고, *요약/절단 컨텍스트* 조건, 사람 라벨, 단일 에이전트만 남음 |
| G6 | judge 신뢰도 프로토콜 없음 | 부분 해소 | 5개 차원을 같은 judge·같은 사람 라벨에서 한 번에 보는 프로토콜 없음; ECE 없음; 벤더 미공개 |
| G7 | grounding 분류기의 도구 관측 적용 없음 | 부분 해소 | 멀티턴 궤적 + 사람 라벨에서 off-the-shelf NLI baseline 없음 |
| G8 | Align AI step-level 없음 / 벤더 정확도 미공개 | Align 유지 / 벤더 절반 해소 | Align은 세션 단위·스키마 없음; Deepchecks·FutureAGI만 TRAIL 공개 |

교훈: 조사 시점 기준 3개월 내(2026-06~09) 논문이 G3·G5·G6·G7을 상당 부분 채웠다. 제안서의 novelty 문장은 위 "살아남은 정밀 서술" 수준으로만 써야 안전하다.
