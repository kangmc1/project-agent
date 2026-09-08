# Handoff 계약 스키마와 실패 분류체계 (v1, 2026-09-08)

## 0. 데이터에서 확인한 handoff의 두 유형 (TraceElephant / Magentic-One, 91 runs)

| 유형 | 정의 | 건수 | 압축 여부 | 실패 라벨과의 관계 |
|---|---|---|---|---|
| **I. 지시 handoff** | 오케스트레이터 ledger → `next_speaker`에게 `instruction_or_question` 전달 | 1,228 (run당 중앙값 13) | 없음. 수신자는 공유 대화록 전체(과제, 팀, 이전 지시와 보고)를 본다 | 결정적 실수가 지시 스텝에 찍힘 40건, 수신 구간 안 82건 |
| **II. 재계획 handoff (context reset)** | 정체 시 오케스트레이터가 갱신된 사실 목록 + 새 계획을 쓰고 **대화록을 지운 뒤** 그 요약만으로 재시작 | 75 (40 runs) | **있음**. 중앙값 10,891 토큰의 기록 → 약 1,300자 사실 목록 + 계획 | 결정적 실수가 reset 이전 59건 / 요약 단계 2건 / 이후 14건 |

함의: 유형 I의 실패는 정보 소실이 아니라 **지시의 질**(제약을 실행 시점에 명시했는가, 올바른 수신자인가, 잘못된 사실을 지시에 실었는가)과 **수신자 이탈**의 문제다. 유형 II는 진짜 압축 경계이며, 요약에 잘못 굳어진 사실은 원본이 지워져 복구 불가능하다 → 눈덩이의 출발점. 59/75에서 실수가 reset 전에 있었다는 것은 "틀어진 상태가 사실로 굳어 넘어간" 사례가 대부분임을 뜻한다(가설; A층에서 검증).

## 1. 연구 객체

handoff 이벤트 h = (C_s, A, B_r)
- C_s 송신자 문맥: 산출물을 만들 때 송신자가 본 모든 것 (유형 I: ledger 입력 메시지; 유형 II: reset 직전 대화록 전체)
- A 산출물: 유형 I = 지시문 + 수신자 지정; 유형 II = 갱신된 사실 목록 + 새 계획
- B_r 수신자 행동: 다음 handoff까지의 수신자 스텝(도구 호출, 보고)

## 2. 의무(obligation) — 계약의 단위

O(C_s) = 송신자 문맥에 존재하며 하류가 지켜야/알아야 하는 항목의 집합.

| 유형 | 정의 | 예 |
|---|---|---|
| `constraint` | 과제가 명시한 조건 (단위, 기간, 형식, 범위) | "3 decimal places", "less than 2 hours", "as of 20/10/2020" |
| `fact` | 이전 스텝에서 **검증된** 정보 | "IMDb 페이지 URL은 …", "release 102 archive에 GFF3 존재" |
| `open_question` | 아직 확인 안 된 것으로 표시된 항목 | "release 101과 102 중 어느 것이 2020-10 기준인지 미확인" |
| `goal` | 현재 하위 목표 | "각 영화의 러닝타임과 평점을 표로 모을 것" |
| `prohibition` | 금지/권한 | "do not use sudo", "50 rounds 이내" |

각 의무는 `{id, type, text, source}`이며 source ∈ {task, prior_step:<n>, team_config}.

## 3. 라벨

### 3.1 의무 단위
- `survival(o, A)` ∈ {preserved, weakened, absent, corrupted, n/a}
  - weakened: 필수 조건이 선택/참고로 약화("must"→"may", 조건 일부 탈락)
  - corrupted: 산출물에 **틀린 값**으로 실림 (유형 II에서 핵심: 미확인 추측이 "verified fact"로 승격)
  - n/a: 이 handoff의 하위 목표와 무관
- `adherence(o, B_r)` ∈ {honored, violated, n/a}

### 3.2 handoff 단위 (다중 라벨)
| 코드 | 이름 | 정의 | 실데이터 근거 |
|---|---|---|---|
| S1 | sender_drop | 필요한 의무가 산출물에서 소실 | 유형 II 요약에서 사실 탈락 |
| S2 | sender_weaken | 의무가 약화되어 전달 | Constraint Weakening의 must→maybe와 동일 현상 |
| S3 | sender_corrupt | 틀린/미확인 내용이 사실로 전달 (stale state 포함) | "release 102" 굳힘; "잘못된 연도의 시즌권 가격 사용" |
| S4 | sender_wrong_recipient | 능력이 맞지 않는 수신자 선택 | "PDF 전문가 대신 웹 검색 전문가 선택", "DB 전문가 대신 웹 연구 전문가" |
| S5 | sender_unnecessary | 불필요/우회 handoff | "FileSurfer 대신 직접 Python으로 읽었어야", "상식으로 될 일을 조사" |
| R1 | receiver_ignore | 산출물에 있는 의무를 수신자가 무시 | 지시는 "러닝타임 확인"인데 확인 안 함 |
| R2 | receiver_deviate | 지시와 다른 행동 / 범위 이탈 | "무관한 사이트 클릭" |
| R3 | receiver_false_report | 수신자가 결과를 과장/날조해 보고 (다음 handoff의 S3 씨앗) | "OCR 결과가 틀렸는데 정상 보고" |
| N0 | none | 결함 없음 | |

### 3.3 책임과 인과
- `responsibility` ∈ {sender, receiver, both, none} — S* 만 있으면 sender, R* 만 있으면 receiver
- `causal` ∈ {caused_failure, contributed, no_effect, unclear} — 이 handoff의 결함이 run 실패(또는 TraceElephant의 결정적 실수)로 이어졌는가
- `snowball_depth`: 결함이 처음 생긴 handoff부터 실패가 확정된 스텝까지의 handoff 수 (유형 II를 지나면 +표시)

## 4. 불변량과 "무한 상호작용" 주장의 형태
Inv(h) ≡ ∀o ∈ O(C_s) with survival ≠ n/a: survival(o, A) = preserved ∧ adherence(o, B_r) = honored.
체인 h_1 … h_K에서 ∀k Inv(h_k)이면 의무 집합은 K에 무관하게 보존된다(귀납). 검사기 D2는 Inv(h)를 판정하는 함수이며, 위반 시 복구(누락 의무 재삽입)를 시도할 수 있다. 개입 비용(토큰, 지연)과 오개입(Intervention Paradox)을 함께 잰다.

## 5. 세 층의 데이터 규격
- **A층 (실제, 책임 귀속)**: 유형 I 40건(결정적 실수가 지시 스텝에 찍힌 것) + 유형 II 20건 우선. 각 건에 §3 라벨. LLM 초안 → 사람 검수.
- **B층 (통제 주입, 누락 탐지)**: 유형 II의 (pre_reset_transcript, facts_text)에서 의무 1개를 소실/약화/변조한 facts_text' 생성. 입력 (C_s, A'), 정답 = 조작한 의무. 유형 I에서는 지시문의 제약 삭제/약화.
- **C층 (다단 체인)**: 로컬 모델로 "기록 → 사실 목록 요약 → 다음 라운드 기록 → 재요약"을 K회 반복. 심어둔 의무의 생존 곡선. 가드 없음 vs D2+복구.

## 6. 문맥 예산
Qwen3-8B 16k. 유형 I 송신 문맥 중앙값 6,949 토큰(p90 19k), 유형 II reset 직전 중앙값 10,891 토큰(max 36k). 렌더링 시 과제·팀·최신 사실목록·최근 보고 N개 우선, 오래된 보고는 요약/절단. 절단 비율은 기록해 G5 잔여(압축 문맥에서의 탐지 붕괴) 분석에 사용.
