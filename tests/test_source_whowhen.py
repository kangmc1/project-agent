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

        assert _default_count_tokens(context_to_text(b.context)) <= 6000
