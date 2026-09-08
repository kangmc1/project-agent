"""Tests for the tau source parser."""
from __future__ import annotations

from pathlib import Path

import pytest

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "external" / "tau_airline_traces.parquet"


def _has_data() -> bool:
    return DATA_PATH.is_file()


pytestmark = pytest.mark.skipif(not _has_data(), reason="tau_airline_traces.parquet not present")


def test_parse_tau_candidates():
    from handoffcheck.sources.tau import parse

    boundaries = parse(DATA_PATH)

    rows_with_candidates = {b.meta["row"] for b in boundaries}
    assert len(rows_with_candidates) >= 40

    assert len(boundaries) >= 1

    for b in boundaries:
        tool_call_lines = [
            m for m in b.context
            if isinstance(m.get("content"), str) and "[tool_call]" in m["content"]
        ]
        assert len(tool_call_lines) >= 1

        tool_result_lines = [
            m for m in b.context
            if isinstance(m.get("content"), str) and "[tool_result]" in m["content"]
        ]
        assert len(tool_result_lines) >= 2

        for m in b.context:
            assert m.get("content") != "None"
