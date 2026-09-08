"""Run detectors on handoff events and save raw outputs.

Usage: python scripts/run_detectors.py --layer reset --n 5 --detectors D1,D2 --tag pilot
Outputs: results/raw/<tag>_<layer>_<detector>.jsonl (one line per handoff)
"""
import argparse, json, time, random
from pathlib import Path
from handoffbench.llm import LLM
from handoffbench.data.render import render_reset_handoff, render_instruction_handoff
from handoffbench.detectors.contract import contract_check
from handoffbench.detectors.holistic import holistic_judge

p = argparse.ArgumentParser()
p.add_argument("--layer", choices=["reset", "instruction"], required=True)
p.add_argument("--n", type=int, default=5)
p.add_argument("--select", default="mistake", help="mistake: prefer handoffs where the decisive error is at/near this handoff; random; all")
p.add_argument("--detectors", default="D1,D2")
p.add_argument("--budget", type=int, default=20000)
p.add_argument("--tag", default="dev")
p.add_argument("--seed", type=int, default=0)
a = p.parse_args()

path = Path("data/handoffs") / ("magentic_one_resets.jsonl" if a.layer == "reset" else "magentic_one.jsonl")
items = [json.loads(l) for l in open(path)]
if a.layer == "instruction":
    items = [h for h in items if h["receiver"] in ("WebSurfer", "Coder", "FileSurfer", "ComputerTerminal")]
random.Random(a.seed).shuffle(items)
if a.select == "mistake":
    key = (lambda h: (h["mistake_position"] != "at_reset_summary", h["mistake_position"] != "before_reset")) if a.layer == "reset" else (lambda h: (not h["mistake_at_this_handoff"], not h["mistake_in_segment"]))
    items.sort(key=key)
if a.select == "pilot":
    ids = set(json.load(open("data/pilot/pilot_set.json"))[a.layer])
    items = [h for h in items if h["handoff_id"] in ids]
else:
    items = items if a.select == "all" else items[: a.n]
render = render_reset_handoff if a.layer == "reset" else render_instruction_handoff

llm = LLM()
outdir = Path("results/raw"); outdir.mkdir(parents=True, exist_ok=True)
files = {d: open(outdir / f"{a.tag}_{a.layer}_{d}.jsonl", "w") for d in a.detectors.split(",")}
for i, h in enumerate(items):
    rd = render(h, budget=a.budget)
    for d, f in files.items():
        t0 = time.time(); u0 = llm.usage.as_dict()
        try:
            res = contract_check(llm, rd) if d == "D2" else holistic_judge(llm, rd)
            err = None
        except Exception as e:
            res, err = {"faults": ["ERR"], "responsibility": "none"}, str(e)[:300]
        u1 = llm.usage.as_dict()
        rec = {"handoff_id": h["handoff_id"], "layer": a.layer, "detector": d, "result": res, "error": err,
               "seconds": round(time.time() - t0, 1), "prompt_tokens": u1["prompt_tokens"] - u0["prompt_tokens"],
               "completion_tokens": u1["completion_tokens"] - u0["completion_tokens"], "render_stats": rd["render_stats"],
               "meta": {k: h.get(k) for k in ("mistake_agent", "mistake_step", "mistake_reason", "mistake_position", "mistake_at_this_handoff", "mistake_in_segment", "receiver", "index_in_run")}}
        f.write(json.dumps(rec, ensure_ascii=False) + "\n"); f.flush()
        print(f"[{i+1}/{len(items)}] {d} {h['handoff_id']} -> {res.get('faults')} {res.get('responsibility')} ({rec['seconds']}s)")
for f in files.values():
    f.close()
print("usage", llm.usage.as_dict())
