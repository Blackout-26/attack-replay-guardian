# SPRINT 2 — THREAT DNA

← [Previous](SPRINT_01_DETECTION_FOUNDATION.md) · [Project Plan](../../PROJECT_PLAN.md) · [Backlog](../13_BACKLOG.md) · [Next](SPRINT_03_ATTACK_REPLAY.md) →

| Item | Value |
|---|---|
| **Status** | 🔵 PLANNED |
| **Proposed timebox** | PROPOSED: start of "Tuesday" (proposal: playbooks, replay UI, then trust gap and incident mode; DNA precedes them). Dates TO BE VERIFIED (OD-005). |
| **Lead roles** | ML-API (detectors, grounding), FE-REPLAY (frontend), PLAYBOOK-DEMO (playbook content in parallel) |
| **Sprint type** | Work package (not a fixed duration) |

## Sprint objective

Make the verdict **explainable and visible**: tactic detection with evidence spans, entity enrichment, evidence-grounded explanation and recommended action, and the first frontend (input → verdict → Threat DNA) integrated with the API.

## Why this sprint exists

Threat DNA is what turns 'High risk' into understanding, is the basis of the grounded explanation, and supplies the entities that the replay (Sprint 3) is built from. The frontend shell also starts here so integration risk is found early.

## Scope

**In scope**

- Tactic detectors with strong/present/absent and evidence spans
- Dataset-discovered tactics
- Entity enrichment (sector, ask, channel/link)
- Grounded explanation and recommended action
- Frontend shell: input, verdict card
- Threat DNA UI with highlighting

**Out of scope**

- Replay engine/UI and playbooks (Sprint 3)
- Trust Gap (Sprint 3)
- Incident Mode / Arena (Sprint 4)
- LLM rephrasing

## Backlog items

| ID | Item | Priority | Status |
|---|---|---|---|
| [AR-005](../13_BACKLOG.md#ar-005) | Threat DNA detection | MUST | 🔵 PLANNED |
| [AR-015](../13_BACKLOG.md#ar-015) | Entity & ask extraction | MUST | 🔵 PLANNED |
| [AR-006](../13_BACKLOG.md#ar-006) | Explanation engine | MUST | 🔵 PLANNED |
| [AR-020](../13_BACKLOG.md#ar-020) | Frontend shell | MUST | 🔵 PLANNED |
| [AR-021](../13_BACKLOG.md#ar-021) | Threat DNA UI & evidence highlighting | MUST | 🔵 PLANNED |

Full acceptance criteria per item: [13_BACKLOG](../13_BACKLOG.md).

**Stretch items** (attempted only after every acceptance criterion is met):

| ID | Item | Priority | Status |
|---|---|---|---|
| [AR-029](../13_BACKLOG.md#ar-029) | Embedding enhancements | COULD | 🔵 PLANNED |


## Tasks

1. **AR-005:** Implement detectors for urgency, authority impersonation, fear/loss, reward/lure, secrecy, credential request, payment request, call to action, suspicious links; add dataset-discovered tactics (or log deferral); document strength rules.
2. **AR-015 (enrich):** Improve sector/ask/amount/link extraction using error analysis from Sprint 1; ensure entities are sufficient to populate replay stages later.
3. **AR-006 (ground):** Key explanations and recommended action on DNA evidence; run the groundedness audit.
4. **AR-020:** Build the frontend shell (input incl. optional sender/channel and 'Was I expecting this?', verdict card) wired to `/analyze`; design loading/error/offline states.
5. **AR-021:** Build the Threat DNA panel: highlighted text on the original message (escaped), tags with strength, entity panel, defanged URLs.
6. Extend `/analyze` response with `dna[]` and `entities` (schema change logged).
7. Parallel (no code): playbook content drafting for Sprint 3 [AR-008].

## Dependencies

- Sprint 1 exit: `/analyze`, normalization offset map, extraction, tests
- Frozen taxonomy
- Stack decision (frontend)

## Expected outputs

- Threat DNA detectors with tests
- Extended `/analyze` schema
- Frontend: input → verdict → Threat DNA working end to end
- Groundedness audit results
- Updated regression set including DNA expectations

## Acceptance criteria

- [ ] Every emitted tag has at least one evidence span; no percentages shown
- [ ] Highlights align with the original (un-normalized) text, including on inputs with zero-width characters
- [ ] Explanations reference evidence; audit finds no ungrounded claim
- [ ] A user can paste DEMO-01 and see verdict card + highlighted Threat DNA + entities
- [ ] Works offline; all Sprint 1 acceptance criteria still pass

## Definition of Done

Common DoD (see [PROJECT_PLAN](../../PROJECT_PLAN.md#common-definition-of-done)) plus:

- [ ] Sprint items 🟢 COMPLETE (stretch item AR-029 may be ⚪ DEFERRED with reason)
- [ ] Regression suite (Sprint 1 + DNA) green
- [ ] API schema changes logged and docs updated
- [ ] UI escapes all input; no raw HTML rendering
- [ ] Failure cases recorded

## Testing requirements

- Detector unit tests: positive/negative/hard-benign per tactic
- Offset tests: highlights on mutated inputs map to original
- Groundedness audit: sample of explanations
- UI: manual walkthrough of J1/J2 in [UX doc](../06_UX_AND_USER_JOURNEYS.md); XSS-style inputs
- Regression: Sprint 1 metrics not degraded without a logged reason

## Demo milestone

Milestone: paste DEMO-01 in the UI → verdict card → Threat DNA highlights and entities; paste DEMO-BEN and DEMO-BEN-HARD to show restraint.

## Risks

- R-005 Multilingual handling
- R-007 Model weakness
- R-012 Hallucinated explanations
- R-015 Scope creep
- R-019 Security problems (rendering)
- R-013 Dependency problems (embeddings)

See [Risk Register](../11_RISK_REGISTER.md).

## Stretch goals

- AR-029 embedding-similarity for tactics if lexicons prove brittle (must be offline)
- Basic phone-sized layout pass
- Playbook drafting continuing in parallel

Stretch goals are attempted only after every acceptance criterion is met and must not destabilize the sprint's deliverables.

## Explicitly deferred work

- Replay and playbooks (Sprint 3)
- Trust Gap (Sprint 3)
- Incident Mode, Arena (Sprint 4)
- Slider, Organisation mode, LLM (Sprint 5 stretch)

## Exit criteria

- [ ] Definition of Done met
- [ ] End-to-end path from input to Threat DNA demonstrable
- [ ] Entities sufficient for replay instantiation (checked against draft playbooks)
- [ ] Sprint 3 dependencies satisfied
