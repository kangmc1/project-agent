"""sources → data/boundaries.jsonl (candidate boundaries per domain, real token counts)."""
import argparse, json
from pathlib import Path
from handoffcheck.llm import LLM
from handoffcheck.schema import write_jsonl, to_dict
from handoffcheck.sources import whowhen, tau, swe
from handoffcheck import select as sel

ap = argparse.ArgumentParser()
ap.add_argument("--per-domain", type=int, default=25)
ap.add_argument("--cap", type=int, default=6000)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--out", default="data/boundaries.jsonl")
ap.add_argument("--no-llm", action="store_true", help="use len//3 token estimate instead of /tokenize")
a = ap.parse_args()

if a.no_llm:
    count = lambda t: max(1, len(t) // 3)
else:
    llm = LLM()
    count = llm.count_tokens

ext = Path("data/external")
rows = []
c = whowhen.parse(ext / "whowhen" / "hand_crafted", count_tokens=count, max_context_tokens=a.cap)
w = sel.select_whowhen(c, a.per_domain, count, a.cap, a.seed); rows += w
c = tau.parse(ext / "tau_airline_traces.parquet", count_tokens=count, max_context_tokens=a.cap)
t = sel.select_tau(c, a.per_domain, count, a.cap, a.seed); rows += t
c = swe.parse(ext / "swe_smith_traj_00000.parquet", count_tokens=count, max_context_tokens=a.cap, limit_rows=400)
s = sel.select_swe(c, a.per_domain, count, a.cap, a.seed); rows += s
write_jsonl(a.out, [to_dict(b) for b in rows])
for name, lst in (("whowhen", w), ("tau", t), ("swe", s)):
    toks = sorted(b.meta.get("context_tokens", 0) for b in lst)
    print(f"{name}: {len(lst)} boundaries, context tokens median {toks[len(toks)//2] if toks else 0}, max {toks[-1] if toks else 0}")
print("wrote", a.out, len(rows))
