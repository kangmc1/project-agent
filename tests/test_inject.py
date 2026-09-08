"""Injection contract: what each defect kind must do to a real handoff message."""
import re

import pytest

from handoffcheck.inject import (
    alter_value, find_spans, inject_absent, inject_altered_semantic,
    inject_altered_value, insert_fabricated, make_rng, present, split_units,
)
from handoffcheck.schema import Obligation

MESSAGE = (
    "Handing off the Osaka trip for Olivia Gonzalez (customer olivia_gonzalez_2305).\n"
    "Keep the total at most $200 for the whole booking.\n"
    "The party is 3 passengers travelling together.\n"
    "The existing reservation is K7Q2 and it stays active.\n"
    "Do not cancel the original booking under any circumstances.\n"
    "The return date is still unconfirmed, so ask the customer before you book.\n"
    "Please find martial arts classes near the NYSE and list their addresses.\n"
)

LAST_SENTENCE = "Please find martial arts classes near the NYSE and list their addresses."

BUDGET = Obligation(
    id="ob_budget", type="constraint", statement="total budget is capped at $200",
    key_values=["$200"], evidence="Keep the total at most $200 for the whole booking.",
    numeric={"value": 200.0, "unit": "USD", "direction": "max"})
PARTY = Obligation(
    id="ob_party", type="constraint", statement="the party is 3 passengers",
    key_values=["3 passengers"], evidence="The party is 3 passengers travelling together.",
    numeric={"value": 3.0, "unit": "passengers", "direction": "eq"})
RESERVATION = Obligation(
    id="ob_res", type="verified_fact", statement="reservation K7Q2 is active",
    key_values=["K7Q2"], evidence="The existing reservation is K7Q2 and it stays active.")
NO_CANCEL = Obligation(
    id="ob_cancel", type="prohibition", statement="never cancel the original booking",
    key_values=["cancel the original booking"],
    evidence="Do not cancel the original booking under any circumstances.", negated=True)
RETURN_DATE = Obligation(
    id="ob_return", type="open_question", statement="the return date is not settled",
    key_values=["return date"],
    evidence="The return date is still unconfirmed, so ask the customer before you book.")
GOAL = Obligation(
    id="ob_goal", type="goal", statement="find martial arts classes near the NYSE",
    key_values=["martial arts classes", "NYSE"], evidence=LAST_SENTENCE)

OBLIGATIONS = [BUDGET, PARTY, RESERVATION, NO_CANCEL, RETURN_DATE, GOAL]
ALTERABLE = [BUDGET, PARTY, RESERVATION]


def rng_for(ob, seed=17):
    return make_rng(seed, "b_test", ob.id)


def others_of(ob):
    return [o for o in OBLIGATIONS if o.id != ob.id]


def test_all_obligations_present_in_clean_message():
    for ob in OBLIGATIONS:
        assert present(MESSAGE, ob), ob.id


def test_aliases_stand_in_only_for_their_own_key_value():
    """A flat alias list is attached to a kv by surface-form overlap."""
    msg = "The cap is 1,200 dollars and the party is 3 passengers."
    ob = Obligation("a", "constraint", "cap", ["$1,200"], msg,
                    {"value": 1200.0, "unit": "USD", "direction": "max"},
                    aliases=["1,200 dollars"])
    assert present(msg, ob)
    unrelated = Obligation("b", "constraint", "cap", ["$999"], msg,
                           aliases=["3 passengers"])
    assert not present(msg, unrelated), "an unrelated alias must not satisfy a kv"


def test_injections_return_none_when_the_key_value_is_absent():
    msg = "Nothing relevant here."
    ghost = Obligation("g", "constraint", "cap", ["$200"], msg,
                       {"value": 200.0, "unit": "USD", "direction": "max"})
    rng = make_rng(0, "b", "g")
    assert inject_absent(msg, ghost, [], rng) is None
    assert inject_altered_value(msg, ghost, [], rng) is None
    assert inject_altered_semantic(msg, ghost, rng) is None


# --------------------------------------------------------------- absent

@pytest.mark.parametrize("ob", OBLIGATIONS, ids=lambda o: o.id)
def test_absent_removes_target_and_keeps_others(ob):
    out = inject_absent(MESSAGE, ob, others_of(ob), rng_for(ob))
    assert out is not None
    assert out["level"] in ("sentence", "clause")
    assert out["removed_spans"]
    assert not present(out["message"], ob)
    for other in others_of(ob):
        assert present(out["message"], other), other.id
    assert out["message"] != MESSAGE


def test_absent_falls_back_to_clause_level():
    msg = ("Please book the 9:00 am flight, keep the total at most $200 "
           "and email the receipt to olivia_gonzalez_2305.")
    cap = Obligation("c", "constraint", "cap", ["$200"], msg,
                     {"value": 200.0, "unit": "USD", "direction": "max"})
    receipt = Obligation("r", "goal", "receipt", ["olivia_gonzalez_2305"], msg)
    flight = Obligation("f", "constraint", "flight", ["9:00 am"], msg)
    out = inject_absent(msg, cap, [receipt, flight], make_rng(1, "b", "c"))
    assert out is not None and out["level"] == "clause"
    assert not present(out["message"], cap)
    assert present(out["message"], receipt) and present(out["message"], flight)


# --------------------------------------------------------- altered_value

@pytest.mark.parametrize("ob", ALTERABLE, ids=lambda o: o.id)
def test_altered_value_changes_value_and_keeps_others(ob):
    out = inject_altered_value(MESSAGE, ob, others_of(ob), rng_for(ob))
    assert out is not None
    assert out["kv"] in ob.key_values
    assert out["new_kv"] != out["kv"]
    assert out["message"] != MESSAGE
    assert not find_spans(out["message"], out["kv"])
    for other in others_of(ob):
        assert present(out["message"], other), other.id


@pytest.mark.parametrize("ob", [NO_CANCEL, RETURN_DATE, GOAL], ids=lambda o: o.id)
def test_altered_value_declines_non_value_obligations(ob):
    assert inject_altered_value(MESSAGE, ob, others_of(ob), rng_for(ob)) is None


# ------------------------------------------------------ altered_semantic

@pytest.mark.parametrize("ob", OBLIGATIONS, ids=lambda o: o.id)
def test_altered_semantic_keeps_key_values_but_changes_message(ob):
    out = inject_altered_semantic(MESSAGE, ob, rng_for(ob))
    assert out is not None, ob.id
    assert out["message"] != MESSAGE
    assert present(out["message"], ob), "key value tokens must survive"
    assert out["rule"].startswith(ob.type + ":")


def test_altered_semantic_rules_are_type_specific():
    seen = {ob.id: inject_altered_semantic(MESSAGE, ob, rng_for(ob))["rule"]
            for ob in OBLIGATIONS}
    assert seen["ob_budget"] == "constraint:weaken_bound"
    assert seen["ob_party"] == "constraint:hedge_number"
    assert seen["ob_res"] == "verified_fact:hedge_copula"
    assert seen["ob_cancel"].startswith("prohibition:")
    assert seen["ob_return"] == "open_question:mark_confirmed"
    assert seen["ob_goal"] == "goal:drop_conjunct"


def test_altered_semantic_prohibition_drops_the_negation():
    out = inject_altered_semantic(MESSAGE, NO_CANCEL, rng_for(NO_CANCEL))
    line = [l for l in out["message"].splitlines()
            if "cancel the original" in l.lower()][0]
    assert not line.lower().startswith("do not")
    assert "cancel the original booking" in line.lower()


def test_altered_semantic_goal_drops_a_conjunct_without_key_values():
    out = inject_altered_semantic(MESSAGE, GOAL, rng_for(GOAL))
    assert "list their addresses" not in out["message"]
    assert "martial arts classes" in out["message"] and "NYSE" in out["message"]


# ------------------------------------------------------------ alter_value

@pytest.mark.parametrize("kv", [
    "$200", "1,250", "$1,250.50", "3 passengers", "15%", "500 USD",
    "2015-08-05", "08/05/2015", "August 5, 2015", "5 Aug 2015", "Aug 5",
    "7:30 pm", "19:30", "9 AM", "K7Q2", "olivia_gonzalez_2305", "HAT001",
])
def test_alter_value_never_returns_the_same_string(kv):
    for seed in range(12):
        out = alter_value(kv, make_rng(seed, "b", "o"))
        assert out is not None and out != kv


@pytest.mark.parametrize("kv", ["Olivia Gonzalez", "martial arts classes", "Osaka"])
def test_alter_value_declines_plain_words(kv):
    assert alter_value(kv, make_rng(0, "b", "o")) is None


def test_alter_value_number_keeps_format_and_moves_10_to_50_percent():
    for seed in range(12):
        out = alter_value("$200", make_rng(seed, "b", "o"))
        assert out.startswith("$") and "," not in out
        v = float(out[1:])
        assert v != 200.0 and 19 <= abs(v - 200.0) <= 101
    assert alter_value("1,250", make_rng(0, "b", "o")).replace(",", "").isdigit()
    pct = alter_value("15%", make_rng(0, "b", "o"))
    assert pct.endswith("%") and pct != "15%"
    pax = alter_value("3 passengers", make_rng(0, "b", "o"))
    assert pax.endswith(" passengers") and pax != "3 passengers"


@pytest.mark.parametrize("kv,pattern", [
    ("2015-08-05", r"^\d{4}-\d{2}-\d{2}$"),
    ("08/05/2015", r"^\d{2}/\d{2}/\d{4}$"),
    ("August 5, 2015", r"^[A-Z][a-z]+ \d{1,2}, \d{4}$"),
    ("5 Aug 2015", r"^\d{1,2} [A-Z][a-z]{2} \d{4}$"),
    ("Aug 5", r"^[A-Z][a-z]{2} \d{1,2}$"),
    ("7:30 pm", r"^\d{1,2}:30 (am|pm)$"),
    ("19:30", r"^\d{2}:30$"),
])
def test_alter_value_keeps_date_and_time_format(kv, pattern):
    for seed in range(8):
        out = alter_value(kv, make_rng(seed, "b", "o"))
        assert re.match(pattern, out), (kv, out)


def test_alter_value_id_changes_exactly_two_characters():
    for kv in ("K7Q2", "HAT001", "olivia_gonzalez_2305"):
        for seed in range(8):
            out = alter_value(kv, make_rng(seed, "b", "o"))
            assert len(out) == len(kv)
            diff = [(a, b) for a, b in zip(kv, out) if a != b]
            assert len(diff) == 2
            for a, b in diff:
                assert a.isdigit() == b.isdigit()
                if a.isalpha():
                    assert a.isupper() == b.isupper()


# ------------------------------------------------------------- fabricated

def test_insert_fabricated_goes_before_the_last_sentence():
    claim = "The airline waived the change fee"
    out = insert_fabricated(MESSAGE, claim)
    assert claim + "." in out
    assert out.index(claim) < out.index(LAST_SENTENCE)
    assert len(split_units(out)) == len(split_units(MESSAGE)) + 1


def test_insert_fabricated_appends_when_there_is_one_sentence():
    out = insert_fabricated("Book the cheapest flight.", "The fee was waived")
    assert out == "Book the cheapest flight. The fee was waived."


# ---------------------------------------------------------- determinism

@pytest.mark.parametrize("ob", OBLIGATIONS, ids=lambda o: o.id)
def test_injections_are_deterministic_for_a_seed(ob):
    for fn in (lambda o, r: inject_absent(MESSAGE, o, others_of(o), r),
               lambda o, r: inject_altered_value(MESSAGE, o, others_of(o), r),
               lambda o, r: inject_altered_semantic(MESSAGE, o, r)):
        assert fn(ob, rng_for(ob)) == fn(ob, rng_for(ob))
