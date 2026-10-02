# Handoff to Development

> Written for the **next chat**, which will not have the context of the planning conversation. Everything you need is in the repository documents. Read this file fully first.

**Handoff date:** 2026-09-29 · **Current sprint:** **Sprint 0 — Discovery (🔵 PLANNED, not started)** · **Implementation status:** none (no code, no model, no UI, no API)

---

## 1. What Attack Replay is

A cybersecurity-hackathon product for the *National Cybersecurity Innovation Hackathon 2026* (theme "Don't Make It Easy for Them: Building a Cyber Strong Zimbabwe"; challenge "Cyber Shield Zimbabwe: Detecting and Responding to Cyber Threats").

> **We don't just tell you it's a scam. We let you watch it play out, safely, and show you what you can still undo.**

Philosophy: **DETECT → EXPLAIN → REPLAY → INTERRUPT → RECOVER.** A citizen pastes a suspicious message or an incident narrative; the system gives a verdict (suspicious/benign, threat type, Low/Medium/High risk, one-line reason, recommended action), a **Threat DNA** view (tactics tied to exact words), a safe **Replay** of the typical attack progression (hook → action point → extraction → takeover/cash-out) with a "still recoverable?" strip, a **Trust Gap** verification view, **Incident Mode** for harm already done, and an **Evasion Arena** proving robustness. Endpoints: `/analyze` (UI) and `/batch` (CSV in → CSV out for the hidden evaluation set).

It is **not** a generic cybersecurity platform and **not** "just an AI scam detector."

## 2. What has already been decided (do not relitigate)

Full list: [Decision Log](./12_DECISION_LOG.md) (DEC-001…017). Headlines:

| Decision | Ref |
|---|---|
| Replay is **curated** playbooks, not generative | DEC-001 |
| The **LLM never decides** the verdict; templates are the offline fallback | DEC-002, DEC-014 |
| Explainability is **evidence-grounded** (strong/present/absent tied to exact words; no fake percentages) | DEC-003 |
| **Char n-gram TF-IDF + calibrated logistic regression** first; embeddings optional | DEC-004 |
| Zimbabwe context is **pattern-based**, not brand blacklists | DEC-005 |
| Arena and Incident Mode are **secondary** to the core | DEC-006/007 |
| Risk = **likelihood × irreversibility of the ask** | DEC-008 |
| Toggles are rule-based **guidance**, not learned | DEC-009 |
| Replay is a **typical progression**, not a prediction of one criminal | DEC-010 |
| **No screenshot upload** | DEC-011 |
| Cut line: MUST classifier/DNA/replay/trust gap/batch; SHOULD Arena/incident; COULD Org mode/slider; LATER Tarpit/ScamSigma/Herd Immunity | DEC-012 |

## 3. Authoritative documents

| Need | Document |
|---|---|
| Master index, status, DoD | [PROJECT_PLAN.md](../PROJECT_PLAN.md) |
| Identity and principles | [00 North Star](./00_PROJECT_NORTH_STAR.md) |
| Features and priorities | [01 Product Specification](./01_PRODUCT_SPECIFICATION.md) |
| Hackathon requirements / TO BE VERIFIED list | [02 Requirements](./02_HACKATHON_REQUIREMENTS.md) |
| Architecture | [03 Architecture](./03_PRODUCT_ARCHITECTURE.md) |
| Dataset, ML, normalization, extraction, risk | [04 Data & ML](./04_DATA_AND_ML_STRATEGY.md) |
| Evaluation rules | [05 Evaluation](./05_EVALUATION_STRATEGY.md) |
| UX and journeys | [06 UX](./06_UX_AND_USER_JOURNEYS.md) |
| Playbooks | [07 Playbooks](./07_ATTACK_REPLAY_PLAYBOOKS.md) |
| Safety | [08 Security](./08_SECURITY_AND_SAFETY.md) |
| Demo | [09 Demo](./09_DEMO_STRATEGY.md) |
| Submission | [10 Submission](./10_SUBMISSION_PLAN.md) |
| Risks | [11 Risks](./11_RISK_REGISTER.md) |
| Decisions | [12 Decision Log](./12_DECISION_LOG.md) |
| Work items | [13 Backlog](./13_BACKLOG.md) |
| Sprints | [Sprint 0](./sprints/SPRINT_00_DISCOVERY.md) · [1](./sprints/SPRINT_01_DETECTION_FOUNDATION.md) · [2](./sprints/SPRINT_02_THREAT_DNA.md) · [3](./sprints/SPRINT_03_ATTACK_REPLAY.md) · [4](./sprints/SPRINT_04_ROBUSTNESS_AND_INCIDENT_MODE.md) · [5](./sprints/SPRINT_05_FINAL_HARDENING.md) |

Authority order: official hackathon requirements > proposal > planning docs > Decision Log > implementation details. Conflicts get **documented**, not silently resolved.

## 4. What must NOT be changed casually

- The central idea: interpret + safely replay + show recoverability (not just a verdict).
- The five-step philosophy and the pitch line.
- Curated replay; LLM never sets verdicts; everything works offline.
- Honesty labels: "simulation", "typical progression", toggles = "guidance".
- MUST/SHOULD/COULD/LATER tiers and the cut line.
- Safety prohibitions: never fetch/execute submitted URLs, send messages, or perform transactions.
- Evaluation rules: no leakage, no tuning on hidden/final data, report false positives and failures.

Any change to the above requires a Decision Log entry **first**.

## 5. Sprint sequence

`S0 Discovery → S1 Detection Foundation → S2 Threat DNA → S3 Attack Replay → S4 Robustness + Incident Mode → S5 Final Hardening`

Each sprint has entry dependencies and exit criteria in its document. Do not start a sprint whose dependencies are unmet.

## 6. Current sprint and first actions

**Current sprint: Sprint 0 — Discovery** ([document](./sprints/SPRINT_00_DISCOVERY.md)). Suggested order of first actions:

1. **AR-012 — Get the official flyer/brief** and close the TO BE VERIFIED items (deadlines, judging criteria, exact five minimum features and threat-type names, hidden-set format, rules on external models/LLMs/AI assistance).
2. **AR-000 — Inspect the repository** (none was found while writing these docs; confirm location/name, OD-012) and set up the dev environment.
3. **AR-001 — Inspect the released dataset** using the discovery process in [Data & ML §2](./04_DATA_AND_ML_STRATEGY.md); write `docs/DATA_CARD.md`. Throwaway inspection scripts are fine; **do not train models yet**.
4. **AR-003 — Freeze the taxonomy** from the real labels; map to playbooks.
5. **AR-041 — Confirm architecture and choose the tech stack** (OD-001), log it.
6. Update [PROJECT_PLAN](../PROJECT_PLAN.md) status and the Risk Register; then begin Sprint 1.

Because the proposal's schedule is short, moving quickly from Sprint 0 into Sprint 1 is expected once the taxonomy is frozen.

## 7. Important constraints

- Everything on the core/demo path works **without an LLM and without internet**.
- Deterministic core: same input → same output.
- Normalization must keep an **offset map** so highlights land on the user's original text.
- Text-only input; `/batch` output columns: **label, type, risk, explanation, action**.
- Do not use brand blacklists; do not put real brands/numbers/links in playbooks.
- Do not invent numbers: dataset statistics, model accuracy, prevalence, recoverability windows.
- Extras (Arena, Incident, Org mode) must not destabilize the core; use the sprint-4 stability gate.

## 8. Open questions (see Decision Log §3 for the full list)

| ID | Question |
|---|---|
| OD-001 | Technology stack and repository layout |
| OD-002 | Final taxonomy and mapping (dataset labels win for classification) |
| OD-004 | Does the dataset have sender / channel / risk labels / language fields? |
| OD-005 | Absolute dates and sprint timeboxes |
| OD-006 | Any LLM use at all (default: none) |
| OD-008 | Who owns which role (ML-API, FE-REPLAY, PLAYBOOK-DEMO) |
| OD-010 | Hidden-set `/batch` input schema |
| OD-012 | Repository location/name |
| OD-019 | Trust Gap toggle rules and guardrails |
| OD-020 | Definitions of Tarpit, ScamSigma, Herd Immunity |

## 9. Known unknowns

- Dataset labels, size, balance, languages, duplicates, licence — **unknown until AR-001**.
- Flyer details (dates, judging, submission rules) — **unknown until AR-012**.
- Whether risk labels exist (determines how risk thresholds are fit).
- Zimbabwe-specific provider/regulator recovery procedures — **unverified**; keep generic or flag TO BE VERIFIED.
- Shona lexicon quality — needs a Shona-speaking reviewer.
- Deployment/hosting conditions at the venue.

## 10. Definition of Done for Sprint 1

Sprint 1 ([document](./sprints/SPRINT_01_DETECTION_FOUNDATION.md)) is done when a **working analytical backend** exists:

- [ ] Group-aware, seeded, leakage-checked train/validation/test splits; final test frozen (AR-013)
- [ ] Normalization with offset map; idempotence and offset tests pass (AR-014)
- [ ] Rule-based extraction of URLs, phones, amounts, sector cues and the ask; URLs never fetched (AR-015)
- [ ] Baseline char n-gram/word TF-IDF + logistic regression with calibration; threat classification on the frozen taxonomy (AR-002, AR-019)
- [ ] Risk engine with transparent weights and Low/Medium/High bands (AR-004)
- [ ] Template explanations + recommended action for every taxonomy class (AR-006)
- [ ] `/analyze` returns the five minimum features; `/batch` round-trips CSV robustly (AR-016, AR-017)
- [ ] Security baseline (AR-030); tests and evaluation harness (AR-018)
- [ ] Measured baseline metrics recorded honestly (incl. false-positive rate and per-class results); no tuning on final test
- [ ] Works offline; README explains setup/run/test/evaluate; decisions logged

## 11. How to report progress

- Update statuses (🔵/🟡/🟢/🔴/⚪) in the [Backlog](./13_BACKLOG.md) index and item tables, the sprint document, and PROJECT_PLAN §7.
- At the end of each work session, post: **what changed · what was measured (with data/model versions) · what is blocked · decisions made · next 3 actions**.
- Report results as **measured** vs **proposed goal**; include failures and weaknesses.
- Record risk changes in the [Risk Register](./11_RISK_REGISTER.md).

## 12. Where to record decisions

[Decision Log](./12_DECISION_LOG.md): append `DEC-NNN` using the template; convert closed `OD-nnn` rows; mention the decision in the sprint document. Log **before** implementing anything that deviates from the proposal.

## 13. Environment note

These documents were authored in a workspace that contained **no repository, dataset or flyer**. The whole documentation set is delivered as one folder (`PROJECT_PLAN.md` + `docs/`) to be placed at the repository root. If the real repository already has a `docs/` directory or `PROJECT_PLAN.md`, merge rather than overwrite and note it in the Decision Log.

---

**Read `PROJECT_PLAN.md`, the Project North Star, Product Specification, Architecture, Data/ML Strategy, Backlog, and the Sprint 1 document before beginning implementation. Begin with Sprint 0.**
