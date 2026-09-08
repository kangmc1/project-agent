"""Run tasks through the Deep Agents harness with full-observability capture.

  python -m src.run --domain airline --task 0
  python -m src.run --batch 1 --parallel 4 --resume
"""
from __future__ import annotations

import argparse
import json
import os
import threading
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

RUNS = Path("runs")
TIMEOUTS = {"airline": 22 * 60, "aime": 17 * 60}


def run_dir_for(domain: str, task: str) -> Path:
    return RUNS / f"{domain}_{str(task).zfill(3)}"


def _worker(domain: str, task: str, batch: int) -> dict:
    """Everything (clients, graphs) is created inside the worker process."""
    from src.harness.capture import RunContext

    rd = run_dir_for(domain, task)
    ctx = RunContext(rd)
    t0 = time.time()
    result: dict = {}
    err: list[str] = []

    def target():
        try:
            if domain == "airline":
                from src.harness.airline import run_airline
                result.update(run_airline(int(task), ctx))
            else:
                from src.harness.aime import run_aime
                result.update(run_aime(task, ctx))
        except Exception:
            err.append(traceback.format_exc())

    th = threading.Thread(target=target, daemon=True)
    th.start()
    th.join(TIMEOUTS[domain])
    status = "ok"
    if th.is_alive():
        status = "timeout"
    elif err:
        status = "exception"
    meta = {"run_id": rd.name, "domain": domain, "task": task, "batch": batch, "status": status,
            "success": bool(result.get("success", False)) if status == "ok" else False,
            "wall_time": round(time.time() - t0, 1), "chat_model_starts": ctx.chat_model_starts,
            "n_steps": ctx.step_id, "result": result, "error": (err[0][-3000:] if err else None)}
    ctx.write_meta(**meta)
    ctx.close()
    return meta


def load_batch(batch: int) -> list[tuple[str, str]]:
    tau = json.loads(Path("data/tau_task_ids.json").read_text())[f"batch{batch}"]
    aime = json.loads(Path("data/aime_ids.json").read_text())[f"batch{batch}"]
    jobs: list[tuple[str, str]] = []
    # interleave so both domains progress together
    for i in range(max(len(tau), len(aime))):
        if i < len(tau):
            jobs.append(("airline", str(tau[i])))
        if i < len(aime):
            jobs.append(("aime", str(aime[i])))
    return jobs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--domain", choices=["airline", "aime"])
    ap.add_argument("--task")
    ap.add_argument("--batch", type=int)
    ap.add_argument("--parallel", type=int, default=4)
    ap.add_argument("--resume", action="store_true")
    a = ap.parse_args()
    os.environ.setdefault("OPENAI_BASE_URL", "http://localhost:18001/v1")
    os.environ.setdefault("OPENAI_API_BASE", "http://localhost:18001/v1")
    os.environ.setdefault("OPENAI_API_KEY", "dummy")
    RUNS.mkdir(exist_ok=True)

    if a.domain and a.task is not None:
        meta = _worker(a.domain, a.task, a.batch or 0)
        print(json.dumps({k: v for k, v in meta.items() if k != "result"}, ensure_ascii=False, indent=1))
        print(json.dumps(meta.get("result"), ensure_ascii=False, default=str)[:800])
        return 0 if meta["status"] == "ok" else 1

    jobs = load_batch(a.batch)
    if a.resume:
        jobs = [(d, t) for d, t in jobs if not (run_dir_for(d, t) / "meta.json").exists()]
    print(f"batch {a.batch}: {len(jobs)} jobs, parallel={a.parallel}")
    done = 0
    with ProcessPoolExecutor(max_workers=a.parallel) as ex:
        futs = {ex.submit(_worker, d, t, a.batch): (d, t) for d, t in jobs}
        for f in as_completed(futs):
            d, t = futs[f]
            try:
                m = f.result()
                done += 1
                print(f"[{done}/{len(jobs)}] {d} {t}: status={m['status']} success={m['success']} steps={m['n_steps']} t={m['wall_time']}s", flush=True)
            except Exception as e:  # pragma: no cover
                print(f"[!] {d} {t}: worker crashed: {e!r}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
