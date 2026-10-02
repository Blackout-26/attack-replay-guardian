# SPRINT 1 — DETECTION FOUNDATION

← [Previous](SPRINT_00_DISCOVERY.md) · [Project Plan](../../PROJECT_PLAN.md) · [Backlog](../13_BACKLOG.md) · [Next](SPRINT_02_THREAT_DNA.md) →

| Item | Value |
|---|---|
| **Status** | 🔵 PLANNED |
| **Proposed timebox** | PROPOSED: remainder of "Today" — "ship the baseline (extraction, classifier, risk, template explanations) with /analyze and /batch". Dates TO BE VERIFIED (OD-005). |
| **Lead roles** | ML-API (lead) |
| **Sprint type** | Work package (not a fixed duration) |

## Sprint objective

Produce a **working analytical backend**: data loading and validation, leakage-free splits, normalization, extraction, baseline classifier, threat classification, risk engine, template explanations, `/analyze` and `/batch`, with tests and honest baseline metrics.

## Why this sprint exists

Everything else (Threat DNA, replay, trust gap, Arena) consumes the verdict, entities and risk. `/batch` is required for the hidden evaluation, so a submission-safe core must exist early. This sprint also produces the first honest numbers and the regression suite that protects later sprints.

## Scope

**In scope**

- Data loading, validation, cleaning, group-aware splitting
- Baseline normalization with offset map
- Basic entity and ask extraction
- Char n-gram + word TF-IDF + logistic regression baseline; calibration
- Threat classification on the frozen taxonomy
- Risk engine (likelihood × irreversibility)
- Template explanations and recommended action
- `/analyze` and `/batch` endpoints
- Security baseline; tests; evaluation harness

**Out of scope**

- Frontend UI (Sprint 2)
- Threat DNA tactic detectors (Sprint 2)
- Replay/playbooks (Sprint 3)
- Incident Mode / Arena (Sprint 4)
- Any LLM usage

## Backlog items

| ID | Item | Priority | Status |
|---|---|---|---|
| [AR-013](../13_BACKLOG.md#ar-013) | Data loading, validation & splitting | MUST | 🔵 PLANNED |
| [AR-014](../13_BACKLOG.md#ar-014) | Baseline text normalization | MUST | 🔵 PLANNED |
| [AR-015](../13_BACKLOG.md#ar-015) | Entity & ask extraction | MUST | 🔵 PLANNED |
| [AR-002](../13_BACKLOG.md#ar-002) | Baseline classifier | MUST | 🔵 PLANNED |
| [AR-019](../13_BACKLOG.md#ar-019) | Probability calibration | SHOULD | 🔵 PLANNED |
| [AR-004](../13_BACKLOG.md#ar-004) | Risk engine | MUST | 🔵 PLANNED |
| [AR-006](../13_BACKLOG.md#ar-006) | Explanation engine | MUST | 🔵 PLANNED |
| [AR-016](../13_BACKLOG.md#ar-016) | /analyze endpoint | MUST | 🔵 PLANNED |
| [AR-017](../13_BACKLOG.md#ar-017) | /batch endpoint | MUST | 🔵 PLANNED |
| [AR-018](../13_BACKLOG.md#ar-018) | Test suite & evaluation harness | MUST | 🔵 PLANNED |
| [AR-030](../13_BACKLOG.md#ar-030) | Security baseline | MUST | 🔵 PLANNED |

Full acceptance criteria per item: [13_BACKLOG](../13_BACKLOG.md).


## Tasks

1. **AR-013:** Implement the deterministic loader, schema/label validation, cleaning and group-aware train/validation/test splits; freeze the final test set.
2. **AR-014:** Implement baseline normalization (Unicode, whitespace/case, zero-width stripping) with offset map; test idempotence and offset correctness.
3. **AR-015:** Implement rule-based extraction of URLs, phones, amounts, sector cues and the user ask; never resolve URLs.
4. **AR-002 + AR-019:** Train the char n-gram/word TF-IDF + logistic regression baseline for suspicious/benign and threat type; tune on validation only; calibrate; save artifact with metadata.
5. **AR-004:** Implement the risk engine with transparent irreversibility weights and Low/Medium/High bands; fit to risk labels if they exist.
6. **AR-006:** Implement template explanations (reason naming both factors) and recommended-action templates for every taxonomy class.
7. **AR-016 + AR-017:** Implement `/analyze` and `/batch` (CSV in → CSV out: label, type, risk, explanation, action).
8. **AR-030:** Apply security baseline (validation, no outbound fetch, no body logging, CSV-injection protection).
9. **AR-018:** Write unit/integration tests, the evaluation script (metrics tables, confusion matrices, failure-case log) and the regression set of demo messages.
10. Record the split strategy, calibration method, thresholds and API schema in the [Decision Log](../12_DECISION_LOG.md); draft results for the technical summary.

## Dependencies

- Sprint 0 exit: frozen taxonomy (AR-003), stack decision (AR-041), data card (AR-001), verified batch schema (OD-010)
- Dataset access
- Flyer facts closed (AR-012)

## Expected outputs

- Working backend runnable locally from a clean checkout
- Trained, calibrated baseline model artifact with metadata
- `/analyze` and `/batch` implemented
- Test suite and evaluation harness
- Baseline evaluation report (measured metrics, confusion matrices, per-class, false-positive rate, failure-case log)
- Regression set incl. demo messages (DEMO-01/02/03, benign, hard-benign)
- Decision Log updated

## Acceptance criteria

- [ ] `/analyze` returns label, threat type, risk band, one-line reason and recommended action for valid input (the five minimum features)
- [ ] `/batch` round-trips a CSV, preserves row count, emits the required columns, survives malformed rows
- [ ] Reason names both likelihood and irreversibility
- [ ] Same input → same output (deterministic)
- [ ] Full pipeline works with no LLM and no internet
- [ ] Reported metrics reproduce from the evaluation script; no tuning on the final test set
- [ ] No code path fetches or executes URLs from input

## Definition of Done

Common DoD (see [PROJECT_PLAN](../../PROJECT_PLAN.md#common-definition-of-done)) plus:

- [ ] Backlog items in this sprint 🟢 COMPLETE or explicitly 🔴/⚪ with reason
- [ ] All tests pass; regression set green
- [ ] README covers setup, run, test, evaluate
- [ ] Baseline results recorded honestly (incl. weaknesses) with data/model versions
- [ ] Decisions logged; docs (Architecture, Data & ML) updated for deviations
- [ ] Security baseline checklist items for S1–S8 evidenced

## Testing requirements

- Unit: normalization (idempotence, offsets), extraction (URLs incl. obfuscated, phones, amounts, asks), risk rules, template coverage
- Rule-consistency: OTP/PIN/payment ask ≥ click ≥ reply at equal likelihood
- API: valid/invalid/oversized/empty/non-Latin/hostile inputs
- Batch: malformed rows, large file, formula-injection cells
- Offline: run with network disabled
- Regression: demo messages stable across runs
- Evaluation: reproduce baseline metrics from a clean checkout

## Demo milestone

Milestone (backend, no UI): from a terminal or notebook, submit DEMO-01, DEMO-BEN, DEMO-BEN-HARD and show verdict/type/risk/reason/action; run a small CSV through `/batch`; show baseline metrics and confusion matrix.

## Risks

- R-001 Dataset mismatch
- R-002 Insufficient data quality
- R-003 Class imbalance
- R-004 Data leakage
- R-006 Overfitting
- R-007 Model weakness
- R-011 API failure
- R-013 Dependency problems
- R-017 Time constraints

See [Risk Register](../11_RISK_REGISTER.md).

## Stretch goals

- Compare against an embeddings variant (only if baseline weaknesses justify; else skip) [AR-029 preview]
- Early Threat DNA lexicon prototypes to de-risk Sprint 2
- Early playbook content drafting (Markdown)

Stretch goals are attempted only after every acceptance criterion is met and must not destabilize the sprint's deliverables.

## Explicitly deferred work

- Frontend UI (AR-020, Sprint 2)
- Tactic detectors and highlighting (AR-005, AR-021)
- Replay/playbooks/trust gap (Sprint 3)
- Incident Mode, Arena, advanced normalization (Sprint 4)
- Slider, Organisation mode, LLM (Sprint 5 stretch)

## Exit criteria

- [ ] Definition of Done met
- [ ] Baseline metrics recorded and reviewed by someone other than the author
- [ ] `/analyze` schema frozen enough for the frontend to start (changes go through the Decision Log)
- [ ] Sprint 2 dependencies satisfied: entities available, offset map working
