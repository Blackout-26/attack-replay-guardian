# 05 — Evaluation Strategy

> How Attack Replay will be judged honestly. **No results exist yet.** All numerical values in this document are placeholders or explicitly labelled *proposed goals*, never actual results.

**Status:** 🔵 PLANNED · Backlog: AR-013, AR-018, AR-019, AR-024

## 1. Evaluation principles

| # | Principle |
|---|---|
| E1 | **No data leakage** — group-aware, deduplicated splits ([Data & ML §4–5](./04_DATA_AND_ML_STRATEGY.md)). |
| E2 | **No tuning on hidden or final evaluation data.** |
| E3 | **Separate development and final evaluation** — final test set is frozen before tuning and touched for reporting only. |
| E4 | **Record failure cases** in a failure log (see §8). |
| E5 | **Do not hide weaknesses** — report false positives, weak classes and held-out mutation misses. |
| E6 | Report **what was measured on what data**, with model/data versions. |
| E7 | Distinguish **actual results** from **proposed goals** in every table. |

## 2. Data partitions

| Set | Used for | Reuse allowed? |
|---|---|---|
| Train | Fit | Yes |
| Validation / CV | Tune, calibrate, set risk thresholds | Yes (development) |
| Final test | Reported metrics | **No** — one-shot reporting |
| Mutation development set | Build/patch mutators & normalization | Yes |
| **Mutation held-out set** | Arena honesty (unseen mutation types) | **No tuning** |
| Hidden hackathon set | Organisers' scoring via `/batch` | Never seen |

## 3. Classification metrics

Applies to (a) suspicious/benign and (b) threat type.

| Metric | Use |
|---|---|
| Accuracy | Context only (misleading under imbalance) |
| Precision, Recall, F1 | Per class and for the suspicious class |
| **Confusion matrix** | Always shown; both counts and row-normalized |
| **Per-class performance** | Required for every threat type |
| **Macro F1** | Primary multi-class summary (treats classes equally) |
| **Weighted F1** | Secondary (reflects class frequencies) |
| **False-positive rate** | Benign flagged as suspicious — primary trust metric; also report on *hard benign* examples |
| Calibration | Reliability check on validation (probabilities feed the risk engine) |

Confidence intervals / variance across CV folds should be reported where sample sizes allow (TO BE DECIDED per dataset size).

## 4. Risk-level evaluation

- If the dataset has risk labels: agreement metrics per band (report confusion between adjacent bands separately from Low↔High errors).
- If not: **no accuracy claim** for risk. Evaluate via rule-consistency tests (e.g., an OTP/PIN ask never scores lower than a plain reply ask at equal likelihood) and a documented review of examples. State plainly that the risk is rule-based.

## 5. Robustness evaluation (Evasion Arena)

| Mutation class | Example of what is changed | Metric |
|---|---|---|
| Paraphrase | Reworded scam, same intent | Caught rate |
| Unicode manipulation | Compatibility forms, mixed scripts | Caught rate |
| Homoglyphs | Look-alike characters | Caught rate |
| Zero-width characters | Hidden characters in words/links | Caught rate |
| Split links | Obfuscated URLs | Caught rate + URL extraction rate |
| AI-polished text | Fluent, professional rewrite | Caught rate |
| Shona/English mixing | Code-mixed variants | Caught rate |
| Benign controls | Benign messages, incl. mutated and hard negatives | **False-positive rate** |

Protocol:
1. Generate mutations from **seed scams** (tracked lineage).
2. Run **before patch** → record caught rate and FPR per class.
3. Apply patch (normalization + retraining on misses from the *development* mutation set).
4. Re-run on **held-out mutation types** not used in patching → this is the honest number.
5. Report **DNA stability**: do the same tactic tags survive rewrites?
6. Publish both before/after and held-out results, including remaining misses.

Mutation-generation method (rules vs LLM-assisted) and the exact held-out split: OPEN ([OD-009](./12_DECISION_LOG.md#open-decisions)). If an LLM is used to create paraphrases, record that and keep it out of the runtime path.

## 6. Non-ML component evaluation

| Component | Check |
|---|---|
| Explanations | **Groundedness audit:** every claim traces to an indicator/entity; no invented facts |
| Threat DNA | Evidence spans point to the intended words in the **original** text; strength rules consistent |
| Replay/playbooks | Review checklist: labelled as typical progression; recoverability statements verified or marked TO BE VERIFIED; no real infrastructure |
| Trust Gap | Toggle behaviour matches documented rules; labelled "guidance" |
| `/batch` | Row count preserved; required columns present; no crashes on malformed rows; works with LLM/internet disabled |
| Offline mode | Full pipeline test with LLM and network disabled |

## 7. What is a successful model?

Defined by **comparison and honesty**, not by an invented number:

- Beats trivial and simple baselines on the final test set (macro F1 and suspicious-class recall/precision).
- False-positive rate on benign/hard-benign data is reported and judged acceptable for a citizen-facing tool (threshold: OPEN — [OD-017](./12_DECISION_LOG.md#open-decisions)).
- Per-class weaknesses are identified, not averaged away.
- Robustness shows measurable improvement on **held-out** mutation types after the patch, or the shortfall is reported.
- Numerical **proposed goals** are set only after the baseline exists, recorded in the Decision Log, and labelled *proposed*.

| Metric | Proposed goal | Actual result |
|---|---|---|
| Suspicious-class F1 | TBD after baseline | — |
| Macro F1 (threat type) | TBD after baseline | — |
| False-positive rate | TBD after baseline | — |
| Held-out mutation caught rate | TBD after baseline | — |

## 8. Failure-case log format

| ID | Input (or ID) | Expected | Got | Category (FP/FN/type confusion/extraction/highlight/replay) | Root-cause hypothesis | Action | Status |
|---|---|---|---|---|---|---|---|

Maintained in the repository by the ML/API owner; summarized in the technical summary.

## 9. Regression suite

A small fixed set of demo and edge-case messages (see [Demo Strategy](./09_DEMO_STRATEGY.md)) runs on every change: verdict stability, DNA tags, entity extraction, replay pointer, offline behaviour. Test requirements per sprint are in each sprint doc.

## 10. Reporting

Final evaluation report (input to the technical summary, AR-033): dataset description, splits, methods, metrics tables, confusion matrices, Arena before/after/held-out, false positives, known weaknesses, limitations.
