"""tau-bench airline environment helpers: task sampling and env construction."""

import json
import random
from pathlib import Path
from typing import Any, Dict, List, Optional

from tau_bench.envs.airline.env import MockAirlineDomainEnv
from tau_bench.envs.airline.tasks_test import TASKS as AIRLINE_TEST_TASKS

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
IDS_PATH = DATA_DIR / "tau_task_ids.json"


def make_airline_env(task_index: Optional[int] = None) -> MockAirlineDomainEnv:
    """Construct the tau-bench airline env with the llm user strategy.

    Note: MockAirlineDomainEnv's LLM user strategy makes a live completion
    call as soon as the env is constructed (see
    tau_bench.envs.user.LLMUserSimulationEnv.__init__), so this requires a
    reachable user-sim server/model and is not exercised by tests.
    """
    return MockAirlineDomainEnv(
        user_strategy="llm",
        user_model="qwen32b",
        user_provider="openai",
        task_split="test",
        task_index=task_index,
    )


def sample_task_ids(seed: int = 0, n: int = 30) -> List[int]:
    """Deterministically sample n task indices from the test split."""
    rng = random.Random(seed)
    return sorted(rng.sample(range(len(AIRLINE_TEST_TASKS)), n))


def write_ids() -> Path:
    """Write data/tau_task_ids.json = {"batch1": first 15, "batch2": rest}."""
    ids = sample_task_ids()
    batches = {"batch1": ids[:15], "batch2": ids[15:]}
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    IDS_PATH.write_text(json.dumps(batches, indent=2))
    return IDS_PATH


def tools_info(env: Any) -> List[Dict]:
    """Return the env's OpenAI tool schemas."""
    return env.tools_info


def policy_wiki(env: Any) -> str:
    """Return the env's policy wiki text."""
    return env.wiki


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.write:
        path = write_ids()
        ids = sample_task_ids()
        print(f"{len(ids)} task ids written to {path}")
