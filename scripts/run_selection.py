"""B0 experiment: selection loss over scenarios (task-unknown setting). Output: results/selection.json"""
import json, statistics, collections
from agent_handoff.llm import LLM
from agent_handoff.workflow.selection import load_catalog, select_team, selection_loss
cat = load_catalog(); llm = LLM(); rows = []
for l in open("data/scenarios/scenarios.jsonl"):
    sc = json.loads(l); req = sc.get("required_capabilities") or []
    if not req: continue
    sel = select_team(llm, sc["task"], cat); loss = selection_loss(sel, req)
    rows.append({"scenario_id": sc["id"], "domain": sc["domain"], "selected": sel["selected"], "slots": sel["slots"], **loss})
    print(f"{sc['id']:22s} selected={sel['selected']} missing={loss['missing']} slots_missing={loss['slots_missing']}", flush=True)
json.dump(rows, open("results/selection.json", "w"), indent=1)
print(f"\nn={len(rows)} mean selection loss={statistics.mean(r['loss'] for r in rows):.2f} | scenarios with any missing capability={sum(1 for r in rows if r['missing'])} | missing slots={collections.Counter(s for r in rows for s in r['slots_missing'])}")
