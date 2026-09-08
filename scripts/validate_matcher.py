"""Validate the rule matcher on ground truth by construction.

For each scenario: compress the transcript once (free + json) with the local model to get a realistic state,
then apply programmatic edits whose effect is known:
  keep     -> expected preserved for all items
  drop(o)  -> remove the line/item holding o's key values -> expected absent (or altered)
  alter(o) -> change one numeric key value -> expected absent/altered
  promote(o: open_question) -> move its line into the verified section, strip hedges / set status verified -> expected promoted
Reports the matcher's confusion matrix per edit type.
"""
import argparse, json, re, random, collections
from pathlib import Path
from agent_handoff.llm import LLM
from agent_handoff.chain.stress import COMPRESS_FREE, COMPRESS_JSON
from agent_handoff.matching import survival_report, _present, HEDGES, _items

p = argparse.ArgumentParser(); p.add_argument("--scenarios", default="data/scenarios/scenarios.jsonl"); p.add_argument("--n", type=int, default=0); a = p.parse_args()
scs = [json.loads(l) for l in open(a.scenarios)]
if a.n: scs = scs[: a.n]
llm = LLM(); rng = random.Random(0)
conf = collections.defaultdict(collections.Counter); rows = []

def line_of(text, vals):
    for ln in _items(text):
        if all(_present(v, ln) for v in vals): return ln
    for ln in _items(text):
        if any(_present(v, ln) for v in vals): return ln
    return None

for sc in scs:
    obls = sc["obligations"]
    for fmt, tmpl in (("free", COMPRESS_FREE), ("json", COMPRESS_JSON)):
        state = llm.chat("You are a precise orchestrator.", tmpl.format(task=sc["task"], state=sc["transcript"], log="(no new work yet; compress the transcript above)", budget=220), max_tokens=1400, temperature=0.0, thinking=False)
        base = survival_report(obls, state)
        for o in obls:
            conf[(fmt, "keep")][base[o["id"]]] += 1
        # edits on items that survived the base compression
        for o in obls:
            if base[o["id"]] != "preserved": continue
            ln = line_of(state, o["key_values"])
            if not ln: continue
            # drop
            st = state.replace(ln, "", 1); conf[(fmt, "drop")][survival_report(obls, st)[o["id"]]] += 1
            # alter a number if present
            nums = [v for v in o["key_values"] if re.search(r"\d", v)]
            if nums:
                v = nums[0]; nv = re.sub(r"\d", lambda m: str((int(m.group(0)) + 3) % 10), v, count=1)
                st = state.replace(ln, ln.replace(v, nv), 1); conf[(fmt, "alter")][survival_report(obls, st)[o["id"]]] += 1
            # promote open questions
            if o["type"] == "open_question":
                if fmt == "json":
                    nl = re.sub(r'"status"\s*:\s*"[a-z_]+"', '"status": "verified"', ln)
                    st = state.replace(ln, nl, 1)
                else:
                    nl = HEDGES.sub("", ln).replace("?", ".")
                    st = state.replace(ln, "", 1)
                    st = re.sub(r"(1\.\s*GIVEN OR VERIFIED FACTS[^\n]*\n)", r"\1" + nl.strip() + "\n", st, count=1)
                conf[(fmt, "promote")][survival_report(obls, st)[o["id"]]] += 1
    rows.append({"id": sc["id"], "base_free": None})
print("format  edit     -> matcher verdicts")
for (fmt, edit), c in sorted(conf.items()):
    tot = sum(c.values()); exp = {"keep": "preserved", "drop": "absent/altered", "alter": "absent/altered", "promote": "promoted"}[edit]
    ok = c["preserved"] if edit == "keep" else (c["absent"] + c["altered"] if edit in ("drop", "alter") else c["promoted"])
    print(f"{fmt:5s}   {edit:8s} n={tot:3d} correct={ok/tot:.0%}  {dict(c)}  (expected {exp})")
json.dump({f"{k[0]}|{k[1]}": dict(v) for k, v in conf.items()}, open("results/matcher_validation.json", "w"), indent=1)
print("usage", llm.usage.as_dict())
