"""Load TraceElephant runs and extract handoff events.

A TraceElephant run is a directory with `trace_metadata.json` and `step_records.json`.
Each step record is one LLM API call: {step_id, agent_id, agent_name, input{messages,...}, output{choices,...}, tool_logs}.

Magentic-One handoff = an Orchestrator "ledger" step whose output JSON contains
`next_speaker` and `instruction_or_question` (identified by content; the recorded
`agent_name` on these steps is unreliable and often names the previous speaker). The receiver's behaviour is every step
between that ledger step and the next ledger step (or the end of the run).
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Iterator


@dataclass
class Run:
    run_id: str
    system: str
    task_id: str
    task_instruction: str
    ground_truth: str
    mistake_agent: str
    mistake_step: int | None
    mistake_reason: str
    steps: list[dict[str, Any]]
    path: str


@dataclass
class Handoff:
    handoff_id: str
    run_id: str
    system: str
    task_instruction: str
    ground_truth: str
    step_id: int                      # ledger step id (sender's decision step)
    sender: str
    receiver: str
    instruction: str                  # the handoff artifact (what the receiver is told to do)
    instruction_reason: str
    ledger: dict[str, Any]            # full parsed ledger JSON (progress flags etc.)
    sender_context: list[dict]        # messages the sender saw when producing the artifact
    sender_prompt_tokens: int | None
    receiver_steps: list[dict]        # compact view of the receiver segment (LLM calls + tool calls)
    receiver_report: list[dict]       # messages the receiver sent back before the next ledger (its observations/report)
    segment_end_step: int             # exclusive: next ledger step id or last step + 1
    index_in_run: int
    n_handoffs_in_run: int
    mistake_agent: str
    mistake_step: int | None
    mistake_reason: str
    mistake_in_segment: bool
    mistake_at_this_handoff: bool


def _content(step: dict) -> str:
    try:
        return step["output"]["choices"][0]["message"].get("content") or ""
    except (KeyError, IndexError, TypeError):
        return ""


def _tool_calls(step: dict) -> list[dict]:
    try:
        return step["output"]["choices"][0]["message"].get("tool_calls") or []
    except (KeyError, IndexError, TypeError):
        return []


def _parse_ledger(text: str) -> dict | None:
    """Extract the ledger JSON object from an orchestrator output (may be wrapped in ``` fences)."""
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    try:
        obj = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
    if isinstance(obj, dict) and "next_speaker" in obj and "instruction_or_question" in obj:
        return obj
    return None


def _ans(field_obj: Any) -> Any:
    if isinstance(field_obj, dict) and "answer" in field_obj:
        return field_obj["answer"]
    return field_obj


def _compact_step(step: dict, max_chars: int = 4000) -> dict:
    """Receiver-side view: what the agent produced (text + tool calls + tool results)."""
    tool_results = []
    for tl in step.get("tool_logs") or []:
        if isinstance(tl, dict):
            fn = tl.get("function", {}) if isinstance(tl.get("function"), dict) else {}
            tool_results.append({
                "name": fn.get("name") or tl.get("name"),
                "arguments": (fn.get("arguments") or "")[:max_chars],
                "result": str(tl.get("result", tl.get("output", "")))[:max_chars],
            })
    return {
        "step_id": int(step["step_id"]),
        "agent_name": step["agent_name"],
        "content": _content(step)[:max_chars],
        "tool_calls": [
            {"name": tc.get("function", {}).get("name"), "arguments": (tc.get("function", {}).get("arguments") or "")[:max_chars]}
            for tc in _tool_calls(step)
        ],
        "tool_results": tool_results,
    }


def load_run(run_dir: Path) -> Run:
    md = json.loads((run_dir / "trace_metadata.json").read_text())
    steps = json.loads((run_dir / "step_records.json").read_text())
    ms = md.get("mistake_step")
    return Run(
        run_id=md["run_id"], system=md["system_name"], task_id=md.get("task_id", ""),
        task_instruction=md.get("task_instruction", ""), ground_truth=str(md.get("ground_truth", "")),
        mistake_agent=md.get("mistake_agent", ""), mistake_step=int(ms) if str(ms).isdigit() else None,
        mistake_reason=md.get("mistake_reason", ""), steps=steps, path=str(run_dir),
    )


def iter_runs(data_root: Path, system: str | None = None) -> Iterator[Run]:
    for md in sorted(data_root.glob("*/*/trace_metadata.json")):
        run = load_run(md.parent)
        if system is None or run.system == system:
            yield run


def extract_magentic_handoffs(run: Run) -> list[Handoff]:
    assert run.system == "magentic-one", run.system
    ledger_idx = []
    for i, s in enumerate(run.steps):
        # NOTE: TraceElephant's `agent_name` on ledger steps carries the *previous* speaker
        # (e.g. "WebSurfer"), so ledgers are identified by content, not by agent_name.
        if _parse_ledger(_content(s)):
            ledger_idx.append(i)
    handoffs: list[Handoff] = []
    for k, i in enumerate(ledger_idx):
        s = run.steps[i]
        ledger = _parse_ledger(_content(s))
        j_end = ledger_idx[k + 1] if k + 1 < len(ledger_idx) else len(run.steps)
        seg = [_compact_step(t) for t in run.steps[i + 1 : j_end]]
        # Messages appended to the orchestrator's transcript between this ledger and the next one:
        # [instruction (role=Orchestrator), receiver report(s) (role=<receiver>), ..., next ledger prompt]
        cur_msgs = s["input"]["messages"]
        if k + 1 < len(ledger_idx):
            nxt_msgs = run.steps[ledger_idx[k + 1]]["input"]["messages"]
            new_msgs = nxt_msgs[len(cur_msgs):]
            report = [m for m in new_msgs[:-1] if str(m.get("role", "")) not in ("MagenticOneOrchestrator", "Orchestrator")]
        else:
            report = []
        report = [{"role": m.get("role"), "content": (m.get("content") if isinstance(m.get("content"), str) else json.dumps(m.get("content"), ensure_ascii=False))[:6000]} for m in report]
        step_id = int(s["step_id"])
        seg_end = int(run.steps[j_end]["step_id"]) if j_end < len(run.steps) else int(run.steps[-1]["step_id"]) + 1
        ms = run.mistake_step
        handoffs.append(Handoff(
            handoff_id=f"{run.run_id}::h{k:02d}::s{step_id}",
            run_id=run.run_id, system=run.system,
            task_instruction=run.task_instruction, ground_truth=run.ground_truth,
            step_id=step_id, sender="Orchestrator", receiver=str(_ans(ledger.get("next_speaker"))),
            instruction=str(_ans(ledger.get("instruction_or_question"))),
            instruction_reason=str((ledger.get("instruction_or_question") or {}).get("reason", "")) if isinstance(ledger.get("instruction_or_question"), dict) else "",
            ledger={kk: _ans(v) for kk, v in ledger.items()},
            sender_context=s["input"]["messages"],
            sender_prompt_tokens=(s["output"].get("usage") or {}).get("prompt_tokens"),
            receiver_steps=seg, receiver_report=report, segment_end_step=seg_end,
            index_in_run=k, n_handoffs_in_run=len(ledger_idx),
            mistake_agent=run.mistake_agent, mistake_step=ms, mistake_reason=run.mistake_reason,
            mistake_in_segment=(ms is not None and step_id <= ms < seg_end),
            mistake_at_this_handoff=(ms is not None and ms == step_id),
        ))
    return handoffs


def to_jsonl(handoffs: list[Handoff], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for h in handoffs:
            f.write(json.dumps(asdict(h), ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Type II: context-reset ("replan") handoffs.
# When Magentic-One stalls, the orchestrator writes an updated fact sheet and a new plan,
# then CLEARS the shared transcript and restarts with only [task + team + facts + plan].
# Everything the team learned survives only through that summary: a true compression boundary.
# ---------------------------------------------------------------------------

@dataclass
class ResetHandoff:
    handoff_id: str
    run_id: str
    system: str
    task_instruction: str
    ground_truth: str
    reset_step_id: int                 # first ledger step after the reset
    prev_ledger_step_id: int           # last ledger step before the reset
    facts_step_id: int | None          # step whose output is the updated fact sheet
    plan_step_id: int | None           # step whose output is root-cause explanation + new plan
    pre_reset_transcript: list[dict]   # full messages the orchestrator saw before compressing
    pre_reset_prompt_tokens: int | None
    facts_text: str                    # updated fact sheet (orchestrator output)
    plan_text: str                     # root cause + new plan (orchestrator output)
    post_reset_context: str            # messages[0] of the reset step: what the team sees afterwards
    post_reset_steps: list[dict]       # compact steps after reset until next reset / end
    n_steps_before: int
    n_steps_after: int
    index_in_run: int
    n_resets_in_run: int
    mistake_agent: str
    mistake_step: int | None
    mistake_reason: str
    mistake_position: str              # "before_reset" | "at_reset_summary" | "after_reset" | "unknown"


def extract_magentic_resets(run: Run) -> list[ResetHandoff]:
    assert run.system == "magentic-one", run.system
    steps = run.steps
    ledger_idx = [i for i, s in enumerate(steps) if _parse_ledger(_content(s))]
    resets = []
    for a, b in zip(ledger_idx, ledger_idx[1:]):
        if len(steps[b]["input"]["messages"]) < len(steps[a]["input"]["messages"]):
            resets.append((a, b))
    out: list[ResetHandoff] = []
    for k, (a, b) in enumerate(resets):
        facts_i = plan_i = None
        for i in range(a + 1, b):
            c = _content(steps[i])
            if "GIVEN OR VERIFIED FACTS" in c:
                facts_i = i
            elif facts_i is not None and i > facts_i and c.strip():
                plan_i = i
        next_b = resets[k + 1][1] if k + 1 < len(resets) else len(steps)
        post = [_compact_step(t) for t in steps[b : next_b]]
        ms = run.mistake_step
        rs = int(steps[b]["step_id"])
        if ms is None:
            pos = "unknown"
        elif ms < int(steps[a]["step_id"]) + 1:
            pos = "before_reset"
        elif ms < rs:
            pos = "at_reset_summary"
        else:
            pos = "after_reset"
        out.append(ResetHandoff(
            handoff_id=f"{run.run_id}::r{k:02d}::s{rs}",
            run_id=run.run_id, system=run.system,
            task_instruction=run.task_instruction, ground_truth=run.ground_truth,
            reset_step_id=rs, prev_ledger_step_id=int(steps[a]["step_id"]),
            facts_step_id=int(steps[facts_i]["step_id"]) if facts_i is not None else None,
            plan_step_id=int(steps[plan_i]["step_id"]) if plan_i is not None else None,
            pre_reset_transcript=steps[a]["input"]["messages"],
            pre_reset_prompt_tokens=(steps[a]["output"].get("usage") or {}).get("prompt_tokens"),
            facts_text=_content(steps[facts_i]) if facts_i is not None else "",
            plan_text=_content(steps[plan_i]) if plan_i is not None else "",
            post_reset_context=str(steps[b]["input"]["messages"][0].get("content", "")),
            post_reset_steps=post,
            n_steps_before=a + 1, n_steps_after=len(steps) - b,
            index_in_run=k, n_resets_in_run=len(resets),
            mistake_agent=run.mistake_agent, mistake_step=ms, mistake_reason=run.mistake_reason,
            mistake_position=pos,
        ))
    return out
