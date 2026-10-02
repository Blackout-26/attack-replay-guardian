# SPRINT 3 — ATTACK REPLAY

← [Previous](SPRINT_02_THREAT_DNA.md) · [Project Plan](../../PROJECT_PLAN.md) · [Backlog](../13_BACKLOG.md) · [Next](SPRINT_04_ROBUSTNESS_AND_INCIDENT_MODE.md) →

| Item | Value |
|---|---|
| **Status** | 🔵 PLANNED |
| **Proposed timebox** | PROPOSED: "Tuesday" (proposal: write the playbook library, build the replay UI, then the trust gap). Dates TO BE VERIFIED (OD-005). |
| **Lead roles** | PLAYBOOK-DEMO (playbooks), ML-API (engine, trust gap rules), FE-REPLAY (replay UI) |
| **Sprint type** | Work package (not a fixed duration) |

## Sprint objective

Deliver the **central innovation**: a curated playbook library, replay engine, staged attack progression built from the message's entities, user choices and consequences, recoverability at every stage, and the Trust Gap with verification guidance and guidance toggles.

## Why this sprint exists

This is what differentiates Attack Replay from a scam detector ([North Star](../00_PROJECT_NORTH_STAR.md)). It is a MUST for both the proposal's cut line and the pitch. Everything after this sprint is either proof (Arena), extra (Incident Mode) or hardening.

## Scope

**In scope**

- Playbook architecture and library (10 proposed scenarios + generic fallback)
- Replay engine with Click/Reply/Ignore/Report
- Consequences and recoverability per stage
- Trust Gap: missing evidence, verification checklist, guidance toggles
- Replay UI and Trust Gap UI

**Out of scope**

- Incident Mode (Sprint 4)
- Evasion Arena (Sprint 4)
- LLM-generated replay (rejected by [DEC-001](../12_DECISION_LOG.md#dec-001))
- Organisation mode

## Backlog items

| ID | Item | Priority | Status |
|---|---|---|---|
| [AR-008](../13_BACKLOG.md#ar-008) | Playbook library | MUST | 🔵 PLANNED |
| [AR-007](../13_BACKLOG.md#ar-007) | Replay engine | MUST | 🔵 PLANNED |
| [AR-009](../13_BACKLOG.md#ar-009) | Trust Gap | MUST | 🔵 PLANNED |
| [AR-022](../13_BACKLOG.md#ar-022) | Replay UI | MUST | 🔵 PLANNED |

Full acceptance criteria per item: [13_BACKLOG](../13_BACKLOG.md).


## Tasks

1. **AR-008:** Finalize playbook schema; author playbooks per [Playbooks doc](../07_ATTACK_REPLAY_PLAYBOOKS.md) for mapped taxonomy types and the generic fallback; verify or flag local facts (R-020); second-person review.
2. **AR-007:** Implement playbook selection (threat type + sector/ask entities), stage instantiation from extracted entities, choice handling and per-stage recoverability.
3. **AR-009:** Implement missing-evidence list, verification checklist and rule-based toggles; decide toggle rules and guardrails (closes OD-019); label as guidance.
4. **AR-022:** Build the replay UI: staged graph, action-point decision, consequence view, 'still recoverable?' strip, Trust Gap panel; mandatory simulation labels.
5. Extend `/analyze` (or add a replay endpoint) with `replay` and `trust_gap`; log schema changes.
6. Add replay and trust-gap cases to the regression suite.

## Dependencies

- Sprint 2 exit: entities and DNA available; frontend shell working
- Frozen taxonomy and playbook targets (AR-003)
- Verified/flagged local recovery facts (R-020)

## Expected outputs

- Playbook library (static, version-controlled) with review records
- Replay engine and API integration
- Trust Gap engine and UI
- Replay UI integrated with the analysis view
- Updated regression set

## Acceptance criteria

- [ ] For each mapped taxonomy type, selecting Click/Reply/Ignore/Report yields the documented consequence
- [ ] Every stage shows recoverability; unverified local claims are flagged (not shown as fact)
- [ ] Replay output is labelled as typical progression / simulation on every screen
- [ ] Replay uses the message's own entities and contains no real brands, links or numbers
- [ ] Trust Gap toggles move the risk band by documented rules and are labelled 'guidance'; OTP/PIN/payment warning preserved (R-021)
- [ ] Works offline; earlier acceptance criteria still pass

## Definition of Done

Common DoD (see [PROJECT_PLAN](../../PROJECT_PLAN.md#common-definition-of-done)) plus:

- [ ] Sprint items 🟢 COMPLETE
- [ ] Playbook QA checklist passed for every playbook
- [ ] OD-019 closed in the Decision Log
- [ ] No regression in classifier/DNA metrics
- [ ] Demo path DEMO-01 → Reply → recoverability → trust-gap toggle works end to end

## Testing requirements

- Playbook schema validation tests
- Engine tests: every taxonomy class resolves to a playbook or fallback; every choice yields a next state
- Trust Gap rule tests, including guardrail cases
- UI walkthrough of J1, J3–J6, J9 in the UX doc
- Wording review for overclaiming (R-014)
- Regression: prior sprints

## Demo milestone

Milestone (the pitch core): paste DEMO-01 → verdict → DNA → replay → tap Reply → scammer's likely next message → recoverability strip → toggle 'sender verified' → risk band moves with guidance label.

## Risks

- R-014 Replay overclaiming
- R-020 Incorrect local recovery guidance
- R-021 False reassurance from toggles
- R-015 Scope creep
- R-017 Time constraints
- R-016 Demo failure

See [Risk Register](../11_RISK_REGISTER.md).

## Stretch goals

- Additional playbook variants or scenarios beyond the proposed ten
- Smoother replay animations (only after functional completeness)
- Phone-sized layout pass

Stretch goals are attempted only after every acceptance criterion is met and must not destabilize the sprint's deliverables.

## Explicitly deferred work

- Incident Mode (AR-010, Sprint 4)
- Evasion Arena (AR-011, AR-023–025, Sprint 4)
- Slider, Organisation mode, LLM (Sprint 5 stretch)

## Exit criteria

- [ ] Definition of Done met
- [ ] The core demo path works reliably offline
- [ ] MUST-tier product features complete (verdict, DNA, replay, trust gap, batch)
- [ ] Sprint 4 can start without changing core interfaces
