# 00 — Project North Star

> The single source of truth for Attack Replay's identity. If any other document contradicts this one, this one wins (after the official hackathon requirements — see the [authority hierarchy](../PROJECT_PLAN.md#source-of-truth-hierarchy)).

**Status:** 🔵 PLANNED (documentation complete; no implementation started)
**Last reviewed:** 2026-09-29

---

## 1. Identity

| Item | Value |
|---|---|
| **Project** | ATTACK REPLAY |
| **Hackathon** | National Cybersecurity Innovation Hackathon 2026 |
| **Organisers / context** | NUST; Ministry of Information Communication Technologies, Postal and Courier Services (Zimbabwe) |
| **Theme** | "Don't Make It Easy for Them: Building a Cyber Strong Zimbabwe" |
| **Challenge** | "Cyber Shield Zimbabwe: Detecting and Responding to Cyber Threats" |
| **Product philosophy** | **DETECT → EXPLAIN → REPLAY → INTERRUPT → RECOVER** |

## 2. One-line pitch

> **We don't just tell you it's a scam. We let you watch it play out, safely, and show you what you can still undo.**

## 3. The problem

- A bare verdict such as "High risk, 0.93" does not change what a citizen does. **Seeing the consequence does.**
- Text-only detectors go stale as scammers polish their wording with AI.
- **Working assumption (PROPOSED, not evidenced in this repository):** people often act before they understand what a message is trying to get from them, and once harmed may not know what is still recoverable. The product design assumes this; it should not be quoted as a statistic.

## 4. Product thesis

Attack Replay has **two halves**:

1. **An interpreter** that makes the threat visible and actionable — it explains the tactics, safely replays the *typical* progression of this kind of attack, and shows what can still be undone.
2. **A proof of robustness** (the Evasion Arena) that shows the detector holds up against rewritten attacks — homoglyphs, zero-width characters, split links, Shona/English mixing, paraphrase, AI-polished tone.

This answers the theme directly: **every step of the scam gets harder** because the victim sees it coming and the detector has already seen the tricks.

## 5. Core user

| User | Role in product | Priority |
|---|---|---|
| **Citizen** — receives a suspicious message, or has already acted on one | Primary user; Citizen mode is the default experience | MUST |
| **Organisation / SOC analyst** — triages reports, needs indicators and containment steps | Secondary; Organisation mode | NICE-TO-HAVE |
| **Hackathon judges / hidden evaluation set** | Consume `/batch` output and the demo | MUST |

## 6. Core experience

```
INPUT → VERDICT → THREAT DNA → REPLAY → DECISION → CONSEQUENCE → RECOVERY
```

The user pastes a message (or an incident narrative such as "I already sent the money"). They see a verdict, the tactics used against them (tied to the exact words), then a staged replay of how this kind of attack typically unfolds. At the **action point** they choose Click / Reply / Ignore / Report and see the consequence, with a **"still recoverable?"** strip at every stage. A **Trust Gap** view tells them how to verify independently.

> **The central idea (must survive every future change):** Attack Replay does not merely tell someone that a message is suspicious. It helps them understand the attack and safely experience its likely progression *before* showing them how they can interrupt or recover from it.

## 7. Product principles

| # | Principle | Practical meaning |
|---|---|---|
| P1 | **Show, don't just score** | The replay and Threat DNA are the product; the verdict is the doorway. |
| P2 | **Evidence-grounded** | Every tactic tag and explanation is tied to exact words or extracted entities. No unsupported claims. |
| P3 | **Honest about uncertainty** | No fake percentages, no fake confidence. Toggles are labelled "guidance". |
| P4 | **Curated, not generative, replay** | Playbooks are hand-written per threat type so the replay cannot hallucinate. |
| P5 | **LLM never decides** | An LLM may only rephrase grounded templates; the verdict comes from the classifier + rules. |
| P6 | **Works offline** | Everything must function with templates alone (no LLM, no internet). |
| P7 | **Context over brands** | Zimbabwe relevance comes from patterns (mobile money, utilities, parcels…), not brand blacklists. |
| P8 | **Safe by construction** | Never fetch/execute submitted URLs; never send messages; never present simulation as real action. |
| P9 | **Show weaknesses** | Report false positives and held-out results; record failure cases. |
| P10 | **Core before extras** | Classifier, DNA, replay, trust gap, batch come first; Arena/Incident must never destabilise them. |

## 8. Core differentiator

| Typical scam detector | Attack Replay |
|---|---|
| Outputs a label/score | Outputs a label **and** shows the attack's progression and consequences |
| Tells you *that* it is dangerous | Shows you *what the attack is trying to do* and *what you can still undo* |
| Brittle to rewording | Ships an Evasion Arena that measures robustness incl. held-out mutation types |
| Silent after you've been hit | Incident Mode: first-hour plan, evidence to preserve, drafted report text |

## 9. Definition of success

Success is defined qualitatively and by verifiable deliverables. **Numerical targets are an OPEN DECISION** (see [OD-017](./12_DECISION_LOG.md#open-decisions)) and will be proposed only after the baseline exists; they must be labelled as *proposed goals*, never as results.

- [ ] Meets the five minimum features (suspicious/benign, threat type, risk, one-line reason, recommended action) on the hidden set via `/batch`.
- [ ] The two-minute demo lands the "watch it play out" story without depending on live internet/LLM.
- [ ] Evaluation is honest: leakage-free splits, false positives reported, held-out mutation results reported, failures recorded.
- [ ] Replay and toggles are labelled honestly (curated progression; guidance).
- [ ] All competition deliverables submitted (prototype, technical summary, presentation, source code) — see [Submission Plan](./10_SUBMISSION_PLAN.md).
- [ ] A fresh developer can understand and continue the project from the docs alone.

## 10. What Attack Replay IS / IS NOT

| Attack Replay **is** | Attack Replay **is not** |
|---|---|
| A citizen-facing scam interpreter and safe replay | A generic cybersecurity platform |
| A classifier + risk engine + Threat DNA + curated replay + trust gap | "Just an AI scam detector" |
| An educational, simulated walkthrough of the *typical* progression of an attack type | A prediction of what one specific criminal will do |
| Evidence-grounded and template-first | An LLM chatbot that improvises explanations or verdicts |
| Context/pattern based (Zimbabwe-relevant scenarios) | A brand blacklist |
| Honest about what it can and cannot conclude | A system that claims certainty or guarantees recovery |
| Stateless-by-default and safe | A tool that visits links, sends messages, or performs transactions |
| Text-in (message/narrative) | A screenshot/OCR tool (**no screenshot upload** — [DEC-011](./12_DECISION_LOG.md#dec-011)) |

## 11. Related documents

[Product Specification](./01_PRODUCT_SPECIFICATION.md) · [Hackathon Requirements](./02_HACKATHON_REQUIREMENTS.md) · [Architecture](./03_PRODUCT_ARCHITECTURE.md) · [Decision Log](./12_DECISION_LOG.md) · [Project Plan](../PROJECT_PLAN.md)
