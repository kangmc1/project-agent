"""Family C: reporting-only probes.

Probes are never used to accept or reject a generated contract test; they only
tell us how a passing detector behaves under rewordings it was not validated
on.  They therefore draw their weakening vocabulary exclusively from
``lexicon.L_PROBE``, which is disjoint from the injector's ``L_INJECT`` and from
the (empty) battery vocabulary.
"""
from __future__ import annotations

import random
import re

from .inject import (
    NUMBER_WORDS, WORD_NUMBERS, _content_end, _recap, find_phrase, find_phrases,
    kv_spans, make_rng,
)
from .lexicon import (
    BOUND_WORDS, L_PROBE, NEGATION_WORDS, QUANTITY_BOUNDS, TEMPORAL_BOUNDS,
    UNCERTAINTY_WORDS,
)
from .schema import Obligation

__all__ = ["probes", "make_rng"]

_QUANT_HEDGES = ("about", "more or less", "in the region of")
_TEMPORAL_HEDGES = ("perhaps",)
_MODAL_REPL = {"must": "would be nice", "only": "perhaps"}
_SETTLED = "settled"
# Probes may only introduce L_PROBE wording.
assert set(_QUANT_HEDGES) <= L_PROBE
assert set(_TEMPORAL_HEDGES) <= L_PROBE
assert set(_MODAL_REPL.values()) <= L_PROBE
assert _SETTLED in L_PROBE


def _case(text: str, expected: bool, name: str) -> dict:
    return {"text": text, "expected": expected, "name": name}


def _negation_spans(text: str):
    """Bound words swallowed by a negation ("must not") must be left alone."""
    return [(s, e) for _, s, e in find_phrases(text, NEGATION_WORDS)]


#: Closed-class openers that may be safely lower-cased when a clause moves out
#: of sentence-initial position (never a proper noun).
_DECAP_OK = {
    "the", "a", "an", "this", "that", "these", "those", "it", "they", "we",
    "you", "he", "she", "there", "his", "her", "their", "our", "its", "and",
    "but", "so", "please", "keep", "do", "if", "when", "then", "also",
}


def _decap(clause: str) -> str:
    first = clause.split()[0].strip(".,;:!?") if clause.split() else ""
    if first.lower() in _DECAP_OK and first[:1].isupper():
        return clause[0].lower() + clause[1:]
    return clause


def _swap_clauses(ev: str) -> str | None:
    """Swap the first two comma-separated clauses (order is not meaning)."""
    end = _content_end(ev)
    body, tail = ev[:end], ev[end:]
    parts = re.split(r",\s*", body)
    if len(parts) < 2 or not all(p.strip() for p in parts[:2]):
        return None
    parts[0], parts[1] = parts[1], _decap(parts[0])
    return _recap(ev, ", ".join(parts)) + tail


def _numeral_word(ev: str) -> str | None:
    """Rewrite one small integer as a word (or one number word as a numeral)."""
    for m in re.finditer(r"(?<![0-9A-Za-z_.,$€£¥])(\d{1,2})(?![0-9A-Za-z_.:%])", ev):
        n = int(m.group(1))
        if n in NUMBER_WORDS:
            return ev[:m.start(1)] + NUMBER_WORDS[n] + ev[m.end(1):]
    for m in re.finditer(r"(?<![0-9A-Za-z_])([A-Za-z]+)(?![0-9A-Za-z_])", ev):
        n = WORD_NUMBERS.get(m.group(1).lower())
        if n is not None:
            return ev[:m.start(1)] + str(n) + ev[m.end(1):]
    return None


def _weaken_bound(ev: str, marks, rng: random.Random) -> str | None:
    hit = find_phrase(ev, BOUND_WORDS, avoid=list(marks) + _negation_spans(ev))
    if not hit:
        return None
    phrase, s, e = hit
    low = phrase.lower()
    if low in _MODAL_REPL:
        repl = _MODAL_REPL[low]
    elif low in TEMPORAL_BOUNDS and low not in QUANTITY_BOUNDS:
        repl = f"{rng.choice(_TEMPORAL_HEDGES)} {ev[s:e]}"
    else:
        repl = rng.choice(_QUANT_HEDGES)
    if ev[s:e][:1].isupper():
        repl = repl[0].upper() + repl[1:]
    return ev[:s] + repl + ev[e:]


def _settle(ev: str, marks) -> str | None:
    hit = find_phrase(ev, [w for w in UNCERTAINTY_WORDS if w.strip("? ")], avoid=marks)
    if not hit:
        return None
    _, s, e = hit
    while s >= 6 and ev[s - 6:s].lower() == "still ":
        s -= 6
    repl = _SETTLED.capitalize() if ev[s:e][:1].isupper() else _SETTLED
    return ev[:s] + repl + ev[e:]


def probes(ob: Obligation, rng: random.Random) -> list[dict]:
    """Reporting-only positives (meaning-preserving) and negatives (weakened)."""
    ev = ob.evidence or ""
    if not ev.strip():
        return []
    marks = kv_spans(ev, ob)
    out: list[dict] = []
    for builder, expected, name in (
        (lambda: _swap_clauses(ev), True, "c_clause_swap"),
        (lambda: _numeral_word(ev), True, "c_numeral_word"),
        (lambda: _weaken_bound(ev, marks, rng), False, "c_weaken_bound"),
        (lambda: _settle(ev, marks) if ob.type == "open_question" else None,
         False, "c_settled"),
    ):
        text = builder()
        if text and text != ev:
            out.append(_case(text, expected, name))
    return out
