"""Aggregate stress-chain and workflow grid results into tables and figure-ready JSON."""
from __future__ import annotations
import json, collections, statistics
from pathlib import Path


def load(path):
    """Load a JSONL file, or all shard files matching '<stem>*.jsonl' (e.g. workflow_grid.jsonl + workflow_grid_s0.jsonl ...)."""
    p = Path(path); rows = []
    for f in sorted(p.parent.glob(p.stem + "*.jsonl")):
        if "_v0" in f.name or "leaky" in f.name or "probe" in f.name or "smoke" in f.name: continue
        rows += [json.loads(l) for l in f.open()]
    return rows


def stress_curves(rows):
    """S(k) per condition (format, budget, guard): mean preserved per hop, plus promoted/absent; n scenarios."""
    by = collections.defaultdict(list)
    for r in rows:
        by[(r["format"], r["budget"], r["guard"])].append(r)
    out = {}
    for key, rs in sorted(by.items()):
        hops = max(len(r["hops"]) for r in rs)
        curve = []
        for k in range(hops):
            vals = [r["hops"][k]["score"] for r in rs if k < len(r["hops"])]
            curve.append({"hop": k + 1, "preserved": statistics.mean(v["preserved"] for v in vals), "promoted": statistics.mean(v["promoted"] for v in vals),
                          "absent": statistics.mean(v["absent"] for v in vals), "altered": statistics.mean(v["altered"] for v in vals), "n": len(vals),
                          "words": statistics.mean(r["hops"][k]["words"] for r in rs if k < len(r["hops"]))})
        half = next((c["hop"] for c in curve if c["preserved"] < 0.5), None)
        toks = statistics.mean(r.get("tokens", {}).get("prompt", 0) + r.get("tokens", {}).get("completion", 0) for r in rs)
        out[f"{key[0]}|b{key[1]}|g{int(key[2])}"] = {"format": key[0], "budget": key[1], "guard": key[2], "n": len(rs), "curve": curve, "half_life_hop": half, "tokens_mean": toks}
    return out


def workflow_table(rows):
    """Final-deliverable metrics per condition (visibility, format, guard, width)."""
    by = collections.defaultdict(list)
    for r in rows:
        by[(r["visibility"], r["format"], r["guard"], r.get("width", 1))].append(r)
    out = {}
    for key, rs in sorted(by.items()):
        comp = [e["compression"] for r in rs for e in r["log"] if e.get("compression")]
        out[f"{key[0]}|{key[1]}|g{int(key[2])}|w{key[3]}"] = {
            "visibility": key[0], "format": key[1], "guard": key[2], "width": key[3], "n": len(rs),
            "final_preserved": statistics.mean(r["final_score"]["preserved"] for r in rs),
            "final_promoted": statistics.mean(r["final_score"]["promoted"] for r in rs),
            "final_absent": statistics.mean(r["final_score"]["absent"] for r in rs),
            "constraints_kept": statistics.mean(r["checks"]["constraints_kept"] / max(1, r["checks"]["constraints_total"]) for r in rs),
            "prohibition_violation_rate": statistics.mean(r["checks"]["prohibitions_violated"] / max(1, r["checks"]["prohibitions_total"]) for r in rs),
            "fabricated_final_mean": statistics.mean(len(r["checks"]["fabricated_in_final"]) for r in rs),
            "compressions_mean": statistics.mean(r["n_compressions"] for r in rs),
            # B2 acquisition (entered the team via task or Researcher reports) and transit loss (acquired but absent/altered in the final)
            "acquired_rate": statistics.mean(r["checks"]["n_acquired"] / max(1, r["checks"]["n_obligations"]) for r in rs if "n_acquired" in r["checks"]) if any("n_acquired" in r["checks"] for r in rs) else None,
            "transit_loss_rate": statistics.mean(len(r["checks"]["lost_after_acquired"]) / max(1, r["checks"]["n_acquired"]) for r in rs if "n_acquired" in r["checks"]) if any("n_acquired" in r["checks"] for r in rs) else None,
            "b3_loss_rate_mean": statistics.mean(c["b3_loss_rate"] for c in comp if c.get("b3_loss_rate") is not None) if any(c.get("b3_loss_rate") is not None for c in comp) else None,
            "compression_preserved_mean": statistics.mean(c["score"]["preserved"] for c in comp) if comp else None,
            "compression_promoted_mean": statistics.mean(c["score"]["promoted"] for c in comp) if comp else None,
            "jsd_mean": statistics.mean(c.get("decision_jsd", 0.0) for c in comp) if comp else None,
            "verifier_revise_rate": statistics.mean(r["verifier_revise"] / max(1, r["verifier_revise"] + r["verifier_approve"]) for r in rs if (r["verifier_revise"] + r["verifier_approve"]) > 0) if any((r["verifier_revise"] + r["verifier_approve"]) > 0 for r in rs) else None,
            "entropy_mean": statistics.mean(e["entropy_agent"] for r in rs for e in r["log"] if e.get("entropy_agent") is not None),
            "rounds_mean": statistics.mean(r["rounds_run"] for r in rs),
            "tokens_mean": statistics.mean(r.get("tokens", {}).get("prompt", 0) + r.get("tokens", {}).get("completion", 0) for r in rs),
        }
    return out


def compression_events(rows):
    """One record per compression: features from the preceding round + loss label (for the probe and JSD analysis)."""
    ev = []
    for r in rows:
        prev = None
        for e in r["log"]:
            c = e.get("compression")
            if c:
                p = e.get("p_agent", {}); ps = sorted(p.values(), reverse=True) + [0, 0]
                ev.append({"scenario_id": r["scenario_id"], "condition": f"{r['visibility']}|{r['format']}|g{int(r['guard'])}", "round": e["round"],
                           "p_researcher": p.get("Researcher", 0), "p_executor": p.get("Executor", 0), "p_verifier": p.get("Verifier", 0), "p_finish": p.get("finish", 0),
                           "entropy": e.get("entropy_agent", 0), "margin": ps[0] - ps[1], "words_before": c["words_before"], "jsd": c.get("decision_jsd", 0.0),
                           "entropy_before": c.get("entropy_before"), "entropy_after": c.get("entropy_after"),
                           "preserved": c["score"]["preserved"], "promoted": c["score"]["promoted"],
                           "n_had": c.get("n_had"), "b3_loss_rate": c.get("b3_loss_rate"),
                           # loss label = at least one item the team HAD before compressing is absent/altered/promoted afterwards
                           "loss": int(bool(c.get("lost_ids"))) if "lost_ids" in c else int(c["score"]["preserved"] < 1.0 or c["score"]["promoted"] > 0)})
            prev = e
    return ev


def auroc(pos, neg):
    if not pos or not neg: return None
    return sum((1 if a > b else 0.5 if a == b else 0) for a in pos for b in neg) / (len(pos) * len(neg))
