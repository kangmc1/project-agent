"""C-layer: run telephone chains seeded from real reset handoffs. Compare no-guard vs guard."""
import argparse, json, random, collections
from pathlib import Path
from agent_handoff.llm import LLM
from agent_handoff.chain.telephone import run_chain
from agent_handoff.injection.facts import fact_bullets

p = argparse.ArgumentParser()
p.add_argument("--n_seeds", type=int, default=6)
p.add_argument("--hops", type=int, default=6)
p.add_argument("--budget_words", type=int, default=150)
p.add_argument("--guard", default="0,1")
p.add_argument("--tag", default="chain")
p.add_argument("--seed", type=int, default=0)
a = p.parse_args()

R = [json.loads(l) for l in open("data/handoffs/magentic_one_resets.jsonl")]
R = [r for r in R if len(fact_bullets(r["facts_text"])) >= 3]
rng = random.Random(a.seed); rng.shuffle(R); R = R[: a.n_seeds]
llm = LLM()
Path("results/raw").mkdir(parents=True, exist_ok=True)
out = open(f"results/raw/{a.tag}_b{a.budget_words}.jsonl", "w")
for r in R:
    # seeded obligations = task-relevant verified-fact bullets (+ the task's own constraints are implicit in the task text)
    obls = [{"id": f"o{i+1}", "type": "fact", "text": b.lstrip("-*• ").strip()} for i, b in enumerate(fact_bullets(r["facts_text"])[:6])]
    for g in [int(x) for x in a.guard.split(",")]:
        res = run_chain(llm, r["task_instruction"], obls, r["facts_text"], hops=a.hops, budget_words=a.budget_words, guard=bool(g))
        rec = {"seed_handoff": r["handoff_id"], "guard": bool(g), "budget_words": a.budget_words, "obligations": obls, **res, "usage": llm.usage.as_dict()}
        out.write(json.dumps(rec, ensure_ascii=False) + "\n"); out.flush()
        curve = [sum(1 for v in h["survival"].values() if v == "preserved") for h in res["hops"]]
        print(f"{r['handoff_id'][-28:]} guard={g} preserved-per-hop={curve}/{len(obls)} words={[h['state_words'] for h in res['hops']]}", flush=True)
print("usage", llm.usage.as_dict())
