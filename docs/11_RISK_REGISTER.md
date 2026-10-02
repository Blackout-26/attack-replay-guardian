# 11 — Risk Register

**Status:** 🔵 PLANNED · Likelihood / Impact are **qualitative PROPOSED assessments** (Low / Medium / High) — no numerical scores are used because there is no data to justify them. Review at the start and end of every sprint.

**Owner roles** (from the proposal; names TODO — [OD-008](./12_DECISION_LOG.md#open-decisions)): **ML-API** (ML and API) · **FE-REPLAY** (front-end and replay visuals) · **PLAYBOOK-DEMO** (playbook content and demo script) · **ALL**.
**Status:** 🔵 Open (mitigation planned, not started) · 🟡 Mitigating · 🟢 Closed · 🔴 Realised.

## 1. Register

| ID | Risk | Description | Likelihood | Impact | Mitigation | Trigger | Owner | Status |
|---|---|---|---|---|---|---|---|---|
| **R-001** | Dataset mismatch | Released dataset labels/fields differ from proposal (no threat types, no risk labels, no sender/channel) | High | High | Inspect first (AR-001); build baseline before finalizing playbooks; adapt taxonomy; document mapping (AR-003) | Sprint 0 label inspection shows gaps | ML-API | 🔵 Open |
| **R-002** | Insufficient dataset quality | Noisy/contradictory labels, tiny classes, unrealistic synthetic text | Medium | High | Label audit; dedupe; conflict list; supplement with hard-benign and curated tests; report limitations | High conflict/duplicate rates; unstable CV | ML-API | 🔵 Open |
| **R-003** | Class imbalance | Rare threat types or benign minority | Medium | Medium | Stratified/group splits; class weights; macro F1; per-class reporting; generic fallback playbook | Very small per-class counts | ML-API | 🔵 Open |
| **R-004** | Data leakage | Near-duplicates or artifacts inflate metrics | Medium | High | Group-aware splits; leakage scan; frozen final test; no tuning on hidden data | Suspiciously high scores; feature importance on artifacts | ML-API | 🔵 Open |
| **R-005** | Multilingual handling | Weak Shona/English/mixed-language performance; unreviewed lexicons | Medium | Medium | Char n-grams; language slices; Shona-speaking reviewer for lexicons; Arena mixing mutations; candid reporting | Low recall on non-English slice | ML-API / PLAYBOOK-DEMO | 🔵 Open |
| **R-006** | Overfitting | Memorizes phrases; brittle to rewording | Medium | High | Validation discipline; regularization; Arena held-out mutation types | Big train/test or before/after-mutation gap | ML-API | 🔵 Open |
| **R-007** | Model weakness | Paraphrase/AI-polished text evades detector; poor calibration | Medium | High | Normalization; retraining on misses; optional embeddings (AR-029); calibration (AR-019); honest reporting | Held-out mutation caught rate low | ML-API | 🔵 Open |
| **R-008** | Unicode evasion | Homoglyphs, zero-width, split links defeat extraction/classifier | High | Medium | Advanced normalization with offset map (AR-025); mutation tests | Arena misses in those classes | ML-API | 🔵 Open |
| **R-009** | LLM failure | LLM unavailable, slow, off-policy, or disallowed | Medium | Low | LLM optional (COULD); templates are default & fallback ([DEC-014](./12_DECISION_LOG.md#dec-014)); validate LLM output vs template | Any LLM error or rule check outcome | ML-API | 🔵 Open |
| **R-010** | Internet failure | Venue connectivity fails during demo/eval | Medium | High | Offline-first design; local run; backup video; no network deps in demo path | No connectivity at venue | ALL | 🔵 Open |
| **R-011** | API failure | `/analyze` or `/batch` crashes on malformed input or under load | Medium | High | Input validation; error handling; batch robustness tests; health check; restart script | Exceptions in tests; 5xx | ML-API | 🔵 Open |
| **R-012** | Hallucinated explanations | Explanations state things not in the message/evidence | Low (templates) / Medium (if LLM) | High | Grounded templates keyed to indicators; groundedness audit; LLM rephrase only + validation | Audit finds ungrounded claim | ML-API | 🔵 Open |
| **R-013** | Dependency problems | Heavy/incompatible libraries; model downloads; version drift; licence issues | Medium | Medium | Minimal dependencies; pin versions; offline-capable; inventory licences; avoid optional embeddings unless justified | Install fails on clean machine | ML-API | 🔵 Open |
| **R-014** | Replay overclaiming | Users/judges read replay as prediction or guarantee of recovery | Medium | High | Mandatory labels ([DEC-010](./12_DECISION_LOG.md#dec-010)); wording review; verified-facts flags on recoverability | Copy review flags certainty words | PLAYBOOK-DEMO | 🔵 Open |
| **R-015** | Scope creep | Arena/Org mode/slider/LLM/Tarpit destabilise the core | High | High | Cut line ([DEC-012](./12_DECISION_LOG.md#dec-012)); sprint scope gates; SHOULD/COULD only after MUST stable; Sprint 4 must not break core | Core regression failing; new features added before MUST done | ALL | 🔵 Open |
| **R-016** | Demo failure | Bug, wrong verdict, or setup failure on stage | Medium | High | Rehearsal; regression suite on demo messages; backups B1–B5; offline mode | Rehearsal failures | PLAYBOOK-DEMO | 🔵 Open |
| **R-017** | Time constraints | Compressed schedule (relative build plan of ~days) | High | High | Strict priorities; parallel tracks; Sprint exit criteria; cut order | Sprint slips at any exit gate | ALL | 🔵 Open |
| **R-018** | Deployment problems | Hosting/config differs from local; cold start; environment issues | Medium | Medium | Local-run fallback; early deployment test; documented setup; pinned environment | Deployment failure in Sprint 4/5 | ML-API | 🔵 Open |
| **R-019** | Security problems | Injection (HTML/CSV/prompt), secret leakage, URL fetching, unsafe logging | Low | High | Security baseline (AR-030); output escaping; no outbound fetch; secrets hygiene; Sprint 5 review | Any finding in security checklist | ML-API | 🔵 Open |
| **R-020** | Incorrect local recovery guidance | Playbook claims about providers, reversal windows, reporting channels are wrong | Medium | High | Mark TO BE VERIFIED; verify with reliable sources or keep generic; `verified` flags | Unverified fact shown as fact | PLAYBOOK-DEMO | 🔵 Open |
| **R-021** | False reassurance from toggles | "Sender verified"/"I was expecting this" lowers the risk on a real scam | Medium | High | Guidance label; preserve irreversibility warning for OTP/PIN/payment asks; define rules (OD-019) | Test shows High-risk ask dropped to Low by toggle | ML-API / PLAYBOOK-DEMO | 🔵 Open |
| **R-022** | Official requirements unverified | Flyer not consulted; misread rules/judging | Medium | High | AR-012 in Sprint 0; TO BE VERIFIED checklist | Late discovery of requirement | ALL | 🔵 Open |
| **R-023** | Team capacity/roles unassigned | Three roles may be merged/thin; single points of failure | Medium | Medium | Assign owners (OD-008); keep docs current; parallel tracks; merge roles if few | Owner unavailable | ALL | 🔵 Open |

## 2. Review protocol

- Update **Status** and add new risks at each sprint boundary; record realised risks with 🔴 and the response.
- A risk that changes product direction must also appear in the [Decision Log](./12_DECISION_LOG.md).

## 3. Related

[Sprint documents](../PROJECT_PLAN.md#sprint-roadmap) list sprint-specific risks that reference these IDs.
