"""Score the 60-item D3 gold sample with an LLM-only judge (same prompt as src/audit/llm_only.d3). Env: LLM_JUDGE_BASE/MODEL/TAG."""
import json, sys
sys.path.insert(0, '.')
import src.audit.llm_only as L
from src.audit.extract import map_parallel
sample = json.load(open('labels/d3_loss/sample.json'))
tasks = [{"item_id": it["item_id"], "direction": it["direction"], "prompt": f"{L._D3}\n\nDomain: airline\nBoundary: {it['wrapper']} {it['direction']}\n\n--- TEXT A ---\n{it['A'][:4000]}\n\n--- TEXT B ---\n{(it['B'].strip() or '(empty)')[:4000]}\n\nReturn JSON only."} for it in sample]
def score(t):
    out, lat, toks = L.ask(t["prompt"]); f = (out or {}).get("fidelity") if out else None
    try: f = None if f is None else min(1.0, max(0.0, float(f)))
    except Exception: f = None
    return {"item_id": t["item_id"], "direction": t["direction"], "fidelity": f, "missing": (out or {}).get("missing", []) if out else [], "latency": lat}
rows = map_parallel(score, tasks)
tag = L.TAG or "qwen32b"
json.dump(rows, open(f'labels/d3_loss/llm_{tag}.json', 'w'), ensure_ascii=False, indent=1)
print(tag, "scored", sum(1 for r in rows if r["fidelity"] is not None), "/", len(rows))
