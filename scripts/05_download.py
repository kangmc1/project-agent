"""Download the three public sources into data/external/ (never committed).
- Who&When Hand-Crafted (Magentic-One traces): 58 JSON files
- tau-bench airline traces (jkazdan/taubench_traces_training_data): 1 parquet
- SWE-smith trajectories shard 0 (SWE-bench/SWE-smith-trajectories): 1 parquet (~110 MB)
"""
import json, sys, urllib.request, concurrent.futures as cf
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "data" / "external"
ROOT.mkdir(parents=True, exist_ok=True)
HF = "https://huggingface.co"


def fetch(url: str, dest: Path) -> None:
    if dest.exists() and dest.stat().st_size > 0:
        return
    tmp = dest.with_suffix(dest.suffix + ".part")
    urllib.request.urlretrieve(url, tmp)
    tmp.rename(dest)


def whowhen() -> None:
    api = json.load(urllib.request.urlopen(f"{HF}/api/datasets/Kevin355/Who_and_When"))
    files = [s["rfilename"] for s in api["siblings"] if s["rfilename"].startswith("Who&When/Hand-Crafted/") and s["rfilename"].endswith(".json")]
    out = ROOT / "whowhen" / "hand_crafted"
    out.mkdir(parents=True, exist_ok=True)
    with cf.ThreadPoolExecutor(8) as ex:
        list(ex.map(lambda f: fetch(f"{HF}/datasets/Kevin355/Who_and_When/resolve/main/{urllib.request.quote(f)}", out / Path(f).name), files))
    print("whowhen hand_crafted files:", len(list(out.glob('*.json'))))


def tau() -> None:
    fetch(f"{HF}/datasets/jkazdan/taubench_traces_training_data/resolve/main/data/train-00000-of-00001.parquet", ROOT / "tau_airline_traces.parquet")
    print("tau ok")


def swe() -> None:
    fetch(f"{HF}/datasets/SWE-bench/SWE-smith-trajectories/resolve/main/data/ticks-00000-of-00008.parquet", ROOT / "swe_smith_traj_00000.parquet")
    print("swe ok")


if __name__ == "__main__":
    which = sys.argv[1:] or ["whowhen", "tau", "swe"]
    for w in which:
        {"whowhen": whowhen, "tau": tau, "swe": swe}[w]()
