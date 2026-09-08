"""Select the A-layer pilot set (deterministic): reset handoffs near the decisive error, instruction handoffs at the decisive error, and pre-error controls."""
import json, random
from pathlib import Path
rng = random.Random(0)
R = [json.loads(l) for l in open("data/handoffs/magentic_one_resets.jsonl")]
I = [json.loads(l) for l in open("data/handoffs/magentic_one.jsonl")]
I = [h for h in I if h["receiver"] in ("WebSurfer", "Coder", "FileSurfer", "ComputerTerminal")]
# resets: all at_reset_summary, then before_reset (the summary carries an already-wrong state), then after
rs = [r for r in R if r["mistake_position"] == "at_reset_summary"] + rng.sample([r for r in R if r["mistake_position"] == "before_reset"], 14) + rng.sample([r for r in R if r["mistake_position"] == "after_reset"], 4)
# instruction: 26 at the decisive error + 8 in-segment + 10 pre-error controls (>=4 handoffs before the mistake step)
at = [h for h in I if h["mistake_at_this_handoff"]]
seg = [h for h in I if h["mistake_in_segment"] and not h["mistake_at_this_handoff"]]
pre = [h for h in I if h["mistake_step"] and h["segment_end_step"] + 0 < h["mistake_step"] and (h["mistake_step"] - h["step_id"]) >= 12]
ins = rng.sample(at, 26) + rng.sample(seg, 8) + rng.sample(pre, 10)
out = {"reset": [r["handoff_id"] for r in rs], "instruction": [h["handoff_id"] for h in ins],
       "roles": {**{r["handoff_id"]: "reset_" + r["mistake_position"] for r in rs}, **{h["handoff_id"]: "at_error" for h in ins[:26]}, **{h["handoff_id"]: "in_segment" for h in ins[26:34]}, **{h["handoff_id"]: "pre_error_control" for h in ins[34:]}}}
Path("data/pilot").mkdir(parents=True, exist_ok=True)
json.dump(out, open("data/pilot/pilot_set.json", "w"), indent=1)
print("pilot set: resets", len(out["reset"]), "instruction", len(out["instruction"]), "| pre-error pool", len(pre), "at-error pool", len(at))
