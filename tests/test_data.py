"""Tests for src.data that must pass without a running LLM server."""

from typing import Any, Dict, List

import pytest

from src.data.tau import sample_task_ids
from src.data.tau_user import RawHttpxUserSim


class _FakeResponse:
    def __init__(self, content: str) -> None:
        self._content = content

    def raise_for_status(self) -> None:
        return None

    def json(self) -> Dict[str, Any]:
        return {"choices": [{"message": {"content": self._content}}]}


class _FakeClient:
    """Stands in for httpx2.Client so no real HTTP call is made."""

    def __init__(self, replies: List[str]) -> None:
        self._replies = list(replies)
        self.calls: List[Dict[str, Any]] = []

    def post(self, url: str, **kwargs: Any) -> _FakeResponse:
        self.calls.append({"url": url, **kwargs})
        return _FakeResponse(self._replies.pop(0))


def test_raw_httpx_user_sim_reset_and_step_return_strings():
    fake_client = _FakeClient(["Hi, I need help with my booking.", "###STOP###"])
    sim = RawHttpxUserSim(client=fake_client)

    first = sim.reset(instruction="Book a flight from JFK to SEA.")
    assert isinstance(first, str)
    assert first == "Hi, I need help with my booking."
    assert "###STOP###" not in first

    second = sim.step("Sure, what are your travel dates?")
    assert isinstance(second, str)
    assert second == "###STOP###"
    assert "###STOP###" in second

    assert sim.get_total_cost() == 0.0
    assert len(fake_client.calls) == 2
    assert fake_client.calls[0]["url"] == "http://localhost:18001/v1/chat/completions"
    assert fake_client.calls[0]["headers"]["X-Agent"] == "user_sim"
    assert fake_client.calls[0]["json"]["chat_template_kwargs"] == {
        "enable_thinking": False
    }
    assert fake_client.calls[0]["json"]["temperature"] == 0
    assert fake_client.calls[0]["json"]["max_tokens"] == 512


def test_sample_task_ids_deterministic_and_in_range():
    ids_a = sample_task_ids(seed=0, n=30)
    ids_b = sample_task_ids(seed=0, n=30)
    assert ids_a == ids_b
    assert len(ids_a) == 30
    assert len(set(ids_a)) == 30
    assert ids_a == sorted(ids_a)
    assert all(0 <= i < 50 for i in ids_a)


def test_load_aime2026_returns_30_items_with_int_answers():
    pytest.importorskip("datasets")
    try:
        from src.data.aime import load_aime2026

        items = load_aime2026()
    except Exception as exc:
        pytest.skip(f"AIME dataset unavailable (no network?): {exc}")

    assert len(items) == 30
    for item in items:
        assert isinstance(item["id"], str)
        assert isinstance(item["problem"], str)
        assert isinstance(item["answer"], int)
