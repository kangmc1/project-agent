"""Battery (held-out acceptance) and probe (reporting-only) contracts."""
import re

import pytest

from handoffcheck.battery import battery, family_a, family_a_plus
from handoffcheck.inject import find_spans, kv_present, make_rng
from handoffcheck.lexicon import (
    L_BATTERY, L_INJECT, L_PROBE, assert_disjoint,
)
from handoffcheck.probes import probes
from handoffcheck.schema import Obligation

BUDGET = Obligation(
    id="ob_budget", type="constraint", statement="the total is capped at $1,200",
    key_values=["$1,200"], evidence="Keep the total at most $1,200 for the whole booking.",
    numeric={"value": 1200.0, "unit": "USD", "direction": "max"})
PARTY = Obligation(
    id="ob_party", type="constraint", statement="the party is 3 passengers",
    key_values=["3 passengers"], evidence="The party is 3 passengers travelling together.",
    numeric={"value": 3.0, "unit": "passengers", "direction": "eq"})
PICKUP = Obligation(
    id="ob_pickup", type="constraint", statement="the driver arrives by 5 pm",
    key_values=["5 pm"], evidence="The driver must arrive by 5 pm at the latest.",
    numeric={"value": 17.0, "unit": "time", "direction": "max"})
NO_CANCEL = Obligation(
    id="ob_cancel", type="prohibition", statement="never cancel the original booking",
    key_values=["cancel the original booking"],
    evidence="Do not cancel the original booking under any circumstances.", negated=True)
RETURN_DATE = Obligation(
    id="ob_return", type="open_question", statement="the return date is not settled",
    key_values=["return date"],
    evidence="The return date is still unknown, so ask the customer first.")
RESERVATION = Obligation(
    id="ob_res", type="verified_fact", statement="reservation K7Q2 is active",
    key_values=["K7Q2"], evidence="The existing reservation (K7Q2) is active.")

OBLIGATIONS = [BUDGET, PARTY, PICKUP, NO_CANCEL, RETURN_DATE, RESERVATION]


# ------------------------------------------------------------- lexicon

def test_replacement_vocabularies_are_disjoint():
    assert_disjoint()
    assert L_BATTERY == frozenset()
    assert not (L_INJECT & L_PROBE)


# ------------------------------------------------------------- family A

@pytest.mark.parametrize("ob", OBLIGATIONS, ids=lambda o: o.id)
def test_family_a_positives_keep_every_key_value(ob):
    cases = family_a(ob)
    names = [c["name"] for c in cases]
    assert names[:3] == ["a_exact", "a_lower_ws", "a_no_punct"]
    for case in cases:
        if not case["expected"]:
            continue
        for kv in ob.key_values:
            assert kv_present(case["text"], kv, ob.aliases), (case["name"], kv)


@pytest.mark.parametrize("ob", OBLIGATIONS, ids=lambda o: o.id)
def test_family_a_deletion_negatives_lose_their_key_value(ob):
    for case in family_a(ob):
        m = re.fullmatch(r"a_del_kv(\d+)", case["name"])
        if not m:
            continue
        assert case["expected"] is False
        kv = ob.key_values[int(m.group(1))]
        assert not kv_present(case["text"], kv, ob.aliases)
        assert case["text"] != ob.evidence and case["text"].strip()


def test_family_a_digit_negatives_change_the_value():
    case = [c for c in family_a(BUDGET) if c["name"] == "a_digit_kv0"][0]
    assert case["expected"] is False
    assert not find_spans(case["text"], "$1,200")
    assert "$1,201" in case["text"]


def test_family_a_no_punct_keeps_numbers_and_ids_intact():
    text = [c for c in family_a(BUDGET) if c["name"] == "a_no_punct"][0]["text"]
    assert "$1,200" in text and text.endswith("booking")
    text = [c for c in family_a(RESERVATION) if c["name"] == "a_no_punct"][0]["text"]
    assert "K7Q2" in text and "(" not in text


# ------------------------------------------------------------ family A+

def test_family_a_plus_comma_toggle_drops_the_original_number_form():
    case = [c for c in family_a_plus(BUDGET) if c["name"] == "aplus_commas"][0]
    assert case["expected"] is True
    assert "1,200" not in case["text"]
    assert "$1200" in case["text"]
    assert find_spans(case["text"], "$1,200"), "still the same value"


def test_family_a_plus_currency_and_word_and_time_forms():
    names = {c["name"]: c for c in family_a_plus(BUDGET)}
    assert "1,200 USD" in names["aplus_cur_code"]["text"]
    assert "1,200 dollars" in names["aplus_cur_word"]["text"]
    assert all(c["expected"] for n, c in names.items() if n.startswith("aplus_cur"))
    assert "three passengers" in {c["name"]: c["text"] for c in family_a_plus(PARTY)}["aplus_words"]
    assert "17:00" in {c["name"]: c["text"] for c in family_a_plus(PICKUP)}["aplus_time"]


def test_family_a_plus_negatives_are_deletion_only():
    """No replacement wording may appear in a battery negative."""
    for ob in OBLIGATIONS:
        for case in family_a_plus(ob):
            if case["expected"]:
                continue
            assert len(case["text"]) < len(ob.evidence)
            for phrase in L_INJECT | L_PROBE:
                assert not re.search(rf"\b{re.escape(phrase)}\b", case["text"], re.I)


def test_family_a_plus_deletes_the_bound_that_governs_the_value():
    assert [c for c in family_a_plus(BUDGET) if c["name"] == "aplus_del_bound"][0][
        "text"] == "Keep the total $1,200 for the whole booking."
    assert [c for c in family_a_plus(PICKUP) if c["name"] == "aplus_del_bound"][0][
        "text"] == "The driver must arrive 5 pm at the latest."
    # direction "eq" has no bound to widen
    assert not [c for c in family_a_plus(PARTY) if c["name"] == "aplus_del_bound"]


def test_family_a_plus_negation_deletion_for_prohibitions():
    case = [c for c in family_a_plus(NO_CANCEL) if c["name"] == "aplus_del_negation"][0]
    assert case["expected"] is False
    assert case["text"].lower().startswith("cancel the original booking")


def test_family_a_plus_is_empty_when_not_applicable():
    assert family_a_plus(RESERVATION) == []


# --------------------------------------------------------------- battery

@pytest.mark.parametrize("ob", OBLIGATIONS, ids=lambda o: o.id)
def test_battery_names_are_unique_and_cover_both_families(ob):
    cases = battery(ob)
    names = [c["name"] for c in cases]
    assert len(names) == len(set(names))
    assert [c["text"] for c in cases] == [
        c["text"] for c in family_a(ob) + family_a_plus(ob)]
    assert any(c["expected"] for c in cases) and any(not c["expected"] for c in cases)
    assert all(set(c) == {"text", "expected", "name"} for c in cases)
    assert all(isinstance(c["expected"], bool) and c["text"].strip() for c in cases)


# ---------------------------------------------------------------- probes

@pytest.mark.parametrize("ob", OBLIGATIONS, ids=lambda o: o.id)
def test_probes_never_use_injection_wording(ob):
    for case in probes(ob, make_rng(5, "b_test", ob.id)):
        for phrase in L_INJECT:
            rx = rf"\b{re.escape(phrase)}\b"
            assert len(re.findall(rx, case["text"], re.I)) <= \
                len(re.findall(rx, ob.evidence, re.I)), (ob.id, case["name"], phrase)


def test_probes_build_the_expected_cases():
    names = {c["name"]: c for c in probes(BUDGET, make_rng(5, "b", BUDGET.id))}
    assert names["c_weaken_bound"]["expected"] is False
    assert "at most" not in names["c_weaken_bound"]["text"]
    assert any(p in names["c_weaken_bound"]["text"] for p in L_PROBE)
    names = {c["name"]: c for c in probes(RETURN_DATE, make_rng(5, "b", RETURN_DATE.id))}
    assert names["c_settled"]["text"] == "The return date is settled, so ask the customer first."
    assert names["c_clause_swap"]["expected"] is True
    assert names["c_clause_swap"]["text"] == \
        "So ask the customer first, the return date is still unknown."
    assert "three passengers" in {
        c["name"]: c["text"] for c in probes(PARTY, make_rng(5, "b", PARTY.id))}["c_numeral_word"]


@pytest.mark.parametrize("ob", OBLIGATIONS, ids=lambda o: o.id)
def test_probes_are_deterministic(ob):
    assert probes(ob, make_rng(5, "b", ob.id)) == probes(ob, make_rng(5, "b", ob.id))
