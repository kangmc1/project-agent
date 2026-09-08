# 반증 논문 본문 정독 결과 (2026-09-08, 3차 검토)

목적: 2차 검증에서 "해소/부분 해소" 판정의 근거가 된 논문들의 *본문*이 실제로 그 빈틈을 채우는지 확인. 인용 실재 여부는 arXiv abs 페이지 18편 직접 조회로 선확인(모두 실재, 초록 일치).

## OpenClawBench (2605.29253) — G2 관련
- 라벨: **전부 LLM 생성**(DeepSeek 계열 silver judge). 사람 감사 300개(모두 oracle-pass)에서 96.0% 일치(288/300), κ 미보고. §6.3 "All FullTax labels are LLM-generated."
- 실패 성격: 자연 발생, 주입 없음(A.2).
- 정상 비율: detector split 26,503 (train 23,857 / test 2,646), anomaly 14.7% → test 정상 ≈2,258.
- **step/span 지표: 정의만 있고(F.8 onset exact match, step-distance, span IoU; F.9 "false-alarm on non-anomalous" 권고) 결과는 전무.** 보고된 것은 trajectory-binary만(Table 2: Gemma-3-12B zero-shot P 0.290, GPT-5.4 P 0.289 / PredAnom 41.6% vs base rate 14.7%, LoRA P 0.660).
- 탐지기: Gemma 3 12B(zero-shot), GPT-5.4, Gemma 3 12B+LoRA. Qwen 없음.
- 주입 vs 자연 비교 없음. 공개: CC-BY-4.0(익명 4open.science), 단일 에이전트 BFCL 함수 호출.
- **결론: G2 step-level은 유지.** OpenClawBench는 "정상 궤적에서 step localizer가 오류 위치를 지어내는 비율"을 측정하지 않았고, 정상 라벨 자체가 LLM silver.

## Real-Time Detection and Repair (2608.02464) — G1 관련
- §9: T=0.9 비주입 에피소드 30개 → 자연 실패 11개(silent abort 7, fabricated count 3, ungrounded blend 1). 통계 모니터가 fabrication 3개 중 1개만 탐지, within-organic AUROC 0.31–0.42. 재현 55 에피소드에서는 후보 환각 2개만.
- **LLM judge(gemini-2.5-flash)는 주입 데이터 161 프롬프트에서만 평가**, organic split에는 미적용.
- 전이 격차를 명시적으로 주장하나("transfer only weakly to organic"), 시뮬레이터 텔레메트리라 배포 주장은 없음.
- 공개: github/HF `sunnydubey1111/agent-trajectory-sentinel`, 2,823 에피소드, MIT.
- **결론: G1 정밀 서술 유지.** "LLM judge/localizer, 매칭 태스크, 자연 실패 ≥100" 조건을 만족하는 비교는 여전히 없음. 유일한 직접 증거는 자연 실패 11개·통계 모니터·단독 저자.

## AgentProcessBench (2603.14465, KDD 2026) — 추천 방향 C의 토대, 실현성 확인
- 구성: 4 환경 × 250 = 1,000 궤적, 8,509 스텝. 성공/실패(Table 2): HotpotQA 161/89, GAIA 83/167, BFCL 102/148, τ² 126/124. 정책 모델 5개(Qwen3-4B, Qwen3-30B-A3B, DeepSeek-V3.2, GPT-5-mini, GPT-5) × 태스크 50개/환경 → **같은 태스크에 성공·실패 궤적이 모두 존재(매칭 태스크 설계 가능)**. JSONL의 `sample_index` 0–4가 모델을 가리키는 듯하나 매핑 미명시.
- 라벨: 스텝별 +1/0/−1 + final_label. 전문가 2인 독립 주석, IAA 89.1%, κ 0.767. **오류 유형 라벨 없음**(±1/0만). 첫 오류 스텝은 첫 −1로 도출 가능. 전파 규칙: 오류에 의존하는 후속 스텝도 −1.
- 실패 성격: 실제 환경에서의 자연 rollout, 주입 없음.
- 공개 내용: OpenAI 스타일 messages(**tool role에 원시 도구 출력 포함**), `tools`(함수 스키마), `tool_metrics`, `step_labels`, `final_label`. **실행 환경은 미공개** → 재실행 불가, 오프라인 편집만 가능.
- 지표: StepAcc(마이크로), FirstErrAcc(−1 없으면 error-free로 간주). **성공 궤적/+1 스텝에 대한 precision/FPR 미보고**; 정성적으로 "+1 과예측" 언급만(Fig. 6). 성공 궤적 중 −1 포함: 17/163, 17/83, 32/91, 27/123 → 완전 정상(−1 없음) ≈ 146/66/59/96.
- 기준선(Table 3, StepAcc/FirstErrAcc): Qwen3-4B 55.9/38.9, Qwen3-8B 57.1/40.7, Qwen3-8B-Thinking 63.2/46.0, Qwen3-30B-A3B-Thinking 68.5/52.0, GPT-5.2 74.8/61.1, Gemini-3-Flash-Thinking 81.6/65.8. 프로토콜: **궤적 전체를 한 번에 넣고 모든 스텝 라벨을 JSON으로 출력**, 단일 실행, self-consistency 없음.
- Judge 실패 테마(App. D): 정보 오류 간과, 논리 오류 간과, 도구 호출 오류 간과, 과잉사고로 정답 스텝 오판, 중립 스텝 경계 모호.
- 라이선스: HF 카드 MIT, GitHub LICENSE 없음. 약 40MB. `hf.co/datasets/LulaCola/AgentProcessBench`.
- **실현성 판단**: (a) 유형 매칭 주입은 유형 라벨이 없어 자체 정의 필요; 환경 재실행 불가라 주입은 텍스트 편집 + 하류 도구 출력 위조 또는 주입 스텝 이후 절단 방식이어야 함(아니면 judge가 오류가 아니라 불일치 흔적을 잡을 위험). (b) 매칭 태스크는 충분(완전 정상 성공 궤적 146/66/59/96). (c) 정상 궤적에서 judge가 −1을 찍는 비율은 논문 미보고 → 즉시 얻을 수 있는 새 숫자. 주요 리스크: GAIA 성공 83개로 적음, 유형 라벨 부재.

## AgentForesight (2605.08715) — G5
- 라벨: 사람 주석 없음. 주입 스트림 + LLM 합의(제안 5회/검증 3회, 과반) 스트림. judge 모델 미명시. 사람 검증 subset·κ 미보고.
- 멀티에이전트 전용(AutoGen, MetaGPT, Smolagents; GPT-5.4-mini 백본).
- FAR = safe 궤적 중 alarm이 1회라도 난 비율; deployable region FAR ≤20% & Step-Acc ≥50%. **지연은 보고됨**(7B 1.03s/call vs DeepSeek-V4-Pro 25.77s).
- 데이터: "supplementary materials"에 포함, 다운로드 URL·라이선스 미명시.

## CatchBench (2608.22808) — G5
- 단독 저자(USC), "work in progress", 비심사.
- LIVE 보드: SWE-Gym 376 run, τ-bench 660 run; 라벨은 코퍼스의 *태스크 결과* 라벨(스텝 라벨 아님). stale-state 보드는 주입(82 pairs)이며 자체 human-validation 기준 미충족.
- ROC-AUC per prefix: SWE-Gym 0.742/0.766/0.804/0.804; τ-bench 0.632–0.665 ("no early warning"). TPR@5%FPR은 stale-state 보드만(0.122). 지연 미보고. 요약/절단 prefix 없음(raw growing prefix만).

## AgentAsk (2510.07593) — G3
- 824 로그, 메시지 단위 주석, "multiple professional annotators", Fleiss κ 0.84. 주석자 수·코퍼스 공개 URL 미명시.
- 라벨은 *송신 메시지*의 결함(DG/RD/SC/CG). 수신자 행동은 서술만, 라벨 없음. sender/receiver 책임 라벨 없음.
- 태스크: GSM8K, MATH, MMLU, HumanEval, MBPP(GPTSwarm/AFlow/MaAS/MasRouter). 도구 사용·엔터프라이즈 에이전트 없음.

## Bound-Handoff / Facts Without Rules (2608.29028) — G3
- 범위: **프라이버시 누출 특화**("summary collapse"). 태스크 성공은 부차 지표.
- 합성: 손으로 쓴 36 시나리오 × 4 surface × 5 조건 = 720셀; GPT-5-mini, DeepSeek-R1-32B, Qwen3-32B. PrivacyLens 493 trace 외부 점검. 코드 공개(EMNLP 2026).
- 마커 단위 생존 점수(σ_b 4단계)는 있으나 **trace 단위 인과 라벨은 없음**; 인과는 별도 매칭 실험으로만.

## Trajel (2605.24219) — G7
- 탐지기: BERT(subtask) AUC 0.613, 일반 NLI 정식화(trajectory) 0.689, Longformer 0.599, LLM judge F1 0.855. NLI 체크포인트 미명시. MiniCheck/HHEM/LettuceDetect/AlignScore 미평가.
- 225 궤적, 기관 2곳, 궤적당 사람 리뷰어 1명; κ 0.456은 LLM-vs-human. 사람 간 일치 미보고. **아직 미공개**(acceptance 후 CC BY 4.0 예정).

## Beyond Document Grounding (2607.00895) — G7
- 도구 출력 subset 라벨: Qwen 3.6 35B가 생성한 합성 편집; 사람 리뷰는 코드 split만(2,038). **도구 출력 사람 리뷰 0건.**
- 단일 관측(query + 도구 관측 1개), "not full agent trajectories" 명시.
- 도구 출력(n=617) span-F1: LettuceDetect-Qwen-2B 0.719, mmBERT 0.588, gpt-oss-120b 0.331. **LettuceDetect-large(0.172), HHEM-2.1, MiniCheck-7B는 코드 에이전트 split에서만 평가, 도구 출력에서는 미평가.**

---

## 3차 검토 최종 판정표

| # | 2차 판정 | 3차(본문 기준) 판정 | 근거 요약 |
|---|---|---|---|
| G1 | 부분 해소(약) | **유지에 가까움** | 유일한 직접 증거(2608.02464)는 자연 실패 11개·통계 모니터·단독 저자; LLM judge는 주입 데이터에서만 평가 |
| G2 (step) | 유지 | **유지** | OpenClawBench는 step 지표를 정의만 하고 결과 0건; 라벨 전부 LLM; AgentProcessBench도 성공 궤적 FPR 미보고 |
| G3 | 부분 해소 | **부분 해소(범위 축소)** | AgentAsk는 송신 메시지만·수학/코드만·미공개; Bound-Handoff는 프라이버시 특화·합성·trace 인과 라벨 없음 |
| G4 | 유지 | 유지 | (3차 미검토, 2차 근거 충분) |
| G5 | 해소 | **부분 해소로 하향** | AgentForesight 라벨 LLM 합의·멀티에이전트·데이터 URL 없음; CatchBench 단독 저자·비심사·스텝 라벨 없음; 둘 다 요약/절단 prefix 없음 |
| G6 | 부분 해소 | 부분 해소 | (초록 기준 재확인: REFLECT 연구 에이전트만, AgentJudgeBench 도구 DAG만, BabelJudge 단독 저자·7B 1개) |
| G7 | 부분 해소 | **부분 해소(범위 축소)** | BDG는 단일 관측·합성·MiniCheck/HHEM은 도구 출력 미평가; Trajel은 RAG 분류기 미평가·미공개 |
| G8 | Align 유지 / 벤더 절반 해소 | 유지 | (3차 미검토) |

교훈: 2차 검증 에이전트는 초록·검색 스니펫 수준에서 반증을 과대평가하는 경향이 있었다(특히 G5 "해소"). 제안서에는 3차 표의 서술만 사용.
