# SPRINT 0 — DISCOVERY

[Project Plan](../../PROJECT_PLAN.md) · [Backlog](../13_BACKLOG.md) · [Next](SPRINT_01_DETECTION_FOUNDATION.md) →

| Item | Value |
|---|---|
| **Status** | 🔵 PLANNED |
| **Proposed timebox** | PROPOSED: part of "Today" in the proposal build plan ("read the dataset, freeze labels"). Calendar dates TO BE VERIFIED (OD-005). |
| **Lead roles** | ML-API (lead), PLAYBOOK-DEMO (requirements verification), ALL |
| **Sprint type** | Work package (not a fixed duration) |

## Sprint objective

Replace assumptions with facts: confirm the repository and environment, inspect the released dataset, verify the official requirements, freeze the threat taxonomy, and confirm the architecture and technology stack. **No implementation.**

## Why this sprint exists

Attack Replay's plan is built on unknowns that only the dataset and flyer can resolve (labels, threat types, risk labels, sender/channel fields, language mix, hidden-set format, deadlines). The proposal's own risk section says: build/inspect first, then adapt. Skipping this sprint would risk building the wrong taxonomy, playbooks and evaluation.

## Scope

**In scope**

- Repository discovery (or confirming none exists)
- Development environment setup
- Dataset discovery and data card
- Official requirements verification against the flyer
- Threat taxonomy freeze
- Architecture confirmation and technology-stack decision
- Listing technical unknowns and updating OD entries

**Out of scope**

- Any product code (analysis, API, UI)
- Model training or tuning
- Playbook implementation
- Frontend work

## Backlog items

| ID | Item | Priority | Status |
|---|---|---|---|
| [AR-000](../13_BACKLOG.md#ar-000) | Repository & environment discovery | MUST | 🔵 PLANNED |
| [AR-001](../13_BACKLOG.md#ar-001) | Dataset inspection | MUST | 🔵 PLANNED |
| [AR-012](../13_BACKLOG.md#ar-012) | Official requirements verification | MUST | 🔵 PLANNED |
| [AR-003](../13_BACKLOG.md#ar-003) | Threat taxonomy | MUST | 🔵 PLANNED |
| [AR-041](../13_BACKLOG.md#ar-041) | Architecture confirmation & tech-stack decision | MUST | 🔵 PLANNED |

Full acceptance criteria per item: [13_BACKLOG](../13_BACKLOG.md).


## Tasks

1. **AR-000:** Inspect the repository (structure, existing docs, tooling, CI); if none exists, record that and choose the location/name (OD-012). Set up and document the local development environment.
2. **AR-012:** Obtain the official flyer/brief. Close every item in the TO BE VERIFIED checklist in [Hackathon Requirements](../02_HACKATHON_REQUIREMENTS.md); record the competition timeline with absolute dates (OD-005) and the hidden-set input format (OD-010).
3. **AR-001:** Run the dataset discovery process from [Data & ML Strategy §2](../04_DATA_AND_ML_STRATEGY.md): schema, labels, distribution, missing values, duplicates, language mix, leakage scan, fitness for the proposal. Write `docs/DATA_CARD.md` (new file). Exploratory inspection scripts are allowed but are throwaway, not product code. Do not train models.
4. **AR-003:** Map dataset labels to the product taxonomy; freeze; map every type to a playbook or the generic fallback; log the decision (closes OD-002).
5. **AR-041:** Confirm the architecture against the findings; decide the technology stack and repository layout (OD-001, OD-014); list technical unknowns; update the Architecture doc if anything deviates.
6. Update [Risk Register](../11_RISK_REGISTER.md) statuses; update [PROJECT_PLAN](../../PROJECT_PLAN.md) status and [HANDOFF](../HANDOFF_TO_DEVELOPMENT.md) 'Known unknowns'.

## Dependencies

- Access to the released dataset (external)
- Access to the official flyer/brief (external)
- Team roles/owners (OD-008)
- No upstream sprint

## Expected outputs

- `docs/DATA_CARD.md` (dataset facts, measured statistics, leakage findings, field availability)
- Frozen taxonomy table and mapping (in Decision Log and/or Data & ML doc)
- Updated Hackathon Requirements (TO BE VERIFIED items closed) incl. timeline
- Decision Log entries: stack, taxonomy, split strategy candidates, closed ODs
- Repository/environment notes and working setup instructions
- Updated Risk Register and PROJECT_PLAN status

## Acceptance criteria

- [ ] Every TO BE VERIFIED item is closed or explicitly re-logged with reason
- [ ] Dataset statistics in the data card are measured, with the method noted
- [ ] Taxonomy is frozen and each class maps to a playbook target
- [ ] Stack decision recorded with reasons and offline/determinism constraints confirmed
- [ ] Dev environment reproducible on a second machine or by a teammate
- [ ] No product code or trained model added

## Definition of Done

Common DoD (see [PROJECT_PLAN](../../PROJECT_PLAN.md#common-definition-of-done)) plus:

- [ ] Backlog items AR-000, AR-001, AR-003, AR-012, AR-041 updated to 🟢 COMPLETE (or 🔴 BLOCKED with reason)
- [ ] All findings recorded in files under version control (not only in chat)
- [ ] Discrepancies with the proposal recorded in the Decision Log (not silently absorbed)
- [ ] HANDOFF and PROJECT_PLAN updated to reflect reality

## Testing requirements

- No automated product tests (no product code yet)
- Verification checks: data loads reproducibly; counts in data card can be re-derived by a second person; internal doc links still valid

## Demo milestone

No user-facing demo. Milestone: a five-minute readout — 'here is what the data and flyer actually say, here is the frozen taxonomy and stack, here is what changed from the proposal'.

## Risks

- R-001 Dataset mismatch
- R-002 Insufficient dataset quality
- R-003 Class imbalance
- R-004 Data leakage (early detection)
- R-022 Official requirements unverified
- R-023 Team capacity/roles unassigned
- R-017 Time constraints

See [Risk Register](../11_RISK_REGISTER.md).

## Stretch goals

- Start the technical summary skeleton (proposal: start the summary early) [AR-033]
- Begin drafting playbook content in Markdown (no code) [AR-008]
- Draft candidate tactic lexicons from dataset observations

Stretch goals are attempted only after every acceptance criterion is met and must not destabilize the sprint's deliverables.

## Explicitly deferred work

- All implementation (AR-002 onward)
- Model training or hyperparameter work
- Frontend/UX build
- Arena, Incident Mode, Organisation mode

## Exit criteria

- [ ] All five backlog items complete
- [ ] Taxonomy frozen; stack decided; TO BE VERIFIED items closed
- [ ] Sprint 1 entry conditions in [SPRINT_01](./SPRINT_01_DETECTION_FOUNDATION.md) are satisfiable
- [ ] If the dataset lacks threat types or risk labels: fallback decisions logged BEFORE Sprint 1 starts
