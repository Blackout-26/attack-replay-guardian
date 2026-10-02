"""Train the baseline on the TRAIN partition only. C is chosen by stratified CV on train (validation); final test untouched."""
import sys, hashlib, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import numpy as np
from sklearn.metrics import f1_score
from sklearn.model_selection import StratifiedKFold
from ar import config as C
from ar.data import build_splits
from ar.model import fit, proba, save

tr, te = build_splits()
res = {}
for c in (1.0, 10.0, 100.0):
    f = []
    for seed in (1, 2, 3):
        for a, b in StratifiedKFold(5, shuffle=True, random_state=seed).split(tr.content, tr.threat_label):
            m = fit(tr.content.iloc[a], tr.threat_label.iloc[a], c)
            P, cl = proba(m, tr.content.iloc[b])
            f.append(f1_score(tr.threat_label.iloc[b], [cl[i] for i in P.argmax(1)], average="macro"))
    res[c] = float(np.mean(f)); print(f"C={c:<6} CV macro-F1 (train only) = {res[c]:.3f}")
best = max(res, key=res.get)
m = fit(tr.content, tr.threat_label, best)
save(m, {"C": best, "cv_macro_f1": res, "n_train": len(tr), "train_sha": hashlib.sha256("".join(sorted(tr.group)).encode()).hexdigest()[:12],
         "data": "released(12 unique)+developer-authored supplement(train)", "calibration": "sigmoid, 3-fold"})
print("saved", C.MODEL_FILE, "with C =", best)
