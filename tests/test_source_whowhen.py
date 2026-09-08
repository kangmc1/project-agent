"""Tests for the whowhen source parser."""
from __future__ import annotations

from pathlib import Path

import pytest

from handoffcheck.schema import context_to_text
from handoffcheck.sources.whowhen import parse, _default_count_tokens

DATA_ROOT = Path(__file__).resolve().parents[1] / "data" / "external" / "whowhen" / "hand_crafted"


def _has_data() -> bool:
    return DATA_ROOT.is_dir() and len(list(DATA_ROOT.glob("*.json"))) >= 1


pytestmark = pytest.mark.skipif(not _has_data(), reason="whowhen hand_crafted data not present")


def test_parse_whowhen_candidates():
    boundaries = parse(DATA_ROOT)

    assert len(boundaries) >= 1

    for b in boundaries:
        assert b.message is not None
        assert len(b.message.strip()) >= 40

        worker_msgs = [
            m for m in b.context
            if not (m.get("role") or "").startswith("Orchestrator") and m.get("role") != "human"
        ]
        assert len(worker_msgs) >= 2

        n_tokens = _default_count_tokens(context_to_text(b.context))
        if n_tokens > 6000:
            # Truncation drops messages until it fits, but it never drops the
            # first 'human' message, the first 'Orchestrator (thought)' plan,
            # or the >=2 worker replies required for the boundary to be a
            # candidate at all. When those alone exceed the cap (e.g. a huge
            # embedded table in the initial plan), nothing more can be
            # dropped -- that shows up here as an irreducibly small context.
            assert len(b.context) <= 4, (
                f"{b.id}: {n_tokens} tokens over cap with droppable content still present"
            )
