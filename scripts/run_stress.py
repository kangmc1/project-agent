"""Run the C-layer stress grid on synthetic scenarios. Results: results/raw/stress_<tag>.jsonl (one line per chain)."""
import argparse, json, itertools, time
from pathlib import Path
from agent_handoff.llm import LLM
from agent_handoff.chain.stress import run_stress

p = argparse.ArgumentParser()
p.add_argument("--scenarios", default="data/scenarios/scenarios.jsonl")
p.add_argument("--n", type=int, default=0)
p.add_argument("--hops", type=int, default=8)
p.add_argument("--budgets", default="80,150,300")
p.add_argument("--formats", default="free,json")
p.add_argument("--guards", default="0,1")
p.add_argument("--tag", default="grid")
a = p.parse_args()
scs = [json.loads(l) for l in open(a.scenarios)]
if a.n: scs = scs[: a.n]
llm = LLM(); Path("results/raw").mkdir(parents=True, exist_ok=True)
out = open(f"results/raw/stress_{a.tag}.jsonl", "a")
done = set()
try:
    for l in open(f"results/raw/stress_{a.tag}.jsonl"):
        r = json.loads(l); done.add((r["scenario_id"], r["format"], r["budget"], r["guard"]))
except FileNotFoundError:
    pass
grid = list(itertools.product(scs, a.formats.split(","), [int(b) for b in a.budgets.split(",")], [bool(int(g)) for g in a.guards.split(",")]))
for i, (sc, fmt, b, g) in enumerate(grid):
    if (sc["id"], fmt, b, g) in done: continue
    t0 = time.time(); u0 = llm.usage.as_dict()
    res = run_stress(llm, sc, fmt=fmt, hops=a.hops, budget=b, guard=g)
    u1 = llm.usage.as_dict(); res["tokens"] = {"prompt": u1["prompt_tokens"] - u0["prompt_tokens"], "completion": u1["completion_tokens"] - u0["completion_tokens"]}; res["seconds"] = round(time.time() - t0, 1)
    out.write(json.dumps(res, ensure_ascii=False) + "\n"); out.flush()
    curve = [round(h["score"]["preserved"], 2) for h in res["hops"]]
    print(f"[{i+1}/{len(grid)}] {sc['id']} {fmt} b={b} guard={int(g)} preserved={curve} promoted_last={res['hops'][-1]['score']['promoted']:.2f} ({res['seconds']}s)", flush=True)
print("usage", llm.usage.as_dict())
