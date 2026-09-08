"""Deterministic, surface-level defect injection at a handoff boundary.

Every function is pure and takes an explicit ``random.Random``; the convention
for building it is ``make_rng(seed, boundary_id, ob.id)`` so a (seed, boundary,
obligation) triple always yields the same variant.

Injection kinds implemented here:
  absent            - the obligation's sentence(s)/clause(s) are deleted
  altered_value     - a key value is changed (number / date / time / id)
  altered_semantic  - the *force* of the obligation is weakened, tokens intact
  fabricated        - an unsupported sentence is inserted

Only ``lexicon.L_INJECT`` wording may be introduced by altered_semantic.
"""
from __future__ import annotations

import random
import re
from datetime import date, timedelta

from .lexicon import (
    BOUND_WORDS, L_INJECT, NEGATION_WORDS, QUANTITY_BOUNDS, TEMPORAL_BOUNDS,
    UNCERTAINTY_WORDS,
)
from .schema import Obligation

CURRENCY_SYMBOLS = "$€£¥"
_WS_RE = re.compile(r"\s+")

NUMBER_WORDS: dict[int, str] = {
    0: "zero", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six",
    7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve",
    13: "thirteen", 14: "fourteen", 15: "fifteen", 16: "sixteen",
    17: "seventeen", 18: "eighteen", 19: "nineteen", 20: "twenty",
}
WORD_NUMBERS: dict[str, int] = {w: n for n, w in NUMBER_WORDS.items()}

_MONTHS = ["january", "february", "march", "april", "may", "june", "july",
           "august", "september", "october", "november", "december"]
_MONTH_IDX = {m: i + 1 for i, m in enumerate(_MONTHS)}
_MONTH_IDX.update({m[:3]: i + 1 for i, m in enumerate(_MONTHS)})
_MONTH_IDX["sept"] = 9

Span = tuple[int, int]


def make_rng(seed, boundary_id: str, ob_id: str) -> random.Random:
    """The one blessed way to derive randomness (see module docstring)."""
    return random.Random(f"{seed}:{boundary_id}:{ob_id}")


# --------------------------------------------------------------------------
# span search
# --------------------------------------------------------------------------

_NUM_NEEDLE = re.compile(
    r"^(?P<cur>[$€£¥])?(?P<sp1>\s*)"
    r"(?P<num>\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)"
    r"(?P<sp2>\s*)(?P<suf>%|[A-Za-z][A-Za-z%./\- ]*)?$"
)


def _ws_tolerant(s: str) -> str:
    return r"\s+".join(re.escape(p) for p in _WS_RE.split(s.strip()) if p)


def _strip_commas(n: str) -> str:
    return n.replace(",", "")


def _add_commas(n: str) -> str:
    if "." in n:
        head, frac = n.split(".", 1)
        return f"{int(head):,}.{frac}"
    return f"{int(n):,}"


def _num_forms(num: str) -> set[str]:
    forms = {num, _strip_commas(num)}
    try:
        forms.add(_add_commas(_strip_commas(num)))
    except ValueError:
        pass
    return forms


def _needle_regex(needle: str):
    s = (needle or "").strip()
    if not s:
        return None
    m = _NUM_NEEDLE.match(s)
    if m:
        alts = "|".join(re.escape(f) for f in
                        sorted(_num_forms(m.group("num")), key=len, reverse=True))
        pat = (r"(?<![0-9A-Za-z_.,])(?:[" + re.escape(CURRENCY_SYMBOLS) + r"]\s*)?"
               r"(?:" + alts + r")")
        suf = (m.group("suf") or "").strip()
        if suf:
            pat += r"\s*" + _ws_tolerant(suf) + r"(?![0-9A-Za-z_])"
        else:
            pat += r"(?!\.?\d)(?![0-9A-Za-z_])"
        return re.compile(pat, re.IGNORECASE)
    pat = _ws_tolerant(s)
    if re.match(r"[0-9A-Za-z_]", s):
        pat = r"(?<![0-9A-Za-z_])" + pat
    if re.search(r"[0-9A-Za-z_]$", s):
        pat = pat + r"(?![0-9A-Za-z_])"
    return re.compile(pat, re.IGNORECASE)


def find_spans(text: str, needle: str) -> list[Span]:
    """Case-insensitive, whitespace-tolerant occurrences of ``needle``.

    Numeric needles additionally match thousands-separator variants and an
    optional leading currency symbol (which is included in the returned span).
    """
    rx = _needle_regex(needle)
    if rx is None or not text:
        return []
    return [(m.start(), m.end()) for m in rx.finditer(text)]


def _core(s: str) -> str:
    return re.sub(r"[^0-9a-z]+", "", (s or "").lower())


def _alias_applies(alias: str, kv: str) -> bool:
    """An alias only stands in for a key value it is a surface variant of.

    Resolved ambiguity: ``Obligation.aliases`` is a flat list, not a per-kv map,
    so an alias is attached to a kv when their alphanumeric cores coincide or
    one contains the other (>=2 chars).  Without this, an unrelated alias would
    keep ``present()`` true forever and no ``absent`` injection could verify.
    """
    a, k = _core(alias), _core(kv)
    if not a or not k:
        return False
    if a == k:
        return True
    return min(len(a), len(k)) >= 2 and (a in k or k in a)


def kv_present(text: str, kv: str, aliases=()) -> bool:
    if find_spans(text, kv):
        return True
    return any(_alias_applies(a, kv) and find_spans(text, a) for a in (aliases or ()))


def present(text: str, ob: Obligation) -> bool:
    """True iff every key value of ``ob`` (or an applicable alias) occurs."""
    return all(kv_present(text, kv, ob.aliases) for kv in ob.key_values)


def kv_spans(text: str, ob: Obligation) -> list[Span]:
    """Occurrence spans of every key value (falling back to applicable aliases)."""
    out: list[Span] = []
    for kv in ob.key_values:
        spans = find_spans(text, kv)
        if not spans:
            for a in (ob.aliases or ()):
                if _alias_applies(a, kv):
                    spans = find_spans(text, a)
                    if spans:
                        break
        out.extend(spans)
    return sorted(set(out))


def overlaps(span: Span, spans) -> bool:
    s, e = span
    return any(not (e <= a or s >= b) for a, b in spans)


def find_phrases(text: str, phrases, avoid=()) -> list[tuple[str, int, int]]:
    """Every occurrence of any phrase, skipping ``avoid`` spans, by position."""
    hits = []
    for p in sorted({p for p in phrases}):
        for s, e in find_spans(text, p):
            if not overlaps((s, e), avoid):
                hits.append((p.strip(), s, e))
    return sorted(hits, key=lambda h: (h[1], -(h[2] - h[1])))


def find_phrase(text: str, phrases, avoid=()) -> tuple[str, int, int] | None:
    """Longest (then earliest) occurrence of any phrase, skipping ``avoid`` spans."""
    hits = find_phrases(text, phrases, avoid)
    if not hits:
        return None
    return min(hits, key=lambda h: (-(h[2] - h[1]), h[1]))


# --------------------------------------------------------------------------
# segmentation
# --------------------------------------------------------------------------

_UNIT_END = re.compile(r"(?:[.!?;]+(?=\s|$)|\n+)")
_CLAUSE_END = re.compile(r",\s+|\s+and\s+|\s+but\s+", re.IGNORECASE)


def _spans_from_splits(text: str, start: int, end: int, rx) -> list[Span]:
    spans, cur = [], start
    for m in rx.finditer(text, start, end):
        seg = text[cur:m.end()]
        if seg.strip():
            lead = len(seg) - len(seg.lstrip())
            spans.append((cur + lead, cur + len(seg.rstrip())))
        cur = m.end()
    tail = text[cur:end]
    if tail.strip():
        lead = len(tail) - len(tail.lstrip())
        spans.append((cur + lead, cur + len(tail.rstrip())))
    return spans


def split_units(text: str) -> list[Span]:
    """Sentence spans (split on . ! ? newline, and ; before whitespace/end)."""
    return _spans_from_splits(text, 0, len(text), _UNIT_END)


def split_clauses(text: str) -> list[Span]:
    """Finer spans: sentences further split on ', ', ' and ', ' but '."""
    out: list[Span] = []
    for s, e in split_units(text):
        out.extend(_spans_from_splits(text, s, e, _CLAUSE_END))
    return out


# --------------------------------------------------------------------------
# deletion / replacement plumbing
# --------------------------------------------------------------------------

def _tidy(s: str) -> str:
    s = re.sub(r"[ \t]{2,}", " ", s)
    s = re.sub(r"[ \t]+([,.;:!?])", r"\1", s)
    s = re.sub(r"([,;:])\s*([.!?])", r"\2", s)
    s = re.sub(r"(?i)\b(and|but|or)\s*([.!?])", r"\2", s)
    s = re.sub(r"(?i)\b(and|but|or)\s*$", "", s)
    s = re.sub(r"\(\s*\)", "", s)
    s = re.sub(r"[ \t]+\n", "\n", s)
    s = re.sub(r"\n[ \t]+", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    s = re.sub(r"[ \t]{2,}", " ", s)
    return s.strip()


def _expand_cut(text: str, s: int, e: int) -> Span:
    line_start = text.rfind("\n", 0, s) + 1
    nl = text.find("\n", e)
    line_end = len(text) if nl < 0 else nl
    if not text[line_start:s].strip() and not text[e:line_end].strip():
        return line_start, min(line_end + 1, len(text))
    while e < len(text) and text[e] in " \t":
        e += 1
    return s, e


def delete_spans(text: str, spans, tidy: bool = True) -> str:
    out = text
    for s, e in sorted(set(spans), reverse=True):
        s2, e2 = _expand_cut(out, s, e)
        out = out[:s2] + out[e2:]
    return _tidy(out) if tidy else out


def _fit_replacement(matched: str, new_kv: str) -> str:
    """Make ``new_kv`` wear the surface clothes of the text it replaces."""
    m_cur = matched[:1] if matched[:1] in CURRENCY_SYMBOLS else ""
    n_cur = new_kv[:1] if new_kv[:1] in CURRENCY_SYMBOLS else ""
    out = new_kv
    if n_cur and not m_cur:
        out = out[1:].lstrip()
    elif m_cur and not n_cur:
        out = m_cur + out
    m_num = re.search(r"\d[\d,]*", matched)
    o_num = re.search(r"\d[\d,]*", out)
    if m_num and o_num:
        if "," not in m_num.group(0) and "," in o_num.group(0):
            out = out[:o_num.start()] + _strip_commas(o_num.group(0)) + out[o_num.end():]
        elif "," in m_num.group(0) and "," not in o_num.group(0):
            try:
                out = out[:o_num.start()] + _add_commas(o_num.group(0)) + out[o_num.end():]
            except ValueError:
                pass
    return out


def replace_spans(text: str, spans, new_kv: str, fit: bool = True) -> str:
    """Substitute ``new_kv`` at every span; ``fit=False`` inserts it verbatim."""
    out = text
    for s, e in sorted(set(spans), reverse=True):
        piece = _fit_replacement(text[s:e], new_kv) if fit else new_kv
        out = out[:s] + piece + out[e:]
    return out


# --------------------------------------------------------------------------
# absent
# --------------------------------------------------------------------------

def inject_absent(message: str, target: Obligation, others: list[Obligation],
                  rng: random.Random) -> dict | None:
    """Delete the unit(s) carrying ``target``'s key values; keep every other one."""
    for level, splitter in (("sentence", split_units), ("clause", split_clauses)):
        marks = kv_spans(message, target)
        if not marks:
            return None
        hit = [sp for sp in splitter(message) if overlaps(sp, marks)]
        if not hit:
            continue
        new = delete_spans(message, hit)
        if not new.strip():
            continue
        if present(new, target):
            continue
        if not all(present(new, o) for o in others):
            continue
        return {"message": new, "removed_spans": [list(sp) for sp in hit], "level": level}
    return None


# --------------------------------------------------------------------------
# altered_value
# --------------------------------------------------------------------------

def _sign(rng: random.Random) -> int:
    return 1 if rng.random() < 0.5 else -1


def _alter_number(s: str, rng: random.Random) -> str | None:
    m = _NUM_NEEDLE.match(s)
    if not m:
        return None
    num = m.group("num")
    raw = _strip_commas(num)
    has_commas = "," in num
    is_int = "." not in raw
    decimals = 0 if is_int else len(raw.split(".", 1)[1])
    v = float(raw)
    out_num = None
    for _ in range(16):
        pct = rng.randint(10, 50) / 100.0
        nv = v * (1 + _sign(rng) * pct)
        if is_int:
            iv = int(round(nv))
            if iv == int(v) or iv <= 0:
                continue
            out_num = str(iv)
        else:
            fv = round(nv, decimals)
            if abs(fv - v) < 0.5 * 10 ** (-decimals) or fv <= 0:
                continue
            out_num = f"{fv:.{decimals}f}"
        break
    if out_num is None:
        out_num = str(int(v) + 1) if is_int else f"{v + 10 ** (-decimals):.{decimals}f}"
    if has_commas:
        out_num = _add_commas(out_num)
    suf = m.group("suf") or ""
    return f"{m.group('cur') or ''}{m.group('sp1')}{out_num}{m.group('sp2')}{suf}"


_ISO = re.compile(r"^(\d{4})-(\d{1,2})-(\d{1,2})$")
_US = re.compile(r"^(\d{1,2})/(\d{1,2})/(\d{4})$")
_MDY = re.compile(r"^([A-Za-z]{3,9})\.?\s+(\d{1,2})(?:(,?)\s*(\d{4}))?$")
_DMY = re.compile(r"^(\d{1,2})\s+([A-Za-z]{3,9})\.?(?:\s+(\d{4}))?$")
_REF_YEAR = 2000


def _month_style(src: str, month: int) -> str:
    full = _MONTHS[month - 1]
    out = full[:3] if len(src.rstrip(".")) <= 3 else full
    if src.isupper():
        return out.upper()
    if src.islower():
        return out
    return out.capitalize()


def _pad_like(src: str, value: int) -> str:
    return f"{value:02d}" if len(src) == 2 and src.startswith("0") else str(value)


def _shift(d: date, rng: random.Random) -> date:
    return d + timedelta(days=rng.randint(3, 30) * _sign(rng))


def _alter_date(s: str, rng: random.Random) -> str | None:
    m = _ISO.match(s)
    if m:
        y, mo, dy = (int(x) for x in m.groups())
        try:
            nd = _shift(date(y, mo, dy), rng)
        except ValueError:
            return None
        return f"{nd.year:04d}-{nd.month:02d}-{nd.day:02d}"
    m = _US.match(s)
    if m:
        mo_s, dy_s, y_s = m.groups()
        try:
            nd = _shift(date(int(y_s), int(mo_s), int(dy_s)), rng)
        except ValueError:
            return None
        return f"{_pad_like(mo_s, nd.month)}/{_pad_like(dy_s, nd.day)}/{nd.year:04d}"
    m = _MDY.match(s)
    if m:
        mon_s, dy_s, comma, y_s = m.groups()
        mo = _MONTH_IDX.get(mon_s.lower().rstrip("."))
        if not mo:
            return None
        year = int(y_s) if y_s else _REF_YEAR
        try:
            nd = _shift(date(year, mo, int(dy_s)), rng)
        except ValueError:
            return None
        out = f"{_month_style(mon_s, nd.month)} {_pad_like(dy_s, nd.day)}"
        if y_s:
            out += f"{comma or ''} {nd.year:04d}"
        return out
    m = _DMY.match(s)
    if m:
        dy_s, mon_s, y_s = m.groups()
        mo = _MONTH_IDX.get(mon_s.lower().rstrip("."))
        if not mo:
            return None
        year = int(y_s) if y_s else _REF_YEAR
        try:
            nd = _shift(date(year, mo, int(dy_s)), rng)
        except ValueError:
            return None
        out = f"{_pad_like(dy_s, nd.day)} {_month_style(mon_s, nd.month)}"
        if y_s:
            out += f" {nd.year:04d}"
        return out
    return None


_T12 = re.compile(r"^(\d{1,2})(?::(\d{2}))?(\s*)([APap]\.?[Mm]\.?)$")
_T24 = re.compile(r"^(\d{1,2}):(\d{2})$")


def _meridiem_style(src: str, pm: bool) -> str:
    letter = "p" if pm else "a"
    out = letter + ("." if "." in src else "") + "m" + ("." if src.rstrip().endswith(".") else "")
    return out.upper() if src.strip()[0].isupper() else out


def _alter_time(s: str, rng: random.Random) -> str | None:
    m = _T12.match(s)
    if m:
        h_s, mi_s, sp, mer = m.groups()
        h = int(h_s)
        if not 1 <= h <= 12:
            return None
        pm = mer.lower().startswith("p")
        h24 = (h % 12) + (12 if pm else 0)
        h24 = (h24 + rng.randint(1, 4) * _sign(rng)) % 24
        nh = h24 % 12 or 12
        out = _pad_like(h_s, nh)
        if mi_s:
            out += f":{mi_s}"
        return f"{out}{sp}{_meridiem_style(mer, h24 >= 12)}"
    m = _T24.match(s)
    if m:
        h_s, mi_s = m.groups()
        h = int(h_s)
        if h > 23 or int(mi_s) > 59:
            return None
        nh = (h + rng.randint(1, 4) * _sign(rng)) % 24
        return f"{nh:02d}:{mi_s}" if len(h_s) == 2 else f"{nh}:{mi_s}"
    return None


_ID_OK = re.compile(r"^[A-Za-z0-9_.\-/]{4,}$")


def _flip_char(ch: str, rng: random.Random) -> str:
    if ch.isdigit():
        return rng.choice([c for c in "0123456789" if c != ch])
    pool = "abcdefghijklmnopqrstuvwxyz"
    pool = pool.upper() if ch.isupper() else pool
    return rng.choice([c for c in pool if c != ch])


def _alter_id(s: str, rng: random.Random) -> str | None:
    if not _ID_OK.match(s):
        return None
    if not (re.search(r"[A-Za-z]", s) and re.search(r"\d", s)):
        return None
    idx = [i for i, ch in enumerate(s) if ch.isalnum()]
    if len(idx) < 2:
        return None
    out = list(s)
    for i in rng.sample(idx, 2):
        out[i] = _flip_char(s[i], rng)
    return "".join(out)


def alter_value(kv: str, rng: random.Random) -> str | None:
    """Perturb a key value while preserving its surface format.

    Numbers move by 10-50%, dates by 3-30 days, times by 1-4 hours, id-like
    tokens have 2 characters swapped.  Plain words/names return None.
    """
    s = (kv or "").strip()
    if not s:
        return None
    for fn in (_alter_date, _alter_time, _alter_number, _alter_id):
        out = fn(s, rng)
        if out and out != s:
            return out
    return None


def inject_altered_value(message: str, target: Obligation, others: list[Obligation],
                         rng: random.Random) -> dict | None:
    kvs = list(target.key_values)
    rng.shuffle(kvs)
    for kv in kvs:
        spans = find_spans(message, kv)
        if not spans:
            continue
        new_kv = alter_value(kv, rng)
        if not new_kv or new_kv.strip() == kv.strip():
            continue
        new = replace_spans(message, spans, new_kv)
        if new == message or find_spans(new, kv):
            continue
        if not all(present(new, o) for o in others):
            continue
        return {"message": new, "kv": kv, "new_kv": new_kv}
    return None


# --------------------------------------------------------------------------
# altered_semantic
# --------------------------------------------------------------------------

_QUANT_HEDGES = ("approximately", "around", "roughly")
_TEMPORAL_HEDGES = ("ideally", "preferably")
_MODAL_REPL = {"must": "should ideally", "only": "preferably"}
_FACT_HEDGES = {
    " is ": (" is probably ", " seems to be "),
    " are ": (" are probably ",),
    " has ": (" has probably ",),
    " was ": (" was probably ",),
    " were ": (" were probably ",),
}
# Every wording this module introduces must come from L_INJECT.
assert set(_QUANT_HEDGES) <= L_INJECT
assert set(_TEMPORAL_HEDGES) <= L_INJECT
assert set(_MODAL_REPL.values()) <= L_INJECT
assert {r.strip() for v in _FACT_HEDGES.values() for r in v} <= (
    L_INJECT | {"are probably", "has probably", "was probably", "were probably"})


def _recap(original: str, new: str) -> str:
    o, n = original.lstrip(), new.lstrip()
    if o and n and o[0].isupper() and n[0].islower():
        n = n[0].upper() + n[1:]
    return n


def _content_end(sent: str) -> int:
    e = len(sent)
    while e > 0 and sent[e - 1] in " \t.!?;,":
        e -= 1
    return e


def _edit_constraint(sent, target, marks, rng):
    # A bound word inside a negation ("must not exceed") cannot be swapped for a
    # hedge without producing nonsense; leave those to the prohibition path.
    negs = [(s, e) for _, s, e in find_phrases(sent, NEGATION_WORDS)]
    hit = find_phrase(sent, BOUND_WORDS, avoid=list(marks) + negs)
    if hit:
        phrase, s, e = hit
        low = phrase.lower()
        if low in _MODAL_REPL:
            repl, rule = _MODAL_REPL[low], "weaken_modal"
        elif low in QUANTITY_BOUNDS:
            repl, rule = rng.choice(_QUANT_HEDGES), "weaken_bound"
        elif low in TEMPORAL_BOUNDS:
            repl, rule = f"{rng.choice(_TEMPORAL_HEDGES)} {sent[s:e]}", "soften_deadline"
        else:
            repl, rule = rng.choice(_QUANT_HEDGES), "weaken_bound"
        if sent[s:e][:1].isupper():
            repl = repl[0].upper() + repl[1:]
        return sent[:s] + repl + sent[e:], rule
    if target.numeric:
        m = re.search(r"[$€£¥]\s*\d|\d", sent)
        if m:
            at = m.start()
            return sent[:at] + "approximately " + sent[at:], "hedge_number"
    return None, None


def _edit_prohibition(sent, target, marks, rng):
    hit = find_phrase(sent, NEGATION_WORDS, avoid=marks)
    if not hit:
        return None, None
    _, s, e = hit
    out = _recap(sent, (sent[:s] + sent[e:]).replace("  ", " ").lstrip())
    if rng.random() < 0.5:
        at = _content_end(out)
        out = out[:at] + " if possible" + out[at:]
        return out, "invert_negation"
    return out, "drop_negation"


def _edit_open_question(sent, target, marks, rng):
    hit = find_phrase(sent, [w for w in UNCERTAINTY_WORDS if w.strip("? ")], avoid=marks)
    if hit:
        _, s, e = hit
        while s >= 6 and sent[s - 6:s].lower() == "still ":
            s -= 6
        repl = rng.choice(("confirmed", "verified"))
        if sent[s:e][:1].isupper():
            repl = repl.capitalize()
        return sent[:s] + repl + sent[e:], "mark_confirmed"
    return "Confirmed: " + sent, "prefix_confirmed"


def _edit_verified_fact(sent, target, marks, rng):
    for pat, repls in _FACT_HEDGES.items():
        for m in re.finditer(re.escape(pat), sent, re.IGNORECASE):
            if overlaps((m.start(), m.end()), marks):
                continue
            repl = rng.choice(repls)
            return sent[:m.start()] + repl + sent[m.end():], "hedge_copula"
    return None, None


def _edit_goal(sent, target, marks, rng):
    end = _content_end(sent)
    conj = [m for m in re.finditer(r"\s+and\s+", sent[:end], re.IGNORECASE)]
    if conj:
        m = conj[-1]
        if not overlaps((m.start(), end), marks) and len(sent[:m.start()].split()) >= 3:
            return sent[:m.start()] + sent[end:], "drop_conjunct"
    for m in re.finditer(r"\s*\([^()]*\)", sent):
        if not overlaps((m.start(), m.end()), marks):
            return sent[:m.start()] + sent[m.end():], "drop_parenthetical"
    quals = list(re.finditer(
        r"\s+(?:within|near|by|before|after|during|under|over|for|from|until|"
        r"in|on|at)\s+[^,.;!?]+", sent[:end], re.IGNORECASE))
    for m in reversed(quals):
        if overlaps((m.start(), m.end()), marks):
            continue
        if len(sent[:m.start()].split()) < 3:
            continue
        return sent[:m.start()] + sent[m.end():], "drop_qualifier"
    return None, None


_SEMANTIC_EDITS = {
    "constraint": _edit_constraint,
    "prohibition": _edit_prohibition,
    "open_question": _edit_open_question,
    "verified_fact": _edit_verified_fact,
    "goal": _edit_goal,
}


def inject_altered_semantic(message: str, target: Obligation,
                            rng: random.Random) -> dict | None:
    """Weaken the force of ``target`` while keeping every key value token."""
    edit = _SEMANTIC_EDITS.get(target.type)
    if edit is None:
        return None
    marks = kv_spans(message, target)
    if not marks:
        return None
    for s, e in split_units(message):
        if not overlaps((s, e), marks):
            continue
        sent = message[s:e]
        local = [(a - s, b - s) for a, b in marks if a >= s and b <= e]
        new_sent, rule = edit(sent, target, local, rng)
        if not new_sent or new_sent == sent:
            continue
        new = message[:s] + new_sent + message[e:]
        if new == message:
            continue
        if not present(new, target):
            continue
        return {"message": new, "rule": f"{target.type}:{rule}"}
    return None


# --------------------------------------------------------------------------
# fabricated
# --------------------------------------------------------------------------

def insert_fabricated(message: str, sentence: str) -> str:
    """Place an unsupported sentence just before the final sentence."""
    s = (sentence or "").strip()
    if not s:
        return message
    if s[-1] not in ".!?":
        s += "."
    units = split_units(message)
    if len(units) < 2:
        base = message.rstrip()
        return f"{base} {s}" if base else s
    at = units[-1][0]
    sep = "\n" if at > 0 and message[at - 1] == "\n" else " "
    return message[:at] + s + sep + message[at:]
