"""Korean reading aid for the review page: translate task/artifact/obligations, summarize receiver behaviour."""
import json, sys
from pathlib import Path
from handoffbench.llm import LLM
from handoffbench.data.render import render_reset_handoff, render_instruction_handoff

pilot = json.load(open("data/pilot/pilot_set.json"))
R = {json.loads(l)["handoff_id"]: json.loads(l) for l in open("data/handoffs/magentic_one_resets.jsonl")}
I = {json.loads(l)["handoff_id"]: json.loads(l) for l in open("data/handoffs/magentic_one.jsonl")}
out_path = Path("data/pilot/ko.json")
ko = json.load(open(out_path)) if out_path.exists() else {}
llm = LLM()
SYS = "You are a professional English-to-Korean translator for technical logs. Translate faithfully; keep URLs, code, numbers, proper nouns and tool names unchanged. Output Korean only."

def tr(text, max_tokens=1800):
    return llm.chat(SYS, "다음 텍스트를 자연스러운 한국어로 번역하세요. 형식(줄바꿈, 번호, 불릿)은 유지하세요.\n\n" + text, max_tokens=max_tokens, thinking=False)

def summ(text):
    return llm.chat(SYS, "다음은 에이전트가 지시를 받은 뒤 실제로 한 행동과 보고의 기록입니다. 무엇을 했고 무엇을 관찰했으며 지시대로 했는지 한국어 불릿 4~7개로 요약하세요. 페이지 제목, 검색어, 숫자 등 판단에 필요한 구체적 정보는 그대로 인용하세요.\n\n" + text[:7000], max_tokens=700, thinking=False)

gold = json.load(open("data/pilot/gold20.json")) if Path("data/pilot/gold20.json").exists() else []
order = [(("reset" if h in R else "instruction"), h) for h in gold]
order += [("reset", h) for h in pilot["reset"] if h not in gold] + [("instruction", h) for h in pilot["instruction"] if h not in gold]
for layer, hid in order:
    if True:
        if hid in ko and ko[hid].get("behavior_ko"):
            continue
        h = R[hid] if layer == "reset" else I[hid]
        rd = render_reset_handoff(h, budget=14000) if layer == "reset" else render_instruction_handoff(h, budget=14000)
        rec = {"task_ko": tr(h["task_instruction"], 400)}
        if layer == "reset":
            core = "UPDATED FACT SHEET:\n" + h["facts_text"] + "\n\nNEW PLAN:\n" + h["plan_text"][:3000]
            rec["artifact_ko"] = tr(core, 2500)
        else:
            rec["artifact_ko"] = tr(rd["artifact"], 500)
        rec["behavior_ko"] = summ(rd["receiver_behavior"])
        ko[hid] = rec
        json.dump(ko, open(out_path, "w"), ensure_ascii=False, indent=0)
        print(f"{layer} {hid[-26:]} ok", flush=True)
print("done", len(ko), llm.usage.as_dict())
