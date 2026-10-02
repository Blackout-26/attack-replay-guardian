# Baseline evaluation — model `0.1.0-sprint1` (C = 10.0)

**Read this first.** The released dataset has 100 rows but only **12 unique messages** (2 per class). All 12 are in TRAIN. Every held-out number below therefore comes from a **developer-authored supplement** (written by the team, labelled `developer-authored`). It measures generalisation to *our own* paraphrases; it is **not** an estimate of accuracy on the organisers' hidden set. Numbers are *measured*, goals are not yet set (Eval §7).


## 1. Validation — stratified 5-fold CV on TRAIN (seed 1), out-of-fold predictions

### Model, out-of-fold on TRAIN

- n = 72 · accuracy = 0.931 · **macro-F1 (type) = 0.920** · weighted-F1 = 0.929
- Suspicious class: precision 1.000 · recall 0.980 · F1 0.990 · **false-positive rate on Benign = 0.000** (0/22)

| Class | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| Phishing | 1.00 | 0.80 | 0.89 | 10 |
| Financial Scam | 0.89 | 0.80 | 0.84 | 10 |
| Identity Fraud | 0.83 | 1.00 | 0.91 | 10 |
| Malicious Link | 1.00 | 1.00 | 1.00 | 10 |
| AI-Enabled Threat | 0.90 | 0.90 | 0.90 | 10 |
| Benign | 0.96 | 1.00 | 0.98 | 22 |

Confusion matrix (rows = true, cols = predicted; order: Phishing, Financial Scam, Identity Fraud, Malicious Link, AI-Enabled Threat, Benign)

```
  8   0   1   0   0   1
  0   8   1   0   1   0
  0   0  10   0   0   0
  0   0   0  10   0   0
  0   1   0   0   9   0
  0   0   0   0   0  22
```

### Keyword-rule baseline on TRAIN (binary only; type collapsed to 'Phishing' so ignore type metrics)
- Suspicious F1 0.804 · FPR 0.227. Majority-class baselines: always-'Suspicious' → FPR 1.000; always-one-type → accuracy 0.167.

## 2. Resubstitution on the released dataset (IN-SAMPLE — not generalisation)
- Threat type agrees on 100.0% of 100 rows; risk band agrees on 100.0% (12 unique messages, all seen in training). Risk weights are rule-based and were **not** fit to these labels; with 12 unique points no risk-accuracy claim is made.

## 3. Leakage scan (final test vs train, char-5-gram Jaccard)

- Exact/normalized duplicates across partitions: **0** (enforced in code).
- Max similarity of any test message to any train message: **0.29**; median 0.15. Most similar: “We are updating our records. Reply with your full name, ID number and …”
- Test messages were written in a separate pass with different wording, but by the same authors as the train supplement, so stylistic overlap is possible.

## 4. FINAL TEST (frozen, scored once) — n=30, developer-authored

### Model on frozen final test

- n = 30 · accuracy = 0.967 · **macro-F1 (type) = 0.966** · weighted-F1 = 0.966
- Suspicious class: precision 1.000 · recall 1.000 · F1 1.000 · **false-positive rate on Benign = 0.000** (0/5)

| Class | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| Phishing | 1.00 | 1.00 | 1.00 | 5 |
| Financial Scam | 0.83 | 1.00 | 0.91 | 5 |
| Identity Fraud | 1.00 | 0.80 | 0.89 | 5 |
| Malicious Link | 1.00 | 1.00 | 1.00 | 5 |
| AI-Enabled Threat | 1.00 | 1.00 | 1.00 | 5 |
| Benign | 1.00 | 1.00 | 1.00 | 5 |

Confusion matrix (rows = true, cols = predicted; order: Phishing, Financial Scam, Identity Fraud, Malicious Link, AI-Enabled Threat, Benign)

```
  5   0   0   0   0   0
  0   5   0   0   0   0
  0   1   4   0   0   0
  0   0   0   5   0   0
  0   0   0   0   5   0
  0   0   0   0   0   5
```

Keyword-rule baseline on same set (binary): FPR 0.400, suspicious recall 0.560