# 산업 현장의 멀티에이전트 배치와 handoff 동인 (조사 2026-09-08, 벤더 페이지 직접 확인 기준)

(vendor) = 벤더 자체 주장, [unverified] = 미확인.

## A. 산업별 배치
| 산업 | 제품 | 에이전트 분업 | 규모 | 출처 |
|---|---|---|---|---|
| 고객지원 | Sierra (Agent OS 2.0, Horizon) | supervisor + 결정/응답 에이전트, 수일~수주 걸친 inbound/outbound 오케스트레이션, 사람 이관 지표 | >$150M ARR (vendor) | sierra.ai |
| 고객지원 | Decagon | Agent Operating Procedures, 채널 간 메모리, Proactive Agents | $4.5B 밸류(2026-03), Chime 70% 해결 (vendor) | decagon.ai |
| 고객지원 | Intercom Fin | Fin AI Engine + Procedures, 헬프데스크로 사람 이관 | 12,000+ 고객사, 주 2M 해결 (vendor) | fin.ai |
| 고객지원 | Salesforce Agentforce | "Multi-Agent Orchestration", 사람 에스컬레이션 | 18,000+ 기업 (vendor) | salesforce.com |
| 고객지원(KR) | 채널톡 ALF | 에이전트 + 사람 이관 | 129만+ 상담 해결 (vendor) | channel.io |
| 코딩 | Claude Code subagents | 서브에이전트마다 자체 문맥 창·도구·권한, "요약만 반환", 모델 티어링(haiku), 동시 20개 | — | code.claude.com/docs/en/sub-agents |
| 코딩 | Cognition Devin 2.0 | 의도적 단일 스레드; 병렬은 독립 Devin 여러 개; Devin Wiki 메모리 | — | cognition.com |
| 코딩 | OpenAI Codex cloud, GitHub Copilot coding agent, Cursor cloud agents(2026-08 서브에이전트 VM "clean context"), Google Jules, AWS Kiro | 과제별 격리 샌드박스 병렬, 사람 리뷰·승인 게이트 | Jules 140k+ 개선 (vendor) | 각 문서 |
| 리서치 | Anthropic 멀티에이전트 리서치 | lead가 3~5 서브에이전트 병렬 생성, 각자 압축된 결과 반환, 200k 초과 시 plan을 Memory에 저장 | 토큰 15배, 단일 대비 +90.2% (vendor eval) | anthropic.com/engineering |
| 리서치 | OpenAI Deep Research, Gemini Deep Research | 단일 에이전트 순차 탐색(서브에이전트 없음) | — | 각 문서 |
| 엔터프라이즈 | Microsoft Copilot Studio | child agent(문맥 공유) vs connected agent(자체 오케스트레이션, context-inclusion 설정), 도구 30~40개 넘으면 분할 권고, A2A 연결 | — | learn.microsoft.com |
| 엔터프라이즈 | UiPath Maestro, Workday Agent Gateway | BPMN으로 에이전트·로봇·사람 오케스트레이션; 에이전트 레지스트리·권한·미터링 | — | 각 사이트 |
| 의료 | Hippocratic AI (Polaris) | 주 에이전트 + 전문 지원 모델 constellation, 간호사 에스컬레이션 | 250M+ 상호작용, 31K+ 에스컬레이션 (vendor) | hippocraticai.com |
| 의료 | Abridge | 방문 전/중/후 파이프라인, 임상의 검토 | 300+ 병원, 연 100M+ 대화 (vendor) | abridge.com |
| 보안/IT | Microsoft Security Copilot agents, CrowdStrike Charlotte AI("multi-agent architecture"), Datadog Bits AI SRE(가설 생성·검증 → on-call 이관) | 제품 표면별 에이전트, 승인 게이트 | Charlotte 98%+ triage (vendor) | 각 사이트 |
| 영업 | 11x | SDR 에이전트 → CRM으로 사람 인계 | — | 11x.ai |
| KR | Samsung SDS Brity Copilot(50만+ 임직원), Upstage Solar Pro 4(KB, IBK, AIA), Coxwave(에이전트 평가·모니터링; 고객 Anthropic 표기; 2025-12 OpenAI 멀티에이전트 해커톤) | — | 각 사이트 |

프로토콜/프레임워크: A2A 2025-04 출시 50+ 파트너 → 2025-06 Linux Foundation 100+ 지지사. MCP 10,000+ 서버, 2025-12 Agentic AI Foundation. CrewAI 월 450M+ 워크플로(vendor). Microsoft Agent Framework(2025-10) sequential/concurrent/handoff/group-chat/magentic 패턴. OpenAI Agents SDK handoff 기본은 전체 기록 전달, `nest_handoff_history`(beta)로 압축.

## B. handoff가 많아지는 동인과 경계를 넘는 것
| 동인 | 배치 예 | 전체 기록 vs 압축 |
|---|---|---|
| 문맥 창 초과·compaction | Anthropic Research(200k 초과 시 Memory), Claude Code 95%에서 auto-compact, tool result clearing | **압축(손실)** |
| 긴 도구 루프 | Manus 과제당 평균 ~50 도구 호출, 파일시스템을 복원 가능한 압축으로 사용 | 복원 가능 오프로드 |
| 도구·지식 특화 | Copilot Studio 30~40 액션 넘으면 분할 | child=전체, connected=설정에 따름 |
| 권한·최소권한 | Claude Code 서브에이전트별 tools/permissionMode | 요약 반환 |
| 병렬 fan-out/in | Anthropic Research 3~5 서브에이전트, Cursor clean-context VM, Codex 샌드박스 | **압축**(1~2k 토큰 요약) |
| 사람 에스컬레이션 | Hippocratic→간호사, Fin/Zendesk/Sierra 사람 이관, Jules/Copilot 승인 | 대개 전체 티켓 |
| 벤더 간 A2A | Copilot Studio A2A, Workday Agent Gateway | task/message + artifacts |
| 비용 계층화 | Claude Code haiku 서브에이전트, Intercom Apex Flash | 요약 |
| 직무 분리·규제 | Copilot coding agent: 할당자는 승인 불가; 감사용 별도 transcript | ID로 연결된 별도 로그 |
| CS 턴 경계 | OpenAI SDK triage→refund/billing handoff | 기본 전체 기록, nesting 시 압축 |
| 세션 간 메모리 | Decagon 채널 간 메모리, Devin Wiki, Anthropic memory tool | 요약 노트 |

반론(Cognition, "Don't build multi-agents"): "전체 trace를 공유하라, 메시지 조각만 공유하지 말라"; "행동에는 암묵적 결정이 실려 있고 상충하는 결정은 나쁜 결과를 낳는다"; 문맥 초과의 답은 병렬 에이전트가 아니라 전용 압축 모델. Claude Code 문서도 서브에이전트는 대화 기록 없이 시작하고 요약만 반환한다고 명시.

결론: handoff가 구조적으로 많은 배치는 (a) 병렬 fan-out 리서치/코딩 오케스트레이터, (b) 도구 분할 엔터프라이즈 오케스트레이터, (c) 대량 CS + 사람 이관. (a)(b)에서 handoff는 거의 항상 압축된 요약이며 그곳이 정보가 사라지는 지점.
