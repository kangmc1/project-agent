"""D2 (DESIGN ONLY, NOT USED IN RESULTS — user decision 07:05) — LLM-verbalized dependence of a subagent response on its evidence.

The 8B model receives two texts — (A) the evidence the subagent had in this request (tool results, plus the instruction
it was given) and (B) the subagent's response — and verbalizes, claim by claim, how the response relates to the evidence,
in a fixed JSON schema:
  supported    : stated in / directly readable from the evidence
  derived      : computed, converted, summed or paraphrased from evidence values
  unsupported  : not obtainable from the evidence or the instruction
  contradicted : conflicts with the evidence
The LLM acts as a judge here (a deliberate departure from "LLM extracts, code judges", recorded in the proposal); it never
sees labels or ground truth. Step score = (unsupported + contradicted) / claims; derived ratio reported alongside.
Output: audit/d2_judge.jsonl   Usage: python -m src.audit.d2_judge [--runs runs] [--labeled-only]
"""
from __future__ import annotations

import argparse
import glob
import json
from pathlib import Path

from ..d3_args import _load_run
from ..extract import extract_json, map_parallel

AUX = {"user_sim", "summarizer", "planner"}
AUDIT = Path("audit")
LABELS = {"supported", "derived", "unsupported", "contradicted"}

_SCHEMA = (
    'Return a single JSON object: {"claims": [{"claim": str, "relation": "supported"|"derived"|"unsupported"|"contradicted", '
    '"evidence": str}, ...]}. You are given EVIDENCE (tool results an agent received, plus the instruction it was given) and a '
    "RESPONSE written by that agent. Split the RESPONSE into its atomic factual claims (every value, id, date, price, status, "
    "conclusion). For each claim state how it relates to the EVIDENCE: supported = stated verbatim or directly readable in the "
    "evidence; derived = computed, converted, summed or paraphrased from evidence values (say which); unsupported = cannot be "
    "obtained from the evidence or the instruction; contradicted = conflicts with the evidence. evidence = the shortest quote "
    "or computation that justifies your relation label (empty for unsupported)."
)


def judge(evidence: str, instruction: str, response: str) -> list[dict]:
    text = f"INSTRUCTION GIVEN TO THE AGENT:\n{instruction[:2000]}\n\nEVIDENCE (tool results):\n{evidence[:12000]}\n\nRESPONSE:\n{response[:4000]}"
    out = extract_json(text, _SCHEMA)
    claims = (out or {}).get("claims")
    if not isinstance(claims, list):
        return []
    res = []
    for c in claims:
        if isinstance(c, dict):
            rel = str(c.get("relation", "")).lower().strip()
            if rel in LABELS:
                res.append({"claim": str(c.get("claim", ""))[:300], "relation": rel, "evidence": str(c.get("evidence", ""))[:300]})
    return res


def step_targets(run: Path):
    steps, calls, meta = _load_run(run)
    domain = meta.get("domain", run.name.split("_")[0])
    for s in steps:
        if s["agent"] in AUX:
            continue
        content = (s["response"].get("content") or "").strip()
        if not content:
            continue
        msgs = s["request"]["messages"]
        tool_msgs = [m.get("content") or "" for m in msgs if m["role"] == "tool"]
        if not tool_msgs:
            continue  # nothing to depend on yet
        instr = next((m.get("content") or "" for m in msgs if m["role"] == "user"), "")
        yield {"run_id": run.name, "domain": domain, "step_id": s["step_id"], "agent": s["agent"],
               "evidence": "\n---\n".join(str(t) for t in tool_msgs), "instruction": str(instr), "response": content}


def score(t: dict) -> dict:
    claims = judge(t["evidence"], t["instruction"], t["response"])
    base = {"run_id": t["run_id"], "domain": t["domain"], "step_id": t["step_id"], "agent": t["agent"]}
    if not claims:
        return {**base, "n_claims": 0, "score": None, "derived_ratio": None, "claims": []}
    n = len(claims)
    bad = sum(1 for c in claims if c["relation"] in ("unsupported", "contradicted"))
    return {**base, "n_claims": n, "n_unsupported": sum(1 for c in claims if c["relation"] == "unsupported"),
            "n_contradicted": sum(1 for c in claims if c["relation"] == "contradicted"),
            "score": bad / n, "derived_ratio": sum(1 for c in claims if c["relation"] == "derived") / n, "claims": claims}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default="runs")
    ap.add_argument("--labeled-only", action="store_true")
    a = ap.parse_args()
    labeled = {json.load(open(f))["run_id"] for f in glob.glob("labels/*.json")} if a.labeled_only else None
    targets = []
    for run in sorted(Path(a.runs).glob("*/")):
        if not (run / "steps.jsonl").exists() or (labeled is not None and run.name not in labeled):
            continue
        targets += list(step_targets(run))
    print(f"D2-judge: {len(targets)} subagent response steps with tool evidence")
    rows = list(map_parallel(score, targets))
    AUDIT.mkdir(exist_ok=True)
    with (AUDIT / "d2_judge.jsonl").open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    sc = [r["score"] for r in rows if r["score"] is not None]
    print(f"rows {len(rows)}, scored {len(sc)}, mean score {sum(sc)/len(sc) if sc else 0:.3f}, "
          f"steps with any unsupported/contradicted {sum(x>0 for x in sc)}, no claims parsed {len(rows)-len(sc)}")


if __name__ == "__main__":
    main()
