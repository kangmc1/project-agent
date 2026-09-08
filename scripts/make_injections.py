"""Build the B-layer injection set from reset handoffs: for each handoff, one of each op (drop/weaken/corrupt) + a control."""
import argparse, json, random
from pathlib import Path
from handoffbench.llm import LLM
from handoffbench.data.render import _trim
from handoffbench.injection.facts import inject, fact_bullets, to_jsonl

p = argparse.ArgumentParser()
p.add_argument("--n_handoffs", type=int, default=30)
p.add_argument("--ops", default="none,drop,weaken,corrupt")
p.add_argument("--out", default="data/injections/reset_facts.jsonl")
p.add_argument("--seed", type=int, default=0)
a = p.parse_args()

hs = [json.loads(l) for l in open("data/handoffs/magentic_one_resets.jsonl")]
hs = [h for h in hs if h["facts_text"] and len(fact_bullets(h["facts_text"])) >= 2 and h["facts_text"] in h["post_reset_context"]]
rng = random.Random(a.seed); rng.shuffle(hs)
hs = hs[: a.n_handoffs]
llm = LLM()
out = []
for h in hs:
    def build_artifact(facts, plan, _h=h):
        # same artifact the detectors see for a real reset handoff, with the fact sheet swapped
        return _trim(_h["post_reset_context"].replace(_h["facts_text"], facts, 1), 9000)
    for op in a.ops.split(","):
        inj = inject(llm, h, op, rng, build_artifact)
        if inj: out.append(inj)
to_jsonl(out, Path(a.out))
import collections
print(f"handoffs used={len(hs)} injections={len(out)} by op={dict(collections.Counter(i.op for i in out))} | usage {llm.usage.as_dict()}")
for i in out[:6]:
    if i.op != "none": print(f"[{i.op}] {i.target_line[:100]}  -->  {str(i.modified_line)[:100]}")
