# 07 — Attack Replay Playbooks

> The playbook library powers the replay. Playbooks are **hand-curated** so the replay cannot hallucinate ([DEC-001](./12_DECISION_LOG.md#dec-001)).

**Status:** 🔵 PLANNED · Backlog: AR-007, AR-008 (Sprint 3) · Content drafting by the playbook/demo owner may start earlier; it needs no code.

## 1. Two things that must never be confused

| **CURATED ATTACK PROGRESSION** (what we show) | **PREDICTION OF AN INDIVIDUAL ATTACKER** (what we do **not** claim) |
|---|---|
| The typical way this *kind* of attack unfolds, written by us from general scam patterns | A forecast of what the specific sender of this message will do |
| Labelled "typical progression — simulation" | Never implied by wording, UI or narration |
| Stable and reviewable | — |

The scenarios below are **proposed demonstration/playbook contexts**. We do **not** claim they are statistically the most common in Zimbabwe unless evidence is later supplied (TO BE VERIFIED).

## 2. Playbook architecture

```mermaid
stateDiagram-v2
    [*] --> Hook
    Hook --> ActionPoint
    ActionPoint --> Click: user taps Click
    ActionPoint --> Reply: user taps Reply
    ActionPoint --> Ignore: user taps Ignore
    ActionPoint --> Report: user taps Report
    Click --> Extraction
    Reply --> Pressure
    Pressure --> Extraction
    Extraction --> Takeover
    Ignore --> Stopped
    Report --> Stopped
    Takeover --> [*]
    Stopped --> [*]
```

### 2.1 Playbook schema (conceptual; file format OPEN — [OD-001](./12_DECISION_LOG.md#open-decisions))

| Field | Description |
|---|---|
| `id`, `version` | Stable identifier |
| `threat_types[]` | Taxonomy types it serves (after AR-003) |
| `scenario_context` | Sector/context (e.g., mobile money) — pattern-based |
| `hook` | Template using extracted entities (sector, ask, amount, channel) |
| `tactics[]` | Expected Threat DNA tactics |
| `action_point` | Prompt + available choices |
| `stages[]` | Ordered stages: id, label, description, `typical_next_message?`, `entities_used[]` |
| `choices{}` | Choice → next stage / outcome |
| `consequences{}` | Per stage/choice: what happens (simulated) |
| `recoverability{}` | Per stage: level + what can/can't be undone + `verified` flag |
| `interruption` | What stops the attack at each stage |
| `recovery_steps[]` | Ordered steps; local specifics flagged TO BE VERIFIED |
| `incident_map` | Which stage each harm-already-happened case jumps to |
| `disclaimers[]` | Mandatory labels |
| `review` | Author, reviewer, date, verified-facts status |

### 2.2 Recoverability vocabulary (PROPOSED)

| Level | Meaning |
|---|---|
| ✅ **Undoable** | Nothing lost yet; the user can still stop the attack |
| ⏱ **Time-critical** | Harm can still be limited if the user acts now (window unknown → never state a number unless verified) |
| ◐ **Partly recoverable** | Some things can be restored (e.g., account access), some cannot (e.g., disclosed data) |
| ✖ **Likely irreversible** | Typically cannot be undone (e.g., cash already withdrawn) — still lists steps that limit further harm |

### 2.3 Rules

1. Playbooks contain **no live URLs, real phone numbers, real brand names or working phishing content**; fake pages are illustrated mock-ups.
2. Local claims (provider procedures, reversal windows, police/regulator channels, hotline numbers) are marked **TO BE VERIFIED** until confirmed by a reliable source; the UI must not display unverified local specifics as fact.
3. Every playbook ends with **interruption** and **recovery** content.
4. A **generic fallback playbook** exists for taxonomy classes without a dedicated playbook.
5. Playbook selection uses threat type + sector/ask entities, not brand names ([DEC-005](./12_DECISION_LOG.md#dec-005)).
6. Each playbook is reviewed by someone other than its author before Sprint 3 exit.

### 2.4 Common recovery skeleton (reused; local details TO BE VERIFIED)

1. Stop interacting with the sender. 2. Do not use links/numbers in the message. 3. Contact the real provider through an independently sourced channel. 4. Secure accounts (change credentials from a clean path; end other sessions). 5. Preserve evidence (message, sender, time, references) — do not delete. 6. Report (provider; police/other channel — TO BE VERIFIED). 7. Warn people who may have received the same message.

---

## 3. Playbooks (all 🔵 PLANNED)

> Field abbreviations: **Ask** = what the message wants; **Rec.** = recoverability level (§2.2).

### PB-01 — Mobile money
| Field | Content |
|---|---|
| Threat type | Financial scam / phishing (mapping after AR-003) |
| Initial hook | "Your wallet has a problem / a transaction needs confirming" — a message from a supposed mobile-money service |
| Tactics | Urgency, authority impersonation, fear/loss, credential request (PIN/OTP), call to action |
| Action point | Click the link or reply/call with PIN/OTP |
| Typical progression | Hook → user follows link or replies → fake page/agent asks for PIN/OTP → attacker uses code to access/drain wallet → attempts to move funds onward |
| User choices | Click · Reply · Ignore · Report |
| Consequences | Click → credential-capture page (illustrated). Reply → "verification agent" asks for PIN/OTP, pressure if hesitant. Ignore/Report → attack stops |
| Recoverability | Before sharing PIN/OTP: ✅ Undoable. After sharing: ⏱ Time-critical. After funds cashed out: ✖ Likely irreversible (verify local process) |
| Interruption | Never share PIN/OTP; verify via provider's official app/number opened independently |
| Recovery steps | Common skeleton + immediately contact provider; change PIN; provider-specific dispute steps TO BE VERIFIED |
| Verification status | Local procedures TO BE VERIFIED |

### PB-02 — Banking
| Field | Content |
|---|---|
| Threat type | Phishing / identity fraud |
| Initial hook | "Suspicious activity / account locked / card expired — verify now" |
| Tactics | Authority impersonation, fear/loss, urgency, credential request, suspicious link |
| Action point | Click link to "verify" or reply with login details |
| Typical progression | Hook → fake login page → credentials (and one-time codes) captured → attacker logs in / initiates transfers |
| Consequences | Click → fake banking login (illustrated). Reply → request for details/OTP. |
| Recoverability | Before entering details ✅; after entering credentials/OTP ⏱; after transfers ◐/✖ (bank-dependent, TO BE VERIFIED) |
| Interruption | Open the bank's app/website yourself; call the number on your card |
| Recovery steps | Common skeleton + contact bank via card-number, freeze/lock channels, change credentials |
| Verification status | Bank procedures TO BE VERIFIED |

### PB-03 — Utility
| Field | Content |
|---|---|
| Threat type | Financial scam / phishing |
| Initial hook | "Your electricity/water account is overdue — pay to avoid disconnection" |
| Tactics | Urgency, fear/loss (disconnection), authority impersonation, payment request |
| Action point | Pay via supplied number/link or click |
| Typical progression | Hook → payment instructions to non-official destination → payment sent → follow-up demands / reuse of victim data |
| Recoverability | Before paying ✅; after paying ⏱/✖ depending on payment route (TO BE VERIFIED) |
| Interruption | Check balance/status with the utility through its official channel |
| Recovery steps | Skeleton + payment provider dispute + report |
| Verification status | Utility procedures TO BE VERIFIED |

### PB-04 — Government
| Field | Content |
|---|---|
| Threat type | Financial scam / identity fraud |
| Initial hook | "Tax/licence/fine/registration notice — action required" |
| Tactics | Authority impersonation, fear/loss (penalty/arrest), urgency, payment/credential request |
| Action point | Click to view notice / pay penalty / send documents |
| Typical progression | Hook → fake portal collects ID details and/or payment → data reused for further fraud |
| Recoverability | Before submitting ✅; after ID data disclosed ◐ (data cannot be "unshared"); after payment ⏱/✖ |
| Interruption | Contact the agency via independently sourced official channel |
| Recovery steps | Skeleton + watch for identity misuse; reporting channels TO BE VERIFIED |

### PB-05 — University
| Field | Content |
|---|---|
| Threat type | Phishing / identity fraud |
| Initial hook | "Student account expiring / fees / results / scholarship — sign in to confirm" |
| Tactics | Authority impersonation, urgency, reward/lure (scholarship), credential request |
| Action point | Click sign-in link |
| Typical progression | Hook → fake university login → credentials captured → mailbox/account takeover → phishing sent to contacts |
| Recoverability | Before sign-in ✅; after credentials ⏱ (reset immediately); after contacts phished ◐ |
| Interruption | Go to the university's portal via saved bookmark; contact IT help desk independently |
| Recovery steps | Skeleton + password reset + notify IT/contacts |

### PB-06 — Job scam
| Field | Content |
|---|---|
| Threat type | Financial scam / identity fraud |
| Initial hook | "You're shortlisted / job offer — pay registration/training fee or send ID" |
| Tactics | Reward/lure, urgency, secrecy, payment request, credential/ID request |
| Action point | Reply with documents or pay a fee |
| Typical progression | Hook → documents requested → fee requested → further fees / disappearance; ID data reused |
| Recoverability | Before paying/sending ✅; after fee ✖ likely; after ID sent ◐ |
| Interruption | Verify the employer and vacancy independently; legitimate employers do not demand upfront fees (state as guidance, not law) |
| Recovery steps | Skeleton + monitor ID misuse; report |

### PB-07 — Parcel / delivery
| Field | Content |
|---|---|
| Threat type | Malicious link / phishing / financial scam |
| Initial hook | "Parcel held — pay small release/delivery fee or reschedule via link" |
| Tactics | Urgency, call to action, payment request, suspicious link |
| Action point | Click link |
| Typical progression | Hook → fake tracking page → small fee + card/mobile-money details captured → later larger charges |
| Recoverability | Before paying ✅; after details entered ⏱ (block card/wallet) ; after charges ◐/✖ |
| Interruption | Use the courier's official channel with your tracking number from the original source |
| Recovery steps | Skeleton + block/replace card or wallet credentials |

### PB-08 — Investment
| Field | Content |
|---|---|
| Threat type | Financial scam |
| Initial hook | "Guaranteed returns / double your money / exclusive opportunity" |
| Tactics | Reward/lure, urgency, secrecy/exclusivity, payment request |
| Action point | Reply or deposit an initial amount |
| Typical progression | Hook → small "profit" shown to build trust → larger deposit requested → withdrawal blocked with new fees → loss |
| Recoverability | Before depositing ✅; after deposits ✖ likely; stopping further deposits ⏱ |
| Interruption | No guaranteed returns are legitimate; verify registration with the relevant regulator (channel TO BE VERIFIED) |
| Recovery steps | Skeleton + stop further payments + report |

### PB-09 — SIM / account
| Field | Content |
|---|---|
| Threat type | Identity fraud / phishing |
| Initial hook | "SIM/account will be deactivated / re-register / verify your number" |
| Tactics | Authority impersonation, fear/loss, urgency, credential/ID request |
| Action point | Reply with ID details or codes / click link |
| Typical progression | Hook → personal details or OTP obtained → attacker attempts SIM-swap or account takeover → access to wallets/accounts tied to the number |
| Recoverability | Before details ✅; after codes/ID ⏱; after takeover ◐ (operator-dependent, TO BE VERIFIED) |
| Interruption | Contact the operator via official channel; never share codes |
| Recovery steps | Skeleton + operator contact + secure linked accounts |

### PB-10 — Wrong-number reversal scam
| Field | Content |
|---|---|
| Threat type | Financial scam |
| Initial hook | "Sorry, I sent money to your number by mistake — please send it back" (often accompanied by a fake transaction notice) |
| Tactics | Fear/guilt-lure, urgency, payment request, social pressure |
| Action point | Reply or send money "back" |
| Typical progression | Hook → fake credit notice or real-looking message → victim "refunds" → real loss; possible follow-up pressure |
| Recoverability | Before sending ✅; after sending ⏱/✖ (provider-dependent, TO BE VERIFIED) |
| Interruption | Check your actual balance/statement through the official app/channel; do not rely on the message; ask the sender to use the provider's official reversal process |
| Recovery steps | Skeleton + provider dispute + report |

---

## 4. Mapping to taxonomy

Mapping from **dataset threat types** to playbooks is finalized in AR-003/AR-008 after dataset inspection. Until then this document's "Threat type" column is **PROPOSED**. A generic fallback playbook covers any unmapped type.

## 5. Playbook QA checklist

- [ ] Uses only entities from the message + curated text; no invented specifics
- [ ] Every stage has recoverability with `verified` flag
- [ ] Interruption and recovery present
- [ ] No real brands/numbers/links
- [ ] Labelled as simulation / typical progression
- [ ] Reviewed by a second person
- [ ] Incident map covers clicked / replied / submitted credentials / transferred money where applicable
