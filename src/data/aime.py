"""Loader for the AIME 2026 practice dataset (MathArena/aime_2026).

The HF dataset ships a single "train" split with columns
["problem_idx", "answer", "problem"] and 30 rows; "answer" is an
integer in [0, 999].
"""

import json
from pathlib import Path
from typing import Dict, List, Optional

import datasets

DATASET_NAME = "MathArena/aime_2026"
DATA_DIR = Path(__file__).resolve().parents[2] / "data"
IDS_PATH = DATA_DIR / "aime_ids.json"


def load_aime2026() -> List[Dict]:
    """Load the AIME 2026 dataset, normalized to {id, problem, answer}."""
    ds = datasets.load_dataset(DATASET_NAME)["train"]
    return [
        {
            "id": str(row["problem_idx"]),
            "problem": row["problem"],
            "answer": int(row["answer"]),
        }
        for row in ds
    ]


def write_ids(items: Optional[List[Dict]] = None) -> Path:
    """Write data/aime_ids.json = {"batch1": first 15 ids, "batch2": rest}."""
    if items is None:
        items = load_aime2026()
    ids = [item["id"] for item in items]
    batches = {"batch1": ids[:15], "batch2": ids[15:]}
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    IDS_PATH.write_text(json.dumps(batches, indent=2))
    return IDS_PATH


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.write:
        items = load_aime2026()
        path = write_ids(items)
        print(f"{len(items)} items written to {path}")
