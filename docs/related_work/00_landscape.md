# 관련 연구 지형도와 후보 방향 (2026-09-08 조사 기준)

원자료: `01_*.md` ~ `05_*.md` (영역별 조사 노트, 출처 arXiv ID 포함).

## 1. 지형 요약

### 1.1 2025~2026년에 벌어진 일
에이전트 궤적의 오류 탐지는 2025년 상반기까지 소규모 수동 주석 벤치마크(TRAIL 148, AgentErrorBench 200, Who&When 184)뿐이었으나, 2026년에 급격히 커졌다.
- 자연 발생 실패 + 사람 주석: AgentRx(170, MS), AgentProcessBench(1,000 궤적 / 8,509 스텝, 사람 라벨), TELBench(1,000), TraceElephant(220), LongRCA(1,140), MP-Bench(289), AgentHallu(693)
- 주입(injection) 기반 대규모: Who&When Pro(12,326), TrajBench(60k 합성), AgenTracer/TracerTraj(2k+), CRITICTOOL(2,740), trajectory-judge(400 합성)
- 분류체계: TRAIL 20+, AgentErrorBench 16, AgentRx 9, TELBench 18, Who&When Pro 18, MAST 14 — 서로 호환되지 않음
- 탐지기: 프론티어 모델 judge도 step-level 정확도 11~30%대(TRAIL, Who&When). 궤적 전용 RL/SFT한 8B 모델(AgenTracer-8B)이 Gemini-2.5-Pro를 이김. Qwen3-8B zero-shot은 AgentProcessBench에서 step 60.4%.
- 상용 제품(LangSmith, Langfuse, Arize, Galileo, Patronus Percival, Datadog): span/trace 단위 LLM judge 제공하나 **사람 라벨 대비 정확도를 공개한 곳이 없음**. Coxwave Align AI는 세션/메시지 단위 대화 분석이며 step-level 실패 위치 특정은 없음(로드맵에 실시간 이상 탐지 명시).

### 1.2 처음 계획에 대한 정정
초기 PLAN.md의 "실패 주입으로 정답 라벨 자동 생성" 아이디어는 Who&When Pro(warm-start injection), TrajBench, trajectory-judge가 이미 수행했다. 주입 벤치마크 하나를 더 만드는 것만으로는 차별점이 약하다.

### 1.3 다섯 영역에서 반복적으로 확인된 빈틈
| # | 빈틈 | 근거 |
|---|---|---|
| G1 | 주입 실패 vs 자연 실패의 탐지 난이도 차이(sim-to-real gap)를 같은 태스크에서 비교한 연구 없음 | Who&When 계열 AG/HC 격차, trajectory-judge 자인 |
| G2 | 정상(성공) 궤적에 대한 탐지기 오탐(false positive) 평가가 사실상 없음. 대부분 실패 궤적만 수록 | TRAIL 정상 4개, False Success, AgentLens |
| G3 | handoff 실패를 1급 라벨로 다루는 벤치마크 없음. 컨텍스트 유실은 비용으로만 측정, 송신/수신 양측 책임 라벨 없음 | MAST(분산), Handoff Debt, MP-Bench |
| G4 | 분류체계 간 정렬/전이 연구 없음 | 6개 taxonomy 비호환 |
| G5 | 온라인/부분 컨텍스트(prefix) 탐지와 오경보 예산은 연구만 있고 벤치마크 없음. 제품의 "실시간"은 비동기 샘플링 judge | PrefixGuard, RT-Detect, Who&When Pro 길이 붕괴 |
| G6 | 탐지기 자체의 신뢰도(judge reliability) 측정 부재. 프롬프트 방식(step-wise vs holistic) 차이 30pp 이상, 위치 편향, 자기 선호 | Time to Reflect, trajectory-judge, AgentProp-Bench |
| G7 | 도구 출력 대비 주장(claim)의 근거 검증: RAG용 grounding 분류기를 도구 관측에 적용한 평가 없음 | ToolFailBench, Tool Receipts, LettuceDetect |
| G8 | 대화 분석 제품은 세션 KPI에서 멈춤. step-level 실패 위치 특정과 정확도 공개가 없음 | Align AI, 벤더 문서 |

### 1.4 바로 쓸 수 있는 공개 데이터 (접근 확인 완료)
AgentProcessBench(GitHub), AgentRx(HF), TRAIL(HF), Who&When(HF), MAST-Data(HF), TraceElephant(GitHub). 모두 2026-09-08 HTTP 200 확인.

## 2. 후보 방향 (2일 제약 + 로컬 Qwen3-8B 기준)

### A. 탐지기 신뢰도 벤치마크 프로토콜 (G2, G5, G6, G8)
"에이전트를 평가하는 벤치마크"가 아니라 **"탐지기를 평가하는 프로토콜"**을 제안한다. 사람 라벨이 있는 AgentProcessBench(+AgentRx)를 재사용하고, 여기에 (a) 정상 궤적 세트(오탐 측정), (b) prefix 절단 세트(온라인 탐지 시뮬레이션)를 추가한다. Qwen3-8B judge를 holistic / step-wise / 규칙 prefilter+judge / self-consistency 4가지 프로토콜로 돌려 정확도-비용-오탐 프론티어를 그린다.
- 장점: 실제 사람 라벨로 진짜 숫자가 나옴. 제품화 관점(싼 judge를 어떤 프로토콜로 배포해야 하는가)에 직결. Align AI가 비어 있는 자리(G8)를 정확히 짚음.
- 단점: 데이터셋 "구축" 색채가 약함. 외부 데이터 포맷 파싱 리스크.
- 실현성: 높음.

### B. Handoff 실패 벤치마크 (G3)
멀티에이전트 handoff를 1급 이벤트로 스키마화하고, handoff 전용 실패(제약 누락, 잘못된 수신자, 오래된 상태 전달, 상충 지시, 수신자 무시)를 주입해 **송신/수신 이중 책임 라벨**을 부여한다. 모의 도구 환경에서 궤적 생성 + Who&When/TraceElephant의 실제 handoff 구간을 소량 재라벨링해 자연 실패와 대조. Qwen3-8B로 탐지/위치/귀속 평가.
- 장점: 과제문에 명시된 handoff를 정면으로 다루며 조사상 가장 뚜렷한 공백. 연구적 신선도 최고.
- 단점: 합성 데이터 위주라 sim-to-real 한계를 스스로 인정해야 함. 생성기 구현량이 가장 큼.
- 실현성: 중간.

### C. 주입 실패 vs 자연 실패 탐지 난이도 비교 (G1)
AgentProcessBench의 자연 실패와, 같은 태스크의 정상 궤적에 동일 유형을 주입한 실패를 짝지어 judge 정확도를 비교한다. "합성 벤치마크 점수를 얼마나 할인해서 믿어야 하는가"라는 보정 계수를 산출.
- 장점: 아무도 안 한 질문이며 방법이 단순.
- 단점: 유형 매칭이 까다롭고, 도구 상태가 있는 궤적에 그럴듯하게 주입하려면 환경 접근 필요. 단독 주제로는 폭이 좁음. A의 확장 실험으로 붙이기 좋음.
- 실현성: 중간.

### D. 도구 출력 근거 검증기 (G7)
에이전트의 thought/최종 답에서 주장을 추출해 원시 도구 관측과 NLI(MiniCheck/LettuceDetect)로 대조하는 검증기 vs LLM judge를 비교. 주입한 도구 출력 날조/왜곡에 대해 평가.
- 장점: 가볍고 명확. RAG 환각 탐지기의 전이라는 명확한 연구 질문.
- 단점: 4개 실패군 중 환각 하나만 다룸. 데이터 준비가 결국 주입 방식.
- 실현성: 높음.

## 3. 추천
**A를 주축으로, C를 확장 실험으로 결합**하는 안을 추천한다. 이유: (1) 사람 라벨 데이터가 있어 이틀 안에 실제 결과가 나온다, (2) "리서치 및 제품화" 직무와 Align AI의 로드맵(실시간 이상 탐지)에 직결된다, (3) 주입 데이터의 한계를 C로 스스로 정량화하면 면접에서 방어가 쉽다.
B는 가장 야심찬 선택지로, handoff에 강한 흥미가 있다면 충분히 방어 가능하다. 단 합성 데이터 한계를 명시하고 규모를 작게 잡아야 한다.

## 4. 재검증 후 수정 (2026-09-08 오후, 상세는 `06_gap_verification.md`)

재검증 결과 G5는 해소, G3·G6·G7은 부분 해소, G1·G2(step)·G4·G8(Align)만 유지. 후보 방향에 미치는 영향:

- **A(탐지기 신뢰도 프로토콜)**: REFLECT, AgentJudgeBench, BabelJudge가 차원별로 이미 측정. AFTraj/CatchBench가 prefix 벤치마크를 냄. "최초의 judge 신뢰도 벤치마크"라는 포지셔닝은 불가. 남는 것은 (i) step-level localizer의 *정상 궤적 오탐*(G2), (ii) *요약/절단 컨텍스트* 조건(G5 잔여), (iii) 같은 judge·같은 사람 라벨에서 여러 차원 동시 보고 + ECE(G6 잔여).
- **B(handoff 벤치마크)**: AgentAsk(edge-level 824), Bound-Handoff(명제 단위 생존), Constraint Weakening(sender/receiver 분리)이 합성·주입 영역을 상당히 채움. 합성 handoff 주입기는 novelty가 약해짐. 살아남는 것은 *실제 궤적*(Who&When, TraceElephant)에 이중 책임 + 유형 라벨을 붙이는 재주석 작업 — 사람 라벨링 시간이 필요해 이틀 안에는 소규모(수십 handoff)만 가능.
- **C(주입 vs 자연, 매칭 태스크)**: 가장 깨끗하게 살아남음. 정밀 서술: "LLM judge/localizer에 대해 매칭 태스크·매칭 샘플링 조건에서 주입 실패 vs 자연 실패의 정확도 차이를 자연 실패 ≥100 규모로 측정한 연구 없음". AgentProcessBench가 같은 태스크에서 성공 궤적(~472)과 자연 실패 궤적을 모두 사람 라벨과 함께 제공하므로, 성공 궤적에 유형 매칭 주입 → 자연 실패와 짝 비교가 바로 가능.
- **D(grounding 분류기 vs 도구 관측)**: Kovács 2607.00895가 단일 관측·합성 라벨에서 이미 수행. 남는 것은 *멀티턴 궤적 + 사람 라벨*에서 off-the-shelf NLI baseline. AgentProcessBench/AgentRx의 도구 오해석·날조 라벨로 가능하나 해당 유형 표본이 적을 수 있음.

### 수정된 추천
**C를 주축으로 하고 G2(step-level 오탐)를 결합**한다. 한 문장 주제: *"주입 벤치마크는 얼마나 믿을 수 있고, 스텝 단위 탐지기는 정상 궤적에서 얼마나 오류를 지어내는가 — 매칭 태스크 보정 연구와 주입 파이프라인"*.
- 데이터: AgentProcessBench(사람 스텝 라벨, 4개 환경)에서 (a) 자연 실패 세트, (b) 같은 태스크의 성공 궤적에 유형 매칭 주입한 세트, (c) 미주입 성공 궤적(정상 세트).
- 탐지기: Qwen3-8B judge(holistic / step-wise / self-consistency) + 규칙 prefilter. 필요 시 Qwen3-4B로 규모 효과.
- 지표: 자연 vs 주입 정확도 격차(보정 계수), 정상 궤적 오탐률(culprit step 날조율), 유형별 격차, 비용.
- 제출물: 주입 파이프라인 + 정상/주입/자연 3분할 벤치마크 프로토콜 + 결과. 과제문의 "벤치마크 데이터셋 및 파이프라인" 요건과 "탐지 모델" 요건을 모두 충족.
- 왜 이것인가: 유일하게 "아무도 안 했다"를 정밀하게 방어할 수 있고, 사람 라벨 데이터로 이틀 안에 실제 숫자가 나오며, 결과가 "합성 벤치마크로 탐지기를 검증하는 모든 제품·연구"에 바로 쓰이는 보정 계수라 제품화 함의가 명확하다.

B는 handoff에 강한 흥미가 있을 때의 대안. 이 경우 합성 생성기는 버리고, TraceElephant/Who&When의 실제 handoff 구간 30~50개를 이중 책임 스키마로 재주석하는 "파일럿 벤치마크 + 주석 프로토콜"로 축소해야 방어 가능.
