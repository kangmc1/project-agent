"""Add `required_capabilities` (catalog capability ids) to each scenario with one LLM call, constrained to the catalog vocabulary."""
import json
from agent_handoff.llm import LLM
from agent_handoff.workflow.selection import load_catalog
cat = load_catalog(); vocab = sorted({c for x in cat for c in x["capabilities"]})
llm = LLM(); out = []
for l in open("data/scenarios/scenarios.jsonl"):
    sc = json.loads(l)
    if sc.get("required_capabilities"):
        out.append(sc); continue
    r = llm.chat_json("Reply with ONLY JSON.", f"Which of these capabilities are REQUIRED to complete the task correctly (2-4 items, only from the list)?\n\nTASK: {sc['task']}\n\nOBLIGATIONS: " + "; ".join(o['text'] for o in sc['obligations']) + f"\n\nLIST: {', '.join(vocab)}\n\nReply: {{\"required\": [\"...\"]}}", thinking=False, max_tokens=150)
    req = [x for x in (r.get("required", []) if isinstance(r, dict) else []) if x in vocab][:4]
    sc["required_capabilities"] = req; out.append(sc); print(sc["id"], req, flush=True)
with open("data/scenarios/scenarios.jsonl", "w") as f:
    for sc in out: f.write(json.dumps(sc, ensure_ascii=False) + "\n")
