# 08 — Security and Safety

**Status:** 🔵 PLANNED · Backlog: AR-030 (baseline, Sprint 1), AR-031, AR-036 (review, Sprint 5)

Attack Replay handles untrusted, potentially malicious text and teaches people about attacks. Safety is a product requirement, not an afterthought.

## 1. Hard prohibitions

Attack Replay must **never**:

| # | Prohibition | How it is enforced (PROPOSED) |
|---|---|---|
| S1 | **Execute submitted URLs** (fetch, resolve, preview, screenshot, unshorten) | No HTTP client is used on input-derived URLs; static analysis of the string only; code review + test |
| S2 | **Send messages** (SMS, email, chat, reports) on the user's behalf | No sending integration exists; report text is copy-only |
| S3 | **Perform transactions** | No payment/provider integrations |
| S4 | **Execute attacker-controlled code** | No `eval`/dynamic execution of input; no rendering of input as HTML/script; safe parsing only |
| S5 | **Interact with real criminal infrastructure** | No outbound requests derived from input; playbooks contain no real endpoints |
| S6 | **Expose secrets** | Secrets via environment/secret store; never in repo, logs, client bundles or error messages |
| S7 | **Treat untrusted input as executable** | Input is data everywhere — templates, prompts, CSV, filenames |
| S8 | **Present simulated actions as real actions** | Persistent "Simulation" labelling; wording review; no real-looking transaction UI |

## 2. Input sanitization and handling

- Enforce maximum input length and size limits (values OPEN — [OD-018](./12_DECISION_LOG.md#open-decisions)).
- Validate encoding; normalize safely (Unicode handling per [Data & ML §10](./04_DATA_AND_ML_STRATEGY.md)).
- **Escape on output**: highlighted text is rendered from spans onto escaped text; never `innerHTML` raw input.
- **CSV (`/batch`)**: guard against formula injection when output CSVs are opened in spreadsheets (prefix/escape cells beginning with `=`, `+`, `-`, `@`); limit rows/size; tolerate malformed rows without crashing.
- No user-controlled file paths or filenames used on the server.
- Rate/size limiting on endpoints (values OPEN).

## 3. URL handling

- URLs are **strings to analyse**, displayed **defanged** (non-clickable) in the UI.
- Never render URLs as live links; if the user copies them, that is their action.
- Indicators (shorteners, odd TLDs, obfuscation, mixed scripts) are computed from the string only.
- The replay's "fake page" is a **static mock-up** — no real page is loaded or embedded.

## 4. Secret management

- Secrets (e.g., an LLM API key if used) live in environment variables/secret manager; `.env` files git-ignored.
- Commit hygiene: secret scanning before every push and before submission.
- No secret is required for the offline path (templates only).

## 5. Logging

- Default: **do not log message bodies**. Log operational events (timing, error class, mode flags, model version).
- If content logging is ever enabled for debugging: opt-in, local only, short retention, documented.
- Never log secrets or full request headers with credentials.

## 6. Data retention and privacy

| Topic | Position (PROPOSED) |
|---|---|
| Submitted messages | Processed in memory; **not stored** by default |
| Incident narratives | Highly sensitive (may include financial harm, phone numbers) — same as above |
| Batch CSVs | Processed and returned; temporary files deleted after response |
| Analytics | None by default; if added, aggregate and non-content |
| Dataset | Used per its licence; no personal data extraction beyond need; do not redistribute if licence forbids |
| Third parties | If an LLM API is ever used, message content leaves the system → requires explicit consent copy, opt-in and rule check ([OD-006](./12_DECISION_LOG.md#open-decisions)); the default path sends nothing anywhere |
| User-facing privacy statement | Short, plain-language, in the UI footer (AR-037) |

## 7. Safe simulation

- The replay is **educational and simulated**: it shows *typical* progressions from curated playbooks.
- Consistent labels: "Simulation — nothing was sent, opened or paid."
- No real attacker scripts that would work as-is; scammer "next messages" are generic and reviewed for operational usefulness — they should teach recognition, not provide a template for fraud.
- No real brands/phone numbers/links in playbooks.
- Recovery guidance is generic unless verified; never promise reversal or refunds.

## 8. LLM limitations (if an LLM is used at all)

| Limitation | Control |
|---|---|
| May hallucinate | LLM may **only rephrase** grounded templates; never sets verdict/type/risk ([DEC-002](./12_DECISION_LOG.md#dec-002)) |
| **Prompt injection** from the scam text | The message is passed as delimited data; the LLM output is validated against the source template (facts, entities, action unchanged); fall back to the template on any mismatch |
| Unavailable / slow / rate-limited | Templates are the default and the fallback ([DEC-014](./12_DECISION_LOG.md#dec-014)) |
| Privacy | See §6; opt-in only |
| Non-determinism | Result flagged `llm_used`; tests run with LLM off |

## 9. Security review checklist (Sprint 5)

- [ ] No code path issues an HTTP request derived from user input
- [ ] Output escaping verified with hostile inputs (HTML/script, control chars, RTL overrides, giant payloads)
- [ ] CSV formula-injection test passes
- [ ] Secrets scan clean; `.env` ignored
- [ ] Logs contain no message bodies
- [ ] Dependencies reviewed; versions pinned; licences inventoried ([Submission Plan](./10_SUBMISSION_PLAN.md))
- [ ] Simulation labels present on every replay screen
- [ ] Error messages leak no internals

## 10. Related

[Risk Register](./11_RISK_REGISTER.md) (R-019) · [Architecture](./03_PRODUCT_ARCHITECTURE.md)
