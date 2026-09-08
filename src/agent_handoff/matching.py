"""Rule-based survival matcher for seeded obligations (no LLM judge).

status(o, text):
  preserved : all key_values present (normalized) AND, for open_question, still marked uncertain
  promoted  : open_question whose key_values are present but the surrounding statement is asserted as verified/fact
  altered   : some but not all key_values present, or a numeric key value appears changed (same slot, different number)
  absent    : no key_value present
The matcher is deliberately conservative and enumerable; its own precision/recall is measured on the injection set.
"""
from __future__ import annotations
import re, json

HEDGES = re.compile(r"\b(unverified|unconfirmed|not (yet )?(verified|confirmed)|could not (be )?(verify|confirm)|to (be )?(verify|verified|confirm|confirmed)|need(s)? to (verify|confirm|check)|pending|unknown|unclear|assum(e|ed|ption)|might|possibly|likely|tbd|open question|to look up|guess|\?)", re.I)
VERIFIED_SECTION = re.compile(r"(verified|confirmed|given)\s*(facts?)?", re.I)


def _norm(s: str) -> str:
    s = s.replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'")
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s


def _present(v: str, text: str) -> bool:
    v = _norm(v); t = _norm(text)
    if v in t:
        return True
    # numbers: allow formatting differences ($3,000 vs $3000; 10:00 AM vs 10:00am)
    vd = re.sub(r"[^0-9a-z]", "", v)
    if len(vd) >= 2 and vd.isdigit() is False and vd in re.sub(r"[^0-9a-z]", "", t):
        return True
    if vd.isdigit() and len(vd) >= 2:
        return re.search(r"(?<![0-9])" + re.escape(vd) + r"(?![0-9])", re.sub(r"[^0-9a-z ]", "", t)) is not None
    return False


def _window(text: str, values: list[str], width: int = 240) -> str:
    """The bullet/line (or JSON item) containing the first found key value, for hedge checks."""
    low = _norm_keep_len(text)
    for v in values:
        i = low.find(_norm(v))
        if i >= 0:
            a = max(text.rfind("\n", 0, i), text.rfind("{", 0, i), 0)
            b_candidates = [x for x in (text.find("\n", i), text.find("}", i)) if x != -1]
            b = min(b_candidates) if b_candidates else len(text)
            return text[a:b]
    return ""


def _norm_keep_len(s: str) -> str:
    # lowercase + quote normalization without changing length, so indices map back to `text`
    return s.replace("\u201c", '"').replace("\u201d", '"').replace("\u2019", "'").replace("\u2018", "'").lower()


def _section_of(text: str, pos: int) -> str:
    """Name of the nearest preceding section header (e.g. 'GIVEN OR VERIFIED FACTS', 'open_questions')."""
    head = text[:pos]
    m = list(re.finditer(r"(?m)^\s*(?:\d+\.\s*)?\**([A-Za-z_ ]{4,40})\**\s*:?\s*$|\"([a-z_]+)\"\s*:\s*\[", head))
    if not m:
        return ""
    g = m[-1]
    return (g.group(1) or g.group(2) or "").strip().lower()


def status(obl: dict, text: str) -> str:
    vals = obl.get("key_values") or []
    if not vals:
        return "unknown"
    found = [v for v in vals if _present(v, text)]
    if not found:
        return "absent"
    if len(found) < len(vals):
        return "altered"
    if obl.get("type") == "open_question":
        # Decide on the lines/items that contain ALL key values; an open question stays open if any such
        # line is hedged, marked unverified, or sits in an open/look-up section. It is promoted only if
        # every such line asserts it without hedge (or with explicit status verified).
        low = _norm_keep_len(text)
        lines = _items(text)
        full = [ln for ln in lines if all(_present(v, ln) for v in vals)]
        if not full:
            return "preserved"  # values scattered, no single assertion -> treat as not promoted
        verdicts = []
        for ln in full:
            pos = low.find(_norm_keep_len(ln)[:40])
            sec = _section_of(text, max(pos, 0))
            in_open_section = any(k in sec for k in ("open", "look up", "derive", "guess", "unverified", "question", "assum"))
            m = re.search(r'"status"\s*:\s*"([a-z_]+)"', ln)
            if m:
                verdicts.append("preserved" if m.group(1) in ("unverified", "extraction_failed") else "promoted"); continue
            if in_open_section or HEDGES.search(ln):
                verdicts.append("preserved")
            else:
                verdicts.append("promoted")
        return "preserved" if "preserved" in verdicts else "promoted"
    return "preserved"


def _items(text: str) -> list[str]:
    """Split into bullet lines, or JSON items when the text looks like JSON."""
    if text.lstrip().startswith("{"):
        return re.findall(r"\{[^{}]*\}", text)
    return [ln for ln in text.splitlines() if ln.strip()]


def survival_report(obligations: list[dict], text: str) -> dict[str, str]:
    return {o["id"]: status(o, text) for o in obligations}


def score(report: dict[str, str]) -> dict[str, float]:
    n = max(1, len(report))
    return {
        "preserved": sum(v == "preserved" for v in report.values()) / n,
        "promoted": sum(v == "promoted" for v in report.values()) / n,
        "altered": sum(v == "altered" for v in report.values()) / n,
        "absent": sum(v == "absent" for v in report.values()) / n,
    }
