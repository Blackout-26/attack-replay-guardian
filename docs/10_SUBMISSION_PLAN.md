# 10 — Submission Plan

> Competition deliverables per the proposal ("a working prototype, a short technical summary, a presentation and source code"). Format, length, channel and deadline are **TO BE VERIFIED** against the flyer ([AR-012](./13_BACKLOG.md#ar-012--official-requirements-verification)).

**Status:** 🔵 PLANNED · Backlog: AR-032–036

## 1. Deliverables

| # | Deliverable | Owner (role) | Backlog | Start | Format / limits | Status |
|---|---|---|---|---|---|---|
| D1 | **Working prototype** (web app + API), runnable/hosted | ML-API + FE-REPLAY | AR-016–022, AR-032 | Sprint 1 | TO BE VERIFIED | 🔵 PLANNED |
| D2 | **Short technical summary** | ML-API (with all) | AR-033 | **Start early (proposal: "start the summary tonight")** — Sprint 0/1, finish Sprint 5 | TO BE VERIFIED (length) | 🔵 PLANNED |
| D3 | **Presentation** (incl. "what's next": Tarpit, ScamSigma, Herd Immunity) | PLAYBOOK-DEMO | AR-034 | Sprint 4 | TO BE VERIFIED | 🔵 PLANNED |
| D4 | **Source code** (clean repo, README, run instructions) | ML-API | AR-036 | Continuous | TO BE VERIFIED | 🔵 PLANNED |
| D5 | **Documentation** (this docs/ set, README) | All | — | Done (planning) | — | 🟢 COMPLETE (planning docs) / maintain |
| D6 | **Backup demo video** | PLAYBOOK-DEMO | AR-035 | Sprint 5 | Not required by flyer (proposal-driven) | 🔵 PLANNED |
| D7 | **Hidden-set batch compatibility** (`/batch`) | ML-API | AR-017 | Sprint 1 | CSV → CSV | 🔵 PLANNED |

Owners are roles from the proposal ("ML and API", "front-end and replay visuals", "playbook content plus the demo script"). **Actual names: TODO** ([OD-008](./12_DECISION_LOG.md#open-decisions)).

## 2. Technical summary — planned contents

Problem & thesis · Architecture · Data (source, licence, splits, leakage controls) · Models (baseline, calibration, optional embeddings) · Risk fusion · Threat DNA · Replay/playbooks (curated) · Trust Gap · Incident mode · Evasion Arena + honest results · Evaluation results with failures · Safety & privacy · Limitations · **Inventory of every external model, library, dataset, API** · What's next.

## 3. Dependency & attribution inventory (fill as you go)

| Category | Item | Version | Licence | Used for | Attribution needed? | Runtime or dev only? |
|---|---|---|---|---|---|---|
| External models | TODO (e.g., any pretrained embedding model — only if used) | | | | | |
| Libraries | TODO | | | | | |
| Datasets | Released hackathon dataset (licence TO BE VERIFIED) | | | Training/eval | | |
| APIs / LLMs | TODO (only if used; default none) | | | | | |
| Fonts / icons / images | TODO | | | | | |
| Code snippets / tutorials | TODO | | | | | |

Rule: **list every external model and library** (proposal). Keep this table updated during development, not at the end.

## 4. Submission checklist

### Content
- [ ] Prototype runs from a clean checkout (README steps tested by someone else)
- [ ] Prototype works with LLM and internet **disabled**
- [ ] `/batch` tested with sample CSV and malformed rows
- [ ] Technical summary complete, within length limit
- [ ] Presentation complete, rehearsed, includes the two-minute demo
- [ ] Source code cleaned: no dead code, no secrets, no large accidental files
- [ ] README: overview, setup, run, test, data provenance, licences, limitations
- [ ] Evaluation report figures match what the prototype actually does
- [ ] Known weaknesses stated honestly

### Compliance
- [ ] Dataset use complies with its licence/terms
- [ ] All external models/libraries/APIs listed with licences
- [ ] Attribution added where required
- [ ] Rules on AI assistance and external services checked (TO BE VERIFIED)
- [ ] Team information/eligibility forms completed (TO BE VERIFIED)

### Packaging
- [ ] Submission channel and file formats confirmed (TO BE VERIFIED)
- [ ] Final tag/commit recorded; archive built and re-tested
- [ ] Backup video uploaded/accessible
- [ ] Submitted **before** the deadline with buffer; confirmation saved

## 5. Before final submission — freeze rules

| Milestone | Rule |
|---|---|
| **Feature freeze** | Start of Sprint 5: no new features except to fix blockers ([Sprint 5](./sprints/SPRINT_05_FINAL_HARDENING.md)) |
| **Doc freeze** | Technical summary/presentation numbers taken from a tagged evaluation run |
| **Code freeze** | Final tag; only demo-blocking fixes after this |
| **Submission** | Package tested from scratch on a clean machine |

## 6. Related

[Hackathon Requirements](./02_HACKATHON_REQUIREMENTS.md) · [Demo Strategy](./09_DEMO_STRATEGY.md) · [Sprint 5](./sprints/SPRINT_05_FINAL_HARDENING.md)
