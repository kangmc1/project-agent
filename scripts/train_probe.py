"""D3: linear probe from the orchestrator's policy vector (+ cheap context features) to 'loss at the next compression'.
Scenario-level cross-validation; reports AUROC per feature set."""
import json, random, statistics
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from agent_handoff.eval.aggregate import auroc

ev = json.load(open("results/compression_events.json"))
if len(ev) < 30:
    raise SystemExit(f"too few compression events ({len(ev)})")
FEATS = {
    "policy4": ["p_researcher", "p_executor", "p_verifier", "p_finish"],
    "policy4+entropy+margin": ["p_researcher", "p_executor", "p_verifier", "p_finish", "entropy", "margin"],
    "summary(entropy,margin,round,words)": ["entropy", "margin", "round", "words_before"],
    "all(+jsd)": ["p_researcher", "p_executor", "p_verifier", "p_finish", "entropy", "margin", "round", "words_before", "jsd"],
    "jsd only": ["jsd"],
}
scen = sorted({e["scenario_id"] for e in ev}); rng = random.Random(0); rng.shuffle(scen)
folds = [scen[i::5] for i in range(5)]
y_all = np.array([e["loss"] for e in ev])
print(f"events={len(ev)} scenarios={len(scen)} loss_rate={y_all.mean():.2f}")
for name, cols in FEATS.items():
    scores, labels = [], []
    for f in folds:
        tr = [e for e in ev if e["scenario_id"] not in f]; te = [e for e in ev if e["scenario_id"] in f]
        if not te or len({e["loss"] for e in tr}) < 2: continue
        Xtr = np.array([[e[c] for c in cols] for e in tr]); ytr = np.array([e["loss"] for e in tr])
        Xte = np.array([[e[c] for c in cols] for e in te]); yte = [e["loss"] for e in te]
        clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, C=1.0)).fit(Xtr, ytr)
        scores += list(clf.predict_proba(Xte)[:, 1]); labels += yte
    a = auroc([s for s, l in zip(scores, labels) if l], [s for s, l in zip(scores, labels) if not l])
    print(f"{name:36s} AUROC={a:.3f} (n={len(labels)})")
