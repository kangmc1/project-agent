"""Evaluate detectors on the B-layer injection set: (sender context, artifact') -> did the detector flag the manipulated item?

Scoring per injection:
  drop    -> hit if some obligation judged 'absent'  matches target_line (token overlap >= thr) or fault_items mention it
  weaken  -> hit if some obligation judged 'weakened'/'absent'/'corrupted' matches target_line
  corrupt -> hit if some obligation judged 'corrupted'/'weakened' matches target_line OR an artifact claim judged unsupported/contradicted matches modified_line
  none    -> false alarm if any S1/S2/S3 fault is raised (control)
"""
import argparse, json, time, collections
from pathlib import Path
from handoffbench.llm import LLM
from handoffbench.data.render import render_transcript
from handoffbench.detectors.contract import contract_check
from handoffbench.detectors.holistic import holistic_judge
from handoffbench.injection.facts import overlap

p = argparse.ArgumentParser()
p.add_argument("--injections", default="data/injections/reset_facts.jsonl")
p.add_argument("--detectors", default="D2")
p.add_argument("--n", type=int, default=0)
p.add_argument("--budget", type=int, default=20000)
p.add_argument("--thr", type=float, default=0.35)
p.add_argument("--tag", default="inj")
a = p.parse_args()

resets = {json.loads(l)["handoff_id"]: json.loads(l) for l in open("data/handoffs/magentic_one_resets.jsonl")}
injs = [json.loads(l) for l in open(a.injections)]
if a.n: injs = injs[: a.n]
llm = LLM()
Path("results/raw").mkdir(parents=True, exist_ok=True)
outs = {d: open(f"results/raw/{a.tag}_{d}.jsonl", "w") for d in a.detectors.split(",")}
score = collections.defaultdict(lambda: collections.Counter())

def match(items, target, thr):
    return any(overlap(t, target) >= thr for t in items)

for i, inj in enumerate(injs):
    h = resets[inj["handoff_id"]]
    ctx, stats = render_transcript(h["pre_reset_transcript"][:-1], a.budget)
    rendered = {"task": h["task_instruction"], "sender_context": ctx, "artifact": inj["artifact_modified"], "receiver_behavior": "(not applicable)", "render_stats": stats}
    for d, f in outs.items():
        t0 = time.time()
        try:
            res = contract_check(llm, rendered, stages=("obligations", "survival")) if d == "D2" else holistic_judge(llm, rendered)
            err = None
        except Exception as e:
            res, err = {"faults": ["ERR"]}, str(e)[:200]
        # scoring
        hit = None
        if d == "D2" and err is None:
            obs = {o["id"]: o["text"] for o in res.get("obligations", [])}
            by = collections.defaultdict(list)
            for oid, s in res.get("survival", {}).items():
                by[str(s.get("status", "")).lower()].append(obs.get(oid, ""))
            claims = [c.get("claim", "") for c in res.get("artifact_claims", []) if str(c.get("status", "")).lower() in ("unsupported", "contradicted")]
            if inj["op"] == "drop":
                hit = match(by["absent"], inj["target_line"], a.thr)
            elif inj["op"] == "weaken":
                hit = match(by["weakened"] + by["absent"] + by["corrupted"], inj["target_line"], a.thr)
            elif inj["op"] == "corrupt":
                hit = match(by["corrupted"] + by["weakened"], inj["target_line"], a.thr) or match(claims, inj["modified_line"] or "", a.thr)
            else:
                hit = any(fl in ("S1", "S2", "S3") for fl in res.get("faults", []))  # false alarm
        elif err is None:  # holistic
            items = [str(x) for x in res.get("fault_items", [])] + [res.get("explanation", "")]
            if inj["op"] == "none":
                hit = any(fl in ("S1", "S2", "S3") for fl in res.get("faults", []))
            else:
                hit = bool(match(items, inj["target_line"], a.thr) or (inj["modified_line"] and match(items, inj["modified_line"], a.thr)))
        score[d][(inj["op"], "hit" if hit else "miss")] += 1
        rec = {"injection_id": inj["injection_id"], "op": inj["op"], "detector": d, "hit": hit, "error": err, "target_line": inj["target_line"], "modified_line": inj["modified_line"],
               "result": res, "seconds": round(time.time() - t0, 1), "render_stats": stats}
        f.write(json.dumps(rec, ensure_ascii=False) + "\n"); f.flush()
        print(f"[{i+1}/{len(injs)}] {d} {inj['op']:7s} hit={hit} ({rec['seconds']}s) {inj['injection_id'][-40:]}", flush=True)
for d, c in score.items():
    print(d, dict(c))
print("usage", llm.usage.as_dict())
