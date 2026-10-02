# 09 — Demo Strategy

> The final two-minute demo. It maps only to features in the [Backlog](./13_BACKLOG.md); anything not built by the freeze is cut per §7. **All example messages below are illustrative fictional text written for planning; they must be re-cast in the style of the real dataset and hidden set after Sprint 0/1** (and contain no real brands, numbers or links).

**Status:** 🔵 PLANNED · Backlog: AR-035 (rehearsal/backup video) + all demo-dependent features

## 1. Message to land

> **"Don't just tell me it's dangerous. Show me what the attack is trying to do."**

Story arc: a citizen sees a realistic mobile-money scam → the verdict lands → the tactics are laid bare → they watch the attack play out and choose an action → they see what's still undoable → they see what to do if it already happened → they see the detector is robust, including its false positives.

## 2. Two-minute script

Base timeline follows the proposal's demo; the structure requested for planning (message → detection → DNA → replay → choice → recoverability → incident/Arena → close) is preserved. Reconciliation logged as [DEC-017](./12_DECISION_LOG.md#dec-017); timings to be confirmed in rehearsal.

| Time | Screen / action | Narration (draft) | Depends on |
|---|---|---|---|
| **0:00–0:15** | Paste **DEMO-01** (mobile-money PIN/OTP scam). Verdict card appears | "A citizen gets this message. Most tools stop at a score. Watch." | AR-016, AR-020, AR-002–004, AR-006 |
| **0:15–0:30** | Verdict card: Suspicious · type · High · one-line reason ("likely malicious, and it asks for something you can't undo") + action | "High risk, and the reason is the *ask* — a PIN can't be taken back." | AR-004, AR-006 |
| **0:30–0:45** | **Threat DNA:** highlighted words — urgency, authority, fear, credential request; entities | "Every tag is tied to the exact words. No fake percentages." | AR-005, AR-021 |
| **0:45–1:05** | **Replay:** hook → action point; tap **Reply** → the scammer's likely next message | "This is how this *kind* of attack typically unfolds — a simulation, nothing sent." | AR-007, AR-008, AR-022 |
| **1:05–1:15** | Recoverability strip; toggle **"sender verified"** → band drops (labelled *guidance*) | "Verify independently and the risk moves — as guidance, not magic." | AR-009 |
| **1:15–1:30** | Paste **DEMO-INC** ("I already sent the money"): pointer jumps to the cash-out stage; first-hour plan | "If it's already happened: what's still undoable, what to keep, what to report." | AR-010 |
| **1:30–1:50** | **Evasion Arena:** caught rate before/after patch; **false positives shown**; held-out mutation results | "We attack our own detector — and show the misses." | AR-011, AR-023–025 |
| **1:50–2:00** | Closing slide/banner | "Every step of the scam gets harder: you see it coming, and the detector has seen the tricks." | — |

**Timing tightness:** the proposal's own timeline places the incident beat at 1:10 and the Arena at 1:30; this script compresses earlier beats by ~10 s each to fit both. If rehearsal shows it is rushed, cut order (see §7): drop the toggle first, then shorten Arena.

## 3. Demo data (illustrative — to be finalized)

| ID | Purpose | Text (fictional) |
|---|---|---|
| **DEMO-01** | Primary: mobile-money credential scam | "URGENT: Your mobile wallet has been flagged. Confirm your PIN within 30 minutes or it will be suspended: hxxp://wallet-verify[.]example" |
| **DEMO-02** | Wrong-number reversal | "Sorry, I sent you money by mistake. Please send it back to this number, I'm in a hurry." |
| **DEMO-03** | Utility notice | "Your electricity account is overdue. Pay now to avoid disconnection: hxxp://pay-utility[.]example" |
| **DEMO-BEN** | Benign control (proves false-positive control) | A normal, non-urgent message with no ask for secrets/money/links (e.g., a lecture time change from a lecturer) |
| **DEMO-BEN-HARD** | Hard benign (contains urgency/money words but legitimate) | A genuine-sounding reminder with a deadline and no secret/payment/link ask |
| **DEMO-INC** | Incident Mode | "I already sent the money" (+ variants: "I clicked the link", "I gave them my OTP") |
| **DEMO-MUT** | Arena seed set | Curated seeds + mutations (homoglyph, zero-width, split link, Shona/English mix, paraphrase, AI-polished) |

Requirements: demo messages must produce **stable** results across runs (regression suite); no dependence on network or LLM.

## 4. Backup scenarios

| Scenario | Use when |
|---|---|
| **B1** Alternative scam (DEMO-02 wrong-number) | DEMO-01 misclassifies or replay glitches |
| **B2** DEMO-03 utility | Second alternative |
| **B3** Recorded backup video (AR-035) | UI/hosting/laptop failure |
| **B4** Static screenshots deck | Video also fails |
| **B5** Pre-saved Arena results view | Arena runner fails live |

## 5. Failure fallbacks

| Failure | Fallback |
|---|---|
| No internet | Fully offline build (templates only) — nothing in the demo path should require the network |
| LLM unavailable | Not in demo path; templates |
| API/server crash | Restart script; switch to local run; then B3 |
| Wrong verdict on stage | Move to B1; use it honestly: "this is why we show failures" (pivot to Arena) |
| Arena slow/failing | Show saved results (B5) |
| Projector/resolution problem | Pre-tested zoom level; mobile-friendly layout |
| Time overrun | Cut per §7 |

## 6. Questions judges may ask (and answers we must be able to defend)

| # | Question | Defensible answer (grounded in decisions) | Needs data? |
|---|---|---|---|
| 1 | "Isn't this just another scam classifier?" | The classifier is the doorway; the product is interpretation: Threat DNA, safe replay, trust gap, incident guidance, and a robustness proof. | — |
| 2 | "Is the replay AI-generated? Could it hallucinate?" | No — curated playbooks per threat type; an LLM (if used) only rephrases templates and never decides ([DEC-001/002](./12_DECISION_LOG.md)). | — |
| 3 | "Are you predicting what the scammer will do?" | No. It shows the typical progression of this kind of attack, and says so on screen ([DEC-010](./12_DECISION_LOG.md#dec-010)). | — |
| 4 | "How accurate is it?" | Report measured results on our held-out set with confusion matrix and per-class scores, including false positives and weaknesses. | **Yes** (Sprint 1/4 results) |
| 5 | "What about false positives?" | Measured and shown in the Arena; hard-benign examples included. | **Yes** |
| 6 | "Does it work if the wording changes / AI polishes it?" | Char-n-gram baseline + normalization + Arena with held-out mutation types; we show remaining misses. | **Yes** |
| 7 | "Shona support?" | Char n-grams + Shona/English mixed mutations in the Arena; measured on the slice available. Be candid about the coverage the dataset gave us. | **Yes** |
| 8 | "Why not just brand-block lists?" | Hidden-set items may use unseen names; we reason by context and ask type ([DEC-005](./12_DECISION_LOG.md#dec-005)). | — |
| 9 | "What does the risk score mean?" | likelihood × irreversibility of the ask; bands, transparent rule weights ([DEC-008](./12_DECISION_LOG.md#dec-008)). | — |
| 10 | "What do the toggles do — are they learned?" | No; transparent rule-based adjustments labelled 'guidance' ([DEC-009](./12_DECISION_LOG.md#dec-009)). | — |
| 11 | "Is it safe? Does it open the links?" | Never — strings only, defanged; nothing is fetched, sent or paid ([Security](./08_SECURITY_AND_SAFETY.md)). | — |
| 12 | "What about privacy?" | Stateless by default; message bodies not stored or logged; no third-party calls on the default path. | — |
| 13 | "Can it work without internet?" | Yes; templates-only path is the default. | — |
| 14 | "How is this Zimbabwe-specific?" | Playbooks for mobile money, banking, utilities, government, university, jobs, parcels, investment, SIM/account, wrong-number reversal; language mixing; local pattern focus. Do not claim prevalence statistics. | Local verification |
| 15 | "Can you guarantee recovery?" | No. We show what is typically undoable and what isn't; local procedures verified before display. | Local verification |
| 16 | "What's next?" | Tarpit, ScamSigma, Herd Immunity (named on the roadmap slide; be ready to explain concepts — definitions TODO, not in proposal). | **TODO** |
| 17 | "Which external models/data/libraries did you use?" | Answer from the inventory in the [Submission Plan](./10_SUBMISSION_PLAN.md). | Inventory |
| 18 | "How does it scale in an organisation?" | `/batch` CSV endpoint; Organisation mode (if built) with ATT&CK-style tags; otherwise roadmap. | Depends on AR-027 |

## 7. Cut order if features slip (mirrors proposal cut line)

1. Organisation mode, slider (already NICE-TO-HAVE) → not in demo.
2. Trust-gap toggle beat (keep the checklist).
3. Shorten Arena to a static before/after view.
4. Drop Incident Mode beat **only** if AR-010 is not stable at freeze.
5. **Never cut:** verdict, Threat DNA, replay with recoverability, trust-gap checklist, batch.

## 8. Rehearsal plan

- [ ] Full run-through ≤ 2:00 with a timer (twice minimum)
- [ ] Offline run-through
- [ ] Each fallback rehearsed once
- [ ] Recorded backup video reviewed by someone not on the build
- [ ] Judge-question drill using §6 (assign presenter/answerer)
- [ ] Demo machine checklist: charger, display adapter, browser profile, zoom, notifications off, offline mode tested

## 9. Related

[Product Spec](./01_PRODUCT_SPECIFICATION.md) · [Sprint 5](./sprints/SPRINT_05_FINAL_HARDENING.md) · [Submission Plan](./10_SUBMISSION_PLAN.md)
