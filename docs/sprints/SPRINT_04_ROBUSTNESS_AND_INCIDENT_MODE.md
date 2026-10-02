# SPRINT 4 — ROBUSTNESS AND INCIDENT MODE

← [Previous](SPRINT_03_ATTACK_REPLAY.md) · [Project Plan](../../PROJECT_PLAN.md) · [Backlog](../13_BACKLOG.md) · [Next](SPRINT_05_FINAL_HARDENING.md) →

| Item | Value |
|---|---|
| **Status** | 🔵 PLANNED |
| **Proposed timebox** | PROPOSED: late "Tuesday" into "Wednesday morning" (proposal: incident mode after trust gap; start Arena mutators Tuesday; finish Arena scoreboard Wednesday morning). Dates TO BE VERIFIED (OD-005). |
| **Lead roles** | ML-API (mutators, robustness, normalization), FE-REPLAY (Arena UI), PLAYBOOK-DEMO (incident content) |
| **Sprint type** | Work package (not a fixed duration) |

## Sprint objective

Add the **proof of robustness** and the incident response path — Incident Mode, Evasion Arena, Unicode hardening, mutation testing, robustness and false-positive evaluation, and held-out mutation tests — **without destabilizing the core experience**.

## Why this sprint exists

The proposal's bet has two halves: an interpreter (done) and proof that it holds up against rewritten attacks (this sprint). Incident Mode shows the product helps after harm. Both are SHOULD-haves; the core is protected by a stability gate.

## Scope

**In scope**

- Incident Mode (four harm situations, first-hour plan, evidence preservation, report drafts)
- Mutators (homoglyph, zero-width, split link, Shona/English mixing, paraphrase, AI-polished)
- Advanced normalization hardening and retraining on development misses (the patch)
- Robustness evaluation incl. false positives and held-out mutation types
- Evasion Arena scoreboard

**Out of scope**

- New core features
- Organisation mode, slider, LLM (Sprint 5 stretch)
- Tarpit, ScamSigma, Herd Immunity (LATER)

## Backlog items

| ID | Item | Priority | Status |
|---|---|---|---|
| [AR-010](../13_BACKLOG.md#ar-010) | Incident Mode | SHOULD | 🔵 PLANNED |
| [AR-023](../13_BACKLOG.md#ar-023) | Mutators | SHOULD | 🔵 PLANNED |
| [AR-025](../13_BACKLOG.md#ar-025) | Advanced normalization hardening | SHOULD | 🔵 PLANNED |
| [AR-024](../13_BACKLOG.md#ar-024) | Robustness evaluation & held-out mutation tests | SHOULD | 🔵 PLANNED |
| [AR-011](../13_BACKLOG.md#ar-011) | Evasion Arena | SHOULD | 🔵 PLANNED |

Full acceptance criteria per item: [13_BACKLOG](../13_BACKLOG.md).


## Tasks

1. **Stability gate first:** freeze a core regression baseline (Sprint 1–3 metrics and demo paths); every change in this sprint must keep it green; use feature flags or isolated modules so Arena/Incident can be switched off (R-015).
2. **AR-010:** Implement harm-already-happened detection and the pointer jump for clicked / replied / submitted credentials / transferred money; first-hour plan, evidence preservation, report drafts; verify or flag local channels.
3. **AR-023:** Implement mutators with seed lineage; assign mutation types to development vs held-out sets (closes OD-009); include benign controls and hard negatives.
4. **AR-025:** Harden normalization (homoglyph folding, zero-width stripping, split-link re-joining); retrain on development misses; confirm offset map still valid.
5. **AR-024:** Run before/after-patch and held-out evaluations; false positives; DNA stability; record misses honestly.
6. **AR-011:** Build the Arena scoreboard UI and runner integration; provide saved-results fallback for the demo.
7. Update the failure-case log, technical summary inputs and demo data (DEMO-INC, DEMO-MUT).

## Dependencies

- Sprint 3 exit: replay, playbooks, trust gap stable
- Sprint 1 evaluation harness and normalization
- Development vs held-out mutation split decided (OD-009)

## Expected outputs

- Incident Mode integrated with the replay pointer
- Mutator suite and robustness evaluation scripts
- Hardened normalization and patched model with logged results
- Arena scoreboard with before/after/held-out and false-positive views, plus saved results
- Updated failure-case log

## Acceptance criteria

- [ ] Each of the four incident situations jumps to the correct stage and shows plan, evidence list and report draft
- [ ] Arena reports caught rate before and after patch, false positives on benign controls, and results on held-out mutation types, including remaining misses
- [ ] No tuning on held-out mutation types (process evidence recorded)
- [ ] DNA stability across rewrites is reported
- [ ] Core regression baseline unchanged or improved; Arena/Incident can be disabled without affecting core
- [ ] Works offline

## Definition of Done

Common DoD (see [PROJECT_PLAN](../../PROJECT_PLAN.md#common-definition-of-done)) plus:

- [ ] Sprint items 🟢 COMPLETE (or ⚪ DEFERRED with reason and cut-order applied)
- [ ] Core regression baseline green
- [ ] Robustness results reproducible by script and recorded in the evaluation report
- [ ] OD-009 closed
- [ ] Incident content flagged/verified per R-020

## Testing requirements

- Mutator determinism and lineage
- Normalization idempotence and offset tests on mutated inputs
- Robustness runs before/after patch and held-out
- False-positive runs on benign and hard-benign sets
- Incident detection: phrase variants and negatives
- Core regression (mandatory on every merge)
- UI walkthrough of J7, J8

## Demo milestone

Milestone: paste DEMO-INC ('I already sent the money') → pointer jumps to cash-out stage with first-hour plan; open the Arena → before/after caught rate with false positives, then held-out results.

## Risks

- R-008 Unicode evasion
- R-007 Model weakness
- R-006 Overfitting to mutations
- R-015 Scope creep (destabilizing core)
- R-020 Incorrect local recovery guidance
- R-021 Toggle false reassurance
- R-017 Time constraints

See [Risk Register](../11_RISK_REGISTER.md).

## Stretch goals

- More mutation types (only held-out ones kept separate)
- Arena UI polish (charts)
- Incident report-draft variants per provider type (generic; no invented contacts)

Stretch goals are attempted only after every acceptance criterion is met and must not destabilize the sprint's deliverables.

## Explicitly deferred work

- Organisation mode, slider, LLM rephrasing (AR-026–028 → Sprint 5 stretch)
- Tarpit, ScamSigma, Herd Immunity (LATER)
- Any new core features

## Exit criteria

- [ ] Definition of Done met
- [ ] Feature freeze decision taken: what is in/out of the demo, following the cut order in the [Demo Strategy](../09_DEMO_STRATEGY.md)
- [ ] Core demo path still reliable
- [ ] Final evaluation numbers available for the technical summary
