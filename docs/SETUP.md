# 실험 환경 정의 v1 (2026-09-08 18:10)

이 문서가 시스템 정의의 기준이다. 코드(`src/agent_handoff/workflow/`)와 어긋나면 코드가 틀린 것이다.
이전 결과는 모두 폐기했다(2026-09-08 17:55, 세팅 오류: 출처가 모든 역할에 공유되어 있었음).

## 1. 데이터: 시나리오 20개 (`data/scenarios/scenarios.jsonl`)
| 필드 | 내용 | 누가 보는가 |
|---|---|---|
| `task` | 사용자 요청 1문단. 제약 ≥2, 금지 1 포함 | 모두 |
| `transcript` | 300~580단어의 합성 작업 기록. 어떤 팀이 도구로 알아낸 것처럼 쓰여 있음(확인된 사실 ≥3, 미해결 질문 ≥2) | **Researcher만** (private source) |
| `obligations` | 정답 라벨 8개: constraint 2, verified_fact 3, open_question 2, prohibition 1. 각각 key_values(날짜·금액·이름·ID) | 아무도 못 봄 (채점용) |

도메인: scheduling 6, research 6, coding 5, customer_support 3. 모델이 만든 기록이므로 사실의 참·거짓은 재지 않는다. 재는 것은 "기록에 있던 정보가 경계를 거쳐 살아남는가"뿐이다.

## 2. 역할과 정보 비대칭
모두 같은 모델(Qwen3-8B, vLLM), 시스템 프롬프트만 다르다. 외부 도구·world 시뮬레이션은 없다.

| 역할 | 하는 일 | 보는 것 |
|---|---|---|
| Orchestrator | 매 라운드 다음 에이전트·행동 유형·대상·지시문 결정, 압축, 최종 답 | task + state + 행동 이력 + 최근 보고 4개 |
| Researcher | 출처에서 지시된 항목의 사실·조건을 정확한 값과 함께 보고. 없으면 `UNAVAILABLE in context` | task + state(+보고) + **출처 원문** |
| Executor | state·보고만으로 구체 행동 초안. 값이 없으면 `MISSING: <what>` | task + state(+보고) |
| Verifier | 초안을 state의 제약·금지·사실과 대조, PASS/FAIL/CANNOT VERIFY, `VERDICT: APPROVE|REVISE` | task + state(+보고) |

- state는 처음에 "아직 확립된 것 없음" 한 줄이다. 사실은 Researcher의 보고를 통해서만 팀에 들어온다.
- 가시성 변수: `shared` = state + 마지막 압축 이후 보고 전부, `summary` = state만. Researcher는 둘 다에서 출처를 추가로 본다.
- 실제 시스템과의 대응: Researcher의 출처 = worker만 갖는 도구 결과·문서. Executor/Verifier가 출처를 못 보는 것 = 오케스트레이터가 worker의 사적 문맥을 못 보는 것.

## 3. 행동 공간과 분포
- 행동 = 다음 에이전트 선택 {Researcher, Executor, Verifier, finish} (4지선다). 그 뒤 에이전트별 행동 유형(Researcher: lookup_fact|resolve_open_question, Executor: draft_action|revise, Verifier: verify_claim), 그 뒤 자유 서술 대상·지시문.
- 분포는 vLLM `guided_choice` + 첫 토큰 `top_logprobs`로 한 번에 읽는다(샘플링 없음). 두 번 잰다: (a) state만 보고 잰 정책 분포 `p_agent`/`entropy_agent`, (b) 짧은 평가문 뒤의 실제 결정.
- 반복 방지 마스크: 같은 (에이전트, 유형, 유사 대상) 2회 연속 → 그 에이전트 제외; UNAVAILABLE로 보고된 대상을 Researcher에게 다시 묻는 결정 → Executor 초안으로 전환. 마스크 적용 여부는 로그에 남긴다.

## 4. 압축 (오케스트레이터의 호출 하나, 별도 에이전트 아님)
- 트리거: 마지막 압축 이후 대화록(지시+보고) 단어 수 > 예산. 출처는 대화록에 포함되지 않으므로 압축 대상이 아니다(출처는 압축돼도 사라지지 않는다. 손실을 알아채면 Researcher에게 다시 물어 복구할 수 있다).
- 포맷: `free`(구역 4개 자유 서술) | `json`(constraints/verified_facts/open_questions/prohibitions/goal, 항목 status).
- 압축 후: state = 새 요약, 대화록·보고 목록 모두 폐기. 에이전트도 오케스트레이터도 원본을 다시 볼 수 없다.
- 가드(`guard`): 압축 직전 팀이 실제로 갖고 있던 항목(task + 대화록에서 preserved) 중 압축 후 absent/altered/promoted가 된 것만 재삽입한다. 한 번도 획득되지 않은 항목은 건드리지 않는다(정답을 Researcher 우회로 흘리지 않기 위함). 문구는 정답 라벨을 쓰므로 **상한(oracle) 개입**이다.

## 5. 경계와 측정
| 경계 | 송신 → 수신 | 넘어가는 것 | 재는 것 |
|---|---|---|---|
| B0 선정 (확장) | 카탈로그 → 팀 구성 | 후보 에이전트·스킬 | required_capabilities 누락률 |
| B1 지시 | Orchestrator → Agent | (유형, 대상, 지시문) + 가시성 | (B2·B3 결과로 관측) |
| B2 반환 | Researcher → 팀 | 보고 | **획득**: 출처에만 있던 의무가 보고에 preserved로 처음 등장(`acquired`). 보고 속 날조 값. Verifier의 근거 없는 PASS |
| B3 압축 | Orchestrator(t) → 팀(t+1) | 새 state | 압축 직전 갖고 있던 항목 대비 손실률 `b3_loss_rate`(absent/altered/promoted), 정책 JSD(압축 전후 분포), 가드 복구 수 |
| B4 최종 | Orchestrator → 사용자 | final | 제약 보존, 금지 위반(부정어 인식), 승격, 날조 값, `lost_after_acquired`(획득됐는데 최종에서 사라짐) vs `never_acquired` |

최종 손실은 두 갈래로 나뉜다: **획득 실패**(Researcher를 안 부르거나 보고가 누락) vs **전달 손실**(획득 후 압축·초안·최종에서 사라짐). 이 벤치마크의 주 대상은 후자다. 전자는 별도로 보고한다.

## 6. 변수와 그리드 (미확정, §8 결정 후)
시나리오 20 × 가시성 {shared, summary} × 포맷 {free, json} × 예산 {?} × 가드 {0, 1} × 폭 1. 예산은 출처가 대화록에서 빠졌으므로 다시 잡아야 한다(보고 1건 ≈ 100~200단어).

체인 스트레스(`chain/stress.py`)는 역할 없이 출처를 K번 연속 압축하는 B3 전용 통제 실험이다. 세팅 변경의 영향을 받지 않는다.

## 7. 프로브 (D3)
입력: 압축 직전 라운드의 [p(4), 엔트로피, 상위 1·2위 차, 라운드, 단어 수, JSD]. 라벨: 그 압축에서 `lost_ids`가 비어 있지 않은가(갖고 있던 것 중 하나라도 손실). 로지스틱 회귀, 시나리오 단위 5-fold.

## 8. 미결 사항 (사용자 결정 필요)
1. **오케스트레이터가 Researcher를 부르지 않는 문제.** 스모크 1회(scheduling_00, shared/json/600): 1라운드부터 Executor에게 초안을 시켰고(p: Researcher 0.30, Executor 0.58), Executor는 호텔·요금·예약을 전부 지어냈으며(최종 날조 값 7개), Verifier는 "handoff state에서 확인됨"이라며 전부 PASS를 줬다. 출처 속 사실 5개 중 획득 0. 선택지:
   - (a) 그대로 둔다. 이것 자체가 P1(날조)+P3(근거 없는 검증)이며 `never_acquired`로 보고된다. 단, 매 실행이 이러면 전달 손실은 측정되지 않는다.
   - (b) 오케스트레이터 규칙을 강화한다("팀은 Researcher 보고 전에는 아무 사실도 모른다. 초안 전에 사실을 모아라"). 기준 시스템을 합리적으로 만들고, 그래도 안 부르면 `never_acquired`로 보고. **권장.**
   - (c) 1라운드를 Researcher lookup으로 고정한다(실제 시스템의 계획/조사 단계). 가장 확실하지만 정책 분포의 1라운드 값을 잃는다.
2. **예산 값.** 보고 기준으로 {200, 400, 800} 정도가 압축 0~4회를 만든다. 스모크로 확인 후 확정.
3. **Verifier의 검증 능력.** 지금은 출처를 못 보므로 사실은 CANNOT VERIFY만 가능하다(제약·금지는 task로 검증 가능). 이대로 두면 "근거 없는 PASS"가 곧 측정값이 된다. 대안: Verifier에게 출처의 읽기 전용 접근을 주는 변형(실제의 fact_verifier 도구에 해당)을 확장 변수로 둔다.
4. **폐기한 결과 관련 문서 수정.** `docs/proposal.md` §4.2 예비 결과는 비웠다. 매처 검증(`scripts/validate_matcher.py`)은 세팅과 무관하므로 다시 돌려 채운다.
