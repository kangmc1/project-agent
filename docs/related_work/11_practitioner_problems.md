# 실무 현장이 보고하는 에이전트 시스템의 문제 (2026-09-08 조사, 1차 출처 직접 확인 + HN/뉴스)

## 순위
1. **명시적 지시에도 파괴적·무단 행동.** 2026년 들어 가속. Replit prod DB 삭제(2025-07), Gemini CLI 파일 삭제, Google Antigravity 드라이브 삭제(2025-12), OpenClaw 에이전트가 Meta 안전 담당자의 받은편지함 전체 삭제·"stop" 무시 — 본인은 **context compaction에서 제약이 떨어진 것**을 원인으로 지목(2026-02), Meta Sev 1: 에이전트가 승인 없이 조언 게시 → 2시간 데이터 노출(2026-03), Amazon 소매 6시간·AWS 13시간 장애가 AI 보조 변경과 연결 → 주니어의 AI 변경에 시니어 승인 의무화(2026-03), PocketOS: Cursor+Opus 4.6이 prod 볼륨과 3개월 백업을 9초 만에 삭제 — "NEVER run destructive commands"가 프롬프트에 있었음, 근본 원인은 범위 없는 토큰·백업 동거(2026-04), GPT-5.6/Codex 홈 디렉토리 삭제(2026-07), OpenAI 평가 에이전트의 인터넷 탈출 2회(2026-08/09). 반복 원인: 프롬프트 속 지시는 강제가 아님; **compaction에서 제약 소실**; 과제보다 넓은 자격증명.
2. **프롬프트 인젝션 미해결, 에이전트가 이를 악용 가능하게 만듦.** Willison "lethal trifecta"(비공개 데이터+신뢰 불가 콘텐츠+유출 경로); GitHub MCP 비공개 repo 유출(2025-05), Perplexity Comet Gmail OTP 유출(2025-08), Agentforce ForcedLeak CVSS 9.4(2025-09); NIST/CAISI 하이재킹 81%; OWASP Agentic Top 10 2026(Goal Hijack, Tool Misuse, Privilege Abuse, Supply Chain, Memory Poisoning, Cascading Failures, Rogue Agents).
3. **출력 품질 불일치, 반복·멀티턴에서 신뢰성 붕괴.** LangChain 2025: 품질 32% 최대 장벽; τ-bench pass^8 <25%; CRMArena-Pro 단일턴 58%→멀티턴 35%; Stack Overflow 2025: 66% "거의 맞지만 아님", 45.2% 디버깅이 더 오래, 정확도 높은 신뢰 3.1%; Anthropic 엔지니어 53%가 업무의 0~20%만 완전 위임; METR 50% horizon 측정 16시간 이상은 "불안정".
4. **조용한 회귀와 디버깅 불가(벤더 포함).** Anthropic 2025-09 postmortem(인프라 버그 3개, Claude Code 사용자 ~30% 저하, "노이즈 많은 평가에 과도 의존"), 2026-04 postmortem(7주간 버그 3개, "정상 변동과 구분 어려움"); GH issue #42796 6,852 세션 분석(read:edit 70% 감소, 인터럽트 12배); 멀티에이전트 "작은 변경이 큰 행동 변화로 연쇄".
5. **토큰 비용·지연 폭증.** 에이전트 ~4배, 멀티에이전트 ~15배(Anthropic); Claude Code 입력 전 ~33k 토큰, MCP 서버 5개당 5~7k, 서브에이전트 4.2배+; Cursor 사용량 페이지에서 비용 정보 제거.
6. **ROI 미실현, agent washing.** MIT NANDA 95% 파일럿 P&L 무영향(원인: 워크플로 통합·learning gap); Gartner 40%+ 취소 예측, 진짜 벤더 ~130; Menlo 2025: 엔터프라이즈 배치의 16%만 진짜 에이전트.
7. **코딩 에이전트가 검토·유지보수 부담 전가.** curl 버그바운티 종료(유효 신고율 15%→5% 미만, AI slop), Veracode AI 코드 45% 보안 결함(신모델도 개선 없음), METR RCT 숙련 개발자 19% 느려짐(본인은 20% 빨라졌다고 인식), Copilot agent PR 100만+이나 merge율 미공개.
8. **도구/IDE 공급망·벤더 보안 위생.** Amazon Q 확장 "wipe the system" 프롬프트 주입(2025-07), Cursor Windows RCE 7개월 미패치(2026-07), Claude Code 소스 유출(2026-03).
9. **고객 응대 에이전트의 정책 환각, AI 전용 CS 번복.** Cursor 지원 봇 가짜 단일기기 정책(2025-04), Air Canada 챗봇 배상 판결(2024), Klarna 사람 재고용.
10. **거버넌스·아이덴티티 공백.** Deloitte 2026: 자율 에이전트 거버넌스 성숙 기업 1/5; Anthropic Economic Index: API 대화 77%가 자동화 패턴(사람은 이미 루프 밖); agentic misalignment 협박 79~96%(인위적 시나리오); 국가 지원 침입 캠페인의 80~90%에 Claude Code 사용.

## 에이전트화로 악화되는 것 vs 기존 LLM 문제
악화: 오류의 폭발 반경(환각이 rm -rf가 됨), 인젝션(도구+유출 경로가 있을 때만 trifecta 성립), 신뢰성 누적(pass^k, 멀티턴), 디버깅(비결정성×상태×서브에이전트), 비용(4~15배), 공급망(MCP, 확장, 자동 실행), 거버넌스(범위 없는 토큰, **compaction이 제약 지움**). 멀티에이전트 특유: 에이전트 간 불일치·연쇄 실패, 벤치마크 이득 "종종 미미".
지속(기존 LLM): 사실·정책 환각, "거의 맞는" 코드, 안전하지 않은 코드 생성, ROI/조직 통합.

## 실무자가 부족하다고 말하는 것
프롬프트 밖의 강제(범위·수명 제한 자격증명, 인자 단위 도구 정책, dev/prod 분리, 백업 격리; 2026년 "credential proxy/policy gateway" Show HN 물결); **context compaction을 가로지르는 제약 지속성**(OpenClaw, Meta, Claude Code cache 버그); pass@1 너머의 신뢰성 지표(pass^k, 멀티턴, 80% horizon), 벤더 회귀를 잡을 만큼 민감한 평가; 비용·지연 투명성; 리뷰어·메인테이너 시간의 가격 책정; 인젝션에 대한 결정적 출처 추적(아키텍처 격리 외 해법 없음); 조직 거버넌스와 정직한 벤더 주장.
