"""Generate N scenarios per domain; keep only rule-valid ones (retry up to 3x per slot)."""
import argparse, json, random
from pathlib import Path
from agent_handoff.llm import LLM
from agent_handoff.scenarios.generate import generate_one, DOMAINS
from agent_handoff.scenarios.schema import validate

p = argparse.ArgumentParser(); p.add_argument("--per_domain", type=int, default=6); p.add_argument("--out", default="data/scenarios/scenarios.jsonl"); p.add_argument("--seed", type=int, default=0); p.add_argument("--domains", default=",".join(DOMAINS)); p.add_argument("--start", type=int, default=0); a = p.parse_args()
llm = LLM(); rng = random.Random(a.seed)
out = open(a.out, "w"); kept = 0; tried = 0
for domain in a.domains.split(","):
    for i in range(a.start, a.start + a.per_domain):
        for attempt in range(3):
            tried += 1
            sc, probs = generate_one(llm, domain, i, seed=f"{rng.randint(0, 10**6)}")
            if sc and not probs:
                out.write(sc.to_json() + "\n"); out.flush(); kept += 1
                print(f"OK  {sc.id} words={len(sc.transcript.split())}", flush=True); break
            print(f"RETRY {domain}_{i:02d} attempt {attempt+1}: {probs[:3]}", flush=True)
out.close()
print(f"kept {kept} / tried {tried} | usage {llm.usage.as_dict()}")
