# Labeling rubric (step-level failure annotation)

Labeler: Claude (Claude Fable 5.1), acting as the human annotator. Labels are the **evaluation gold**; the detector
never reads them. Input per trace: `runs/<run_id>/summary.md` (step-ordered digest incl. tool calls/results, customer
turns, final outcome and ground-truth success flag). Labelers do NOT see any detector output (`audit/`).

## Output schema — `labels/<run_id>.json`

```json
{
  "run_id": "airline_007", "batch": 1,
  "decisive_step": 9,
  "error_events": [
    {"step": 6, "agent": "policy_checker", "category": "reasoning_stability", "subtag": "reasoning_like",
     "recovered": true, "recovery_step": 8,
     "evidence": "Verdict 'allowed' for basic-economy change contradicts policy §Modify flight; planner re-asked at step 8"},
    {"step": 9, "agent": "planner", "category": "handoff", "subtag": "handoff_induced",
     "recovered": false, "recovery_step": null,
     "evidence": "db_agent reported total $340; planner told the customer $430"}
  ]
}
```

- `step`: the LLM-call index shown in summary.md (`### step N — agent`). Only planner / policy_checker / db_agent / solver /
  verifier steps may be labeled. Never label `[customer]` (user_sim) or summarizer steps.
- `decisive_step`: the earliest error event with `recovered=false` **that leads to the task failure**. `null` for
  successful runs and for failed runs where no step-level cause can be identified (say so in `evidence` of a
  synthetic event? no — leave `error_events` as observed and `decisive_step: null`; note the reason in `labels/notes.md`).
- Every event needs `evidence`: quote or paraphrase the offending text and the record it contradicts (tool result,
  customer statement, policy clause, subagent report, python output).

## Categories (choose one per event)

| category | when | typical subtag |
|---|---|---|
| `handoff` | information is lost/altered/added when crossing an agent boundary: planner instruction ≠ what the subagent assumed; subagent report ≠ what the planner relayed/used; wrong subagent chosen; delegation with missing ids | `handoff_induced` |
| `tool` | wrong tool, wrong/malformed arguments, tool error ignored, result misread, required tool never called, needless repetition | `null` (or `hallucination_like` if the agent invented a tool result) |
| `reasoning_stability` | a conclusion not supported by the record: fabricated value/fact (`hallucination_like`), wrong policy application / arithmetic / logic on correct premises (`reasoning_like`), belief that only makes sense after context was summarized away (`compression_induced`) | see left |

Subtags are **descriptive** (used only for analysis); when unsure between hallucination_like and reasoning_like, pick
`reasoning_like` and mention the ambiguity in evidence.

## Procedure

1. Read the header: success/failure, gold answer vs submitted (AIME) or reward (airline).
2. Walk steps in order. For each labeled-agent step ask:
   - Did it state a value/fact absent from all prior tool results, customer turns, and the problem? → reasoning_stability / hallucination_like
   - Did it misapply policy, miscalculate, or draw an unsupported conclusion from correct premises? → reasoning_stability / reasoning_like
   - Did it call a tool wrongly (bad args, wrong tool), ignore an error, or skip a required lookup? → tool
   - Did information change at a boundary (instruction → subagent premise, report → planner statement)? → handoff (label the step where the corrupted information is *used or emitted*)
3. For each event decide `recovered`: a later step corrects it (re-query, re-derivation, customer correction accepted) → `true` + `recovery_step`.
4. `decisive_step` = first unrecovered event on the path to the final failure. Successful runs may have only recovered
   (transient) events.
5. Do not label stylistic issues, verbosity, or harmless extra tool calls. Do not label the customer's mistakes.
6. If a failed run has no identifiable erroneous step (e.g. environment/tool-server error), set `decisive_step: null`
   and record `"category": "tool"` events only where actually observed.

## Derived step classes (computed by `src/eval/labels.py`)

`decisive` = decisive_step; `transient` = recovered events; `cascade` = steps after decisive_step; `clean` = all other
labeled-agent steps. Cascade steps are excluded from detection scoring and used only for latency.

## Quality control

Six traces are re-labeled independently by the main session; agreement on (decisive_step exact, category per event)
is reported in `labels/index.csv` / proposal §4.3. Disagreements trigger a rubric wording fix and re-labeling of that batch.
