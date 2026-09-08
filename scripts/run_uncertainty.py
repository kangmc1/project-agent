"""D3 auxiliary: does action-distribution disagreement at the orchestrator's decision point flag decisive-error steps?

For instruction handoffs (H1): re-run the orchestrator's exact input prompt k times at T=0.9 with the local model,
cluster the sampled instructions by (next_speaker, normalized instruction), and measure disagreement
(1 - max cluster share) and the number of distinct clusters. Compare decisive-error handoffs vs pre-error controls.
"""
import argparse, json, random, re, collections, time
from pathlib import Path
from agent_handoff.llm import LLM
from agent_handoff.matching import _norm

p = argparse.ArgumentParser(); p.add_argument("--k", type=int, default=8); p.add_argument("--n_each", type=int, default=40); p.add_argument("--budget_chars", type=int, default=30000); a = p.parse_args()
H = [json.loads(l) for l in open("data/handoffs/magentic_one.jsonl")]
H = [h for h in H if h["receiver"] in ("WebSurfer", "Coder", "FileSurfer")]
rng = random.Random(0)
err = [h for h in H if h["mistake_at_this_handoff"]]
ctrl = [h for h in H if h["mistake_step"] and h["segment_end_step"] < h["mistake_step"] and (h["mistake_step"] - h["step_id"]) >= 12]
rng.shuffle(err); rng.shuffle(ctrl)
items = [(h, "error") for h in err[: a.n_each]] + [(h, "control") for h in ctrl[: a.n_each]]
llm = LLM(); out = open("results/raw/uncertainty_h1.jsonl", "w")

def canon(txt):
    m = re.search(r"\{.*\}", txt, re.S)
    try:
        obj = json.loads(m.group(0)); ins = obj.get("instruction_or_question", {}); ins = ins.get("answer", ins) if isinstance(ins, dict) else ins
        sp = obj.get("next_speaker", {}); sp = sp.get("answer", sp) if isinstance(sp, dict) else sp
    except Exception:
        return None
    words = [w for w in re.findall(r"[a-z0-9]+", _norm(str(ins))) if len(w) > 3][:12]
    return (str(sp), " ".join(sorted(set(words))))

for i, (h, grp) in enumerate(items):
    msgs = h["sender_context"]
    # keep the prompt faithful: system-ish first message + recent messages within budget
    text_msgs = []
    for m in msgs:
        c = m.get("content"); c = c if isinstance(c, str) else "\n".join(pp.get("text", "") for pp in c if isinstance(pp, dict)) if isinstance(c, list) else str(c)
        text_msgs.append({"role": "user" if m.get("role") != "assistant" else "assistant", "content": c})
    total = sum(len(m["content"]) for m in text_msgs)
    while total > a.budget_chars and len(text_msgs) > 2:
        total -= len(text_msgs[1]["content"]); del text_msgs[1]
    samples = []
    t0 = time.time()
    for _ in range(a.k):
        r = llm.client.chat.completions.create(model=llm.model, temperature=0.9, max_tokens=400, messages=text_msgs, extra_body={"chat_template_kwargs": {"enable_thinking": False}})
        samples.append(r.choices[0].message.content or "")
    cl = collections.Counter(c for c in (canon(s) for s in samples) if c)
    n = sum(cl.values()); dis = 1 - (max(cl.values()) / n if n else 0); speakers = collections.Counter(c[0] for c in cl.elements())
    rec = {"handoff_id": h["handoff_id"], "group": grp, "k": a.k, "parsed": n, "clusters": len(cl), "disagreement": round(dis, 3), "speaker_disagreement": round(1 - (max(speakers.values()) / n if n else 0), 3), "seconds": round(time.time() - t0, 1)}
    out.write(json.dumps(rec) + "\n"); out.flush()
    print(f"[{i+1}/{len(items)}] {grp:7s} clusters={len(cl)} dis={dis:.2f} spk_dis={rec['speaker_disagreement']:.2f}", flush=True)
print("usage", llm.usage.as_dict())
