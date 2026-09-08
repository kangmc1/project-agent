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
