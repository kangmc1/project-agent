"""Evaluate D4 evidence-dependence judge outputs against the step labels (same cells and definitions as src/eval/metrics.py).
Usage: python scripts/eval_d4.py audit/d4_evidence_judge_gptoss20b.jsonl [more files...]
Per file x domain (subagent role): n_pos / n_neg, AUROC all errors / decisive [95% CI], flag = score > 0 -> precision, recall,
FPR (clean steps flagged), decisive recall, and the parse-failure count."""
from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from src.eval.metrics import labeled_steps, auroc, auroc_ci, fmt_auc, read_jsonl

POS = ("decisive", "transient", "error")

def evaluate(path: Path, rows_by_key: dict) -> list[list[str]]:
    scores, unparsed = {}, 0
    for r in read_jsonl(path):
        if r.get("score") is None:
            unparsed += 1; continue
        scores[(r["run_id"], int(r["step_id"]))] = float(r["score"])
    out = []
    for domain in ("airline", "aime"):
        usable = [(row, scores[k]) for k, row in rows_by_key.items() if row.domain == domain and row.role == "subagent" and k in scores and row.cls != "cascade"]
        neg = np.array([s for r, s in usable if r.cls == "clean"]); pos = np.array([s for r, s in usable if r.cls in POS]); dec = np.array([s for r, s in usable if r.cls == "decisive"])
        if len(neg) == 0 or len(pos) == 0:
            continue
        a_all, a_dec = auroc_ci(pos, neg), (auroc_ci(dec, neg) if len(dec) >= 3 else None)
        tp, fp = int((pos > 0).sum()), int((neg > 0).sum())
        prec = tp / (tp + fp) if tp + fp else float("nan"); rec = tp / len(pos); fpr = fp / len(neg); drec = float((dec > 0).mean()) if len(dec) else float("nan")
        out.append([path.name, domain, f"{len(pos)} / {len(neg)}", fmt_auc(a_all), str(len(dec)), fmt_auc(a_dec) if a_dec else "n/a",
                    f"{prec:.2f}", f"{rec:.2f}", f"{fpr:.2f}", f"{drec:.2f}", str(unparsed)])
    return out

def main() -> None:
    rows_by_key = {(r.run_id, r.step_id): r for r in labeled_steps(".")}
    hdr = ["file", "domain", "n_pos / n_neg", "AUROC all [95% CI]", "n_dec", "AUROC decisive [95% CI]", "flag precision", "recall", "FPR", "decisive recall", "unparsed"]
    lines = [hdr] + [row for a in sys.argv[1:] for row in evaluate(Path(a), rows_by_key)]
    print("| " + " | ".join(hdr) + " |"); print("|" + "---|" * len(hdr))
    for row in lines[1:]:
        print("| " + " | ".join(row) + " |")

if __name__ == "__main__":
    main()
