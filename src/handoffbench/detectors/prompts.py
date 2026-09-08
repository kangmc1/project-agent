"""Prompt templates for handoff-contract checking (D2) and holistic judging (D1)."""

SYSTEM = (
    "You are an expert auditor of multi-agent LLM systems. You analyse handoffs between agents: "
    "the SENDER's context, the ARTIFACT the sender passes on, and the RECEIVER's subsequent behaviour. "
    "Be precise, cite short evidence (never more than 20 words per quote; never reproduce long lists or tables), and reply with ONLY a JSON object."
)

OBLIGATIONS = """We are auditing one handoff. Below is the TASK and everything the SENDER could see (its context) when it produced the handoff artifact.

Extract the OBLIGATIONS: items in the sender's context that any downstream agent must respect or know in order to solve the task correctly. Types:
- constraint: a condition stated by the task (units, dates, formats, ranges, "as of", "less than", output structure)
- fact: information that has been VERIFIED earlier in the transcript (from a tool result or page content)
- open_question: something the transcript explicitly marks as unresolved / not yet verified / a guess
- goal: the current sub-goal that must be pursued next
- prohibition: forbidden actions or hard limits (e.g. no sudo, round limits)

Rules:
- 4-10 obligations, ordered by importance for solving THIS task. Skip generic environment boilerplate (today's date, OS version, "do not use sudo", round limits) unless the task itself depends on it.
- constraint: only task-specific conditions (dates/"as of", numeric thresholds, units, required sources, output format demanded by the user).
- fact: only information actually VERIFIED by a tool result or page content in the transcript; quote it. Mark the verification status.
- open_question: assumptions the current plan is relying on that were NOT verified (e.g. "we assumed release X is the right archive"), or explicitly unresolved items.
- Each obligation is one short self-contained statement. Do not invent obligations that are not in the context.

=== TASK ===
{task}

=== SENDER CONTEXT ===
{sender_context}

Reply with JSON: {{"obligations": [{{"id": "o1", "type": "constraint|fact|open_question|goal|prohibition", "text": "...", "evidence": "short verbatim quote (max 20 words) or 'task'", "verified": true|false}}]}}"""

SURVIVAL = """We are auditing one handoff. The SENDER compressed its knowledge into the ARTIFACT below, which is ALL the downstream agents will rely on for the next actions.
For each obligation, decide how it survived in the ARTIFACT:
- preserved: fully and correctly present (explicitly or by unambiguous implication)
- weakened: present but softened (a requirement became optional/vague; part of the condition dropped)
- absent: not present at all
- corrupted: present but WRONG or OVERSTATED (a value/date/name changed; an open_question / unverified assumption is now stated as a verified fact; a "should verify" became "verified")
- n/a: irrelevant to what this artifact is for (only use for goals/facts that clearly do not matter for the next actions)

=== TASK ===
{task}

=== OBLIGATIONS ===
{obligations}

=== ARTIFACT ===
{artifact}

Additionally, AUDIT the artifact: list every statement the artifact presents as an ESTABLISHED / VERIFIED fact (e.g. items under "GIVEN OR VERIFIED FACTS", or asserted without hedging in the plan), and check each against the sender context: supported (a tool result/page in the context confirms it, or it is given by the task), unsupported (the context only assumed/guessed it, or never mentions it), contradicted (the context shows otherwise).
Do NOT audit items the artifact itself marks as unverified: anything under "FACTS TO LOOK UP", "FACTS TO DERIVE", "EDUCATED GUESSES", or hedged with may/might/possibly/likely. Those are not claims.

Reply with JSON: {{"survival": [{{"id": "o1", "status": "preserved|weakened|absent|corrupted|n/a", "evidence": "short quote (max 20 words) or 'none'"}}], "artifact_claims": [{{"claim": "...", "status": "supported|unsupported|contradicted", "evidence": "short quote (max 20 words) or 'none'"}}]}}"""

ADHERENCE = """We are auditing one handoff. Given the obligations and the ARTIFACT that the receiver was given, judge the RECEIVER's behaviour.
For each obligation: honored (receiver's actions respect it), violated (receiver's actions CONTRADICT it: used a wrong date/unit/source/value, did the forbidden thing, or explicitly skipped a required check), n/a (nothing the receiver did was related to it).
Failing to finish the task, being slow, or hitting website/tool errors is NOT a violation.
Also flag receiver-level problems: deviate (the receiver pursued a different goal or target than the artifact asked for, e.g. clicked an unrelated site, changed the question), false_report (reported success/data that its own actions do not support). Tool/website failures are not deviation.

=== TASK ===
{task}

=== OBLIGATIONS ===
{obligations}

=== ARTIFACT (what the receiver was given) ===
{artifact}

=== RECEIVER BEHAVIOUR ===
{receiver_behavior}

Reply with JSON: {{"adherence": [{{"id": "o1", "status": "honored|violated|n/a", "evidence": "max 20 words"}}], "receiver_deviate": true|false, "receiver_false_report": true|false, "notes": "one sentence"}}"""

HOLISTIC = """We are auditing one handoff between agents in a multi-agent system.

=== TASK ===
{task}

=== SENDER CONTEXT (what the sender knew) ===
{sender_context}

=== ARTIFACT (what the sender passed on) ===
{artifact}

=== RECEIVER BEHAVIOUR (what happened next) ===
{receiver_behavior}

Decide whether this handoff is faulty. Fault codes (multi-label):
S1 sender_drop (a needed obligation is missing from the artifact), S2 sender_weaken (requirement softened), S3 sender_corrupt (wrong/unverified content passed as fact), S4 sender_wrong_recipient, S5 sender_unnecessary (handoff not needed / detour), R1 receiver_ignore (obligation present in artifact but ignored), R2 receiver_deviate, R3 receiver_false_report, N0 none.

Reply with JSON: {{"faults": ["S1", ...] or ["N0"], "responsibility": "sender|receiver|both|none", "dropped_or_corrupted_items": ["..."], "explanation": "2-3 sentences with evidence (max 80 words)"}}"""
