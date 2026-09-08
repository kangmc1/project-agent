# 실패 유형별 빈도 증거 모음 (2026-09-08, arXiv 본문/그림에서 직접 추출)

## 출처별 표
**MAST (2503.13657; 1,642 traces, 7 MAS)**: FC1 시스템 설계 43.8% (task spec 불복 11.8, 역할 불복 1.5, 스텝 반복 15.7, 기록 손실 2.8, 종료 인지 실패 12.4) / FC2 에이전트 간 불일치 32.4% (대화 리셋 2.2, 명확화 질문 실패 6.8, 과제 이탈 7.4, 정보 은폐 0.85, 입력 무시 1.9, 추론-행동 불일치 13.2) / FC3 검증 23.5% (조기 종료 6.2, 검증 없음 8.2, 잘못된 검증 9.1). 과제 실패율: MetaGPT 60%, ChatDev 66.7%, HyperAgent 74.7%, AppWorld 86.7%, AG2 41%, Magentic-One/GAIA 62%.

**TRAIL (2505.08638; 841 errors, 148 traces)**: 형식 오류 23.4%, 지시 불이행 18.5%, 환각 12.6%(언어 53/도구 53), 목표 이탈 7.7%, 자원 남용 6.8%, 오케스트레이션 5.8%, 문맥 처리 5.8%, 도구 선택 5.4%, 검색 부실 4.9%, 문제 오식별 3.3%, 도구 출력 오해석 2.0%, 시스템 3.7%. 그룹: Reasoning ≈70%, Planning/coordination ≈26%, System 3.7%. 영향 high 36.1%.

**AgentRx (2602.02475; 170)**: 도구 출력 오해석 20.5~34.1%, 지시/계획 불이행 18.2~33.3%, 의도 미명세(τ-bench) 33.3%, 정보 날조 2.6~17.8%, 가드레일 차단(Magentic-One) 20.5%, 시스템 실패(Flash) 14.3%.

**AgentErrorBench (2509.25370; 200)**: Planning 39% (비효율 계획 48, 불가능 행동 16, 제약 무시 14), Reflection 19.5%, Memory 19% (과단순화 22, 환각 13), Action 11%, System 11%. 오류는 6~15스텝에 집중. (본문은 memory/reflection 지배라고 쓰나 그림은 planning 최다.)

**Who&When Pro (2607.09996; 12,326 주입)**: 빈도는 설계값. 발견: judge step acc 69~74%이나 joint ≤25%; planning/verification/coordination 오류가 reasoning으로 오분류되는 경우 다수.

**TELBench (2606.02060; deep research, 2,790 궤적 중 67.7% 오류 보유)**: 첫 오류 family — evidence grounding 34~45%, constraint handling 26~36%, search/retrieval 8~16%, information processing 1~14%, entity mapping 7~10%, process control 1~4%. 탐지기 F1 50~55%, 첫 오류 21~24%.

**TraceElephant (2604.22708; 220)**: 책임 에이전트 — Captain-Agent web 49% / orchestrator 19% / verification 17% / data 15%; Magentic-One web 62% / orchestrator 29% / data 9%; SWE-Agent code-editing 79% / command 18% / orchestrator ~3%. 결정적 스텝은 Magentic-One·SWE에서 초반 집중.

**AgentHallu (2601.06818; 693, 63.9% 환각)**: Reasoning 17.0%, Tool-use 14.9%(잘못된 인자 36, 누락 도구 32, 불필요 도구 23), Retrieval 11.8%, Human-interaction 10.5%, Planning 9.7%. 탐지 41.1%, tool-use 11.6%.

**OpenClawBench (2605.29253; 31,264)**: anomaly 14.7%; 하위 — capability-gap overcommitment ≈52%, 미해결 모호성 하 쓰기 ≈34%, 기타 ≈14%. oracle-pass 중 9.33%가 process anomaly; high-risk oracle-pass의 92.7%가 anomaly.

**τ-bench/τ²**: gpt-4o pass^1 retail 61.2 / airline 35.2, pass^8 <25%. 실패 — 잘못된 인자/정보 누락 ~50%, 규칙 위반 ~25%, 복합 요청 부분 완료 ~19%. τ² dual-control 시 ~20pt 하락; 사용자 시뮬레이터 오류율 16~47%.

**프로덕션**: Catching One in Five (2606.10315; F&B 주문 에이전트 291 transcripts, 30 결함 패턴): 상태 추적 27%, 지식/도구 27%, 브랜드 톤 23%, 복구/안전 13%, 가드레일 10%; LLM judge 게이트가 9개 중 2개, 이후 23개 중 0개 포착. Klarna: 2024-02 2.3M 대화/700 FTE → 2025-05 "품질 저하"로 사람 재고용. LangChain State of Agents 2024(N>1,300): 51% 프로덕션, 최대 장벽 품질(>2배); 2025(N=1,340): 57% 프로덕션, 품질 32%, 보안 24.9%(엔터프라이즈), 지연 20%, 89% 관측성 보유. Gartner 2025-06: 2027년까지 agentic 프로젝트 40%+ 취소 [unverified]. MIT NANDA 2025: 파일럿 95% P&L 무영향, 원인은 "learning gap"(메모리·적응 부재). 산업 MAS 환각 감사(2605.24219): 225 궤적 68.3% 환각, procedural 38.5%.

**조정/handoff 특정**: MAST FC2 32~37%이나 엄격한 에이전트 간 모드(2.1+2.2+2.4+2.5)=11.75%; TraceElephant orchestrator 19~29%(MAS), 3%(SWE); TRAIL orchestration 5.8%+context 5.8%; AgentAsk 824 edge errors — signal corruption 36.8%, data gap 29.1%, referential drift 27.3%; Constraint Weakening: 통상 압축 시 blocker 100% 비활성화·금지 행동 54.2%, 4필드 구조화 시 0%; Facts Without Rules: 마커 생존 0.80→0.57(25단어 예산).

## 종합
- 단일 에이전트 도구 사용: 인자/형식/지시 오류(τ-bench ~50%, TRAIL 42%) → 도구 출력 오해석·근거 부족(AgentRx 20~34%, TELBench 33~45%) → 계획(AgentErrorBench 39%). 시스템 ≤4~14%.
- 멀티에이전트: worker 측 관찰(web/code) 49~79%; 오케스트레이션/조정 12~37%(정의에 따라); 검증 17~24%; 가드레일 차단 최대 20.5%.
- 프로덕션 고객 응대: 턴 간 상태 추적 27%, 지식/도구 27%, 브랜드/정책 33%; judge가 결함의 75%+ 놓침; 사업 차원 이탈은 통합·학습 격차.
- 대략적 귀속: 관찰/도구 35~60%(MAS) / 20~45%(단일); 추론/계획 25~40%; 검증 17~24%; 시스템 4~14%; 에이전트 간 조정/handoff 엄격 ~12% ~ 넓게 ~30%(MAS), 단일 ~0. 단 handoff 압축 실험은 발생 시 제약 거의 전부 손실.
- 주의: 단위 상이(다중 라벨 vs 결정적 스텝 vs 결함 패턴), MAST는 대부분 LLM 주석, Who&When Pro는 설계 빈도, AgentErrorBench 본문·그림 불일치, taxonomy 중첩.
