## Batch 1 — labeler notes (airline_008, airline_018, aime_002, aime_008, aime_014)

- **airline_008 (failed).** Two unrecovered events; `decisive_step = 2` by the rubric's "earliest unrecovered
  error on the path to the failure". Step 2 (planner delegates the balance lookup with no user id) is earliest, but
  step 3 (db_agent claims the tools cannot reach gift-card/certificate balances and fires `transfer_to_human_agents`,
  which ends the episode) is the proximate cause. The escalation was **not** justified: `get_user_details` was in the
  db_agent's tool list and the policy puts payment methods in the user profile; the customer never asked for a human,
  which the transfer tool's own description requires. If the rubric is later read as "most proximate unrecovered
  cause", the decisive step for this run becomes 3.
- **Successful runs with unrecovered events (airline_018 steps 10 and 30).** `derive_step_classes` maps an
  unrecovered, non-decisive event in a run with `decisive_step = null` to `clean`, so these genuinely erroneous steps
  are scored as clean. They are recorded as events anyway (faithfulness to the observed trace); flagging here in case
  the class derivation should grow a "harmless unrecovered" class.
- **aime_002 (succeeded).** 27 events: 5 fabricated `run_python` outputs (steps 3-7 report explicit enumerations for
  calls whose stdout was empty because the code ended in a bare expression) and the steps 14-35 degeneration, where
  the byte-identical 708-char call is re-issued 21 times with verbatim-identical text after the same TypeError.
  Each repetition is labeled individually so that the loop steps are not scored as `clean`.
- Not labeled (deliberately conservative): fabricated clause numbers that carry a correct verdict
  (airline_018 step 18 cites "Policy clause 5.3"; the policy is unnumbered but the quoted text and verdict are right);
  redundant but harmless re-queries (airline_018 step 14 re-asks db_agent for values already in the step-4 report);
  first-attempt tool failures that are genuine debugging (aime_002 steps 12-13).

## Batch 1 — labeler notes (airline_002, airline_010, airline_021, aime_004, aime_010)

- **airline_010 (failed) — decisive_step = 9, not 7.** Step 7 (planner drops the passenger "Ethan Lopez" that
  db_agent had just reported and answers only about "Ethan Johnson") is an earlier unrecovered event, but it is not
  on the path to the failure: the customer had already pre-committed to the cancel-and-rebook fallback in their very
  first turn, and passenger removal is impossible under the policy anyway ("cannot modify the number of passengers").
  The scored failure is the cancellation of H9ZU1C (economy, `insurance: no`, `created_at 2024-05-01`, i.e. outside
  the 24-hour window and without insurance) ordered at step 9 with no `policy_checker` call — that agent is never
  invoked in this run. Under a "first unrecovered event, full stop" reading the decisive step would be 7.
- **airline_002 (failed) — decisive_step = 19.** The whole task hinges on economy fares that
  `search_direct_flight` / `search_onestop_flight` return; the db_agent never calls either tool in 69 steps, and
  answers five separate requests with `get_reservation_details` alone. Steps 22 and 54 relabel the business fares as
  economy prices (identical numbers), which is why the planner told the customer at step 55 that both cabins cost
  the same.
- **aime_004 (succeeded).** All four events are marked recovered at step 9: the planner discarded the verifier's 274
  and the step-8 garbage and submitted the solver's original 70. Step 7 is labeled `handoff` because the re-solve
  delegation carries no problem statement, which is what lets step 8 "assume a hypothetical problem".
- Not labeled (deliberately conservative): `read_file` on a not-yet-existing `/case_notes.md` (airline_021 step 7,
  airline_002 step 12) — the db_agent prompt tells it to read the file first, and the miss is handled; db_agent
  executing the planner's cancellation instruction (airline_010 step 10), since that subagent is given no policy
  text; planner steps that faithfully relay an erroneous subagent report (airline_002 steps 34/55/65).

## airline_003 (labeler note)
The run fails on three independent counts (return legs never moved off 2024-05-28; a slower-than-available
itinerary chosen; nonfree_baggages=1 charged although silver+economy allows 2 free bags; payment on
gift_card_7091239 $157 instead of the smallest-balance gift_card_7480005 $6). Per the rubric I set
`decisive_step` to the earliest unrecovered event on a path to the failure — step 10, the planner's
context-free policy_checker delegation that never got resolved (need_info at 12 and again at 16), which is
why the baggage allowance was never established. The flight-selection errors at 22/24/25/27 are equally
causal but later, so they derive as cascade.

## airline_013 (labeler note)
Successful run (reward 1.0) that reaches the right end state for the wrong reason: the planner accepted a
modification the policy_checker had declared `not_allowed` (basic economy) and invented a $50 change fee, but
every write attempt was rejected by the environment ("flight HAT030 not available on date 2024-05-13") and the
db_agent's self-initiated transfer_to_human_agents happened to be the graded action. Events at 15/17/19/31 are
therefore unrecovered but not decisive; `decisive_step` is null as required for a successful run.
  Following that same convention I dropped airline_003 step 32 (planner repeats db_agent's step-30 success and
  "smallest balance" claims verbatim; the planner never saw the raw reservation record).

## airline_006 / airline_017 / aime_001 / aime_007 / aime_013 (labeler note)
Convention used for `decisive_step` in these five failed runs: the earliest **unrecovered** event that is a
but-for cause of the observed failure; events whose corrupted value is later discarded without being corrected
stay `recovered: false` but are not made decisive.
- **aime_001 (failed, gold 277, submitted None) — decisive_step = 7.** Solver and verifier both returned 277; the
  only defect is that the planner's last turn is the text "Submitted 277." with no `submit_answer` call.
- **aime_007 — decisive_step = 2.** The solver's cycle-type enumeration is wrong at step 2 (276) and wrong again,
  differently, at step 8 (296, submitted). Step 8 is a re-derivation, not a correction, so step 2 is not marked
  recovered; it is the first unrecovered error on the chain (wrong 276 -> verifier disagreement -> re-solve -> 296).
  Step 7 (re-delegation that omits the verifier's objection) and step 5 (verifier counts a 4+2 cycle type, whose
  order 4 does not divide 6) are equally real but later / off the submitted path, so they derive as cascade.
- **aime_013 — decisive_step = 3.** Two independent sufficient causes: the solver never produced an answer
  (steps 3-7 resubmit byte-identical timing-out code) and the planner never called `submit_answer` (step 11,
  "Submitted 502."). I set the earliest, step 3; step 11 is recorded as its own unrecovered event.
- **airline_006 — decisive_step = 4.** No reservation was ever identified. The planner asks for a reservation id,
  a passenger name and a booking channel but never for the user id, and delegates five id-less lookups; the
  db_agent answers each by inventing a user id (`sara_doe_496`, then `aarav_garcia_123` four times). Step 4 is the
  first delegation that no db tool could execute.
- **airline_017 — decisive_step = 43.** Chosen over the earlier unrecovered events at 35/36 (the fabricated
  "$1400 one-leg upgrade", a dead end the customer moved past) because step 43's fabricated "$440 (220 + 220)"
  is the value the customer accepted at step 45 and the itinerary the agent then tried to book; it is the first
  unrecovered corruption carried into the final outcome. The later steps 67-69 (update_reservation_flights that
  drops both return legs of a round_trip, a returned reservation that is unchanged, and a "successfully updated,
  $440 already processed" message to the customer) are the visible failure but derive as cascade.
- Not labeled (deliberately conservative): the policy_checker's correct 5-7 business days answer in airline_006
  step 32 (matches the policy clause, only the VERDICT format is missing); airline_017 step 26/32, where the
  db_agent reports the tool's business fares faithfully and the "upgrade cost" framing comes from the planner's
  own instruction; planner turns that relay a subagent report without altering it (airline_006 step 7,
  airline_017 steps 33/38/44); aime_013 step 2, the first brute-force attempt that timed out.

## Spot check (main-session independent annotator, 6 runs) — 2026-09-09 03:05
decisive_step exact agreement 6/6 (100%); event-step Jaccard 0.56 (second annotator's events were a strict subset: did not
label repeated emissions / downstream uses). Resolution: RUBRIC §5b fixes the recall-oriented convention (repeats count);
batch-1 labels kept as is; batch 2 labeled under the same rule. Files: labels/spotcheck/*.json, agreement.json.

## Batch 2 — labeler notes (airline_029, airline_039, airline_048, aime_021, aime_027)

Convention used for `decisive_step` throughout: the earliest **unrecovered** event that is a *but-for* cause of the
observed failure (same reading as the airline_006/017 batch). Earlier unrecovered events that only explain part of a
failure that would have happened anyway are recorded but not made decisive; the three cases are spelled out below.

- **airline_029 (failed, reward 0.0) — decisive_step = 12, not 7.** Gold for task 29 is reads only: nothing is
  cancellable. UDMOP1 is basic_economy, `insurance: "no"`, `created_at 2024-05-09` (outside 24 h); 4XGCCM's segments
  are 2024-05-03/04, i.e. already flown at the policy's current time 2024-05-15. Step 7 (db_agent calls 4XGCCM
  "upcoming") is earlier and unrecovered, but it is only a but-for cause of the *second* bad write — UDMOP1 would have
  been cancelled regardless, so reward would still be 0. The but-for cause of the failure is step 12: the planner
  orders both cancellations with no `policy_checker` call at all (that agent is never invoked in this run) and without
  ever asking the reason for cancellation. Note also that the db_agent has no clock: its system prompt contains no
  current date, which is why step 7's "upcoming" claim is labeled `reasoning_like` (unsupported conclusion) rather
  than made decisive. Step 13 (db_agent executing the cancellations) is not labeled, following the airline_010
  convention that this subagent is given no policy text.
- **airline_039 (failed, reward 0.0) — decisive_step = 8, not 7.** The customer's real reason (a friend's birthday)
  is neither a health nor a weather reason, so the insurance "condition" is not met and the basic-economy reservation
  (created 2024-05-03) cannot be cancelled; gold is `get_reservation_details` only. Step 7 is labeled (the planner's
  delegation omits the cancellation reason and `created_at`), but it is not a but-for cause: the planner never had the
  reason — it never asked — and adding `created_at` alone would not have flipped a checker that ignores the second
  conjunct of the clause. Step 8 is the decisive step: the policy_checker quotes "only if travel insurance is bought
  **and the condition is met**" and then concludes "allowed" from the insurance flag alone. Step 13's "$104 refund
  already processed" is *not* labeled — the cancel_reservation result really does contain
  `{"payment_id": "credit_card_4196779", "amount": -104}`.
- **airline_048 (failed, reward 0.0) — decisive_step = 9.** The date change is correctly refused (step 8 VERDICT
  not_allowed for basic economy), but the planner then invents the cancel-and-rebook remedy at step 9 on its own
  authority; the customer asks to cancel only in response. EUJUY6's first two segments are dated 2024-05-14 and are
  already flown at 2024-05-15, so the trip is not cancellable at all ("cannot help and transfer is needed"). The run
  then dies at step 24, where the planner writes the `respond_to_user` call out as literal `<tool_call>` text and hits
  the token limit (finish_reason `length`), so no tool call is made — labeled as its own `tool` event. Not labeled
  (conservative): step 4's "Total price: $306" (a per-passenger sum of the four segment prices, never used downstream;
  the planner quotes the correct $1008 at step 14), step 7's context-free policy delegation (the returned verdict was
  correct and complete), and step 23's truncated option list.
- **aime_021 (failed, gold 50, submitted 74) — decisive_step = 4.** The solver's algebra at step 2 is correct
  (quartic `x^4/4 - 4x^3 - 16x^2 + 256x + 1105 = r^2`, `f' = x^3 - 12x^2 - 32x + 256`, roots 4 and 4±4√5, hence
  r = 41 and r = 9, sum 50), but the step-3 run_python printed nothing (bare expression) and step 4 reports "74" as
  if it were the code's output — the submitted value. Step 10 follows the aime_004 precedent: a re-solve delegation
  with no problem statement, which is what lets steps 11-12 answer for a circle centred at (0, r) tangent to y = x².
  Step 13 (submit_answer 74) is a verbatim relay of the step-4 error and is not labeled (rubric §5b).
- **aime_027 (failed, gold 223, submitted 123) — decisive_step = 2.** Two independent sufficient causes, as in
  aime_013: neither subagent ever produced an integer, and the planner then fabricated one. Step 2 is the earliest:
  the solver imposes AD = BD = 5√10 on a point it has already placed at C's foot, gets z² = 0, and re-emits the
  identical "Wait! That would place D at the same point as C" block eight times until finish_reason `length`.
  Steps 4-29 are 26 byte-identical run_python calls whose snippet ends in a bare expression and prints nothing;
  following the aime_002 treatment, step 4 is left unlabeled as the genuine first attempt and the 25 re-issues
  (5-29) are labeled individually. Step 31's `submit_answer(123)` is a pure fabrication — '123' appears nowhere in
  the planner's context — and is kept as its own unrecovered event even though it derives as cascade.

## airline_031 / airline_042 / aime_017 / aime_023 / aime_029 (labeler note)
Same `decisive_step` convention as the earlier batch-2 notes: the earliest **unrecovered** event that is a but-for
cause of the observed failure.
- **aime_017 (failed, gold 243, submitted 4) — decisive_step = 2.** Steps 1 and 4 are labeled `handoff` because the
  planner, whose prompt says "Send the full problem to `solver`", strips the entire `[asy]` block (grid plus the red
  example path, which traverses vertical segments downward at (2,1)--(2,0), (3,1)--(3,0), (7,1)--(8,1)--(8,0)) while
  keeping the dangling sentence "One such path ... is shown by the thick line segments in the figure". I did **not**
  make step 1 decisive: the prose the solver did receive already restricts direction only "along a horizontal or
  diagonal segment", so the step-2 model ("The bug cannot move left or down") contradicts the text in hand and is the
  but-for cause; the figure loss is contributory, not sufficient. Under a "first unrecovered event, full stop" reading
  the decisive step would be 1. Steps 3 and 6 are the arithmetic claim "√20 = 4" (the 4 is `int(N**0.5)` truncation in
  the run_python stdout `20\n4`), labeled `reasoning_like` rather than `tool` because the code was read correctly.
- **aime_029 (failed, gold 157, submitted 3) — decisive_step = 2.** Solver and verifier independently write the same
  defective enumeration, `combinations_with_replacement(range(1,13), n)`, which generates non-decreasing multisets
  while the problem counts ordered sequences ("the operations are performed from left to right"). Labeled `tool`
  (wrong arguments to run_python) at 2/5 and `reasoning_stability` at 3/6, where the multiset count is asserted to be
  the count of sequences. Step 7 (`submit_answer(3)`) is a faithful relay of two agreeing subagents — not labeled
  per §5b.
- **aime_023 (failed, gold 245, submitted 30) — decisive_step = 2, 50 events.** Step 2 is the earliest unrecovered
  but-for cause: the solver makes no tool call at all (its prompt: "You MUST call `run_python` at least once") and is
  cut off by the length cap with no FINAL ANSWER, which is what triggers the re-solve. Step 4 is the verifier
  degenerating into verbatim paragraph repetition, also with no answer. Step 5 follows the aime_004 / aime_021
  precedent (re-solve delegation carrying no problem statement), and step 6 is the resulting substituted problem
  ("perimeter of 150 ... IA = 15, IB = 16, IC = 17 ... find the area"), which has no counterpart anywhere in the
  trace. Steps 8-50 are 43 re-issues of the byte-identical 308-char sympy call from step 6 (identical md5, empty
  stdout every time because the snippet ends in a bare expression), each labeled individually per §5b; step 8 is
  included rather than treated as a genuine retry because it repeats step 6's code unchanged after the Heron
  `ValueError`. Under a "most proximate cause" reading the decisive step would be 5.
- **airline_031 (succeeded, reward 1.0).** Six events, five of them transient. The run reaches the right end state
  (cancel 9HBUV8, refuse D1EW9B) but spends three policy round trips on context-free delegations: step 11 omits the
  `Created At: 2024-05-04` / `Insurance: No` that db_agent had just reported, and steps 31/39 ask the policy_checker
  — whose prompt says "You cannot access the database" — questions it cannot answer, drawing `need_info` at 34/35 and
  again at 42 even though `Insurance: yes` was in the planner's context from step 38. Step 15 is a fabricated system
  claim ("our system does not currently indicate that you are a Silver member") made before any membership lookup and
  contradicted at step 19. Step 45 emits a literal unexecuted `<tool_call>{"name": "write_file", ...}</tool_call>`
  block as report text. Not labeled (conservative): step 21/22's invented "Policy clause 5.3" (correct verdict, per
  the airline_018 precedent); step 43's redundant re-query of 9HBUV8 (rubric §5 — harmless extra tool call); step 47's
  `allowed` verdict, which treats "travel insurance is bought" as sufficient and skips "and the condition is met" —
  the graded outcome is the cancellation, so flagging it would contradict the gold reward.
- **airline_042 (succeeded, reward 1.0).** Six events. The graded end state is right (no cancellation: basic economy,
  `insurance: no`, `created_at 2024-05-02` vs. policy time 2024-05-15), but four unrecovered events are a fabricated
  remedy: the planner invents a proof-of-purchase upload at step 16, db_agent names a "customer portal" at step 18,
  and the planner re-emits it at 19 and finally invents the URL `www.airline.com/customer-portal` plus a navigation
  flow at 21 — against the policy's "You should not provide any information, knowledge, or procedures not provided by
  the user or available tools." Step 6 (db_agent report drops `insurance: no` and `created_at`) and step 11 (planner
  orders "Process the cancellation ... initiate the refund process" on the customer's word alone, with the only
  verdict so far being step 8's `need_info`) are both recovered at step 13. Not labeled (conservative): step 8's
  policy restatement, which omits the 24-hour and airline-cancelled grounds but carries the correct `need_info`
  verdict; the policy_checker's missing `/case_notes.md` `write_file` at step 8 (bookkeeping only, no effect on the
  case, and the airline_021 precedent leaves case-notes misses unlabeled); step 25's summary, which reports what was
  said rather than re-asserting the portal as available.

## Batch 2 — labeler notes (airline_030, airline_041, aime_016, aime_022, aime_028)
Same convention as the earlier batches: `decisive_step` = the earliest **unrecovered** event that is a but-for
cause of the observed failure; repeated emissions labeled individually per RUBRIC §5b.
- **airline_030 — decisive_step = 24, not 7.** Step 7 (db_agent answers "duplicate flights on the same day" with
  intra-itinerary connections: HTR26G's single MSP-EWR-DFW connection is reported as a same-day duplicate, and
  5BGGWZ's 2024-05-17 DFW-EWR leg is declared "not on the same day" although it collides with SE9KEL/FDZ0T5) is an
  earlier unrecovered event, but not a but-for cause: both real collision days (05-17 and 05-22) still reached the
  customer at step 8 and the customer's own pick (FDZ0T5) is the correct May-17 cancellation given the task's "you
  will be in Los Angeles (LAX) on May 17 and in Boston (BOS) on May 22". The failure is that HSR97W (May 22) is never
  cancelled: at step 24 the planner emits its `respond_to_user` call as literal `<tool_call>{...}</tool_call>` text
  (finish_reason=stop, tool_calls=[]), which ends the episode, and the message it tried to send re-asks the customer
  instead of handling "the rest for the other days" as instructed at step 11.
- **airline_041 — decisive_step = 5.** The customer's "booked 10 hours ago" is false (`created_at`
  2024-05-02T06:02:56 vs env date 2024-05-15) and the db_agent reported it correctly at step 4, together with
  `basic_economy` / `insurance: no`. Step 5 is where the planner re-asserts the customer's claim to policy_checker
  and drops all three record fields; steps 6 (VERDICT allowed, "regardless of the cabin class") and 7 (the
  cancellation order) are labeled as their own unrecovered events but derive as cascade. Not labeled: step 10
  (faithful relay of the real cancel_reservation result) and step 12 (the harness-mandated one-line case summary
  after [CONVERSATION_ENDED], which repeats "booked 10 hours ago" but is post-outcome and causally inert).
- **aime_016 — decisive_step = 2.** Solver and verifier make the *same* error independently (admitting negative
  common differences d = -1,-2,-5,-10, whose term positions m = 20/d + 1 are negative), so the verifier confirms 32
  instead of catching it; gold 178 = 13+22+49+94. Step 3 is an aime_002-style fabricated tool output (the step-2
  `sum([...])` call is a bare expression, stdout empty, yet "the sum ... is 32" is reported as its result), and
  step 7 is the recurring "Submitted <n>." text with no `submit_answer` call (submitted=None).
- **aime_022 — decisive_step = 2.** Both the solver (step 2) and the verifier (step 4) degenerate into verbatim
  repetition loops and are cut off at finish_reason=length with no FINAL ANSWER. Following the aime_007 convention
  the step-6 re-solve is a re-derivation, not a correction, so step 2 stays unrecovered and decisive. Step 6's model
  ((2/3)^4 * 1/3 = 16/243) counts AAAA and excludes runs longer than four non-Carol rolls; correct value 7/54 -> 754.
  Not labeled: step 5 (the re-delegation carries the full problem statement, unlike aime_004 step 7) and step 7
  (faithful report of a genuine `run_python` stdout).
- **aime_028 — decisive_step = 4.** Steps 2-3 (invented "known result" f(n) = 2^n - 2, then "the smallest integer n
  such that 2^n = 4042 is 12") are marked recovered at step 4, where the solver checks `2**12` and discards the
  model — the only genuine self-correction in these five runs. Step 4 then adopts an equally unfounded C(2n,n) = 4040
  and never leaves it; steps 5/6/7 re-issue the same impossible search over ranges 20-40, 40-60, 60-80 after empty
  stdout (C(2n,n) passes 4040 between n=7 and n=8), and step 8 returns "Let's try a larger range again." as the
  solver's final report. The submitted 13 comes entirely from the verifier's invented C(n) = 2^{n-1} (steps 10-11),
  which also swaps the problem's "exactly 4040" for "C(n) >= 4040"; gold 107, submitted=None (step 12, no
  `submit_answer` call).

## airline_025 / airline_035 / airline_045 / aime_019 / aime_025 (labeler note)
- **airline_025 (failed) — decisive_step = 28, not 37.** Two independent sufficient causes. (a) Step 28's
  "second cheapest = HAT083+HAT011, $137+$177 = $314" is wrong on the tool's own numbers (direct HAT023 $163;
  one-stop economy totals 290 / 300 / 304 / 314 / 321 / 331 / 335, so the second cheapest is $290 =
  HAT069+HAT258 and $314 is fifth); (b) no `book_reservation` call ever carries a real payment method, so the
  booking never happens and db_agent escalates at step 51. Following the airline_017 convention I set the
  decisive step to the first unrecovered corruption *carried into the final outcome*: the customer accepted the
  $314 itinerary at step 30 and every later attempt books it. Under a strict "but-for cause of the observed
  failure (the transfer)" reading the decisive step is 37 (invented `payment_id credit_card_123456`, never
  replaced; `get_user_details` is never called in that db_agent invocation although the real ids
  credit_card_9074831 / credit_card_4959530 / certificate_9645872 were fetched at step 5).
- **airline_035 (failed) — one event, decisive_step = 2.** The planner's single delegation
  ("Cancel ... PEP4E0 ... Confirm if this action is possible") sends the eligibility question to db_agent, which
  has no policy text; `policy_checker` is never invoked. PEP4E0 is basic_economy, `insurance: no`,
  `created_at 2024-05-05` (current time 2024-05-15), so the cancellation is not allowed. Following the batch-1
  convention I did **not** label db_agent step 4 for executing the cancel (the subagent is given no policy),
  nor step 6 (planner relays the db_agent report faithfully; the -128 refund entry is really in the tool result).
  db_agent also skipped its required `/case_notes.md` append — bookkeeping only, not labeled.
- **airline_045 (failed) — decisive_step = 4**, by the airline_006 precedent (first delegation that no db tool
  could execute). The planner asked for an id at step 2, the customer could not give one, and the planner then
  issued twelve unexecutable lookups (by passenger count, route, airline, flight number, email); db_agent
  answered six of them with ids copied out of its own tool descriptions (`sara_doe_496` x4, `delta_user_123`,
  `8JX2WO`). The proximate missed recovery is step 60/65: the customer's email
  `noah_muller_9847@example.com` is passed whole as `user_id` and the id form `noah_muller_9847` is never tried.
  I did not label steps 36-44 (flight-availability searches that are the wrong instrument but report their empty
  results honestly); step 49 is labeled because it turns one empty `search_direct_flight` into "the reservation
  ... does not exist in the database", and step 55 because it turns "reservation ID 8JX2WO could not be found"
  into "I couldn't find a reservation for United flight 123".
- **aime_019 / aime_025 (both succeeded).** Same shape, one event each: the solver degenerates into a verbatim
  repetition loop and is cut off by the token limit (`finish_reason: length`, 2048 completion tokens) without
  ever emitting a final integer; the verifier's independent `run_python` derivation produces the gold answer
  (279 / 850) at step 5 and the planner submits it, so both events are `recovered` at step 5. The truncation is
  the model's own degeneration, not a harness error — the repeated blocks are byte-identical. Not labeled: the
  planner submitting on the verifier alone although its procedure describes comparing two answers (the solver
  returned none, and the submitted value is correct).

## airline_032 / airline_044 / aime_018 / aime_024 / aime_030 (labeler note)
Same convention as the earlier batches: `decisive_step` = the earliest **unrecovered** event that is a but-for
cause of the observed failure; corrupted values that are later discarded without being corrected stay
`recovered: false` but are not made decisive. No summarization happened in any of these runs
(`summarization_pre/` is empty for airline_032), so no `compression_induced` subtags are used.
- **airline_032 (failed, reward 0.0) — decisive_step = 71.** Nothing was ever booked (ground truth: one
  reservation on HAT271 2024-05-26, two passengers, `certificate_8045380` $348). Step 71 is the first
  unrecovered event on that path: the db_agent's own list in the same message shows `HAT271 ... Available
  Economy Seats: 3 ... $174` yet it concludes "Only Flight HAT289 has enough economy seats available for two
  passengers" (3 >= 2; 2 x 174 = 348 < the customer's $500 cap) and books HAT289 with the invented
  `credit_card_7815826`. The earlier unrecovered event at step 40 (promising aisle/middle seat selection, which
  no tool provides) is **not** made decisive: no booking call was ever rejected because of the bogus `seat`
  field (the rejections were "user not found", `'amount'`, `'payment_id'`) and seats are not part of the graded
  action. Everything from 72 on (identical re-sent calls, the `'amount'` misread, the never-made
  `get_user_details` payment lookup, the invented "add a payment method through our website or mobile app")
  derives as cascade. Not labeled, per the established relay convention: planner steps 45/50/67/78 that pass a
  db_agent report on without adding a false value — including step 67, where "no direct flights found" becomes
  "there was an issue processing the booking for Flight HAT271"; db_agent steps 49/61/66 that report their own
  failed calls honestly; step 72, which is genuine debugging of the `'date'` error; and the redundant
  reservation sweeps at 12-22, which are folded into the events at 10 and 11 that caused them.
- **airline_044 (failed, reward 0.0, expected output "4") — decisive_step = 4.** Two independent defects, both
  from the same missing lookup: membership was never verified (`get_user_details` was in the db_agent's tool
  list and `user_id: anya_garcia_5901` was in the result it had just read; the profile says **silver**, the
  customer only guessed "gold"), and the per-passenger allowance was never multiplied by the two passengers the
  reservation lists. Step 4 is the earliest. The policy_checker is correct at both 8 and 12 for the questions it
  was asked, so it carries no event (its literal `VERDICT: allowed | not_allowed | need_info — <...>` template
  line at step 12 is a format defect only, not labeled, per the airline_006 precedent).
- **aime_018 (failed, gold 503, submitted None) — decisive_step = 2**, by the aime_013 precedent (earliest of
  two independent sufficient causes). The solver degenerates at step 2 into ~19 byte-identical repetitions of
  the same false contradiction and returns no answer; the planner then uses the verifier as a solver, and the
  verifier's setup (step 4) puts D at (20, b+20), i.e. `DE = AB + 20 > AB`, contradicting the given `DE < AB`
  (correct: `D = (20, AB-8)`, area `20*AB - 164`, `AB = 1 mod 4`, `AB > 14` -> 503). Step 6 ("Submitted 506."
  with no `submit_answer` call) is the other sufficient cause and is recorded as its own event.
- **aime_024 (failed, gold 669, submitted 445) — decisive_step = 8.** Three different wrong answers were
  produced: 111 (step 3, fabricated — the step-2 `run_python` returned empty stdout), 656 (steps 5-6, a float64
  sum whose ~16 significant digits cannot resolve the last three digits of a 100-digit integer) and 445 (step 8,
  a Fraction sum truncated at `range(1, 20)`; the dropped tail is `10^100 * sum_{n>=20} 1/(10^n - 1) ~ 1.1e80`).
  111 and 656 were discarded without being corrected, so decisive is step 8, the computation behind the
  submitted 445; steps 9-11 re-issue that byte-identical call three more times under "let's verify using a
  different approach" and are labeled individually per §5b. Planner step 13 (`submit_answer(445)`) relays the
  solver's report and is not labeled.
- **aime_030 (succeeded, gold 393).** Clean: solver and verifier each brute-force all 3^7 tuples with correct
  code, both print 393, `submit_answer(393)` is called. No events.

## Batch 2 — labeler notes (airline_026, airline_037, airline_046, aime_020, aime_026)

- **airline_026 (failed, reward 0) — decisive_step = 4.** The scored break is the cancellation of IFOYYZ
  (`basic_economy`, `insurance: no`, `created_at 2024-05-12T00:14:30`, i.e. outside the 24-hour window), ordered at
  step 4 in the same breath as the legitimate cancellation of NQNU5R (`business`, always cancellable) with no
  `policy_checker` call and no cancellation reason asked. Same shape as batch-1 airline_010, and I followed that
  batch's convention of labeling the planner's order rather than the db_agent that executed it (step 5), since the
  db_agent is given no policy text.
- **airline_026 — the $597 events (steps 20/21) are deliberate but debatable.** $597 is the correct *per-passenger*
  difference (430 + 412 − (136 + 109)); the defect is calling it "the total price difference" for a reservation whose
  own record lists two passengers and a prior charge of $490 = 245 × 2. The customer authorises $597 at step 23 and
  the tool charges $1194 at step 28. Marked `recovered` at step 29, where the db_agent reports the real $1194,
  although the customer is only told after the charge, and step 30 writes both figures into `/case_notes.md`.
  Not labeled (conservative): step 5 executing the planner's cancellation; step 29/31's "successfully upgraded to
  business class" — the returned reservation still reads `"cabin": "economy"`, but `update_reservation_flights`
  never writes that field back, so this is an environment quirk and not an agent claim I can call false; the
  planner's verbatim relays at steps 22/24/32.
- **airline_037 (succeeded, reward 1.0) — decisive_step = null, but the run succeeds by inaction.** No write ever
  happened, so the database hash matched. The two events are real: step 4 delegates an id-less
  "find all reservations for flight HAT045 and Gold members" that no tool can execute, and step 5 is a db_agent-initiated
  `transfer_to_human_agents` although the customer never asked for a human — it just happens to end the episode with the
  DB untouched. Same "unrecovered but not decisive in a successful run" situation flagged for airline_003/airline_018
  in batch 1. Not labeled: step 7, where the planner relays the transfer faithfully (it adds "they will reach out to you
  shortly", which I judged too thin to score against airline_024's fabricated-escalation event).
- **airline_046 (failed, reward 0) — decisive_step = 15, 20 events.** The reservation behind the delay complaint is
  never identified. Step 15 ("Find the last reservation with three passengers.") is the first delegation on the failing
  thread that no db tool could execute; the identical id-less lookup is then re-issued nine more times (20, 25, 29, 33,
  38, 44, 49, 54, 59), twice after the db_agent had said in plain words that no function can do it (steps 26 and 30),
  and the planner keeps soliciting keys no tool accepts (flight number, airline, passenger first name). The db_agent
  answers three of them by inventing the user id `sara_doe_496` (steps 16, 21, 60) and at step 22 calls it
  "the provided user ID" although no one provided it. Each repeat is labeled per RUBRIC §5b; almost all of them derive
  as `cascade`. The closing steps 64/66 hand the customer a fabricated third-party referral
  ("Delta's customer service at 1-800-221-1212", delta.com) after the customer had said at step 12 that the reservation
  was "with you all". Steps 9 and 11 are earlier unrecovered events (a repeated identical `search_direct_flight`, and
  the planner offering a one-stop search the step-7 report had already ruled out) but they sit on the abandoned booking
  thread, not on the path to the scored failure, so they are not decisive. Not labeled: step 2 (the planner's opening
  turn asks for dates and preferences and never for the user id) — real, but batch 1 (airline_006) fixed the convention
  of labeling the first impossible *delegation* rather than the failure to ask.
- **aime_020 (failed, gold 190, submitted 205) — decisive_step = 3.** The solver's step-2 code is *correct*: run
  verbatim it returns [22, 30, 38, 46, 54], sum 190. Step 3 reports "31, 36, 41, 46, 51 ... 205" for a call whose
  stdout was empty (bare expression `valid_n, sum_n`), so the run loses a solved problem to a fabricated tool result.
  The verifier repeats the pattern at step 6 (360, also from empty stdout) on top of a script that silently drops the
  b >= 7 constraint (step 5). Categories follow the batch-1 convention: fabricated `run_python` output is
  `tool` / `hallucination_like`. Step 9 (planner submits 205) is a verbatim relay and is not labeled.
- **aime_026 (failed, gold 132, submitted 100) — decisive_step = 8, not 2 or 7.** Steps 2, 4, 5 and 7 are all
  unrecovered, but the submitted 100 comes from nowhere but step 8's fabrication ("After running the code, we find
  that the valid integer solutions ... n = 100" against `stdout: ""`), which the same step then refutes
  ("50 = 16.67: This is not correct"). Step 2's "two of the roots are equal" premise is wrong (two equal roots give
  six distinct signed sums, not seven) but is discarded when step 7 switches to symmetric functions, so under the
  batch-1 but-for convention it is not decisive; step 7's script omits the seven-values condition entirely but its
  output was never read. Step 9 *is* labeled (handoff): unlike a verbatim relay, the planner submits a value its own
  subagent's report explicitly rejects and never states as an answer.

## Label cut

- Label cut: 2026-09-09 03:27 KST. n = 60 labeled runs (batch 1: 30, batch 2: 30; 30 airline + 30 AIME).
  All 60 validate (`python -m src.eval.labels --validate`: 0 errors, 0 warnings); 434 events, 47 runs with a decisive step.
- Batch-2 labels were produced by six blind subagents (5 runs each) reading only `runs/<id>/summary.md`
  (+ `steps.jsonl` when the summary was ambiguous). No labeler read anything under `audit/`.
