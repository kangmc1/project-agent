"""Data records shared by every stage. Plain dataclasses + JSONL I/O."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Iterator

OBLIGATION_TYPES = ("constraint", "verified_fact", "open_question", "prohibition", "goal")
VARIANT_KINDS = ("clean", "clean_paraphrase", "absent", "altered_value", "altered_semantic", "fabricated")
VERDICT_STATUS = ("preserved", "violated", "grounded", "fabricated", "uncheckable")


@dataclass
class Obligation:
    id: str
    type: str
    statement: str
    key_values: list[str]
    evidence: str
    numeric: dict | None = None      # {"value": float, "unit": str, "direction": "max|min|eq"}
    negated: bool = False
    aliases: list[str] = field(default_factory=list)  # surface forms confirmed by the agent via grep


@dataclass
class Boundary:
    id: str
    domain: str                 # whowhen | tau | swe
    source_ref: str             # file / row id in the source dataset
    sender_role: str
    receiver_role: str
    context: list[dict]         # [{"role": str, "content": str}]
    message: str | None = None  # real handoff message (whowhen) or generated clean message
    obligations: list[Obligation] = field(default_factory=list)
    natural_loss: list[Obligation] = field(default_factory=list)
    meta: dict = field(default_factory=dict)


@dataclass
class Variant:
    id: str
    boundary_id: str
    kind: str
    message: str
    target_obligation_id: str | None = None
    fabricated_claim: dict | None = None      # {"statement", "key_values", "sentence"}
    excluded_obligation_ids: list[str] = field(default_factory=list)
    meta: dict = field(default_factory=dict)


@dataclass
class Verdict:
    item_id: str                # obligation id or claim id
    status: str
    diagnosis: str = ""
    code: str | None = None
    attempts: int = 0
    meta: dict = field(default_factory=dict)


# ---------- serialization ----------

def to_dict(obj: Any) -> dict:
    return asdict(obj)


def obligation_from_dict(d: dict) -> Obligation:
    return Obligation(**{k: d.get(k) for k in Obligation.__dataclass_fields__} | {
        "aliases": d.get("aliases") or [], "negated": bool(d.get("negated", False))})


def boundary_from_dict(d: dict) -> Boundary:
    return Boundary(
        id=d["id"], domain=d["domain"], source_ref=d["source_ref"],
        sender_role=d["sender_role"], receiver_role=d["receiver_role"],
        context=d["context"], message=d.get("message"),
        obligations=[obligation_from_dict(o) for o in d.get("obligations", [])],
        natural_loss=[obligation_from_dict(o) for o in d.get("natural_loss", [])],
        meta=d.get("meta", {}),
    )


def variant_from_dict(d: dict) -> Variant:
    return Variant(**{k: d.get(k) for k in Variant.__dataclass_fields__} | {
        "excluded_obligation_ids": d.get("excluded_obligation_ids") or [], "meta": d.get("meta") or {}})


def read_jsonl(path: str | Path) -> Iterator[dict]:
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def write_jsonl(path: str | Path, rows: list) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            if not isinstance(r, dict):
                r = to_dict(r)
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def append_jsonl(path: str | Path, row) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row if isinstance(row, dict) else to_dict(row), ensure_ascii=False) + "\n")


# ---------- text helpers ----------

def context_to_text(context: list[dict]) -> str:
    """Canonical serialization of a sender context; the same text is used for grep, verbatim checks and prompts."""
    parts = []
    for i, m in enumerate(context):
        parts.append(f"[{i}] {m.get('role', '?')}\n{(m.get('content') or '').rstrip()}\n")
    return "\n".join(parts)


_WS = re.compile(r"\s+")


def norm(s: str) -> str:
    """Whitespace-collapse + casefold. Used for verbatim checks (not for detection)."""
    return _WS.sub(" ", (s or "").replace(" ", " ")).strip().casefold()


def contains_verbatim(haystack: str, needle: str) -> bool:
    return bool(needle) and norm(needle) in norm(haystack)
