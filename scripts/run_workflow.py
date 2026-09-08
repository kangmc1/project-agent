"""Run the closed-book multi-agent workflow over scenarios × variables. Output: results/raw/workflow_<tag>.jsonl"""
import argparse, json, itertools, time
from pathlib import Path
from agent_handoff.llm import LLM
from agent_handoff.workflow.engine import run_workflow

p = argparse.ArgumentParser()
p.add_argument("--scenarios", default="data/scenarios/scenarios.jsonl"); p.add_argument("--n", type=int, default=0)
p.add_argument("--rounds", type=int, default=8); p.add_argument("--visibility", default="shared,summary"); p.add_argument("--formats", default="free,json")
p.add_argument("--budgets", default="900"); p.add_argument("--guards", default="0"); p.add_argument("--tag", default="dev")
a = p.parse_args()
scs = [json.loads(l) for l in open(a.scenarios)]
if a.n: scs = scs[: a.n]
llm = LLM(); Path("results/raw").mkdir(parents=True, exist_ok=True)
path = f"results/raw/workflow_{a.tag}.jsonl"; done = set()
try:
    for l in open(path): r = json.loads(l); done.add((r["scenario_id"], r["visibility"], r["format"], r["budget"], r["guard"]))
except FileNotFoundError: pass
out = open(path, "a")
grid = list(itertools.product(scs, a.visibility.split(","), a.formats.split(","), [int(b) for b in a.budgets.split(",")], [bool(int(g)) for g in a.guards.split(",")]))
for i, (sc, vis, fmt, b, g) in enumerate(grid):
    if (sc["id"], vis, fmt, b, g) in done: continue
    t0 = time.time(); u0 = llm.usage.as_dict()
    try:
        res = run_workflow(llm, sc, rounds=a.rounds, visibility=vis, fmt=fmt, budget=b, guard=g)
    except Exception as e:
        print(f"ERR {sc['id']} {vis} {fmt} {b} {g}: {e}", flush=True); continue
    u1 = llm.usage.as_dict(); res["tokens"] = {"prompt": u1["prompt_tokens"] - u0["prompt_tokens"], "completion": u1["completion_tokens"] - u0["completion_tokens"]}; res["seconds"] = round(time.time() - t0, 1)
    out.write(json.dumps(res, ensure_ascii=False) + "\n"); out.flush()
    c = res["checks"]
    print(f"[{i+1}/{len(grid)}] {sc['id']} vis={vis} fmt={fmt} b={b} g={int(g)} rounds={res['rounds_run']} compr={res['n_compressions']} final_preserved={res['final_score']['preserved']:.2f} promoted={c['open_promoted_in_final']} prohib_viol={c['prohibitions_violated']}/{c['prohibitions_total']} fab={len(c['fabricated_in_final'])} revise={res['verifier_revise']} ({res['seconds']}s)", flush=True)
print("usage", llm.usage.as_dict())
