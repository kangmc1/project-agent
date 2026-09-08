"""Synthetic scenario schema for the handoff-stability stress test.

A scenario = a task + a realistic prior transcript + a set of typed obligations that any downstream
agent must respect. Each obligation carries an exact `key_span` from the transcript and `key_values`
(numbers, names, ids) so survival across compression can be checked by rules, not by a judge.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
import json, re

OBLIGATION_TYPES = ("constraint", "verified_fact", "open_question", "prohibition")


@dataclass
class Obligation:
    id: str
    type: str
    text: str            # one-sentence statement
    key_span: str        # exact substring of the transcript that establishes it
    key_values: list[str]  # distinctive tokens that must survive (numbers, ids, names, dates)


@dataclass
class Scenario:
    id: str
    domain: str
    task: str
    transcript: str
    obligations: list[Obligation]
    notes: str = ""

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)

    @staticmethod
    def from_json(s: str) -> "Scenario":
        d = json.loads(s)
        d["obligations"] = [Obligation(**o) for o in d["obligations"]]
        return Scenario(**d)


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("\u201c", '"').replace("\u201d", '"').replace("\u2019", "'").replace("\u2018", "'")).strip().lower()


def validate(sc: Scenario) -> list[str]:
    """Return a list of problems; empty means valid. Spans/values may come from the transcript OR the task."""
    probs = []
    source = _norm(sc.transcript + "\n" + sc.task)
    if len(sc.transcript.split()) < 150:
        probs.append("transcript too short")
    types = [o.type for o in sc.obligations]
    for t in OBLIGATION_TYPES:
        if t not in types:
            probs.append(f"missing type {t}")
    for o in sc.obligations:
        if o.type not in OBLIGATION_TYPES:
            probs.append(f"{o.id}: bad type {o.type}")
        if not o.key_span.strip() or _norm(o.key_span) not in source:
            probs.append(f"{o.id}: key_span not in transcript/task")
        if not o.key_values:
            probs.append(f"{o.id}: no key_values")
        for v in o.key_values:
            if _norm(v) not in source:
                probs.append(f"{o.id}: key_value '{v}' not in transcript/task")
    return probs
