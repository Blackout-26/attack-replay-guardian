"""AR-018 evaluation harness. Reproduces every reported number.
   python scripts/evaluate.py            -> validation (CV on train) + baselines + in-sample checks + leakage scan
   python scripts/evaluate.py --final    -> ALSO scores the frozen final test ONCE (refuses to rerun without --force)."""
import sys, json, csv, re, argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, f1_score, precision_recall_fscore_support
from sklearn.model_selection import StratifiedKFold
from ar import config as C
from ar.data import build_splits, load_released
from ar.model import fit, proba, load
from ar.normalize import normalize
from ar.pipeline import analyze, reload

ap = argparse.ArgumentParser(); ap.add_argument("--final", action="store_true"); ap.add_argument("--force", action="store_true")
args = ap.parse_args()
C.REPORTS.mkdir(exist_ok=True)
tr, te = build_splits()
T = C.TYPES
art = load(); Cbest = art["meta"]["C"]
fails, md = [], []


def pred(model, texts):
    P, cl = proba(model, texts); out = []
    for row in P:
        ps = 1 - row[cl.index("Benign")]
        out.append(max((c for c in cl if c != "Benign"), key=lambda c: row[cl.index(c)]) if ps >= .5 else "Benign")
    return out


def metrics(y, p, title, src_texts=None, cat=""):
    ys = ["Suspicious" if v != "Benign" else "Benign" for v in y]; ps = ["Suspicious" if v != "Benign" else "Benign" for v in p]
    P, R, F, _ = precision_recall_fscore_support(ys, ps, labels=["Suspicious"], zero_division=0)
    ben = [i for i, v in enumerate(y) if v == "Benign"]
    fpr = sum(p[i] != "Benign" for i in ben) / len(ben)
    rep = classification_report(y, p, labels=T, output_dict=True, zero_division=0)
    cm = confusion_matrix(y, p, labels=T)
    md.append(f"\n### {title}\n\n- n = {len(y)} · accuracy = {np.mean(np.array(y) == np.array(p)):.3f} · **macro-F1 (type) = {f1_score(y, p, labels=T, average='macro', zero_division=0):.3f}** · weighted-F1 = {f1_score(y, p, labels=T, average='weighted', zero_division=0):.3f}")
    md.append(f"- Suspicious class: precision {P[0]:.3f} · recall {R[0]:.3f} · F1 {F[0]:.3f} · **false-positive rate on Benign = {fpr:.3f}** ({sum(p[i] != 'Benign' for i in ben)}/{len(ben)})")
    md.append("\n| Class | Precision | Recall | F1 | Support |\n|---|---|---|---|---|")
    md.extend([f"| {t} | {rep[t]['precision']:.2f} | {rep[t]['recall']:.2f} | {rep[t]['f1-score']:.2f} | {int(rep[t]['support'])} |" for t in T])
    md.append("\nConfusion matrix (rows = true, cols = predicted; order: " + ", ".join(T) + ")\n\n```\n" + "\n".join(" ".join(f"{v:3d}" for v in r) for r in cm) + "\n```")
    if src_texts is not None:
        for t, a, b in zip(src_texts, y, p):
            if a != b:
                fails.append([f"{cat}-{len(fails)+1:03d}", t, a, b, "FP" if a == "Benign" else "FN" if b == "Benign" else "type confusion", "TO REVIEW", "", "OPEN"])
    return dict(macro_f1=f1_score(y, p, labels=T, average="macro", zero_division=0), susp_f1=float(F[0]), fpr=fpr)


md.append(f"# Baseline evaluation — model `{C.VERSION}` (C = {Cbest})\n\n"
          "**Read this first.** The released dataset has 100 rows but only **12 unique messages** (2 per class). All 12 are in TRAIN. "
          "Every held-out number below therefore comes from a **developer-authored supplement** (written by the team, labelled `developer-authored`). "
          "It measures generalisation to *our own* paraphrases; it is **not** an estimate of accuracy on the organisers' hidden set. Numbers are *measured*, goals are not yet set (Eval §7).\n")

# 1. trivial + rule baselines on the final-test texts (no model tuning involved)
KW = re.compile(r"click|link|\bpin\b|otp|password|verify|urgent|send|transfer|won|prize|attached|download|install|suspended|reverse|reply", re.I)
rule = lambda ts: ["Phishing" if KW.search(t) else "Benign" for t in ts]
md.append("\n## 1. Validation — stratified 5-fold CV on TRAIN (seed 1), out-of-fold predictions")
oof = [None] * len(tr)
for a, b in StratifiedKFold(5, shuffle=True, random_state=1).split(tr.content, tr.threat_label):
    m = fit(tr.content.iloc[a], tr.threat_label.iloc[a], Cbest)
    for i, p in zip(b, pred(m, tr.content.iloc[b])): oof[i] = p
val = metrics(list(tr.threat_label), oof, "Model, out-of-fold on TRAIN", list(tr.content), "VAL")
rb = rule(list(tr.content))
md.append("\n### Keyword-rule baseline on TRAIN (binary only; type collapsed to 'Phishing' so ignore type metrics)")
ys = ["Suspicious" if v != "Benign" else "Benign" for v in tr.threat_label]; ps = ["Suspicious" if v != "Benign" else "Benign" for v in rb]
P, R, F, _ = precision_recall_fscore_support(ys, ps, labels=["Suspicious"], zero_division=0)
ben = [i for i, v in enumerate(ys) if v == "Benign"]
md.append(f"- Suspicious F1 {F[0]:.3f} · FPR {sum(ps[i] != 'Benign' for i in ben)/len(ben):.3f}. Majority-class baselines: always-'Suspicious' → FPR 1.000; always-one-type → accuracy {1/6:.3f}.")

# 2. in-sample checks on released data
md.append("\n## 2. Resubstitution on the released dataset (IN-SAMPLE — not generalisation)")
allr, uniq = load_released()
a = [analyze(t) for t in allr.content]
ty = np.mean([x["threat_type"] == y for x, y in zip(a, allr.threat_label)]); rk = np.mean([x["risk"]["band"] == y for x, y in zip(a, allr.risk_level)])
md.append(f"- Threat type agrees on {ty:.1%} of 100 rows; risk band agrees on {rk:.1%} (12 unique messages, all seen in training). Risk weights are rule-based and were **not** fit to these labels; with 12 unique points no risk-accuracy claim is made.")

# 3. leakage scan
def g5(s): s = normalize(s).text; return {s[i:i+5] for i in range(max(1, len(s) - 4))}
G = [g5(t) for t in tr.content]
sims = sorted(((max(len(g5(t) & x) / len(g5(t) | x) for x in G), t) for t in te.content), reverse=True)
md.append("\n## 3. Leakage scan (final test vs train, char-5-gram Jaccard)\n\n- Exact/normalized duplicates across partitions: **0** (enforced in code).\n"
          f"- Max similarity of any test message to any train message: **{sims[0][0]:.2f}**; median {np.median([s for s, _ in sims]):.2f}. Most similar: “{sims[0][1][:70]}…”\n"
          "- Test messages were written in a separate pass with different wording, but by the same authors as the train supplement, so stylistic overlap is possible.")

res = {"validation": val}
# 4. final test — once
done = C.REPORTS / "final_test_result.json"
if args.final:
    if done.exists() and not args.force:
        sys.exit("Final test already scored once. Refusing to re-run (E3). Use --force only to reproduce, never to tune.")
    md.append("\n## 4. FINAL TEST (frozen, scored once) — n=30, developer-authored")
    m = art["model"]
    fin = metrics(list(te.threat_label), pred(m, te.content), "Model on frozen final test", list(te.content), "TEST")
    rr = rule(list(te.content)); md.append(f"\nKeyword-rule baseline on same set (binary): FPR {np.mean([r != 'Benign' for r, y in zip(rr, te.threat_label) if y == 'Benign']):.3f}, suspicious recall {np.mean([r != 'Benign' for r, y in zip(rr, te.threat_label) if y != 'Benign']):.3f}")
    res["final_test"] = fin; done.write_text(json.dumps(res, indent=1))
else:
    md.append("\n## 4. FINAL TEST — not scored in this run (`--final` to score once)")
(C.REPORTS / "BASELINE_EVALUATION.md").write_text("\n".join(md))
with open(C.REPORTS / "failure_log.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["ID", "Input", "Expected", "Got", "Category", "Root-cause hypothesis", "Action", "Status"]); w.writerows(fails)
print("\n".join(md))
