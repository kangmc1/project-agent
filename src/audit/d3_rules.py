"""D3 rules: which tool evidence a claim in an utterance requires (deterministic, regex-based)."""
from __future__ import annotations

import re

# airline value patterns (tau-bench data conventions)
RESERVATION_ID = re.compile(r"\b(?=[A-Z0-9]{6}\b)(?=[A-Z0-9]*\d)(?=[A-Z0-9]*[A-Z])[A-Z0-9]{6}\b")
USER_ID = re.compile(r"\b[a-z]+_[a-z]+_\d{3,5}\b")
FLIGHT_NO = re.compile(r"\bHAT\d{3}\b")
MONEY = re.compile(r"\$\s?(\d{1,3}(?:,\d{3})*(?:\.\d+)?|\d+(?:\.\d+)?)")
DATE = re.compile(r"\b20\d{2}-\d{2}-\d{2}\b")
ACTION_VERBS = {
    "cancel": re.compile(r"\b(cancel(?:l)?ed|has been cancel|cancellation (?:is )?complete)", re.I),
    "update_flights": re.compile(r"\b(changed|rebooked|updated) (?:your |the )?(flight|reservation|itinerary)", re.I),
    "update_baggages": re.compile(r"\b(added|updated) .*\bbag", re.I),
    "update_passengers": re.compile(r"\b(updated|changed) .*\bpassenger", re.I),
    "book": re.compile(r"\b(booked|reservation (?:has been|is) (?:created|confirmed))", re.I),
    "refund": re.compile(r"\brefund(?:ed)?\b", re.I),
}

# claim type -> tools that can ground it (any one suffices) — airline (>= 6 rules)
AIRLINE_RULES: dict[str, list[str]] = {
    "reservation_id": ["get_reservation_details", "book_reservation", "update_reservation_flights",
                       "update_reservation_baggages", "update_reservation_passengers", "cancel_reservation", "get_user_details"],
    "user_id": ["get_user_details", "get_reservation_details"],
    "flight_no": ["search_direct_flight", "search_onestop_flight", "get_reservation_details", "update_reservation_flights", "book_reservation"],
    "money": ["calculate", "get_reservation_details", "search_direct_flight", "search_onestop_flight", "update_reservation_flights",
              "update_reservation_baggages", "book_reservation", "get_user_details"],
    "date": ["get_reservation_details", "search_direct_flight", "search_onestop_flight", "update_reservation_flights", "book_reservation"],
    "cancel": ["cancel_reservation"],
    "update_flights": ["update_reservation_flights"],
    "update_baggages": ["update_reservation_baggages"],
    "update_passengers": ["update_reservation_passengers"],
    "book": ["book_reservation"],
    "refund": ["cancel_reservation", "update_reservation_flights", "get_reservation_details", "calculate"],
}

# AIME (>= 2 rules)
NUMERIC = re.compile(r"(?<![\w.])(\d{2,6})(?![\w.])")
FINAL = re.compile(r"FINAL ANSWER:\s*(\d{1,4})", re.I)
AIME_RULES: dict[str, list[str]] = {
    "numeric": ["run_python"],
    "final_answer": ["run_python"],
}


def extract_claims(domain: str, text: str) -> list[tuple[str, str]]:
    """Return (claim_type, value) pairs found in an utterance."""
    out: list[tuple[str, str]] = []
    if not text:
        return out
    if domain == "airline":
        out += [("reservation_id", m) for m in set(RESERVATION_ID.findall(text))]
        out += [("user_id", m) for m in set(USER_ID.findall(text))]
        out += [("flight_no", m) for m in set(FLIGHT_NO.findall(text))]
        out += [("money", m.replace(",", "")) for m in set(MONEY.findall(text))]
        out += [("date", m) for m in set(DATE.findall(text))]
        for k, rx in ACTION_VERBS.items():
            if rx.search(text):
                out.append((k, ""))
    else:
        fa = FINAL.search(text)
        if fa:
            out.append(("final_answer", fa.group(1)))
        for m in set(NUMERIC.findall(text)):
            if not (fa and m == fa.group(1)):
                out.append(("numeric", m))
    return out


def rules_for(domain: str) -> dict[str, list[str]]:
    return AIRLINE_RULES if domain == "airline" else AIME_RULES
