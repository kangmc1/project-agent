"""D3, proper version on TraceElephant: fixed action space (next speaker among the 4 Magentic-One agents),
distribution read from guided-choice logprobs on the orchestrator's real input prompt. Error vs control handoffs."""
import json, random, math, re
from agent_handoff.llm import LLM
from agent_handoff.workflow.engine import choose

AG = ["WebSurfer", "FileSurfer", "Coder", "ComputerTerminal"]
H = [json.loads(l) for l in open("data/handoffs/magentic_one.jsonl")]
H = [h for h in H if h["receiver"] in AG]
rng = random.Random(0)
err = [h for h in H if h["mistake_at_this_handoff"]]
ctrl = [h for h in H if h["mistake_step"] and h["segment_end_step"] < h["mistake_step"] and (h["mistake_step"] - h["step_id"]) >= 12]
rng.shuffle(err); rng.shuffle(ctrl)
items = [(h, "error") for h in err[:40]] + [(h, "control") for h in ctrl[:40]]
llm = LLM(); out = open("results/raw/uncertainty_fixed_h1.jsonl", "w")

def flat(msgs, budget=30000):
    parts = []
    for m in msgs:
        c = m.get("content"); c = c if isinstance(c, str) else "\n".join(p.get("text", "") for p in c if isinstance(p, dict)) if isinstance(c, list) else str(c)
        parts.append(f"[{m.get('role')}]\n{c}")
    txt = "\n\n".join(parts)
    return txt if len(txt) <= budget else txt[:6000] + "\n…[middle omitted]…\n" + txt[-(budget - 6000):]

for i, (h, grp) in enumerate(items):
    user = flat(h["sender_context"]) + "\n\nBased on everything above, decide ONLY which agent should act next. Answer with one of: " + ", ".join(AG) + "."
    pick, probs, ent = choose(llm, "You are the Magentic-One Orchestrator. Reply with exactly one agent name.", user, AG)
    actual = h["receiver"]
    rec = {"handoff_id": h["handoff_id"], "group": grp, "actual": actual, "picked": pick, "p": probs, "entropy": ent, "p_actual": probs.get(actual, 0.0), "agree": pick == actual}
    out.write(json.dumps(rec) + "\n"); out.flush()
    print(f"[{i+1}/{len(items)}] {grp:7s} H={ent:.2f} p_actual={rec['p_actual']:.2f} actual={actual} picked={pick}", flush=True)

rs = [json.loads(l) for l in open("results/raw/uncertainty_fixed_h1.jsonl")]
import statistics
for g in ("error", "control"):
    xs = [r for r in rs if r["group"] == g]
    print(g, "n=", len(xs), "entropy mean=%.2f" % statistics.mean(r["entropy"] for r in xs), "p_actual mean=%.2f" % statistics.mean(r["p_actual"] for r in xs), "agree=%.0f%%" % (100 * statistics.mean(r["agree"] for r in xs)))
def auc(key):
    e = [r[key] for r in rs if r["group"] == "error"]; c = [r[key] for r in rs if r["group"] == "control"]
    return sum((1 if a > b else 0.5 if a == b else 0) for a in e for b in c) / (len(e) * len(c))
print("AUROC(entropy: error>control)=%.2f" % auc("entropy"), "| AUROC(1-p_actual)=%.2f" % (1 - auc("p_actual")))
