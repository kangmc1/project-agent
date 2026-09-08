"""Held-out acceptance battery for one obligation.

These cases decide whether a generated contract test is *good enough*: family A
checks that trivially-equivalent renderings of the evidence still pass and that
losing the key value fails; family A+ checks robustness to number surface forms
and sensitivity to a silently dropped bound / negation.

The agent never sees this module's output.  Deliberately, family A+ negatives
are DELETION-ONLY (``lexicon.L_BATTERY`` is empty): no replacement wording is
introduced here, so passing the battery cannot be reduced to memorising the
weakeners that ``inject`` or ``probes`` use.

Every function is deterministic: no rng at all.
"""
from __future__ import annotations

import re
import string

from .inject import (
    CURRENCY_SYMBOLS, NUMBER_WORDS, _NUM_NEEDLE, _add_commas, _recap, _strip_commas,
    delete_spans, find_phrase, find_phrases, find_spans, kv_present, kv_spans,
    replace_spans,
)
from .lexicon import BOUND_WORDS, NEGATION_WORDS
from .schema import Obligation

_PUNCT = set(string.punctuation) | set(CURRENCY_SYMBOLS)
_CURRENCY_UNITS = {
    "usd": ("$", "USD", "dollars"), "$": ("$", "USD", "dollars"),
    "dollar": ("$", "USD", "dollars"), "dollars": ("$", "USD", "dollars"),
    "eur": ("€", "EUR", "euros"), "€": ("€", "EUR", "euros"),
    "euro": ("€", "EUR", "euros"), "euros": ("€", "EUR", "euros"),
    "gbp": ("£", "GBP", "pounds"), "£": ("£", "GBP", "pounds"),
    "pound": ("£", "GBP", "pounds"), "pounds": ("£", "GBP", "pounds"),
}


def _case(text: str, expected: bool, name: str) -> dict:
    return {"text": text, "expected": expected, "name": name}


def _lower_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()


def _strip_punct(s: str) -> str:
    """Drop punctuation, but keep it where it is part of a number or an id."""
    out = []
    for i, ch in enumerate(s):
        if ch not in _PUNCT:
            out.append(ch)
            continue
        prev = s[i - 1] if i else ""
        nxt = s[i + 1] if i + 1 < len(s) else ""
        inside_token = prev.isalnum() and nxt.isalnum()
        currency = ch in CURRENCY_SYMBOLS and nxt.isdigit()
        percent = ch == "%" and prev.isdigit()
        if inside_token or currency or percent:
            out.append(ch)
    return re.sub(r"\s+", " ", "".join(out)).strip()


def _bump_digits(text: str, spans) -> str | None:
    """Change one digit inside every occurrence of a key value."""
    out, changed = text, False
    for s, e in sorted(set(spans), reverse=True):
        piece = text[s:e]
        pos = max((i for i, c in enumerate(piece) if c.isdigit()), default=None)
        if pos is None:
            continue
        d = str((int(piece[pos]) + 1) % 10)
        out = out[:s] + piece[:pos] + d + piece[pos + 1:] + out[e:]
        changed = True
    return out if changed else None


def family_a(ob: Obligation) -> list[dict]:
    """Surface-invariance positives + key-value-loss negatives."""
    ev = ob.evidence or ""
    out = [
        _case(ev, True, "a_exact"),
        _case(_lower_ws(ev), True, "a_lower_ws"),
        _case(_strip_punct(ev), True, "a_no_punct"),
    ]
    for i, kv in enumerate(ob.key_values):
        spans = find_spans(ev, kv)
        if not spans:
            continue
        gone = _recap(ev, delete_spans(ev, spans))
        if gone.strip() and gone != ev and not kv_present(gone, kv, ob.aliases):
            out.append(_case(gone, False, f"a_del_kv{i}"))
        if any(c.isdigit() for c in kv):
            bumped = _bump_digits(ev, spans)
            if bumped and bumped != ev and not kv_present(bumped, kv, ob.aliases):
                out.append(_case(bumped, False, f"a_digit_kv{i}"))
    return out


# --- A+ surface forms -------------------------------------------------------

_T12 = re.compile(r"^(\d{1,2})(?::(\d{2}))?\s*([APap]\.?[Mm]\.?)$")
_T24 = re.compile(r"^(\d{1,2}):(\d{2})$")


def _numeric_kv(kv: str) -> re.Match | None:
    return _NUM_NEEDLE.match((kv or "").strip())


def _time_alt(s: str) -> str | None:
    m = _T12.match(s)
    if m:
        h, mi, mer = m.groups()
        h24 = (int(h) % 12) + (12 if mer.lower().startswith("p") else 0)
        return f"{h24:02d}:{mi or '00'}"
    m = _T24.match(s)
    if m:
        h, mi = int(m.group(1)), m.group(2)
        if h > 23:
            return None
        mer = "pm" if h >= 12 else "am"
        h12 = h % 12 or 12
        return f"{h12} {mer}" if mi == "00" else f"{h12}:{mi} {mer}"
    return None


def _surface_forms(kv: str, matched: str, unit: str) -> list[tuple[str, str]]:
    """(replacement, case-name-suffix) renderings of the same value."""
    forms: list[tuple[str, str]] = []
    alt_time = _time_alt(matched.strip()) or _time_alt(kv.strip())
    if alt_time:
        forms.append((alt_time, "time"))
    m = _NUM_NEEDLE.match(matched.strip()) or _numeric_kv(kv)
    if not m:
        return forms
    num, cur = m.group("num"), (m.group("cur") or "")
    suf = (m.group("suf") or "").strip()
    plain, commas = _strip_commas(num), None
    try:
        commas = _add_commas(plain)
    except ValueError:
        commas = plain
    toggled = plain if "," in num else commas
    if toggled != num:
        forms.append((f"{cur}{toggled}{(' ' + suf) if suf else ''}", "commas"))
    sym_unit = _CURRENCY_UNITS.get((unit or "").strip().lower()) or (
        _CURRENCY_UNITS.get(cur) if cur else None)
    if sym_unit:
        sym, code, word = sym_unit
        for cand, tag in ((f"{sym}{num}", "cur_symbol"),
                          (f"{num} {code}", "cur_code"),
                          (f"{num} {word}", "cur_word")):
            if cand.lower() != matched.strip().lower():
                forms.append((cand, tag))
    is_time = bool(alt_time) or bool(_T12.match(matched.strip()))
    if "." not in plain and not cur and not is_time:
        try:
            n = int(plain)
        except ValueError:
            n = None
        if n is not None and n in NUMBER_WORDS:
            forms.append((f"{NUMBER_WORDS[n]}{(' ' + suf) if suf else ''}", "words"))
    return forms


def _bound_near_value(ev: str, marks) -> tuple[str, int, int] | None:
    """The bound phrase that governs the value: the one closest before a kv."""
    hits = find_phrases(ev, BOUND_WORDS, avoid=marks)
    if not hits:
        return None
    scored = []
    for phrase, s, e in hits:
        gaps = [a - e for a, _ in marks if a >= e]
        scored.append(((min(gaps) if gaps else 10 ** 6), -(e - s), s, (phrase, s, e)))
    return min(scored)[3]


def family_a_plus(ob: Obligation) -> list[dict]:
    """Numeric surface-form positives + deletion-only weakening negatives."""
    ev = ob.evidence or ""
    out: list[dict] = []
    num = ob.numeric or {}
    marks = kv_spans(ev, ob)

    if num:
        for kv in ob.key_values:
            spans = find_spans(ev, kv)
            if not spans or not _numeric_kv(kv):
                continue
            for repl, tag in _surface_forms(kv, ev[spans[0][0]:spans[0][1]],
                                            str(num.get("unit") or "")):
                text = replace_spans(ev, spans, repl, fit=False)
                if text != ev:
                    out.append(_case(text, True, f"aplus_{tag}"))
            break

    if num and str(num.get("direction") or "") != "eq":
        hit = _bound_near_value(ev, marks)
        if hit:
            _, s, e = hit
            text = _recap(ev, delete_spans(ev, [(s, e)]))
            if text.strip() and text != ev:
                out.append(_case(text, False, "aplus_del_bound"))

    # Resolved ambiguity: the negation negative is gated on ob.negated only --
    # a prohibition need not carry a numeric field to be weakened by dropping
    # its negation.
    if ob.negated:
        hit = find_phrase(ev, NEGATION_WORDS, avoid=marks)
        if hit:
            _, s, e = hit
            text = _recap(ev, delete_spans(ev, [(s, e)]))
            if text.strip() and text != ev:
                out.append(_case(text, False, "aplus_del_negation"))
    return out


def battery(ob: Obligation) -> list[dict]:
    """Family A + family A+, with unique case names."""
    cases, seen = [], {}
    for c in family_a(ob) + family_a_plus(ob):
        name = c["name"]
        if name in seen:
            seen[name] += 1
            c = dict(c, name=f"{name}#{seen[name]}")
        else:
            seen[name] = 0
        cases.append(c)
    return cases
