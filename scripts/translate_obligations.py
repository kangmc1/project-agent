"""Translate draft obligation sentences to Korean (batched per handoff)."""
import json
from pathlib import Path
from handoffbench.llm import LLM
out_path = Path("data/pilot/ko_obl.json")
ko = json.load(open(out_path)) if out_path.exists() else {}
llm = LLM()
for f in ("results/raw/pilot_reset_D2.jsonl", "results/raw/pilot_instruction_D2.jsonl"):
    if not Path(f).exists(): continue
    for l in open(f):
        r = json.loads(l); hid = r["handoff_id"]
        obs = r["result"].get("obligations", [])
        if not obs or hid in ko: continue
        listing = "\n".join(f"{o['id']}: {o['text']}" for o in obs)
        res = llm.chat_json("You translate English to Korean. Reply with ONLY a JSON object.", "다음 문장들을 한국어로 번역해 JSON으로 답하세요. 형식: {\"o1\": \"...\", \"o2\": \"...\"}. 숫자, URL, 고유명사는 그대로.\n\n" + listing, thinking=False, max_tokens=1500)
        if isinstance(res, dict):
            ko[hid] = {k: str(v) for k, v in res.items()}
            json.dump(ko, open(out_path, "w"), ensure_ascii=False, indent=0)
            print(hid[-26:], len(ko[hid]), flush=True)
print("done", len(ko))
