"""B-layer: controlled manipulation of a reset handoff's fact sheet.

We take a real context-reset handoff (pre-reset transcript -> fact sheet), pick one task-relevant
bullet under "GIVEN OR VERIFIED FACTS", and apply one operation:
  drop    : delete the bullet                      (ground truth: S1 sender_drop)
  weaken  : soften/hedge it, remove a qualifier    (ground truth: S2 sender_weaken)
  corrupt : change one concrete value               (ground truth: S3 sender_corrupt)
  none    : control, artifact unchanged             (ground truth: no injected fault)
The receiver is not needed: the detection task is (sender context, artifact') -> which item was manipulated.
"""
from __future__ import annotations

import json
import re
import random
from dataclasses import dataclass, asdict
from typing import Any

from handoffbench.llm import LLM

BOILERPLATE = re.compile(r"(today'?s date|system: darwin|do not use sudo|sudo|within 50 rounds|50 rounds of conversation|output format|## answer|terminate)", re.I)
SECTION1 = re.compile(r"1\.\s*GIVEN OR VERIFIED FACTS\s*\n(.*?)(?=\n\s*2\.\s*FACTS|\Z)", re.S)


@dataclass
class Injection:
    injection_id: str
    handoff_id: str
    op: str                      # drop | weaken | corrupt | none
    target_line: str | None      # original bullet
    modified_line: str | None    # replacement (weaken/corrupt), None for drop/none
    artifact_original: str
    artifact_modified: str
    n_candidates: int


def fact_bullets(facts_text: str) -> list[str]:
    m = SECTION1.search(facts_text)
    if not m:
        return []
    lines = [ln.strip() for ln in m.group(1).splitlines() if ln.strip().startswith(("-", "*", "•"))]
    return [ln for ln in lines if not BOILERPLATE.search(ln) and len(ln) > 25]


WEAKEN = """Rewrite the following statement from a fact sheet so that it becomes VAGUER or SOFTER while staying on the same topic: turn a hard requirement or precise condition into a loose suggestion, or drop one qualifier (a date, a number, a specific source), so that a reader could no longer rely on the precise condition. Keep the bullet format and similar length. Reply with ONLY the rewritten line.

Statement: {line}"""

CORRUPT = """Rewrite the following statement from a fact sheet so that ONE concrete detail becomes WRONG but plausible: change a date, number, version, name, unit or URL to a different value of the same kind. Keep everything else identical, keep the bullet format. Reply with ONLY the rewritten line.

Statement: {line}"""


def inject(llm: LLM | None, handoff: dict[str, Any], op: str, rng: random.Random, artifact_builder) -> Injection | None:
    """artifact_builder(facts_text, plan_text) -> artifact string (same rendering as the detectors see)."""
    facts = handoff["facts_text"]
    cands = fact_bullets(facts)
    art0 = artifact_builder(facts, handoff["plan_text"])
    if op == "none":
        return Injection(f"{handoff['handoff_id']}::none", handoff["handoff_id"], "none", None, None, art0, art0, len(cands))
    if not cands:
        return None
    line = rng.choice(cands)
    if op == "drop":
        new_facts = facts.replace(line, "", 1)
        new_line = None
    else:
        assert llm is not None
        prompt = (WEAKEN if op == "weaken" else CORRUPT).format(line=line)
        for _ in range(3):
            new_line = llm.chat("You edit text exactly as instructed.", prompt, max_tokens=200, temperature=0.7).strip().splitlines()[0].strip()
            if new_line and new_line != line and len(new_line) > 10:
                break
        else:
            return None
        if not new_line.startswith(("-", "*", "•")):
            new_line = "- " + new_line
        new_facts = facts.replace(line, new_line, 1)
    return Injection(f"{handoff['handoff_id']}::{op}", handoff["handoff_id"], op, line, new_line, art0, artifact_builder(new_facts, handoff["plan_text"]), len(cands))


def content_tokens(s: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9]+", s.lower()) if len(t) > 2 and t not in {"the", "and", "for", "with", "that", "this", "from", "are", "was", "were", "has", "have", "not", "which"}}


def overlap(a: str, b: str) -> float:
    A, B = content_tokens(a), content_tokens(b)
    return len(A & B) / max(1, len(A | B))


def to_jsonl(items: list[Injection], path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for it in items:
            f.write(json.dumps(asdict(it), ensure_ascii=False) + "\n")
