> **상태(2026-09-08 15:45)**: 방향 확정 전 작성. 정의와 스키마는 유효하며 `docs/proposal.md`에서 인용. 연구 주장은 `proposal.md`가 대체함.

# 방향 확정: handoff 경계에서의 오류 눈덩이(snowball) 탐지 (2026-09-08 12:00)

## 사용자의 문제의식 (원문 요지)
1. 에이전트 상호작용/작업 과정의 아주 사소한 오류가 눈덩이처럼 굴러 작업물이 이상해지는 현상
2. 이 오류를 발견하는 방안
3. 상호작용이 무한히 이어져도 내용이 깨지지 않는 방안
4. task-specific 버전 / task를 모를 때 적합한 task를 판단하는 모듈 / general 버전
5. 해법은 아직 모름

## 조사 결과와의 대응
- (1) 눈덩이 = error cascade. 근거: Scaling Agent Systems(2512.08296) 독립 에이전트 오류 17.2배 증폭; From Spark to Fire(2603.04474) 단일 주입 오류 6개 MAS 프레임워크에서 전파; AgentProp-Bench(2604.16706) 파라미터 오류→오답 p≈0.62; AgentAsk(2510.07593) "inter-agent message handoff에서의 error propagation"; Constraint Weakening(2608.24569) "must→maybe" 약화.
- (2) 탐지 = G3 잔여 빈틈. 실제 궤적 + 유형 + 송신/수신 이중 책임 + 인과 라벨 조합 없음.
- (3) 무한 상호작용 견딤 = 불변량(invariant) 보존. 각 handoff에서 의무(obligation)가 보존되면 귀납적으로 임의 길이 체인에서 보존. 탐지기(2)가 곧 경계 가드. 단 Intervention Paradox(2602.03338): 개입이 해칠 수 있음 → 비용 측정 필요.
- (4) task-specific = 도메인별 의무 스키마; general = 문맥에서 의무를 추출하는 추출기; task 판단 모듈 = 스키마 선택 라우터(Routed Graph Handoff 2608.25277의 라우터와 유사 발상).
- (5) 후보 해법 = "handoff 계약(contract)": 의무 목록 추출 → 인수인계 산출물에서 생존 판정(보존/약화/소실) → 수신자 이행 판정(이행/무시) → 책임(송신/수신/양측) → 하류 실패 인과.

## 통합 연구 객체: handoff contract
handoff 이벤트 h = (송신자 문맥 C_s, 인수인계 산출물 A, 수신자 행동 B_r)
- O(C_s): 의무 집합 (사용자 제약, 도구가 알려준 사실, 미해결 질문, 권한/금지)
- surv(o, A) ∈ {preserved, weakened, absent}
- adh(o, B_r) ∈ {honored, ignored, n/a}
- resp(o) ∈ {sender-drop, receiver-ignore, both, none}
- causal(o) ∈ {caused downstream failure, did not, unclear}
불변량: ∀o∈O(C_s): surv=preserved ∧ adh=honored. 체인 h_1..h_K에서 매 단계 불변량이 성립하면 K에 무관하게 내용 보존.

## 벤치마크 3층
- A. 실제 궤적 파일럿(책임 귀속): TraceElephant(220, CC BY 4.0, 전체 입력/도구 로그) + Who&When(184)에서 handoff 구간 추출, 40~60건 라벨(LLM 초안 + 사람 검수).
- B. 통제 주입(누락 탐지): 실제 인수인계 산출물에서 의무 1개를 소실/약화시키고 (C_s, A')만 주어 탐지. 재실행 불필요, 정답 확실.
- C. 다단 전달 체인(눈덩이·무한 상호작용): 로컬 모델로 K-hop 요약/인수인계 체인 생성, 심어둔 의무의 생존 곡선 측정. 가드 없음 vs 계약 검사기 + 복구 비교. 사용자의 (1)(3)을 직접 시연.

## 탐지기
- D0 규칙: 산출물에 의무 키워드/값 존재 여부
- D1 holistic judge: 전체를 주고 "무엇이 잘못됐나"
- D2 contract checker: 의무 추출 → 생존 → 이행 → 책임 (Qwen3-8B)
- 지표: 소실 의무 재현율, 책임 귀속 정확도, 인과 정밀도, K-hop 생존 곡선, 메모 길이 예산별 붕괴, 가드 비용(토큰/지연)

## 기존 연구 대비 차별점 (3차 검증 기준으로만 주장)
AgentAsk: 송신 메시지 결함만, 수학/코드, 미공개. Bound-Handoff: 프라이버시 마커, 합성, trace 인과 없음. Constraint Weakening: 안전 차단 조건만, 합성. Handoff Debt: 비용만. → 본 제안: 일반 작업 의무 + 실제 궤적 + 이중 책임 + 인과 + 다단 체인 생존.

## 이틀 산출물
스키마/분류체계, 주석 프로토콜, A 파일럿 라벨, B 주입 파이프라인, C 체인 생성기, D0~D2 탐지기, 3층 결과표, 제안서. (3)(4)는 결과 + 기대효과/로드맵으로 서술, C로 소규모 시연.
