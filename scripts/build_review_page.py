"""Build the A-layer review page (HTML) from the pilot set + D2 draft labels.

The page is published as an Artifact with the `db` capability: reviewers correct the draft labels,
each handoff is saved to db doc labels/<handoff_id>, and the labels are read back with read_db.
"""
import json, html, datetime
from pathlib import Path
from handoffbench.data.render import render_reset_handoff, render_instruction_handoff

pilot = json.load(open("data/pilot/pilot_set.json"))
R = {json.loads(l)["handoff_id"]: json.loads(l) for l in open("data/handoffs/magentic_one_resets.jsonl")}
I = {json.loads(l)["handoff_id"]: json.loads(l) for l in open("data/handoffs/magentic_one.jsonl")}
drafts = {}
for f in ("results/raw/pilot_reset_D2.jsonl", "results/raw/pilot_instruction_D2.jsonl"):
    if Path(f).exists():
        for l in open(f):
            r = json.loads(l); drafts[r["handoff_id"]] = r["result"]

def clip(s, n):
    return s if len(s) <= n else s[:n] + f"\n…[{len(s)-n} chars omitted]…"

items = []
for layer, ids in (("reset", pilot["reset"]), ("instruction", pilot["instruction"])):
    for hid in ids:
        h = R[hid] if layer == "reset" else I[hid]
        rd = render_reset_handoff(h, budget=14000) if layer == "reset" else render_instruction_handoff(h, budget=14000)
        d = drafts.get(hid, {})
        obls = []
        for o in d.get("obligations", []):
            obls.append({"id": o["id"], "type": o.get("type", "fact"), "text": o["text"],
                         "survival": (d.get("survival", {}).get(o["id"], {}) or {}).get("status", "preserved"),
                         "adherence": (d.get("adherence", {}).get(o["id"], {}) or {}).get("status", "n/a")})
        items.append({
            "id": hid, "layer": layer, "role": pilot["roles"][hid], "run": h["run_id"],
            "task": h["task_instruction"], "ground_truth": h["ground_truth"],
            "sender_context": clip(rd["sender_context"], 12000), "artifact": clip(rd["artifact"], 9000),
            "receiver_behavior": clip(rd["receiver_behavior"], 6000),
            "te_note": f"[{h['mistake_agent']} @ step {h['mistake_step']}] {h['mistake_reason']}",
            "receiver": h.get("receiver", "team"), "step": h.get("step_id", h.get("reset_step_id")),
            "draft": {"obligations": obls, "faults": d.get("faults", []), "responsibility": d.get("responsibility", "none"),
                      "claims": [c for c in d.get("artifact_claims", []) if str(c.get("status", "")).lower() != "supported"],
                      "notes": d.get("adherence_notes", ""), "has_draft": bool(d)},
        })

tpl = open("scripts/review_template.html", encoding="utf-8").read()
out = tpl.replace("/*__DATA__*/", json.dumps(items, ensure_ascii=False)).replace("__BUILT__", datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
Path("results/review/review.html").write_text(out, encoding="utf-8")
print(f"items={len(items)} with_draft={sum(i['draft']['has_draft'] for i in items)} size={len(out)/1e6:.2f}MB")
