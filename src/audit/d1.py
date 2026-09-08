"""D1 — action-distribution confidence from the executor's own logprobs.

Decision point = every assistant LLM call (aux agents user_sim/summarizer excluded).  The decision position is where
the executor actually emitted its action: if the step's generated text contains a tool call, the prefix is the
rendered request PLUS the tokens the model generated before `<tool_call>` (e.g. a premise declaration); otherwise the
prefix is the rendered request (the model's first token decided "no tool").  Candidate set A = tool names bound at
that step ∪ {no_tool}.

Definition (method 2): log P(a | prefix) by swapping only the action tokens '<tool_call>\\n{"name": "<a>' and reading
`prompt_logprobs`.  Execution (stepwise): the same product of one-token conditionals via `allowed_token_ids=[t_i]`
(raw pre-mask logprob), which keeps prefix caching alive.  P4(ii) verifies distribution-level agreement.

Outputs: audit/d1.jsonl (+ optional --out), audit/d1_unscored.json, audit/d1_check.json
Usage:  python -m src.audit.d1 --check [--runs runs]
        python -m src.audit.d1 --all [--method stepwise|m2] [--planner-only] [--batch N] [--out audit/d1.jsonl] [--cut 2026-09-09T13:00]
"""
from __future__ import annotations

import argparse
import json
import math
import random
import statistics
import time
from collections import Counter, defaultdict
from pathlib import Path

try:
    import httpx2 as hx
except ImportError:  # pragma: no cover
    import httpx as hx

from .render import TOOL_CALL_HEAD, TOOL_CALL_ID, encode, render_text, tokenizer

SCORE = "http://localhost:18003/v1"
MODEL = "qwen32b-score"
AUX = {"user_sim", "summarizer"}
WRAPPERS = {"policy_checker", "db_agent", "solver", "verifier"}
MAX_PREFIX = 24576 - 64
AUDIT = Path("audit")
CLIENT = hx.Client(timeout=600)


# ----------------------------------------------------------------------------- scoring primitives
def _post(body: dict) -> dict:
    r = CLIENT.post(SCORE + "/completions", json={"model": MODEL, "temperature": 0, **body})
    r.raise_for_status()
    return r.json()


def cand_ids(name: str) -> list[int]:
    """'<tool_call>' is a special token, so the candidate tokenization is independent of what precedes it."""
    return encode(TOOL_CALL_HEAD + name)


def stepwise_logp(prefix: list[int], cand: list[int]) -> float:
    total = 0.0
    for i, t in enumerate(cand):
        d = _post({"prompt": prefix + cand[:i], "max_tokens": 1, "logprobs": 1, "allowed_token_ids": [t]})
        total += float(d["choices"][0]["logprobs"]["token_logprobs"][0])
    return total


def no_tool_logp(prefix: list[int]) -> float:
    d = _post({"prompt": prefix, "max_tokens": 1, "logprobs": 1, "allowed_token_ids": [TOOL_CALL_ID]})
    lp = float(d["choices"][0]["logprobs"]["token_logprobs"][0])
    p = min(math.exp(lp), 1 - 1e-9)
    return math.log(max(1 - p, 1e-12))


def method2_logp(prefix: list[int], cand: list[int]) -> float:
    d = _post({"prompt": prefix + cand, "max_tokens": 1, "prompt_logprobs": 1})
    pl = d["choices"][0]["prompt_logprobs"]
    total = 0.0
    for pos, t in enumerate(cand):
        entry = pl[len(prefix) + pos] or {}
        v = entry.get(str(t)) or entry.get(t)
        if v is None:
            raise RuntimeError(f"prompt_logprobs missing token {t} at {len(prefix)+pos}")
        total += float(v["logprob"])
    return total


# ----------------------------------------------------------------------------- decision points
def iter_decisions(runs_dir: Path, batch: int | None = None):
    for run in sorted(runs_dir.glob("*/")):
        sp = run / "steps.jsonl"
        if not sp.exists():
            continue
        meta = json.loads((run / "meta.json").read_text()) if (run / "meta.json").exists() else {}
        if batch is not None and meta.get("batch") != batch:
            continue
        used: set[str] = set()
        rows = [json.loads(l) for l in sp.read_text(encoding="utf-8").splitlines() if l.strip()]
        for r in rows:
            for tc in (r["response"].get("tool_calls") or []):
                used.add(tc["function"]["name"])
        for r in rows:
            if r["agent"] in AUX or not r.get("endpoint", "").endswith("/chat/completions"):
                continue
            tools = r["request"].get("tools") or []
            names = [t["function"]["name"] for t in tools]
            tcs = r["response"].get("tool_calls") or []
            actual = tcs[0]["function"]["name"] if tcs else "no_tool"
            yield {"run_id": run.name, "domain": meta.get("domain", run.name.split("_")[0]), "batch": meta.get("batch"),
                   "step_id": r["step_id"], "agent": r["agent"], "role": "planner" if r["agent"] == "planner" else "subagent",
                   "messages": r["request"]["messages"], "tools": tools, "A": names + ["no_tool"], "actual": actual,
                   "gen_logprobs": (r["response"].get("logprobs") or {}).get("content"), "A_used": sorted(used | {"no_tool"})}


def decision_prefix(dp: dict) -> tuple[list[int], int, list[int] | None]:
    """(prefix_ids at the decision position, offset = #generated tokens before <tool_call>, gen_ids or None)."""
    tok = tokenizer()
    prefix = encode(render_text(dp["messages"], dp["tools"]))
    gen = dp.get("gen_logprobs")
    gen_ids = None
    offset = 0
    if gen:
        gen_ids = tok.convert_tokens_to_ids([g["token"] for g in gen])
        if dp["actual"] != "no_tool" and TOOL_CALL_ID in gen_ids:
            offset = gen_ids.index(TOOL_CALL_ID)
            prefix = prefix + gen_ids[:offset]
    return prefix, offset, gen_ids


def score_decision(dp: dict, method: str) -> tuple[dict | None, str | None]:
    prefix, offset, gen_ids = decision_prefix(dp)
    if len(prefix) > MAX_PREFIX:
        return None, "prefix_too_long"
    logps: dict[str, float] = {}
    names = list(dp["A"])
    if dp["actual"] not in names:  # the model called a tool it was not given (hallucinated tool name) -> score it too
        names.append(dp["actual"])
    for a in names:
        if a == "no_tool":
            logps[a] = no_tool_logp(prefix)
        else:
            c = cand_ids(a)
            logps[a] = method2_logp(prefix, c) if method == "m2" else stepwise_logp(prefix, c)
    rec = finalize(dp, logps, method)
    rec["decision_offset"] = offset
    rec["actual_not_in_A"] = dp["actual"] not in dp["A"]
    return rec, None


def finalize(dp: dict, logps: dict[str, float], method: str) -> dict:
    names = list(logps)
    mx = max(logps.values())
    w = {a: math.exp(v - mx) for a, v in logps.items()}
    z = sum(w.values())
    dist = {a: w[a] / z for a in names}
    H = -sum(p * math.log2(p) for p in dist.values() if p > 0)
    n = len(names)
    conf = 1 - H / math.log2(n) if n > 1 else 1.0
    w2 = {a: math.exp((v - mx) / 2.0) for a, v in logps.items()}
    z2 = sum(w2.values())
    dist_T2 = {a: w2[a] / z2 for a in names}
    H_T2 = -sum(p * math.log2(p) for p in dist_T2.values() if p > 0)
    conf_T2 = 1 - H_T2 / math.log2(n) if n > 1 else 1.0
    ps = sorted(dist.values(), reverse=True)
    margin = ps[0] - (ps[1] if len(ps) > 1 else 0.0)
    p_actual = dist.get(dp["actual"], 0.0)
    p_del = sum(p for a, p in dist.items() if a in WRAPPERS)
    H2 = -sum(p * math.log2(p) for p in (p_del, 1 - p_del) if p > 0) if 0 < p_del < 1 else 0.0
    used = [a for a in names if a in set(dp["A_used"])]
    dist_used = None
    if len(used) > 1:
        zu = sum(w[a] for a in used)
        dist_used = {a: w[a] / zu for a in used}
    return {"run_id": dp["run_id"], "domain": dp["domain"], "batch": dp.get("batch"), "step_id": dp["step_id"], "agent": dp["agent"],
            "role": dp["role"], "A": names, "actual": dp["actual"], "logp": logps, "dist": dist, "H": H, "confidence": conf,
            "H_T2": H_T2, "confidence_T2": conf_T2, "p_actual": p_actual, "margin": margin,
            "layer2": {"p_delegate": p_del, "H2": H2}, "A_used": used, "dist_used": dist_used, "method": method}


# ----------------------------------------------------------------------------- template check (P4 i)
def template_check(dp: dict, rec: dict) -> dict | None:
    if dp["actual"] == "no_tool" or not dp.get("gen_logprobs"):
        return None
    _, offset, gen_ids = decision_prefix(dp)
    if gen_ids is None:
        return None
    c = cand_ids(dp["actual"])
    seg = gen_ids[offset: offset + len(c)]
    aligned = seg == c
    gen_sum = sum(float(g["logprob"]) for g in dp["gen_logprobs"][offset: offset + len(c)])
    scored = rec["logp"][dp["actual"]]
    return {"aligned": aligned, "offset": offset, "gen_logp": gen_sum, "scored_logp": scored, "abs_diff": abs(gen_sum - scored)}


def cache_hit_rate() -> float | None:
    try:
        txt = CLIENT.get("http://localhost:18003/metrics").text
        hits = q = 0.0
        for line in txt.splitlines():
            if line.startswith(("vllm:gpu_prefix_cache_hits_total", "vllm:prefix_cache_hits_total")):
                hits += float(line.split()[-1])
            elif line.startswith(("vllm:gpu_prefix_cache_queries_total", "vllm:prefix_cache_queries_total")):
                q += float(line.split()[-1])
        return hits / q if q else None
    except Exception:
        return None


# ----------------------------------------------------------------------------- commands
def cmd_check(runs_dir: Path, n_points: int = 100, batch: int | None = 1) -> dict:
    dps = list(iter_decisions(runs_dir, batch))
    traces = sorted({d["run_id"] for d in dps})
    t0 = time.time()
    recs, tchecks = [], []
    unscored = Counter()
    for dp in dps:
        rec, why = score_decision(dp, "stepwise")
        if rec is None:
            unscored[why] += 1
            continue
        recs.append(rec)
        tc = template_check(dp, rec)
        if tc:
            tchecks.append(tc)
    dt = time.time() - t0
    # stratified sample of decision points (domain x role x decile of p_actual) for method-2 rescoring
    strata = defaultdict(list)
    for r in recs:
        strata[(r["domain"], r["role"], min(int(r["p_actual"] * 10), 9))].append(r)
    rnd = random.Random(0)
    sample = []
    keys = list(strata)
    while len(sample) < min(n_points, len(recs)) and keys:
        for k in list(keys):
            if strata[k]:
                sample.append(strata[k].pop(rnd.randrange(len(strata[k]))))
                if len(sample) >= n_points:
                    break
            else:
                keys.remove(k)
    dp_index = {(d["run_id"], d["step_id"]): d for d in dps}
    dist_diffs, logp_diffs = [], []
    for r in sample:
        dp = dp_index[(r["run_id"], r["step_id"])]
        prefix, _, _ = decision_prefix(dp)
        logps_m2 = {}
        for a in r["A"]:
            logps_m2[a] = r["logp"][a] if a == "no_tool" else method2_logp(prefix, cand_ids(a))
            if a != "no_tool":
                logp_diffs.append(abs(logps_m2[a] - r["logp"][a]))
        rec_m2 = finalize(dp, logps_m2, "m2")
        dist_diffs.append({"run_id": r["run_id"], "step_id": r["step_id"], "role": r["role"],
                           "max_abs_dp": max(abs(rec_m2["dist"][a] - r["dist"][a]) for a in r["A"]),
                           "d_confidence": abs(rec_m2["confidence"] - r["confidence"]), "d_p_actual": abs(rec_m2["p_actual"] - r["p_actual"])})
    confs = [r["confidence"] for r in recs]
    margins = [r["margin"] for r in recs]
    eq_ratio = (sum(1 for d in dist_diffs if d["max_abs_dp"] <= 0.01) / len(dist_diffs)) if dist_diffs else None
    out = {
        "n_traces": len(traces), "n_decisions": len(dps), "n_scored": len(recs), "unscored": dict(unscored),
        "offset_gt0_ratio": (sum(1 for r in recs if r["decision_offset"] > 0) / len(recs)) if recs else None,
        "i_template_check": {"n": len(tchecks), "aligned_ratio": (sum(t["aligned"] for t in tchecks) / len(tchecks)) if tchecks else None,
                             "ratio_within_0.1": (sum(1 for t in tchecks if t["aligned"] and t["abs_diff"] <= 0.1) / len(tchecks)) if tchecks else None,
                             "examples": tchecks[:3]},
        "ii_equivalence": {"criterion": "max over candidates |p_stepwise - p_m2| <= 0.01 per decision point",
                           "n_decision_points": len(dist_diffs), "ratio_within_0.01": eq_ratio,
                           "ratio_within_0.05": (sum(1 for d in dist_diffs if d["max_abs_dp"] <= 0.05) / len(dist_diffs)) if dist_diffs else None,
                           "max_abs_dp": max((d["max_abs_dp"] for d in dist_diffs), default=None),
                           "max_d_confidence": max((d["d_confidence"] for d in dist_diffs), default=None),
                           "logp_level": {"n_pairs": len(logp_diffs), "ratio_within_0.01": (sum(1 for x in logp_diffs if x <= 0.01) / len(logp_diffs)) if logp_diffs else None,
                                          "ratio_within_0.15": (sum(1 for x in logp_diffs if x <= 0.15) / len(logp_diffs)) if logp_diffs else None,
                                          "max_abs_diff": max(logp_diffs, default=None),
                                          "note": "bf16 logit quantization (prefill vs decode rounding) — distribution level is the meaningful criterion"},
                           "examples": sorted(dist_diffs, key=lambda d: -d["max_abs_dp"])[:5]},
        "iii_distribution": {"confidence_sigma": statistics.pstdev(confs) if confs else None,
                             "confidence_gt_0.99_ratio": (sum(c > 0.99 for c in confs) / len(confs)) if confs else None,
                             "confidence_T2_gt_0.99_ratio": (sum(r["confidence_T2"] > 0.99 for r in recs) / len(recs)) if recs else None,
                             "degenerate": ((sum(c > 0.99 for c in confs) / len(confs)) > 0.9) if confs else None,
                             "margin_quantiles": statistics.quantiles(margins, n=4) if len(margins) > 4 else margins},
        "iv_throughput": {"seconds": dt, "decisions_per_sec": len(recs) / dt if dt else None, "prefix_cache_hit_rate": cache_hit_rate()},
        "policy": "stepwise" if (eq_ratio is not None and eq_ratio >= 0.95) else "m2_batch1_planner_only",
    }
    AUDIT.mkdir(exist_ok=True)
    (AUDIT / "d1_check.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(json.dumps({k: v for k, v in out.items() if k not in ("i_template_check",)}, indent=1, ensure_ascii=False, default=str)[:3500])
    print("template:", json.dumps({k: v for k, v in out["i_template_check"].items() if k != "examples"}))
    return out


def cmd_all(runs_dir: Path, method: str | None, planner_only: bool, batch: int | None, out_path: Path, cut_epoch: float | None) -> None:
    AUDIT.mkdir(exist_ok=True)
    if method is None:
        chk = AUDIT / "d1_check.json"
        policy = json.loads(chk.read_text())["policy"] if chk.exists() else "stepwise"
        if policy.startswith("m2"):
            method, planner_only, batch = "m2", True, 1
        else:
            method = "stepwise"
    done = set()
    if out_path.exists():
        for l in out_path.read_text().splitlines():
            if l.strip():
                r = json.loads(l)
                done.add((r["run_id"], r["step_id"]))
    unscored = Counter()
    dps = list(iter_decisions(runs_dir, batch))
    order = sorted(dps, key=lambda d: (0 if d["role"] == "planner" else 1, d["run_id"], d["step_id"]))
    n_new = 0
    with out_path.open("a", encoding="utf-8") as f:
        for dp in order:
            if (dp["run_id"], dp["step_id"]) in done:
                continue
            if planner_only and dp["role"] != "planner":
                unscored["excluded_role_policy"] += 1
                continue
            if cut_epoch and time.time() > cut_epoch:
                unscored["time_cut"] += 1
                continue
            rec, why = score_decision(dp, method)
            if rec is None:
                unscored[why] += 1
                continue
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f.flush()
            n_new += 1
    uns_path = out_path.with_name(out_path.stem + "_unscored.json")
    uns_path.write_text(json.dumps({"method": method, "planner_only": planner_only, "batch": batch, **unscored}, indent=2))
    print(f"D1 {out_path.name}: method={method} new={n_new} unscored={dict(unscored)}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default="runs")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--check-batch", type=int, default=1)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--method", choices=["stepwise", "m2"])
    ap.add_argument("--planner-only", action="store_true")
    ap.add_argument("--batch", type=int)
    ap.add_argument("--out", default="audit/d1.jsonl")
    ap.add_argument("--cut")
    a = ap.parse_args()
    cut = time.mktime(time.strptime(a.cut, "%Y-%m-%dT%H:%M")) if a.cut else None
    if a.check:
        cmd_check(Path(a.runs), batch=a.check_batch)
    if a.all:
        cmd_all(Path(a.runs), a.method, a.planner_only, a.batch, Path(a.out), cut)


if __name__ == "__main__":
    main()
