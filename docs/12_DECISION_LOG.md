# 12 — Decision Log

> Records product and technical decisions. **Only decisions actually established by the proposal or the project brief are listed as decided.** Everything else is an **OPEN DECISION**. Do not silently change product direction — record discrepancies here.

**Status:** 🔵 PLANNED (log established; implementation decisions to be added)

## 1. Format (copy for new decisions)

```markdown
### DEC-NNN — Title
- **Date:** YYYY-MM-DD
- **Decision:** one sentence
- **Context:** why it came up
- **Options considered:** A / B / C
- **Decision made:** the chosen option
- **Reason:** why
- **Consequences:** what this enables / constrains / must be updated
- **Status:** 🟢 DECIDED | 🔵 OPEN | ⚪ SUPERSEDED by DEC-NNN
- **Source:** proposal | brief | planning | implementation
```

Rules: numbering is sequential and never reused; supersede rather than edit history; if implementation conflicts with the proposal, log it here **first**.

## 2. Decisions established by the proposal / brief

<a id="dec-001"></a>
### DEC-001 — Replay is curated, not generative
- **Date:** 2026-09-29 (recorded; established by proposal)
- **Decision:** The replay comes from a hand-curated playbook library per threat type.
- **Context:** Generative replay could hallucinate consequences or recovery claims.
- **Options considered:** Curated playbooks / LLM-generated replay / hybrid
- **Decision made:** Curated playbooks.
- **Reason:** Prevents hallucination; reviewable; works offline.
- **Consequences:** Playbook content is a first-class deliverable (AR-008); coverage limited to authored scenarios; generic fallback playbook needed.
- **Status:** 🟢 DECIDED · **Source:** proposal

<a id="dec-002"></a>
### DEC-002 — The LLM never determines the verdict
- **Date:** 2026-09-29 (recorded)
- **Decision:** Classifier + rules set label/type/risk; an LLM may only rephrase grounded templates at the chosen reading level.
- **Options considered:** LLM-as-classifier / LLM explanation only / no LLM
- **Decision made:** LLM optional, rephrase-only.
- **Reason:** Determinism, groundedness, offline reliability, safety.
- **Consequences:** Templates are the baseline; LLM output must be validated against source template; LLM use is COULD (AR-028).
- **Status:** 🟢 DECIDED · **Source:** proposal

<a id="dec-003"></a>
### DEC-003 — Explainability is evidence-grounded
- **Date:** 2026-09-29 (recorded)
- **Decision:** Tactic tags are strong/present/absent tied to exact words; no fake percentages; explanations key on indicators.
- **Reason:** Trust; auditability; judges can see why.
- **Consequences:** Detectors must return spans; offsets map to original text; groundedness audit in evaluation.
- **Status:** 🟢 DECIDED · **Source:** proposal

<a id="dec-004"></a>
### DEC-004 — Character n-gram TF-IDF + calibrated logistic regression first
- **Date:** 2026-09-29 (recorded)
- **Decision:** Start with char n-gram (plus word) TF-IDF + calibrated logistic regression; embeddings are an optional enhancement.
- **Options considered:** Char n-gram baseline / multilingual sentence embeddings / fine-tuned transformer
- **Decision made:** Char n-gram baseline first (proposal allows "multilingual sentence embeddings or char n-gram TF-IDF"; the planning brief prefers char n-gram initially).
- **Reason:** Robust to obfuscation and code-mixing; fast; offline; simple to calibrate.
- **Consequences:** Embeddings only if baseline weaknesses justify (AR-029).
- **Status:** 🟢 DECIDED (as initial approach) · **Source:** proposal + planning brief

<a id="dec-005"></a>
### DEC-005 — Zimbabwe context is pattern-based, not brand-blacklist based
- **Date:** 2026-09-29 (recorded)
- **Decision:** Reason by context (mobile money, banking, utilities, government, university, jobs, parcels, promotions, investment, SIM/account) rather than brand lists.
- **Reason:** Hidden-set items may use names not seen.
- **Consequences:** Sector/ask lexicons instead of brand lists; playbooks contain no real brands.
- **Status:** 🟢 DECIDED · **Source:** proposal

<a id="dec-006"></a>
### DEC-006 — Evasion Arena is secondary to the core product
- **Decision:** SHOULD-have; must not destabilise the core (Sprint 4 gate). **Status:** 🟢 DECIDED · **Source:** proposal (cut line)

<a id="dec-007"></a>
### DEC-007 — Incident Mode is secondary to the core product
- **Decision:** SHOULD-have; built after replay and trust gap are stable. **Status:** 🟢 DECIDED · **Source:** proposal (cut line)

<a id="dec-008"></a>
### DEC-008 — Risk = likelihood × irreversibility of the ask
- **Decision:** Risk fusion multiplies calibrated likelihood by an ask-based irreversibility weight (OTP/PIN, money, app install highest; click medium; reply lower). If the dataset has risk labels, fit weights and thresholds to them.
- **Consequences:** Explanation names both factors; weights are transparent config; if no risk labels, bands are rule-based and labelled as such (no accuracy claim).
- **Status:** 🟢 DECIDED (approach) · thresholds OPEN · **Source:** proposal

<a id="dec-009"></a>
### DEC-009 — What-if toggles are transparent rule-based guidance
- **Decision:** Trust Gap toggles adjust the band by documented rules and are labelled "guidance", not learned effects. **Status:** 🟢 DECIDED · **Source:** proposal

<a id="dec-010"></a>
### DEC-010 — Replay shows a typical progression, not a prediction
- **Decision:** The replay is labelled as the typical progression of this attack type, not a prediction of a specific criminal. **Status:** 🟢 DECIDED · **Source:** proposal

<a id="dec-011"></a>
### DEC-011 — No screenshot upload
- **Decision:** Input is text (message or narrative). **Status:** 🟢 DECIDED · **Source:** proposal

<a id="dec-012"></a>
### DEC-012 — Cut line and priority tiers
- **Decision:** MUST: classifier, DNA, replay, trust gap, batch endpoint. SHOULD: Arena, incident mode. NICE-TO-HAVE: Organisation mode, reading-level slider. FUTURE ("what's next" slide): Tarpit, ScamSigma, Herd Immunity. Backlog mapping: MUST/SHOULD/COULD/LATER. **Status:** 🟢 DECIDED · **Source:** proposal

<a id="dec-013"></a>
### DEC-013 — Two interfaces: `/analyze` and `/batch`
- **Decision:** `/analyze` for the UI; `/batch` (CSV in → CSV out: label, type, risk, explanation, action) for the hidden evaluation set. **Status:** 🟢 DECIDED · **Source:** proposal

<a id="dec-014"></a>
### DEC-014 — Everything works with templates alone
- **Decision:** No feature on the core/demo path may require an LLM or the internet. **Status:** 🟢 DECIDED · **Source:** proposal (risk section)

<a id="dec-015"></a>
### DEC-015 — Documentation authority hierarchy
- **Decision:** 1) Official hackathon requirements 2) Attack Replay proposal 3) planning documents 4) DECISION LOG 5) implementation details. Conflicts are documented, not silently resolved. **Status:** 🟢 DECIDED · **Source:** planning brief

<a id="dec-016"></a>
### DEC-016 — Status and label conventions
- **Decision:** 🔵 PLANNED · 🟡 IN PROGRESS · 🟢 COMPLETE · 🔴 BLOCKED · ⚪ DEFERRED; labels KNOWN / PROPOSED / TO BE VERIFIED / OPEN DECISION; never invent dataset statistics, model accuracy, prevalence or performance numbers. **Status:** 🟢 DECIDED · **Source:** planning brief

<a id="dec-017"></a>
### DEC-017 — Demo timeline reconciliation
- **Date:** 2026-09-29
- **Decision:** The planning brief's suggested two-minute structure and the proposal's demo timeline are merged in [Demo Strategy](./09_DEMO_STRATEGY.md) (proposal beats: reply, toggle, incident, Arena all retained; timings compressed).
- **Context:** The two orderings differ slightly (brief: incident *or* Arena at 1:30; proposal: incident at 1:10 and Arena at 1:30).
- **Options considered:** Follow brief exactly (drop one beat) / follow proposal exactly / merge with compressed timings
- **Decision made:** Merge; confirm in rehearsal; cut order defined.
- **Consequences:** Timing may need trimming; Incident and Arena remain SHOULD-haves.
- **Status:** 🟢 DECIDED (planning); timings to be confirmed after rehearsal · **Source:** planning

## 2b. Decisions made during implementation (Sprint 0/1 execution)

<a id="dec-018"></a>
### DEC-018 — Technology stack and taxonomy freeze (closes OD-001, OD-002)
- **Date:** 2026-09-30
- **Decision:** Python 3.12 · scikit-learn (TF-IDF + logistic regression, sigmoid calibration) · FastAPI/uvicorn · static HTML front end served by the API. Playbooks/lexicons stay in code/JSON. Taxonomy frozen to the **six dataset labels**: Phishing, Financial Scam, Identity Fraud, Malicious Link, AI-Enabled Threat, Benign (dataset labels win — Data & ML §8).
- **Reason:** Offline, deterministic, reproducible from a clean checkout; no model download risk (R-013).
- **Consequences:** "Malicious Link" also covers attachments (the released data labels an attachment lure as Malicious Link). Playbook mapping for all five threat types is Sprint 3 work.
- **Status:** 🟢 DECIDED

<a id="dec-019"></a>
### DEC-019 — Dataset reality: 12 unique messages; developer-authored supplement; frozen split
- **Date:** 2026-09-30
- **Context (KNOWN, measured):** The released CSV has 100 rows but **12 unique messages, exactly 2 per class**, no label conflicts, no missing values. Fields: channel, source, threat_label, risk_level, recommended_action. No language field; no Shona text observed. A group-aware split of 12 messages cannot produce a meaningful held-out set.
- **Decision:** (1) All 12 unique released messages go to TRAIN. (2) A **developer-authored supplement** (`data/supplement/dev_supplement.csv`, `source=developer-authored`) provides extra train examples and a **frozen final test of 30** (5 per class, incl. hard benign). (3) Final-test SHA-256 is stored in `data/splits/split_v1.json`; code refuses to run if it changes. (4) Final test scored **once** (`reports/final_test_result.json`; script refuses to re-run without `--force`).
- **Consequences:** Held-out metrics measure generalisation to *our own* wording, not the organisers' hidden set, and are reported as such. Supplement text contains no real brands/numbers/links. Shona is **not covered** (needs a Shona-speaking reviewer — R-005).
- **Status:** 🟢 DECIDED

<a id="dec-020"></a>
### DEC-020 — Risk engine rules (implements DEC-008)
- **Date:** 2026-09-30
- **Decision:** `score = P(suspicious) × irreversibility / 3`; **High ≥ 0.70, Medium ≥ 0.25**; Benign → Low; a suspicious message is never Low. Irreversibility: 3 = PIN/OTP, ID/identity details, money, software install, credential-capture (sign-in/verify via link); 2 = password/account details, attachment, link click; 1 = reply. (OTP/PIN/money/install ≥ click ≥ reply is KNOWN from the proposal; the rest is **PROPOSED**.)
- **Reason:** Transparent and monotone. Not fit to risk labels: only 12 unique labelled points, so **no risk-accuracy claim is made**. The rules reproduce all 12 released risk labels (in-sample; rules were written with those labels in view).
- **Status:** 🟡 PROPOSED — revisit when the hidden-set format/flyer is known

<a id="dec-021"></a>
### DEC-021 — Benign hard-negatives added after validation false positives
- **Date:** 2026-09-30
- **Context (measured on validation only):** first CV showed **4/10 Benign flagged Suspicious**, all with no ask/link/attachment.
- **Decision:** Added 12 diverse benign (incl. hard) messages to the **train** supplement; cue tokens (extracted asks, URL, evasion flag) are appended to the model input; asks require a request verb and are negated by "do not / never". Final test untouched (hash unchanged).
- **Consequences:** Validation Benign FPR 0/22 afterwards. Because the fix was chosen after seeing validation errors, validation numbers are slightly optimistic; the final test is the cleaner number.
- **Status:** 🟢 DECIDED

<a id="dec-022"></a>
### DEC-022 — API and /batch contract (provisional; OD-010 still open)
- **Date:** 2026-09-30
- **Decision:** `/batch` returns exactly `label,type,risk,explanation,action` (optional `?include_input=true` appends the source row). `label` ∈ {Suspicious, Benign, Unknown}; `type` uses the six dataset labels; empty/oversized/unreadable rows → `Unknown` (row count always preserved). Accepts multipart `file` or raw `text/csv`; content column named content/text/message/body/sms/narrative, or a single headerless column. Limits: 5,000 chars/message, 5 MB, 20,000 rows (closes OD-018 provisionally). Cells starting `= + - @` are prefixed with `'`.
- **Status:** 🟡 PROPOSED — must be checked against the official hidden-set format (OD-010)

<a id="dec-023"></a>
### DEC-023 — Pivot: IDS-style Guardian agent (supersedes "paste a message" as the primary interface)
- **Date:** 2026-10-01 · **Decision:** A local background agent reads incoming mail/messages automatically and alerts only on suspicious ones; the paste-and-check UI remains optional. Sources: IMAP (read-only), watched folder, authenticated `/ingest` webhook. Packaged by `install.py` (venv, model training, auto-start, shortcut).
- **Reason / limits:** A workstation cannot read phone SMS/WhatsApp; the webhook covers SMS-forwarder apps. Polling not IDLE. OAuth (Outlook/M365) not supported. Status: 🟡 IN PROGRESS (not verified on real Windows/IMAP).

<a id="dec-024"></a>
### DEC-024 — Incident narratives and technical evidence override text-only verdicts
- A first-person "already happened" statement forces Suspicious and sets the replay pointer; email technical signals (link/text mismatch, auth failure, executable attachments) can raise a Benign text verdict to Suspicious when one severity-3 or two severity-2 signals exist. Rule-based; no percentages.

<a id="dec-025"></a>
### DEC-025 — Trust Gap rules (closes OD-019)
- Confirmations lower the band at most one step in total; a suspicious message never falls below Medium; the irreversible-ask warning is never hidden. Labelled as guidance.

<a id="dec-026"></a>
### DEC-026 — Reporting model
- Always write a local outbox report; send to webhook/SMTP only if the user configured them; default mode "ask" (one click per report), "auto" only for High risk; redacted excerpt; original attached only if enabled. No provider addresses invented.

<a id="dec-027"></a>
### DEC-027 — Storage and security baseline
- Store only flagged messages; benign leave counters only. Localhost bind, Host-header check, session token for state-changing calls, bearer token for `/ingest`, secrets in OS keyring (file fallback, user-only). Open risk: evidence folder is unencrypted.


<a id="dec-028"></a>
### DEC-028 — Threat-likelihood percentage on every alert (refines DEC-003)
- **Date:** 2026-10-01
- **Decision:** Every analysis and every stored alert carries `threat_score.percent` (0–100) with the factors behind it (`ar/score.py`). It is a transparent noisy-OR blend of: the classifier's P(suspicious) (weight 0.80), each Threat-DNA tactic found (strong/present), each technical email signal (by severity) and a described incident. It is clamped so it never contradicts the verdict (Suspicious ≥ 50 %, Benign ≤ 49 %). The UI shows the number together with a "Why this score" breakdown.
- **Reason:** A single number lets people triage many alerts quickly, and the breakdown keeps it explainable. DEC-003 forbade *fake* percentages; this one is labelled an evidence-based triage aid and **not** a calibrated probability.
- **Consequences:** Weights are hand-set and not fit to held-out data (same status as DEC-020). Risk band (likelihood × irreversibility) is unchanged and is shown separately. No accuracy claim is made for the percentage. On the 60 non-final-test supplement rows: all 40 threat rows scored ≥ 50 %, 0 of 20 benign rows did (this is in-sample; the frozen final test was not used).
- **Status:** 🟡 PROPOSED — revisit once a larger labelled set exists.

## 3. Open decisions

<a id="open-decisions"></a>

| ID | OPEN DECISION | Needed by | Owner | Notes |
|---|---|---|---|---|
| **OD-001** | Technology stack: language, backend/frontend frameworks, ML library, file formats for playbooks/lexicons, repository layout, hosting | Sprint 0 exit | ML-API | Decide after AR-000/AR-001; must satisfy offline + deterministic constraints | **closed by DEC-018** |
| **OD-002** | Final threat taxonomy and mapping to dataset labels; fallback if dataset lacks threat types | Sprint 0 exit (AR-003) | ML-API | Dataset labels win for classification | **closed by DEC-018** |
| **OD-003** | Whether embeddings/transformer are used beyond baseline | After Sprint 1 metrics | ML-API | Only if justified (AR-029) |
| **OD-004** | Whether dataset has sender, channel, risk-label, language fields | Sprint 0 (AR-001) | ML-API | Determines optional inputs and risk fitting |
| **OD-005** | Calendar timeboxes per sprint; absolute dates | Sprint 0 (AR-012) | ALL | Flyer dates TO BE VERIFIED |
| **OD-006** | Use of an LLM at all (provider, privacy, rules) | Before AR-028 | ALL | Default: none |
| **OD-007** | Deployment target / demo hosting | Before Sprint 4 | ML-API | R-018 |
| **OD-008** | Team members and role ownership | Sprint 0 | ALL | Roles: ML-API, FE-REPLAY, PLAYBOOK-DEMO |
| **OD-009** | Arena mutation generation method and the held-out mutation split; patch loop design | Sprint 4 start | ML-API | Held-out types must not be used to patch |
| **OD-010** | `/batch` input schema of the hidden set | Sprint 0 (AR-012) | ML-API | TO BE VERIFIED |
| **OD-011** | UI language (English only vs some Shona strings) | Sprint 2 | FE-REPLAY | R-005 |
| **OD-012** | Repository location/name; whether one exists | Sprint 0 (AR-000) | ML-API | None found in this authoring workspace |
| **OD-013** | Licence for the project's own source code | Sprint 5 | ALL | Compliance with dataset licence |
| **OD-014** | Persistence (default stateless) — whether Arena results/models are committed | Sprint 1 | ML-API | |
| **OD-015** | Reading-level slider implementation (template variants vs LLM) | Only if AR-026 scheduled | FE-REPLAY | |
| **OD-016** | ATT&CK-style tags list and mapping for Organisation mode | Only if AR-027 scheduled | ML-API | |
| **OD-017** | Numeric *proposed goals* for metrics and acceptable FPR | After baseline | ML-API | Must be labelled proposed |
| **OD-018** | Input limits (length, batch size) and handling of multi-message pastes | Sprint 1 | ML-API | | **provisionally closed by DEC-022** |
| **OD-019** | Exact Trust Gap toggle rules (how far the band can move; guardrails for OTP/PIN/payment asks) | Sprint 3 | ML-API + PLAYBOOK-DEMO | R-021 |
| **OD-020** | Definitions of Tarpit, ScamSigma, Herd Immunity for the roadmap slide | Sprint 5 | PLAYBOOK-DEMO | Named in proposal, not defined |

## 4. Change process

New decision → add `DEC-NNN` above (append) → update affected docs → note in the sprint outcome. Closing an OD → convert to a DEC entry and mark the OD row as closed (do not delete).
