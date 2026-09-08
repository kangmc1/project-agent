"""Replacement vocabularies, kept DISJOINT per consumer.

The point of the split: the acceptance battery (what the detector is *validated*
on) must never share replacement wording with the injections it is *evaluated*
on, nor with the reporting-only probes.  Otherwise the agent could pass the
battery by pattern-matching the exact weakener strings that the injector uses.

  L_INJECT   -> inject.inject_altered_semantic  (evaluation set)
  L_PROBE    -> probes.probes                   (reporting only, family C)
  L_BATTERY  -> battery.*                       (EMPTY on purpose: the battery's
                                                 weakening negatives are
                                                 DELETION-ONLY)

BOUND_WORDS / NEGATION_WORDS / UNCERTAINTY_WORDS are *source* vocabularies: they
name wording that is already in the message.  They are not replacements, so they
are exempt from the disjointness rule.
"""
from __future__ import annotations

# --- replacement vocabularies (must stay pairwise disjoint) ------------------

L_INJECT: frozenset[str] = frozenset({
    "approximately",
    "around",
    "roughly",
    "ideally",
    "preferably",
    "if possible",
    "should ideally",
    "is probably",
    "seems to be",
    "confirmed",
    "verified",
})

L_PROBE: frozenset[str] = frozenset({
    "about",
    "give or take",
    "as a rough guide",
    "more or less",
    "in the region of",
    "would be nice",
    "i believe",
    "perhaps",
    "reportedly",
    "settled",
})

#: Empty on purpose.  Battery A+ negatives delete bound/negation wording; they
#: never substitute new wording.
L_BATTERY: frozenset[str] = frozenset()

# --- source vocabularies (already present in the message) --------------------

#: Bound / direction keywords whose deletion silently widens a constraint.
BOUND_WORDS: frozenset[str] = frozenset({
    "at most",
    "no more than",
    "not more than",
    "up to",
    "maximum of",
    "a maximum of",
    "max",
    "at least",
    "a minimum of",
    "minimum of",
    "no less than",
    "not less than",
    "must",
    "only",
    "exactly",
    "no later than",
    "by",
    "within",
    "before",
    "after",
    "strictly",
})

#: Bound phrases that constrain a quantity: dropping them removes the direction.
QUANTITY_BOUNDS: frozenset[str] = frozenset({
    "at most", "no more than", "not more than", "up to", "maximum of",
    "a maximum of", "max", "at least", "a minimum of", "minimum of",
    "no less than", "not less than", "exactly",
})

#: Bound phrases that constrain a deadline / ordering.
TEMPORAL_BOUNDS: frozenset[str] = frozenset({
    "no later than", "by", "within", "before", "after", "strictly",
})

#: Modal bounds.
MODAL_BOUNDS: frozenset[str] = frozenset({"must", "only"})

NEGATION_WORDS: frozenset[str] = frozenset({
    "do not",
    "don't",
    "does not",
    "doesn't",
    "must not",
    "mustn't",
    "should not",
    "shouldn't",
    "cannot",
    "can't",
    "never",
    "no ",
    "not ",
})

UNCERTAINTY_WORDS: frozenset[str] = frozenset({
    "unconfirmed",
    "not yet confirmed",
    "to be confirmed",
    "still unknown",
    "unknown",
    "unclear",
    "pending",
    "not sure",
    "need to confirm",
    "needs confirmation",
    "tbd",
    "?",
})

_REPLACEMENT_VOCABS = {
    "L_INJECT": L_INJECT,
    "L_PROBE": L_PROBE,
    "L_BATTERY": L_BATTERY,
}


def assert_disjoint() -> None:
    """Raise ValueError if any two replacement vocabularies overlap."""
    names = sorted(_REPLACEMENT_VOCABS)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            overlap = _REPLACEMENT_VOCABS[a] & _REPLACEMENT_VOCABS[b]
            if overlap:
                raise ValueError(
                    f"replacement vocabularies {a} and {b} overlap: {sorted(overlap)}")
    if L_BATTERY:
        raise ValueError("L_BATTERY must stay empty: battery negatives are deletion-only")


assert_disjoint()
