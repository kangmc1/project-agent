"""D1 — action-distribution confidence from the executor's own logprobs.

Definition (method 2): for each decision point (assistant step) and each candidate action a in
A = tool names bound at that step ∪ {no_tool}, score log P(a | context) by fixing the exact rendered
prefix and swapping only the action tokens:  prefix + '<tool_call>\\n{"name": "<a>"'.
Execution (stepwise): the same quantity computed as a product of one-token conditionals with
`allowed_token_ids=[t_i]` (raw pre-mask logprob), which keeps prefix caching alive.  Equivalence between
the two is verified on a stratified sample (P4 ii) before stepwise is used for full scoring.

Outputs: audit/d1.jsonl, audit/d1_unscored.json, audit/d1_check.json
Usage:  python -m src.audit.d1 --check [--runs runs]     python -m src.audit.d1 --all [--method stepwise|m2]
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

from .render import TOOL_CALL_ID, TOOL_CALL_HEAD, candidate_ids, prefix_ids, render_text, tokenizer

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
def iter_decisions(runs_dir: Path):
    for run in sorted(runs_dir.glob("*/")):
        sp = run / "steps.jsonl"
        if not sp.exists():
            continue
        meta = json.loads((run / "meta.json").read_text()) if (run / "meta.json").exists() else {}
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
            yield {"run_id": run.name, "domain": meta.get("domain", run.name.split("_")[0]), "step_id": r["step_id"],
                   "agent": r["agent"], "role": "planner" if r["agent"] == "planner" else "subagent",
                   "messages": r["request"]["messages"], "tools": tools, "A": names + ["no_tool"], "actual": actual,
                   "gen_logprobs": (r["response"].get("logprobs") or {}).get("content"), "A_used": sorted(used | {"no_tool"})}


def score_decision(dp: dict, method: str) -> tuple[dict | None, str | None]:
    """Returns (record, unscored_reason)."""
    text = render_text(dp["messages"], dp["tools"])
    prefix = tokenizer()(text, add_special_tokens=False)["input_ids"]
    if len(prefix) > MAX_PREFIX:
        return None, "prefix_too_long"
    logps: dict[str, float] = {}
    boundary_fail = False
    for a in dp["A"]:
        if a == "no_tool":
            logps[a] = no_tool_logp(prefix)
            continue
        cand, ok = candidate_ids(prefix, text, a)
        if not ok:
            boundary_fail = True
        logps[a] = method2_logp(prefix, cand) if (method == "m2" or not ok) else stepwise_logp(prefix, cand)
    return finalize(dp, logps, method, boundary_fail), None


def finalize(dp: dict, logps: dict[str, float], method: str, boundary_fail: bool) -> dict:
    names = list(logps)
    mx = max(logps.values())
    w = {a: math.exp(v - mx) for a, v in logps.items()}
    z = sum(w.values())
    dist = {a: w[a] / z for a in names}
    H = -sum(p * math.log2(p) for p in dist.values() if p > 0)
    n = len(names)
    conf = 1 - H / math.log2(n) if n > 1 else 1.0
    # temperature-scaled variant (T=2) — pre-mortem 4: raw distributions are extremely peaked
    w2 = {a: math.exp((v - mx) / 2.0) for a, v in logps.items()}
    z2 = sum(w2.values())
    dist_T2 = {a: w2[a] / z2 for a in names}
    H_T2 = -sum(p * math.log2(p) for p in dist_T2.values() if p > 0)
    conf_T2 = 1 - H_T2 / math.log2(n) if n > 1 else 1.0
    ps = sorted(dist.values(), reverse=True)
    margin = ps[0] - (ps[1] if len(ps) > 1 else 0.0)
    p_actual = dist.get(dp["actual"], 0.0)
    # layer 2: delegate vs not
    p_del = sum(p for a, p in dist.items() if a in WRAPPERS)
    H2 = -sum(p * math.log2(p) for p in (p_del, 1 - p_del) if p > 0) if 0 < p_del < 1 else 0.0
    # renormalized over tools actually used in this run
    used = [a for a in names if a in set(dp["A_used"])]
    dist_used = None
    if len(used) > 1:
        zu = sum(w[a] for a in used)
        dist_used = {a: w[a] / zu for a in used}
    return {"run_id": dp["run_id"], "domain": dp["domain"], "step_id": dp["step_id"], "agent": dp["agent"], "role": dp["role"],
            "A": names, "actual": dp["actual"], "logp": logps, "dist": dist, "H": H, "confidence": conf,
            "H_T2": H_T2, "confidence_T2": conf_T2,
            "p_actual": p_actual, "margin": margin, "layer2": {"p_delegate": p_del, "H2": H2}, "A_used": used,
            "dist_used": dist_used, "method": method, "boundary_fail": boundary_fail}


# ----------------------------------------------------------------------------- template check (P4 i)
def template_check(dp: dict, scored_logp_actual: float) -> dict | None:
    gen = dp.get("gen_logprobs")
    if not gen or dp["actual"] == "no_tool":
        return None
    tok = tokenizer()
    text = render_text(dp["messages"], dp["tools"])
    prefix = tok(text, add_special_tokens=False)["input_ids"]
    cand, ok = candidate_ids(prefix, text, dp["actual"])
    if not ok:
        return None
    cand_strs = tok.convert_ids_to_tokens(cand)
    gen_strs = [g["token"] for g in gen[: len(cand)]]
    # vLLM returns decoded strings; compare via ids where possible
    gen_ids = []
    for g in gen[: len(cand)]:
        ids = tok(g["token"], add_special_tokens=False)["input_ids"]
        gen_ids.append(ids[0] if len(ids) == 1 else None)
    aligned = gen_ids == cand
    gen_sum = sum(float(g["logprob"]) for g in gen[: len(cand)])
    return {"aligned": aligned, "gen_logp": gen_sum, "scored_logp": scored_logp_actual, "abs_diff": abs(gen_sum - scored_logp_actual),
            "cand_tokens": cand_strs, "gen_tokens": gen_strs}


def cache_hit_rate() -> float | None:
    try:
        txt = CLIENT.get("http://localhost:18003/metrics").text
        hits = q = 0.0
        for line in txt.splitlines():
            if line.startswith("vllm:gpu_prefix_cache_hits_total") or line.startswith("vllm:prefix_cache_hits_total"):
                hits += float(line.split()[-1])
            elif line.startswith("vllm:gpu_prefix_cache_queries_total") or line.startswith("vllm:prefix_cache_queries_total"):
                q += float(line.split()[-1])
        return hits / q if q else None
    except Exception:
        return None


# ----------------------------------------------------------------------------- commands
def cmd_check(runs_dir: Path, n_pairs: int = 100, min_traces: int = 6) -> dict:
    dps = list(iter_decisions(runs_dir))
    traces = sorted({d["run_id"] for d in dps})
    if len(traces) < min_traces:
        print(f"only {len(traces)} traces available (<{min_traces}); proceeding with what exists")
    t0 = time.time()
    recs: list[dict] = []
    unscored = Counter()
    tchecks: list[dict] = []
    for dp in dps:
        rec, why = score_decision(dp, "stepwise")
        if rec is None:
            unscored[why] += 1
            continue
        recs.append(rec)
        tc = template_check(dp, rec["logp"].get(dp["actual"], float("nan")))
        if tc:
            tchecks.append(tc)
    dt = time.time() - t0
    n_req = sum(len(r["A"]) * 2 for r in recs)  # rough: ~2 tokens per candidate
    # stratified (domain x role x decile of stepwise p) sample of (decision, candidate) pairs
    pairs = []
    for r in recs:
        for a, p in r["dist"].items():
            if a == "no_tool":
                continue
            pairs.append((r, a, p))
    strata = defaultdict(list)
    for r, a, p in pairs:
        strata[(r["domain"], r["role"], min(int(p * 10), 9))].append((r, a))
    rnd = random.Random(0)
    sample = []
    keys = list(strata)
    while len(sample) < min(n_pairs, len(pairs)) and keys:
        for k in list(keys):
            if strata[k]:
                sample.append(strata[k].pop(rnd.randrange(len(strata[k]))))
                if len(sample) >= n_pairs:
                    break
            else:
                keys.remove(k)
    diffs = []
    dist_diffs = []
    dp_index = {(d["run_id"], d["step_id"]): d for d in dps}
    rec_index = {(r["run_id"], r["step_id"]): r for r in recs}
    sampled_dps = []
    seen = set()
    for r, a in sample:
        key = (r["run_id"], r["step_id"])
        if key not in seen:
            seen.add(key)
            sampled_dps.append(key)
    for key in sampled_dps:
        dp = dp_index[key]
        r = rec_index[key]
        text = render_text(dp["messages"], dp["tools"])
        prefix = tokenizer()(text, add_special_tokens=False)["input_ids"]
        logps_m2: dict[str, float] = {}
        for a in dp["A"]:
            if a == "no_tool":
                logps_m2[a] = r["logp"][a]  # same primitive in both methods
                continue
            cand, ok = candidate_ids(prefix, text, a)
            if not ok:
                continue
            logps_m2[a] = method2_logp(prefix, cand)
            diffs.append({"run_id": r["run_id"], "step_id": r["step_id"], "cand": a, "stepwise": r["logp"][a], "m2": logps_m2[a],
                          "abs_diff": abs(logps_m2[a] - r["logp"][a])})
        if len(logps_m2) == len(dp["A"]):
            rec_m2 = finalize(dp, logps_m2, "m2", False)
            dmax = max(abs(rec_m2["dist"][a] - r["dist"][a]) for a in dp["A"])
            dist_diffs.append({"run_id": r["run_id"], "step_id": r["step_id"], "max_abs_dp": dmax,
                               "d_confidence": abs(rec_m2["confidence"] - r["confidence"]), "d_p_actual": abs(rec_m2["p_actual"] - r["p_actual"])})
    confs = [r["confidence"] for r in recs]
    margins = [r["margin"] for r in recs]
    eq_ratio_logp = (sum(1 for d in diffs if d["abs_diff"] <= 0.01) / len(diffs)) if diffs else None
    eq_ratio = (sum(1 for d in dist_diffs if d["max_abs_dp"] <= 0.01) / len(dist_diffs)) if dist_diffs else None
    tmpl_ratio = (sum(1 for t in tchecks if t["aligned"] and t["abs_diff"] <= 0.1) / len(tchecks)) if tchecks else None
    out = {
        "n_traces": len(traces), "n_decisions": len(dps), "n_scored": len(recs), "unscored": dict(unscored),
        "i_template_check": {"n": len(tchecks), "ratio_within_0.1": tmpl_ratio,
                             "aligned_ratio": (sum(t["aligned"] for t in tchecks) / len(tchecks)) if tchecks else None,
                             "examples": tchecks[:3]},
        "ii_equivalence": {"criterion": "max over candidates |p_stepwise - p_m2| <= 0.01 per decision point (distribution level)",
                           "n_decision_points": len(dist_diffs), "ratio_within_0.01": eq_ratio,
                           "max_abs_dp": max((d["max_abs_dp"] for d in dist_diffs), default=None),
                           "max_d_confidence": max((d["d_confidence"] for d in dist_diffs), default=None),
                           "logp_level": {"n_pairs": len(diffs), "ratio_within_0.01": eq_ratio_logp, "ratio_within_0.15": (sum(1 for d in diffs if d["abs_diff"] <= 0.15) / len(diffs)) if diffs else None,
                                          "max_abs_diff": max((d["abs_diff"] for d in diffs), default=None),
                                          "note": "bf16 logit quantization (ulp 0.125-0.25 at |logit|~30) makes logp-level agreement unattainable for negligible-probability candidates; distribution-level agreement is the meaningful criterion"},
                           "examples": dist_diffs[:5]},
        "iii_distribution": {"confidence_sigma": statistics.pstdev(confs) if confs else None,
                             "confidence_gt_0.99_ratio": (sum(c > 0.99 for c in confs) / len(confs)) if confs else None,
                             "confidence_T2_gt_0.99_ratio": (sum(r["confidence_T2"] > 0.99 for r in recs) / len(recs)) if recs else None,
                             "degenerate": ((sum(c > 0.99 for c in confs) / len(confs)) > 0.9) if confs else None,
                             "margin_quantiles": [statistics.quantiles(margins, n=4)] if len(margins) > 4 else margins},
        "iv_throughput": {"seconds": dt, "decisions_per_sec": len(recs) / dt if dt else None, "approx_requests": n_req,
                          "prefix_cache_hit_rate": cache_hit_rate()},
        "policy": "stepwise" if (eq_ratio is not None and eq_ratio >= 0.95) else "m2_batch1_planner_only",
    }
    AUDIT.mkdir(exist_ok=True)
    (AUDIT / "d1_check.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(json.dumps({k: v for k, v in out.items() if k != "i_template_check"}, indent=1, ensure_ascii=False, default=str)[:3000])
    return out


def cmd_all(runs_dir: Path, method: str | None, planner_only: bool, cut_epoch: float | None) -> None:
    AUDIT.mkdir(exist_ok=True)
    policy = method
    if policy is None:
        chk = AUDIT / "d1_check.json"
        policy = json.loads(chk.read_text())["policy"] if chk.exists() else "stepwise"
    if policy.startswith("m2"):
        method, planner_only = "m2", True
    else:
        method = "stepwise"
    done = set()
    outp = AUDIT / "d1.jsonl"
    if outp.exists():
        for l in outp.read_text().splitlines():
            if l.strip():
                r = json.loads(l)
                done.add((r["run_id"], r["step_id"]))
    unscored = Counter()
    dps = list(iter_decisions(runs_dir))
    # planner first (all runs), then subagents — serial per run/step for cache locality
    order = sorted(dps, key=lambda d: (0 if d["role"] == "planner" else 1, d["run_id"], d["step_id"]))
    with outp.open("a", encoding="utf-8") as f:
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
            if rec["boundary_fail"]:
                unscored["boundary_assert_fail_scored_with_m2"] += 1
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f.flush()
    (AUDIT / "d1_unscored.json").write_text(json.dumps({"method": method, "planner_only": planner_only, **unscored}, indent=2))
    print("D1 done:", method, dict(unscored))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default="runs")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--method", choices=["stepwise", "m2"])
    ap.add_argument("--planner-only", action="store_true")
    ap.add_argument("--cut", help="ISO time (local) after which remaining decisions are left unscored, e.g. 2026-09-09T13:00")
    a = ap.parse_args()
    cut = time.mktime(time.strptime(a.cut, "%Y-%m-%dT%H:%M")) if a.cut else None
    if a.check:
        cmd_check(Path(a.runs))
    if a.all:
        cmd_all(Path(a.runs), a.method, a.planner_only, cut)


if __name__ == "__main__":
    main()
