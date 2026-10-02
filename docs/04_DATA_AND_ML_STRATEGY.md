# 04 — Data and ML Strategy

> **The released hackathon dataset must be inspected before the taxonomy, features or thresholds are finalized.** This document does not assume the dataset's labels, size, languages, balance or fields, and contains **no dataset statistics**. Anything numeric is TO BE MEASURED.

**Status:** 🔵 PLANNED · Backlog: AR-001, AR-002, AR-003, AR-004, AR-013, AR-014, AR-015, AR-019, AR-029

## 1. Guiding decisions

| Decision | Ref |
|---|---|
| Char n-gram TF-IDF + calibrated logistic regression is the **initial baseline**; embeddings are an **optional enhancement** | [DEC-004](./12_DECISION_LOG.md#dec-004) |
| LLM never decides the verdict | [DEC-002](./12_DECISION_LOG.md#dec-002) |
| Zimbabwe context = patterns, not brand blacklists | [DEC-005](./12_DECISION_LOG.md#dec-005) |
| Fit risk weights/thresholds to dataset risk labels **only if they exist** | [DEC-008](./12_DECISION_LOG.md#dec-008) |
| Library/framework choice | OPEN ([OD-001](./12_DECISION_LOG.md#open-decisions)) |

## 2. Dataset discovery process (AR-001)

Run in Sprint 0, before any modelling. Record findings in the Sprint 0 output note (dataset data card).

| Step | Check | Output |
|---|---|---|
| 1 | Locate dataset, format, licence, provenance, permitted use | Data card (TO BE VERIFIED items closed) |
| 2 | Schema: columns present (text, label(s), risk?, sender?, channel?, language?, id?) | Field inventory |
| 3 | **Label inspection:** unique values, spelling variants, hierarchy (binary vs type vs risk) | Label map |
| 4 | **Class distribution** overall and per label field | Table (measured, not assumed) |
| 5 | **Missing values** per column; empty/whitespace-only messages | Cleaning rules |
| 6 | **Duplicates & near-duplicates** (exact, normalized, fuzzy) incl. across labels | Dedup policy; conflicting-label list |
| 7 | **Language analysis:** English, Shona, mixed, other; scripts; code-mixing share | Language profile |
| 8 | Length, channel, formatting artifacts (URLs, emojis, casing, punctuation) | Feature notes |
| 9 | **Leakage scan** (see §4) | Leakage report |
| 10 | Fitness for the proposal: does it support sender/channel, risk, threat types, benign hard-negatives? | Gap list → adapt playbooks/taxonomy |

**Exit of discovery:** freeze labels and record the taxonomy decision (AR-003) in the [Decision Log](./12_DECISION_LOG.md). If the dataset labels differ from the proposal's five threat types, the **dataset labels win for classification** and playbook mapping adapts (proposal risk: "dataset mismatch — build the baseline first and adapt the playbooks").

## 3. Data validation (AR-013)

- Schema validation at load; fail loudly on unexpected labels.
- Deterministic cleaning pipeline with logged counts (rows dropped, why).
- Reproducibility: fixed seeds, recorded data hash/version.

## 4. Leakage detection

| Leakage type | Detection | Mitigation |
|---|---|---|
| Duplicates / near-duplicates across splits | Normalized-text hashing, fuzzy clustering | Split by **cluster/group**, not by row |
| Template-generated families spread across splits | Cluster inspection | Group-aware split |
| Label-correlated artifacts (unique domains, sender IDs, formatting, length) | Feature-importance and ablation review | Remove/mask or document |
| Test/hidden data used for tuning | Process control | Never tune on hidden/final evaluation data |
| Arena mutations of the same seed in train and test | Track seed lineage | Hold out mutation *types* and seed groups |

## 5. Train / validation / test strategy

| Partition | Purpose | Rule |
|---|---|---|
| **Train** | Fit models | Group-aware, deduplicated |
| **Validation** (or CV folds) | Tune features, hyperparameters, thresholds, calibration | May be reused during development |
| **Test (final)** | One-time honest numbers | Touched only for reporting; frozen before tuning |
| **Hidden hackathon set** | Organisers' evaluation | Never seen; `/batch` only |
| **Mutation held-out** | Arena honesty | Mutation types not used in patching |

Stratification and split ratios: **OPEN** — decided after class distribution is known (small classes may need CV). Details in [05_EVALUATION_STRATEGY](./05_EVALUATION_STRATEGY.md).

## 6. Baseline model (AR-002)

| Element | Plan |
|---|---|
| Features | **Character n-grams** (robust to obfuscation and code-mixing) and word features, TF-IDF weighted |
| Model | **Logistic regression**, class-weight handling per imbalance findings |
| Calibration | Fit on held-out data; check reliability; choice of method depends on data size (AR-019) |
| Outputs | Suspicious/benign probability; threat type (multi-class or hierarchical, per label structure) |
| Comparison | Report against trivial baselines (majority class) and any simple rule baseline |

n-gram ranges, vocabulary limits, regularization: **TO BE TUNED** on validation only.

## 7. Optional enhancements

| Enhancement | Status | Notes |
|---|---|---|
| Multilingual sentence embeddings (classifier or similarity) | COULD (AR-029) | Only if baseline weaknesses (paraphrase, Shona mixing) justify it; adds dependency/model-download risk (R-013). Must run offline. |
| Embedding similarity in tactic detectors | COULD | So wording changes don't break indicators. |
| LLM rephrasing | COULD (AR-028) | Rephrase only; never verdict. |

## 8. Threat classification and taxonomy (AR-003)

1. Inspect labels (§2). 2. Map dataset labels to product threat types. 3. Record any merges/splits and unmapped classes. 4. Map each final type to at least one playbook (or a generic fallback playbook). 5. Freeze.

The proposal lists **phishing, financial scam, identity fraud, malicious link/content, AI-enabled threat** as the brief's categories (TO BE VERIFIED). If the dataset lacks threat types, fallback options (rule/weak-label typing) are an OPEN DECISION ([OD-002](./12_DECISION_LOG.md#open-decisions)) and must be reported as such.

## 9. Risk modelling (AR-004)

```
risk = likelihood × irreversibility of the ask
```

| Term | Source |
|---|---|
| Likelihood | Calibrated probability of malicious/suspicious |
| Irreversibility | Ordinal weight by extracted **ask**: sharing OTP/PIN, sending money, installing an app = highest; clicking = medium; replying = lower (KNOWN ordering, from proposal) |
| Bands | Low / Medium / High; **thresholds TO BE FIT** to dataset risk labels if present, otherwise documented, rule-based and labelled as such |

Explanation must name both factors. Weights are transparent, versioned config — not hidden model behaviour.

## 10. Normalization and Unicode handling (AR-014, AR-025)

| Concern | Approach (PROPOSED) |
|---|---|
| Unicode forms | Normalize (e.g., NFKC) |
| Zero-width / invisible characters | Strip; record that it occurred (itself an evasion signal) |
| Homoglyphs / confusables | Fold to canonical script characters; flag mixed-script tokens |
| Split links | Re-join obfuscated URLs ("example . com", spaces/zero-width in domains, "hxxp", bracketed dots) |
| Case, whitespace, punctuation | Canonicalize; do not lose evidence spans |
| **Offset map** | Keep mapping normalized→original so highlights land on the user's raw text |
| Idempotence | Normalizing twice = normalizing once (test) |

Basic normalization ships in Sprint 1 (AR-014); hardened handling and the Arena patch are Sprint 4 (AR-025).

## 11. Multilingual considerations

- Expect English, Shona, and mixed Shona/English (**share TO BE MEASURED**); other languages possible.
- Character n-grams reduce dependence on tokenization and spelling variation.
- Lexicons (tactics, asks) must be reviewed by a Shona-speaking team member or reviewer — **OPEN** ([R-005](./11_RISK_REGISTER.md)); do not machine-translate lexicons and assume correctness.
- Evaluate per language slice where labels allow (see Eval doc).

## 12. Extraction (AR-015)

| Entity | Notes |
|---|---|
| **URLs** | Detect incl. obfuscated forms; extract domain/shape indicators; **never resolve or fetch** |
| **Phone numbers** | Local and international formats (Zimbabwe formats TO BE VERIFIED); used as indicators, not looked up |
| **Amounts** | Currency and amount cues (formats/currencies TO BE VERIFIED) |
| **Organisation / sector cues** | Context lexicon (mobile money, bank, utility, government, university, employer, courier, investment, SIM/account) — **not** brand lists |
| **User request / "ask"** | PIN, OTP, password/login, money/reversal, app install, call-back, click, reply |
| Method | Rules first; light NER only if it clearly helps and stays offline |

## 13. Tactic indicators (feeds AR-005)

Lexicon + (optional) embedding similarity per tactic (urgency, authority, fear/loss, reward/lure, secrecy, credential request, payment request, call to action, suspicious link). **Additional tactics are discovered from the dataset** (AR-001), not assumed. Each detector must return evidence spans and a strength level (strong/present/absent) using documented rules.

## 14. Artifact and reproducibility requirements

- Training script/notebook reproducible from a clean checkout with fixed seeds.
- Saved model + metadata (data version, config, metrics).
- No secrets or raw private data committed.
- Dataset licence/attribution recorded ([Submission Plan](./10_SUBMISSION_PLAN.md)).

## 15. Related

[Evaluation](./05_EVALUATION_STRATEGY.md) · [Architecture](./03_PRODUCT_ARCHITECTURE.md) · [Risk Register](./11_RISK_REGISTER.md)
