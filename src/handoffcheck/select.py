"""Pick candidate boundaries per domain (deterministic), verify the real token cap, write data/boundaries.jsonl."""
from __future__ import annotations

import random
from collections import defaultdict

from .schema import Boundary, context_to_text


def _fits(b: Boundary, count_tokens, cap: int) -> bool:
    n = count_tokens(context_to_text(b.context))
    b.meta["context_tokens"] = n
    return n <= cap


def select_whowhen(cands: list[Boundary], n: int, count_tokens, cap: int, seed: int = 0) -> list[Boundary]:
    by_file = defaultdict(list)
    for b in cands:
        by_file[b.source_ref.split("#")[0]].append(b)
    rng = random.Random(f"{seed}:whowhen")
    files = sorted(by_file)
    rng.shuffle(files)
    out = []
    for f in files:
        good = [b for b in by_file[f] if len(b.message or "") >= 120 and b.meta.get("n_worker_msgs_before", 0) >= 3]
        pool = good or [b for b in by_file[f] if len(b.message or "") >= 80]
        pool = [b for b in pool if _fits(b, count_tokens, cap)]
        if not pool:
            continue
        # prefer the longest real handoff message (more obligations to carry)
        pool.sort(key=lambda b: -len(b.message or ""))
        out.append(pool[0])
        if len(out) >= n:
            break
    return out


def select_tau(cands: list[Boundary], n: int, count_tokens, cap: int, seed: int = 0) -> list[Boundary]:
    by_row = defaultdict(list)
    for b in cands:
        by_row[b.meta["row"]].append(b)
    rng = random.Random(f"{seed}:tau")
    rows = sorted(by_row)
    rng.shuffle(rows)
    out = []
    for r in rows:
        pool = sorted(by_row[r], key=lambda b: -b.meta["cut_index"])  # latest cut first
        pick = next((b for b in pool if _fits(b, count_tokens, cap)), None)
        if pick:
            out.append(pick)
        if len(out) >= n:
            break
    return out


def select_swe(cands: list[Boundary], n: int, count_tokens, cap: int, seed: int = 0) -> list[Boundary]:
    by_row = defaultdict(dict)
    for b in cands:
        by_row[b.meta["row"]][b.meta["cut_assistant_turns"]] = b
    rng = random.Random(f"{seed}:swe")
    rows = sorted(by_row)
    rng.shuffle(rows)
    out = []
    for r in rows:
        for k in (10, 6, 14):
            b = by_row[r].get(k)
            if b and _fits(b, count_tokens, cap):
                out.append(b)
                break
        if len(out) >= n:
            break
    return out
