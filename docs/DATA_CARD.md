# Data Card — released Cyber Shield training dataset (AR-001)

**Status:** 🟡 IN PROGRESS (licence/provenance TO BE VERIFIED from the flyer). All numbers below are **measured** by `scripts/evaluate.py` / inspection scripts.

| Item | Finding |
|---|---|
| File | `Cyber_Shield_Training_Dataset.csv` (copied to `data/raw/`) |
| Rows / unique messages | **100 / 12** (88 exact duplicates; each unique message appears 8–9 times) |
| Columns | incident_id, date_time, channel, content, source, threat_label, risk_level, recommended_action |
| Threat labels | Phishing 18 · Financial Scam 18 · Identity Fraud 16 · AI-Enabled Threat 16 · Malicious Link 16 · Benign 16 (rows) — **2 unique messages per label** |
| Risk labels | High 68 · Medium 16 · Low 16 (rows). Low = Benign only. Medium = "reply with password" (Identity Fraud) and "download attached document" (Malicious Link) |
| Channels | Email 42 · SMS 34 · Voice message 8 · Video 8 · Web/SMS 8 (voice/video rows are text descriptions, e.g. "This voice message from your manager…") |
| Source field | Unknown sender 50 · Unknown number 26 · Unknown source 8 · Known service 8 · Known institution 8 |
| Missing values | 0 |
| Conflicting labels | 0 (identical text always has identical label/risk) |
| Languages | English only observed; **no Shona or code-mixing** (a language field does not exist) |
| Dates | 2026-09-28 → 2026-09-30 (synthetic-looking timestamps; not used) |
| Links | Only `example.invalid` |

## Implications
1. Templated/synthetic data: high risk of over-fitting and of a false sense of accuracy. Group-aware splitting leaves nothing to test on → **DEC-019** (developer-authored supplement + frozen 30-message test).
2. The hidden set is probably similar in style but may differ; treat any metric here as optimistic.
3. Risk labels exist but are almost fully determined by the type/ask → rule-based risk, no fitted thresholds (DEC-020).
4. No Shona coverage: do not claim it. Needs a Shona-speaking reviewer for lexicons and mutations.

## Supplement (`data/supplement/dev_supplement.csv`)
90 messages written by the team (`source=developer-authored`): 60 train, 30 frozen final test (5 per class). No real brands, numbers or links.
