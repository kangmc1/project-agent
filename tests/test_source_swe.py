import statistics
from pathlib import Path

import pytest

from handoffcheck.schema import context_to_text
from handoffcheck.sources.swe import DEFAULT_COUNT_TOKENS, parse

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "external" / "swe_smith_traj_00000.parquet"

pytestmark = pytest.mark.skipif(not DATA_PATH.exists(), reason=f"data file missing: {DATA_PATH}")


def test_parse_swe_boundaries():
    boundaries = parse(DATA_PATH, limit_rows=50)

    rows_with_candidates = {b.meta["row"] for b in boundaries}
    assert len(rows_with_candidates) >= 30, (
        f"expected >=30 rows (of 50) to yield >=1 candidate boundary, got {len(rows_with_candidates)}"
    )

    assert len(boundaries) >= 1

    for b in boundaries:
        assert len(b.context) >= 2, f"context too short: {b.id}"
        assert b.context[0]["role"] == "system", f"first message not system: {b.id}"
        assert b.context[1]["role"] == "user", f"second message not user: {b.id}"

        token_count = DEFAULT_COUNT_TOKENS(context_to_text(b.context))
        assert token_count <= 6000, f"context over token cap for {b.id}: {token_count} tokens"
