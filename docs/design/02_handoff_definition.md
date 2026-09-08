> **상태(2026-09-08 15:45)**: 방향 확정 전 작성. 정의와 스키마는 유효하며 `docs/proposal.md`에서 인용. 연구 주장은 `proposal.md`가 대체함.

# Handoff의 정의 (v1, 2026-09-08)

## 1. 정의

**에이전트 간 handoff**란, 한 에이전트 S(송신자)가 만든 명시적 산출물 A가 다른 에이전트 상태 R(수신자)의 **입력 문맥을 구성**하고, 그 뒤 R이 S보다 먼저 **하나 이상의 결정**을 내리는 사건이다.

h = (S, R, t, C_S, A, I_R, B_R)
- C_S: t 시점에 S가 보고 있던 전체 문맥 (S의 입력 프롬프트)
- A: S가 R을 향해 만든 산출물 (지시문, 상태 요약, 위임 과제 등)
- I_R: R의 실제 입력 문맥. I_R ⊇ A. I_R과 C_S의 차이가 **정보 비대칭**이다.
- B_R: 다음 handoff까지 R이 내린 결정과 행동

handoff 실패는 C_S에 있던 의무 o가 B_R에서 지켜지지 않았고, 그 원인이 (i) A의 결함(소실·약화·변조), (ii) R의 결함(무시·이탈·거짓 보고), (iii) 라우팅 결함(잘못된 수신자·불필요한 handoff) 중 하나로 귀속되는 경우다.

## 2. 세 조건이 각각 배제하는 것

| 조건 | 배제되는 것 | 이유 |
|---|---|---|
| A가 **명시적 산출물** | 공유 대화록만 있고 S가 R에게 쓴 메시지가 없는 경우 | 무엇이 "넘어갔는지"를 특정할 수 없음 |
| R이 A로 **입력 문맥을 구성**하는 LLM 에이전트 | 코드 실행기(ComputerTerminal), 검색 API 등 도구 호출 | 도구는 해석·결정을 하지 않음. 도구 호출 실패는 tool-use failure로 별도 범주 |
| R이 **결정을 내림** | S가 사람에게 최종 답을 보고하는 것 | 사람은 시스템 밖. 별도 범주(final answer) |

## 3. 정보 비대칭에 따른 유형

| 유형 | 산출물 A | I_R vs C_S | 우리 데이터 | 산업 예 |
|---|---|---|---|---|
| **H1 지시 handoff (공유 대화록)** | 지시문 | I_R ≈ C_S (공유 기록 전체 + 지시). 비대칭은 S의 사적 추론(ledger)뿐 | Magentic-One 1,228건 | AutoGen GroupChat, Magentic-One |
| **H2 지시 handoff (새 문맥)** | 위임 과제 설명 | I_R = A (+ 시스템 프롬프트). 비대칭 큼 | 없음 (로드맵) | OpenAI Agents SDK `input_filter`, Claude 서브에이전트, A2A task |
| **H3 압축 handoff (context reset)** | 상태 요약 (facts + plan) | I_R = A. 원본 C_S는 폐기됨. 비대칭 완전 | Magentic-One 75건 | Magentic-One outer loop, 장기 실행 에이전트의 context compaction, 세션 간 메모리 |
| **H4 반환 handoff** | R의 보고 | S의 문맥에 추가됨 | 모든 H1의 B_R 안에 포함 | 모든 위임의 결과 반환 |
| **H5 화자 선택 (group chat)** | 다음 화자 이름만 | 공유 기록 | Captain-Agent 85 run (미사용) | AG2 GroupChatManager |

정리:
- H1에서 실패는 **정보 소실이 아니라 지시의 질**로 나타난다(제약을 실행 시점에 명시했는가, 수신자가 맞는가, 지시에 실린 사실이 맞는가). 수신자는 원문을 볼 수 있으므로 S1(소실)보다 S3(변조)·S4(수신자)·R1/R2가 주된 결함이다.
- H3에서는 A가 유일한 통로이므로 S1·S2·S3 모두 가능하고, 결함은 복구 불가능하다 → 눈덩이의 출발점.
- H4는 별도 이벤트로 세지 않고 H1의 B_R 안에서 R3(거짓 보고)로 잡는다. 이유: 반환의 결함은 다음 H1의 S3 씨앗이 되며, 두 방향을 각각 세면 하나의 오류가 두 번 세어진다.
- H2는 우리 데이터에 없다. 그러나 H3와 비대칭 구조가 같으므로(I_R = A), H3에서 검증한 계약 검사기는 H2에 그대로 적용된다. 산업이 가는 방향이 H2라는 점이 이 연구의 확장 근거다.

## 4. 데이터에서의 조작적 정의 (Magentic-One / TraceElephant)

- **H1 이벤트** = 오케스트레이터의 ledger 출력(`next_speaker`, `instruction_or_question`). S = Orchestrator, R = next_speaker, A = instruction, C_S = 그 ledger 호출의 입력 메시지, B_R = 다음 ledger까지의 R 스텝 + R의 보고. 제외: R ∈ {None, terminate, MagenticOneOrchestrator(자기 자신), ComputerTerminal(실행기)}.
- **H3 이벤트** = ledger 입력 메시지 수가 직전 ledger보다 줄어드는 지점. S = Orchestrator(reset 직전 상태), R = reset 이후의 팀 전체(오케스트레이터 자신 포함), A = 갱신된 fact sheet + plan(= reset 후 messages[0]), C_S = reset 직전 대화록 전체, B_R = reset 이후 스텝들.
- TraceElephant의 `agent_name`은 ledger 스텝에 직전 화자를 기록하므로 내용으로 판별한다.

## 5. 관련 연구에서의 용어 대응
- OpenAI Agents SDK: handoff = `transfer_to_<agent>` 도구 호출, 기본은 전체 기록 전달, `input_filter`로 H2화.
- Google A2A: task 객체를 다른 에이전트에 위임 = H2.
- AgentAsk(2510.07593): "inter-agent message handoff"에서의 error propagation; edge-level 주석 = H1/H4의 메시지 결함.
- Bound-Handoff(2608.29028): "handoff artifact"로 upstream 상호작용을 압축 = H3.
- Constraint Weakening(2608.24569): summaries/tickets/handoff notes 등 중간 산출물 = H3.
- Handoff Debt(2606.02875): 다른 에이전트가 작업을 이어받음 = H2/H3.
- MAST(2503.13657): "loss of conversation history", "information withholding" = H3의 S1; "ignored other agent's input" = R1.

## 6. 파일럿에 반영할 결정
1. ComputerTerminal을 수신자로 하는 88건은 H1에서 제외(도구 호출로 재분류). 파일럿 세트에는 포함되어 있지 않음(선택 시 WebSurfer/Coder/FileSurfer/ComputerTerminal 허용 → ComputerTerminal 제거 필요).
2. H4는 별도 세지 않음. 라벨 R3로 흡수.
3. 문서에서 handoff 유형을 H1/H3로 명시하고 결과를 유형별로 분리 보고.
