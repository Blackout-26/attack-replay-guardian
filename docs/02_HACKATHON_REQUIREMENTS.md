# 02 — Hackathon Requirements

> Translates the official challenge into engineering requirements. **The official flyer/brief is not present in the workspace this documentation was authored in.** Everything below is either taken from the project brief/proposal (KNOWN-from-proposal, second-hand) or marked **TO BE VERIFIED**. Sprint 0 task [AR-012](./13_BACKLOG.md#ar-012--official-requirements-verification) closes every TO BE VERIFIED item against the actual flyer.

**Status:** 🔵 PLANNED

## 1. Confidence legend

| Tag | Meaning |
|---|---|
| **KNOWN (proposal)** | Stated in the Attack Replay proposal or project brief. Second-hand until checked against the flyer. |
| **TO BE VERIFIED** | Not known, or unclear. Do **not** invent an interpretation. |

## 2. Event identity

| Item | Value | Confidence |
|---|---|---|
| Hackathon | National Cybersecurity Innovation Hackathon 2026 | KNOWN (proposal) |
| Organisers / context | NUST; Ministry of ICT, Postal and Courier Services (Zimbabwe) | KNOWN (proposal) |
| Theme | "Don't Make It Easy for Them: Building a Cyber Strong Zimbabwe" | KNOWN (proposal) |
| Challenge | "Cyber Shield Zimbabwe: Detecting and Responding to Cyber Threats" | KNOWN (proposal) |

## 3. Requirements known from the proposal

| ID | Requirement | Confidence |
|---|---|---|
| HR-01 | Classify a message as **suspicious or benign** | KNOWN (proposal: "the brief's five minimum features") — wording TO BE VERIFIED |
| HR-02 | Classify **threat type**; brief categories per proposal: phishing, financial scam, identity fraud, malicious link/content, AI-enabled threat | KNOWN (proposal) — exact category names/definitions TO BE VERIFIED |
| HR-03 | Provide a **risk level** (Low / Medium / High) | KNOWN (proposal) — TO BE VERIFIED |
| HR-04 | Provide an **explanation** (one-line reason) | KNOWN (proposal) — TO BE VERIFIED |
| HR-05 | Provide a **recommended action** | KNOWN (proposal) — TO BE VERIFIED |
| HR-06 | **Innovation** is valued | TO BE VERIFIED (whether a formal criterion) |
| HR-07 | **Working prototype** | KNOWN (proposal: "the flyer expects…") |
| HR-08 | **Short technical summary** | KNOWN (proposal) — length/format TO BE VERIFIED |
| HR-09 | **Presentation** | KNOWN (proposal) — format/duration TO BE VERIFIED |
| HR-10 | **Source code** | KNOWN (proposal) — repo/licence rules TO BE VERIFIED |
| HR-11 | A **hidden evaluation set** will be run through the system | KNOWN (proposal) — mechanism and input format TO BE VERIFIED |
| HR-12 | Released **dataset** available for training | KNOWN (proposal: "trained on the released dataset") — content/labels/licence TO BE VERIFIED |

## 4. Traceability matrix

`Hackathon requirement → Attack Replay feature → Implementation requirement → Demonstration requirement → Evidence required`

| Req | Attack Replay feature | Implementation requirement | Demonstration requirement | Evidence required | Backlog |
|---|---|---|---|---|---|
| HR-01 Suspicious/benign | Verdict label | Calibrated classifier; `/analyze`, `/batch`; benign false-positive handling | Paste one suspicious and one benign message; show both verdicts | Held-out precision/recall/F1, confusion matrix, false-positive rate ([Eval](./05_EVALUATION_STRATEGY.md)) | AR-001, AR-002, AR-013, AR-018 |
| HR-02 Threat classification | Threat type on Verdict card | Taxonomy frozen from dataset labels; multi-class model or mapping | Verdict card shows type; replay playbook chosen by type | Per-class P/R/F1, macro/weighted F1, class distribution | AR-003, AR-002 |
| HR-03 Risk level | Risk engine (likelihood × irreversibility) | Risk fusion with ask-type weights; thresholds fit to dataset risk labels **if present** | Show a High-risk credential/payment ask vs a lower-risk message | Risk distribution by class; agreement with risk labels if they exist; documented rules | AR-004 |
| HR-04 Explainability | Explanation engine + Threat DNA | Grounded templates keyed on indicators; evidence spans; no ungrounded claims | Highlighted tactic tags tied to exact words | Groundedness audit: every explanation claim traces to an indicator/entity | AR-005, AR-006, AR-021 |
| HR-05 Recommended action | Action templates; Trust Gap checklist | Action keyed on type + ask + risk; verification guidance | Verdict card action + verify-it-yourself checklist | Action-template coverage for every taxonomy class; review checklist | AR-006, AR-009 |
| HR-06 Innovation | Attack Replay, Trust Gap, Incident Mode, Evasion Arena | Curated playbooks; replay engine; mutators; patch loop | Replay Click/Reply/Ignore/Report; recoverability strip; Arena before/after | Playbook library; Arena results incl. held-out mutations | AR-007–011 |
| HR-07 Working prototype | Web UI + API | Runs from clean checkout; works offline; deployed or locally runnable | Live demo + recorded backup | Running URL/instructions; backup video | AR-020, AR-022, AR-032, AR-035 |
| HR-08 Technical summary | — | Written summary incl. external models/libraries list | — | Summary document; dependency inventory | AR-033, AR-036 |
| HR-09 Presentation | — | Slide deck incl. "what's next" (Tarpit, ScamSigma, Herd Immunity) | 2-minute demo embedded/rehearsed | Deck file | AR-034 |
| HR-10 Source code | — | Clean repo, README, run instructions, licences | — | Repository link/archive | AR-036 |
| HR-11 Hidden set | `/batch` | CSV in → CSV out (label, type, risk, explanation, action); no LLM/internet required | Optional: show batch run | Batch run on validation data; format tested | AR-017 |
| HR-12 Dataset use | Training/eval pipeline | Leakage-free splits; documented provenance | — | Data card; attribution | AR-001, AR-013 |
| Theme fit | Whole product | — | Closing message: every step harder for the scammer | Narrative in deck | AR-034 |

## 5. Competition timeline

| Source | Timeline | Confidence |
|---|---|---|
| Official brief (flyer) | **Dates, deadlines, submission cut-off, finals format — not available in this workspace** | **TO BE VERIFIED** |
| Proposal build plan (relative) | **Today:** read dataset, freeze labels; ship baseline (extraction, classifier, risk, template explanations) with `/analyze` and `/batch`. **Tuesday:** write playbook library, build replay UI, then trust gap and incident mode; start Arena mutators. **Wednesday morning:** finish Arena scoreboard, rehearse demo, record backup video. | KNOWN (proposal) — mapping to absolute dates TO BE VERIFIED |

Sprint-to-timeline mapping is **PROPOSED**: S0+S1 ≈ "Today", S2–S4 ≈ "Tuesday", S5 ≈ "Wednesday morning". Sprints are work packages, not fixed durations — see [OD-005](./12_DECISION_LOG.md#open-decisions).

## 6. TO BE VERIFIED checklist (Sprint 0, AR-012)

- [ ] Exact wording of the five minimum features and the threat-type categories
- [ ] Risk level definition (is Low/Medium/High mandated? any risk labels supplied?)
- [ ] Judging criteria and weightings
- [ ] Submission deadline, channel, format, file size limits
- [ ] Prototype requirements (hosted vs local; live demo vs recorded)
- [ ] Technical summary length/format; presentation length/format
- [ ] Source code rules (public repo? licence? team disclosure?)
- [ ] Hidden evaluation set: how it is delivered/run, column names, size, language mix
- [ ] Rules on external models, APIs and LLMs; rules on AI assistance
- [ ] Dataset licence, permitted use, whether external data is allowed
- [ ] Team size / eligibility constraints
- [ ] Finals/pitch format and time limit

## 7. Principle

Do not invent requirements. If it is not on the flyer or in the proposal, it is not a hackathon requirement here.
