"""Build runs/index.csv from runs/*/meta.json and report status vs. the expected task lists.

Usage: python -m src.eval.index [--runs runs] [--data data]
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

COLUMNS = ["run_id", "domain", "task", "batch", "status", "success", "n_steps", "wall_time"]


def scan_runs(runs_dir: Path) -> list[dict]:
    rows = []
    for run in sorted(runs_dir.glob("*/")):
        meta_path = run / "meta.json"
        if not meta_path.exists():
            continue
        try:
            meta = json.loads(meta_path.read_text())
        except Exception:
            continue
        rows.append({
            "run_id": meta.get("run_id", run.name),
            "domain": meta.get("domain", run.name.split("_")[0]),
            "task": meta.get("task"),
            "batch": meta.get("batch"),
            "status": meta.get("status"),
            "success": meta.get("success"),
            "n_steps": meta.get("n_steps"),
            "wall_time": meta.get("wall_time"),
        })
    return rows


def write_index(rows: list[dict], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def expected_run_ids(data_dir: Path) -> dict[str, set[str]]:
    expected: dict[str, set[str]] = {"airline": set(), "aime": set()}
    tau_path = data_dir / "tau_task_ids.json"
    if tau_path.exists():
        for ids in json.loads(tau_path.read_text()).values():
            expected["airline"].update(f"airline_{str(i).zfill(3)}" for i in ids)
    aime_path = data_dir / "aime_ids.json"
    if aime_path.exists():
        for ids in json.loads(aime_path.read_text()).values():
            expected["aime"].update(f"aime_{str(i).zfill(3)}" for i in ids)
    return expected


def summarize(rows: list[dict]) -> dict[str, dict]:
    by_domain: dict[str, dict] = defaultdict(lambda: {"n": 0, "n_success": 0})
    for r in rows:
        d = by_domain[r["domain"]]
        d["n"] += 1
        if r["success"]:
            d["n_success"] += 1
    return {domain: {"n": v["n"], "n_success": v["n_success"],
                      "success_rate": (v["n_success"] / v["n"]) if v["n"] else None}
            for domain, v in sorted(by_domain.items())}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default="runs")
    ap.add_argument("--data", default="data")
    a = ap.parse_args()
    runs_dir = Path(a.runs)

    rows = scan_runs(runs_dir)
    write_index(rows, runs_dir / "index.csv")
    print(f"indexed {len(rows)} runs -> {runs_dir / 'index.csv'}")
    for domain, s in summarize(rows).items():
        rate = f"{s['success_rate']:.1%}" if s["success_rate"] is not None else "n/a"
        print(f"  {domain}: n={s['n']} success={s['n_success']} rate={rate}")

    found = {r["run_id"] for r in rows}
    expected = expected_run_ids(Path(a.data))
    for domain, ids in expected.items():
        missing = sorted(ids - found)
        shown = missing[:20]
        tail = f" (+{len(missing) - 20} more)" if len(missing) > 20 else ""
        print(f"  {domain}: missing {len(missing)}/{len(ids)}" + (f" -> {shown}{tail}" if missing else ""))


if __name__ == "__main__":
    main()
