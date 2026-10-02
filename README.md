# Attack Replay Guardian

An IDS-style protection agent for ordinary people. It watches incoming email (and messages pushed to it), analyses every one **locally**, notifies you only when something is suspicious, explains **why** (Threat DNA, technical evidence, Attack Replay of what would happen next), and can send a standard report to your provider. You never have to copy and paste anything — but you can open the dashboard and check a message yourself if you want.

```
 sources                      analysis (offline, no LLM)                    output
 IMAP mailbox (read-only) ─┐   normalize → extract → classify → risk          desktop notification
 watched folder (.eml/.txt)├─► + email evidence (links, auth, attachments) ─► dashboard (why / replay / trust gap)
 /ingest webhook (SMS apps)┘   → Threat DNA → Replay → Incident plan          report → outbox + webhook/SMTP
```

## Install (one command) and test on your machine
Requires Python 3.10+ (python.org; on Windows tick **Add Python to PATH**). Open PowerShell/Terminal in this folder:
```
python install.py install          # venv + dependencies + trains the model + auto-start at login + desktop shortcut
```
Dashboard: http://127.0.0.1:8787 (also the desktop shortcut). Use `--no-autostart` if you only want to try it. Remove with `python install.py uninstall`.
Windows paths below use `.venv\Scripts\python`; on macOS/Linux use `.venv/bin/python`.

**1. Prove the tests pass (70 expected):** `.venv\Scripts\python -m pytest -q`

**2. Demo with no mailbox needed (the presentation flow)** — three terminals in this folder:
```
.venv\Scripts\python scripts\provider_console.py        # mock service-provider fraud desk -> http://127.0.0.1:8788
.venv\Scripts\python guardian.py run --open             # (stop the auto-start copy first if running: schtasks /End /TN AttackReplayGuardian)
.venv\Scripts\python scripts\simulate_inbox.py          # drops 5 emails/messages into the watch folder, 6 s apart
```
In the dashboard open **Settings → report webhook** and enter `http://127.0.0.1:8788/intake` (or run `python guardian.py demo` once). Watch: desktop notifications pop up for the 4 bad messages, the benign one is silently ignored, click **Why? / details** (highlighted tactics, technical evidence, replay, trust gap), click **Report to provider** and see it appear on the provider console. The dashboard's yellow "Try the detector" buttons do the same without files.

**3. Your real mailbox:** `.venv\Scripts\python guardian.py setup` → IMAP server, address, **app password** (Gmail: turn on IMAP + 2-step verification, create an app password). Then `guardian.py run`. First start scans your latest 10 mails, then every new mail (checked every 60 s). Send yourself: subject `Urgent: verify your account`, body `Your account will be suspended today. Verify your details immediately using the link below.`
**4. SMS from a phone:** a PC cannot read SMS. Use any Android "SMS forwarder" app that POSTs JSON to `http://<pc>:8787/ingest` with header `Authorization: Bearer <ingest_token>` (token in `~/.attack_replay/config.json`) and body `{"sender":"..","text":".."}`. For phone→PC over Wi-Fi set `"bind":"0.0.0.0"` in config (only on a trusted network).

## What's new in this version
- **Threat likelihood on every alert** — each alert shows a percentage (and a "Why this score" breakdown: wording, tactics, technical evidence). It is a triage aid, not a calibrated probability (DEC-028). Desktop notifications show it too. Old alerts in an existing database are scored automatically on first start.
- **New dashboard** (`web/index.html`) — light-blue layout: threats-per-day chart (this week vs previous), average likelihood, "waiting for you", threat types, repeat senders; alerts open in a side panel; search, filters, sort by likelihood, Undo for "Mark safe", CSV export (`/api/alerts.csv`).
- `scripts/seed_demo.py` fills a *separate* demo folder with two weeks of fictional alerts for presentations (never touches your real data).
- New API: `GET /api/overview`, `GET /api/alerts.csv`, `POST /api/alerts/{id}/trust`, `POST /api/alerts/{id}/reopen`.

## Privacy and safety (by design)
- Mail is opened **read-only** (`BODY.PEEK`); nothing is deleted, moved or marked read. Links are never opened. Analysis never leaves the PC.
- Only **flagged** messages are stored (in `~/.attack_replay`); normal mail leaves a content-free counter. Evidence copies go to `evidence/`.
- A report leaves the PC only when you click **Report** (default "ask") or enable `auto` (High-risk only), and only to destinations **you** configured (webhook / SMTP). Excerpts are redacted; the original `.eml` is attached only if `attach_original` is true. A local copy is always written to `outbox/`. No provider addresses are built in.
- Server binds to localhost, rejects foreign Host headers (DNS-rebinding) and requires a session token for state changes (CSRF). Passwords go to the OS keyring.

## Known limits (read before presenting)
- Not tested by the author on real Windows toasts or a live IMAP server (tested with a fake IMAP server, local webhook and file drops). Gmail needs an app password; Outlook/Microsoft 365 need OAuth, which is **not** supported yet.
- Polling (60 s), not instant IMAP IDLE. English only — no Shona. The text model is trained on short messages (see `reports/BASELINE_EVALUATION.md`: small, authored test; not a hidden-set estimate); long newsletters may false-positive, so alerts are explainable and dismissible.
- Detection of "already happened" incidents is rule-based. Provider/police procedures are marked TO BE VERIFIED; contacts are never invented.
- The Evasion Arena exists only in the offline prototype `web/demo.html`, not on the API. `packaging/build_exe.py` (single .exe) is experimental and unverified.
- Developer docs: `docs/`, `PROJECT_PLAN.md`, `scripts/train.py`, `scripts/evaluate.py`.
