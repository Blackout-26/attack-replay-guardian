# 01 — Product Specification

> Structured translation of the Attack Replay proposal into a product spec. Authority: [Hackathon Requirements](./02_HACKATHON_REQUIREMENTS.md) > proposal > this document. Deviations are recorded in the [Decision Log](./12_DECISION_LOG.md).

**Status:** 🔵 PLANNED · **Labels used:** KNOWN (from proposal) · PROPOSED · TO BE VERIFIED · OPEN DECISION · Priorities: MUST / SHOULD / NICE-TO-HAVE / FUTURE

---

## 1. Feature overview and priority

| ID | Feature | Priority | Backlog | Sprint |
|---|---|---|---|---|
| F-01 | Input (message / narrative / optional fields) | MUST | AR-016, AR-020 | S1, S2 |
| F-02 | Verdict (label, threat type, risk, reason, action) | MUST | AR-002, AR-003, AR-004, AR-006 | S1 |
| F-03 | Threat DNA (tactics + evidence + entities) | MUST | AR-005, AR-015, AR-021 | S2 |
| F-04 | Attack Replay (staged, interactive) | MUST | AR-007, AR-008, AR-022 | S3 |
| F-05 | Trust Gap (missing evidence, verification, toggles) | MUST | AR-009 | S3 |
| F-06 | Batch processing (`/batch`) | MUST | AR-017 | S1 |
| F-07 | Incident Mode | SHOULD | AR-010 | S4 |
| F-08 | Evasion Arena | SHOULD | AR-011, AR-023, AR-024, AR-025 | S4 |
| F-09 | Citizen mode reading-level slider | NICE-TO-HAVE | AR-026 | S5 (stretch) |
| F-10 | Organisation mode (ATT&CK-style tags, indicators, containment) | NICE-TO-HAVE | AR-027 | S5 (stretch) |
| F-11 | LLM rephrasing at chosen reading level | NICE-TO-HAVE | AR-028 | S5 (stretch) |
| F-12 | Tarpit, ScamSigma, Herd Immunity | FUTURE | AR-038–040 | "What's next" slide only |

> **Cut line (KNOWN, from proposal):** classifier, DNA, replay, trust gap and batch endpoint are must-haves. Arena and incident mode are should-haves. Organisation mode and the slider are nice-to-haves. Tarpit, ScamSigma and Herd Immunity go on the "what's next" slide. (The proposal names these three but does not define them — **TODO**: definitions are not required before submission.)

---

## 2. INPUT — F-01 (MUST)

| Field | Required | Notes |
|---|---|---|
| **Message text** | Yes | Raw text pasted by the user. |
| **Incident narrative** | Same field | E.g. "I clicked the link", "I already sent the money". The system detects harm-already-happened language (see [Incident Mode](#7-incident-mode--f-07-should)). |
| **Sender** | Optional | **Only if the dataset has a sender field** (TO BE VERIFIED in [AR-001](./13_BACKLOG.md#ar-001--dataset-inspection)). |
| **Channel** | Optional | Only if the dataset has channel information (TO BE VERIFIED). |
| **"Was I expecting this?"** | Optional, one tap | Expected / Not expected (a third "Not sure" state is PROPOSED). Feeds the [Trust Gap](#6-trust-gap--f-05-must). |
| ~~Screenshot upload~~ | **Out of scope** | KNOWN: "No screenshot upload." ([DEC-011](./12_DECISION_LOG.md#dec-011)) |

OPEN DECISIONS: maximum input length; handling of multiple messages in one paste (proposal only defines a single message/narrative). See [OD-018](./12_DECISION_LOG.md#open-decisions).

## 3. VERDICT — F-02 (MUST)

Covers the brief's five minimum features (per proposal; **TO BE VERIFIED** against the flyer — see [Hackathon Requirements](./02_HACKATHON_REQUIREMENTS.md)).

| Element | Values | Notes |
|---|---|---|
| **Label** | Suspicious / Benign | Binary decision from calibrated classifier. |
| **Threat type** | phishing · financial scam · identity fraud · malicious link/content · AI-enabled threat (per proposal's list of the brief's categories) | **Final taxonomy is set by the released dataset labels** — OPEN DECISION [OD-002](./12_DECISION_LOG.md#open-decisions). Do not hard-code before inspecting the data. |
| **Risk level** | Low / Medium / High | From the risk engine: `risk = likelihood × irreversibility of the ask`. |
| **Explanation** | One-line reason | Names **both** factors, e.g. "likely malicious, and it asks for something you can't undo". Grounded in evidence. |
| **Recommended action** | Short imperative | Template keyed on threat type + ask + risk. |

Rules:
- Show the risk **band**, not a fake-precise percentage. (Internal probabilities are for the engine and `/batch`, not the headline.)
- Benign verdicts still show *why* it looks benign and what to verify if unsure — no false reassurance.
- The LLM (if any) never sets label, type or risk.

## 4. THREAT DNA — F-03 (MUST)

The message is rendered with **tactic tags highlighted on the exact words** that triggered them. Each tag is marked **strong / present / absent** — no percentages.

| Tactic | Description | Evidence type |
|---|---|---|
| Urgency | Time pressure ("within 30 minutes") | Span(s) |
| Authority impersonation | Posing as a bank, utility, government body, employer, etc. | Span(s) + inferred sector |
| Fear / loss | Threat of suspension, penalty, arrest, loss | Span(s) |
| Reward / lure | Prize, refund, job, discount, investment return | Span(s) |
| Secrecy | "Don't tell anyone", isolation instructions | Span(s) |
| Credential request | PIN, OTP, password, login | Span(s) + ask entity |
| Payment request | Send/reverse/pay money, buy vouchers | Span(s) + amount entity |
| Call to action | Click, reply, call, install | Span(s) |
| Suspicious links | Link-based indicators (shorteners, odd domains, obfuscation) | URL entity — **never fetched** |
| *Other tactics discovered from the dataset* | **TODO** — added after dataset inspection (AR-001); each requires a definition and an evidence rule | — |

**Extracted entities (shown alongside):**

| Entity | Examples |
|---|---|
| Impersonated sector / organisation | mobile money, bank, utility, government, university… (context-based, not brand blacklist — [DEC-005](./12_DECISION_LOG.md#dec-005)) |
| The "ask" | PIN, OTP, money, login, app install, call-back |
| Channel / link | SMS/WhatsApp-style channel (if known), URLs, phone numbers |
| Amounts | Currency/amount cues |

**Engine notes (PROPOSED):** lexicons plus optional embedding similarity so wording changes do not break detectors; highlight offsets must map back to the **original** text even after normalization.

## 5. ATTACK REPLAY — F-04 (MUST)

A **staged graph built from the message's own entities**:

```
HOOK → ACTION POINT → EXTRACTION → TAKEOVER / CASH-OUT / COMPROMISE
```

| Stage | Meaning |
|---|---|
| **Hook** | What grabs attention (the message itself: lure, fear, authority). |
| **Action point** | Where the user decides. Options: **Click / Reply / Ignore / Report**. |
| **Extraction** | What the attacker obtains (credentials, OTP/PIN, money, app install, personal data). |
| **Takeover / cash-out / compromise** | What the attacker does with it. |

**User decisions and consequences (KNOWN from proposal):**

| Choice | What the replay shows |
|---|---|
| **Click** | The fake page / credential-capture stage appears (illustrated — never a real page). |
| **Reply** | The scammer's likely next message, including how they pressure you if you hesitate. |
| **Ignore / Report** | What stops the attack and what reporting triggers. |

**Recoverability:** at every stage a **"still recoverable?"** strip shows what can be undone and what cannot.

**Honesty requirements (MUST):**
- Label: *"Typical progression for this kind of attack — a simulation, not a prediction of one specific criminal."* (see [DEC-010](./12_DECISION_LOG.md#dec-010))
- The replay is a **curated playbook** per threat type — not generated ([DEC-001](./12_DECISION_LOG.md#dec-001)). Playbooks: [07_ATTACK_REPLAY_PLAYBOOKS](./07_ATTACK_REPLAY_PLAYBOOKS.md).
- Recoverability statements that depend on Zimbabwean providers/regulators are **TO BE VERIFIED** before being shown as fact.

## 6. TRUST GAP — F-05 (MUST)

| Component | Description |
|---|---|
| **Missing evidence** | What you would need to see before trusting this message (e.g., no verifiable sender, requests a secret, unexpected, link not independently confirmed). |
| **Verification guidance** | Checklist: don't use the message's link; open the official service independently; use an independently sourced phone number. |
| **Independent verification toggles** | "Sender confirmed through an official channel", "I was expecting this" — these **move the risk band**. |

Honesty requirements: toggles are **transparent rule-based adjustments, labelled "guidance"**, not learned effects ([DEC-009](./12_DECISION_LOG.md#dec-009)). Because toggles are unverifiable user assertions, a **PROPOSED guardrail** is that a toggle can lower the band but must not hide the irreversibility warning for OTP/PIN/payment asks — exact rules are OPEN ([OD-019](./12_DECISION_LOG.md#open-decisions)).

## 7. INCIDENT MODE — F-07 (SHOULD)

Triggered when the text says harm already happened; the **replay pointer jumps to the matching stage**.

| Situation | Replay pointer | Immediate response content |
|---|---|---|
| Already **clicked** | Fake page / credential-capture stage | Disconnect/scan guidance, change credentials from a clean path, watch for follow-ups |
| Already **replied** | Scammer's next-message stage | Stop replying, block/report, expect pressure |
| Already **submitted credentials** | Extraction | Change credentials via official service (independently opened), revoke sessions, contact provider |
| Already **transferred money** | Payment / cash-out stage | Contact provider/bank immediately using an independently sourced number, time-critical steps, report |

Outputs: **first-hour plan**, **evidence preservation** (what to keep: message, sender, timestamps, transaction refs — never delete), **pre-drafted report text** for provider or police (templated, user-editable). Local reporting channels and provider procedures are **TO BE VERIFIED** — do not invent contact details.

## 8. CITIZEN MODE — default

- Plain-language explanations, calm tone, actionable steps ([UX doc](./06_UX_AND_USER_JOURNEYS.md)).
- **Reading-level slider** (Technical / Normal / Simple) — **NICE-TO-HAVE** ([AR-026](./13_BACKLOG.md#ar-026--reading-level-slider)). Without an LLM it is implemented by pre-written template variants; an LLM may only rephrase grounded templates.

## 9. ORGANISATION MODE — F-10 (NICE-TO-HAVE)

Adds: **ATT&CK-style tactic tags** (e.g., Initial Access, Credential Access), **indicators to block**, **containment steps**, **evidence preservation**. Must not be started before all MUST items are stable.

## 10. EVASION ARENA — F-08 (SHOULD)

A scoreboard screen that runs mutated versions of known scams through the detector:

| Mutation class | Included |
|---|---|
| Homoglyphs | ✔ |
| Zero-width characters | ✔ |
| Split links | ✔ |
| Shona/English mixing | ✔ |
| Paraphrase | ✔ |
| AI-polished tone | ✔ |

Reports: **caught rate**, **false positives on benign messages**, applies a **patch** (Unicode normalisation + retraining on misses), then **re-runs on held-out mutation types not trained on**. Also shows **DNA stability across rewrites**. Must show false positives and held-out results to be credible. Evaluation rules: [05_EVALUATION_STRATEGY](./05_EVALUATION_STRATEGY.md).

## 11. BATCH PROCESSING — F-06 (MUST)

`/batch`: **CSV in → CSV out** with columns **label, type, risk, explanation, action** (KNOWN). Intended for the hidden evaluation set. Input column names/format of the hidden set are **TO BE VERIFIED** ([OD-010](./12_DECISION_LOG.md#open-decisions)). Batch must not require the LLM or internet.

## 12. Non-goals (for this hackathon)

Screenshot/OCR input · fetching or scanning live URLs · sending/reporting on the user's behalf · account integration with providers · user accounts · generative (LLM-authored) replay · real-time monitoring of inboxes.

## 13. Traceability

Backlog and sprint mappings: [13_BACKLOG](./13_BACKLOG.md). Hackathon mapping: [02_HACKATHON_REQUIREMENTS](./02_HACKATHON_REQUIREMENTS.md).
