# SPRINT 5 — FINAL HARDENING

← [Previous](SPRINT_04_ROBUSTNESS_AND_INCIDENT_MODE.md) · [Project Plan](../../PROJECT_PLAN.md) · [Backlog](../13_BACKLOG.md)

| Item | Value |
|---|---|
| **Status** | 🔵 PLANNED |
| **Proposed timebox** | PROPOSED: "Wednesday morning" (proposal: rehearse the demo, record a backup video). Dates and the submission deadline TO BE VERIFIED (OD-005). |
| **Lead roles** | ALL (integration), PLAYBOOK-DEMO (demo, presentation), ML-API (deployment, summary), FE-REPLAY (polish) |
| **Sprint type** | Work package (not a fixed duration) |

## Sprint objective

Ship a **reliable, honest, submittable** prototype: integration, UX polish, error handling, performance, testing, deployment, documentation, demo rehearsal, technical summary, presentation, source-code cleanup, and a backup video. **No major new features** unless absolutely necessary.

## Why this sprint exists

Judges see a demo and a package, not the backlog. Most hackathon failures are integration, deployment and rehearsal failures. Feature freeze here protects the demo ([R-015](../11_RISK_REGISTER.md), [R-016](../11_RISK_REGISTER.md)).

## Scope

**In scope**

- Integration of all features; end-to-end testing
- Error handling, offline verification, graceful degradation
- Deployment and clean-machine run
- UX polish and performance
- Source-code cleanup, attribution inventory, security review
- Technical summary and presentation
- Demo rehearsal and backup video
- Final documentation update

**Out of scope**

- New features (except blockers)
- New models or datasets
- Architecture changes

## Backlog items

| ID | Item | Priority | Status |
|---|---|---|---|
| [AR-031](../13_BACKLOG.md#ar-031) | Error handling & offline verification | MUST | 🔵 PLANNED |
| [AR-032](../13_BACKLOG.md#ar-032) | Deployment | MUST | 🔵 PLANNED |
| [AR-036](../13_BACKLOG.md#ar-036) | Source cleanup, attribution & security review | MUST | 🔵 PLANNED |
| [AR-037](../13_BACKLOG.md#ar-037) | UX polish & performance | SHOULD | 🔵 PLANNED |
| [AR-033](../13_BACKLOG.md#ar-033) | Technical summary | MUST | 🔵 PLANNED |
| [AR-034](../13_BACKLOG.md#ar-034) | Presentation | MUST | 🔵 PLANNED |
| [AR-035](../13_BACKLOG.md#ar-035) | Demo rehearsal & backup video | MUST | 🔵 PLANNED |

Full acceptance criteria per item: [13_BACKLOG](../13_BACKLOG.md).

**Stretch items** (attempted only after every acceptance criterion is met):

| ID | Item | Priority | Status |
|---|---|---|---|
| [AR-026](../13_BACKLOG.md#ar-026) | Reading-level slider | COULD | 🔵 PLANNED |
| [AR-027](../13_BACKLOG.md#ar-027) | Organisation mode | COULD | 🔵 PLANNED |
| [AR-028](../13_BACKLOG.md#ar-028) | LLM rephrasing layer | COULD | 🔵 PLANNED |
| [AR-038](../13_BACKLOG.md#ar-038) | Tarpit (future) | LATER | 🔵 PLANNED |
| [AR-039](../13_BACKLOG.md#ar-039) | ScamSigma (future) | LATER | 🔵 PLANNED |
| [AR-040](../13_BACKLOG.md#ar-040) | Herd Immunity (future) | LATER | 🔵 PLANNED |


## Tasks

1. **Feature freeze** at sprint start; any exception requires a Decision Log entry.
2. **AR-031:** Test every failure path; verify full operation with LLM and internet disabled; malformed batch input.
3. **AR-032:** Deploy/package; test from a clean machine using the README only; document fallback local run (OD-007).
4. **AR-036:** Clean the repository; complete the dependency/licence/attribution inventory in the [Submission Plan](../10_SUBMISSION_PLAN.md); run the [security checklist](../08_SECURITY_AND_SAFETY.md); secrets scan; final tag.
5. **AR-037:** Copy review (overclaiming, jargon), accessibility basics, latency polish, privacy statement.
6. **AR-033:** Finish the technical summary using numbers from a tagged evaluation run, including failures and limitations.
7. **AR-034:** Build the presentation incl. the two-minute demo and the 'what's next' slide (define Tarpit, ScamSigma, Herd Immunity — OD-020).
8. **AR-035:** Two timed rehearsals + one offline rehearsal; exercise fallbacks B1–B5; record and review the backup video.
9. Update all documentation for reality: PROJECT_PLAN status, backlog statuses, risk register, decision log.
10. Submit with buffer; save confirmation.

## Dependencies

- Sprint 4 exit and feature-freeze decision
- Final evaluation numbers
- Flyer submission rules (AR-012)

## Expected outputs

- Deployable/runnable prototype
- Technical summary
- Presentation
- Clean, documented source repository with final tag
- Backup demo video
- Submission package and confirmation

## Acceptance criteria

- [ ] A teammate not on the build can run the prototype from the README on a clean machine
- [ ] Two-minute demo completes within time offline, twice in a row
- [ ] Everything shown in the demo exists in the product and matches the documentation
- [ ] All claims in summary/deck are traceable to recorded results or labelled proposed/future
- [ ] Submission checklist in the Submission Plan fully checked
- [ ] No secrets or sensitive data in the repository

## Definition of Done

Common DoD (see [PROJECT_PLAN](../../PROJECT_PLAN.md#common-definition-of-done)) plus:

- [ ] All MUST items 🟢 COMPLETE; any unfinished SHOULD/COULD marked ⚪ DEFERRED with reason
- [ ] Security checklist passed
- [ ] Licence/attribution inventory complete
- [ ] Final tag built, archived, re-tested
- [ ] Docs updated; HANDOFF marked as historical/updated

## Testing requirements

- Full regression suite
- Clean-machine install test
- Offline run of demo path
- Load/latency sanity check on demo hardware (no numeric target invented)
- Batch run on malformed and large files
- Security checklist
- Judge-question drill

## Demo milestone

Milestone: the full two-minute demo per [Demo Strategy](../09_DEMO_STRATEGY.md), plus the backup video and fallbacks.

## Risks

- R-010 Internet failure
- R-011 API failure
- R-016 Demo failure
- R-017 Time constraints
- R-018 Deployment problems
- R-013 Dependency problems
- R-019 Security problems
- R-015 Scope creep

See [Risk Register](../11_RISK_REGISTER.md).

## Stretch goals

- Reading-level slider [AR-026]
- Organisation mode [AR-027]
- LLM rephrasing (opt-in, off by default) [AR-028]
- Roadmap detail for Tarpit/ScamSigma/Herd Immunity [AR-038–040]

Stretch goals are attempted only after every acceptance criterion is met and must not destabilize the sprint's deliverables.

## Explicitly deferred work

- Anything not required for submission
- Post-hackathon roadmap (Tarpit, ScamSigma, Herd Immunity)

## Exit criteria

- [ ] Submission delivered and confirmation saved
- [ ] Backup video and fallback materials ready
- [ ] Final status recorded in PROJECT_PLAN
