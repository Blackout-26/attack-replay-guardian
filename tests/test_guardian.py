import json, threading, time
from email.message import EmailMessage
from http.server import BaseHTTPRequestHandler, HTTPServer
import pytest
from ar.emailparse import parse_email, mk
from ar.mailsignals import signals
from ar.guardian import config as G, reporter
from ar.guardian.store import Store
from ar.guardian.service import Guardian
from ar.guardian.monitors import FolderWatch, ImapWatch
from ar.pipeline import analyze


def eml(subject, body, html=None, frm="a@x.example.invalid", atts=(), **h):
    m = EmailMessage(); m["From"] = frm; m["To"] = "me@home.example.invalid"; m["Subject"] = subject; m["Message-ID"] = f"<{hash((subject, body))}@t>"
    for k, v in h.items(): m[k.replace("_", "-")] = v
    m.set_content(body)
    if html: m.add_alternative(html, subtype="html")
    for a in atts: m.add_attachment(b"MZ", maintype="application", subtype="octet-stream", filename=a)
    return m.as_bytes()


@pytest.fixture
def g(tmp_path, monkeypatch):
    monkeypatch.setattr("ar.guardian.service.notify", lambda *a, **k: True)
    monkeypatch.setattr(G, "HOME", tmp_path)
    cfg = G.default(); cfg["watch_dirs"] = [str(tmp_path / "w")]
    return Guardian(cfg, Store(tmp_path / "t.db"))


def test_parse_html_links_and_auth():
    raw = eml("Hi", "see site", html='<p>Go to <a href="http://evil.example.invalid/x">www.mybank.example/login</a></p>', Authentication_Results="mx; dmarc=fail", Reply_To="z@evil.test")
    m = parse_email(raw)
    ids = {s["id"] for s in signals(m)}
    assert {"link_mismatch", "auth_fail", "reply_to"} <= ids


def test_attachment_signals():
    ids = {s["id"]: s["severity"] for s in signals(parse_email(eml("Invoice", "attached", atts=["invoice.pdf.exe"])))}
    assert ids["attach_double_ext"] == 3
    assert "attach_danger" in {s["id"] for s in signals(mk("t", atts=["setup.exe"]))}


def test_benign_mail_has_no_signals():
    assert signals(parse_email(eml("Meeting", "See you at 14:00"))) == []


def test_innocent_words_dangerous_attachment_is_flagged(g):
    al = g.handle(parse_email(eml("Invoice", "Hi, please find the attached invoice.", atts=["invoice.pdf.exe"])))
    assert al and al["band"] == "High" and "hides an executable" in al["reason"]


def test_scam_flagged_benign_not_and_dedupe(g):
    scam = mk("sms", "n", "", "URGENT: Your payment has failed. Send your PIN within 30 minutes so that our agent can reverse the transaction.")
    a = g.handle(scam)
    assert a and a["band"] == "High" and g.handle(scam) is None          # dedupe
    assert g.handle(mk("email", "a@b", "Team meeting", "Reminder: the team meeting is at 14:00 tomorrow in the boardroom.")) is None
    c = g.store.counts(); assert c["scanned"] == 2 and c["flagged"] == 1
    assert len(g.store.list()) == 1                                        # benign content never stored


def test_folder_watch(g, tmp_path):
    w = tmp_path / "w"; fw = FolderWatch(w, g)
    (w / "a.eml").write_bytes(eml("Act now", "Your payment has failed. Send your PIN now to reverse it."))
    (w / "b.txt").write_text("Congratulations! You have won US$500. Send your mobile money details to receive your prize.")
    (w / "c.json").write_text(json.dumps({"sender": "x", "text": "Reminder: your appointment is on Tuesday at 10:00."}))
    (w / "d.exe").write_bytes(b"ignored")
    fw.poll_once(); fw.poll_once()
    assert fw.status["processed"] == 3 and len(g.store.list()) == 2


class FakeIMAP:
    def __init__(self, msgs): self.msgs, self.ro = msgs, None
    def select(self, f, readonly=False): self.ro = readonly; return "OK", [b""]
    def uid(self, cmd, *a):
        if cmd == "SEARCH":
            q = a[1]; lo = int(q.split()[1].split(":")[0]) if q.startswith("UID") else 0
            ids = [str(u) for u in sorted(self.msgs) if u >= lo or q == "ALL"]; return "OK", [" ".join(ids).encode()]
        assert "PEEK" in a[1]; return "OK", [(b"x", self.msgs[int(a[0])])]
    def logout(self): pass


def test_imap_readonly_backfill_then_only_new(g):
    scam = lambda i: eml(f"Alert {i}", f"Your account will be suspended today. Verify your details immediately using the link below {i}.")
    msgs = {1: scam(1), 2: scam(2), 3: scam(3)}; fake = FakeIMAP(msgs)
    w = ImapWatch({"user": "u", "host": "h", "name": "t"}, g, connect=lambda: fake, backfill=2)
    w.poll_once(); assert fake.ro is True and w.status["processed"] == 2
    msgs[4] = scam(4); w.poll_once(); assert w.status["processed"] == 3


def test_report_to_real_local_webhook_and_redaction(g, tmp_path):
    got = []
    class H(BaseHTTPRequestHandler):
        def do_POST(s): got.append(json.loads(s.rfile.read(int(s.headers["Content-Length"])))); s.send_response(200); s.end_headers()
        def log_message(*a): pass
    srv = HTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
    g.cfg["report"]["webhook"] = f"http://127.0.0.1:{srv.server_port}/intake"
    al = g.handle(mk("email", "bad@evil.example.invalid", "Hi", "Send your PIN now to me@home.example.invalid or call +263 77 123 4567 to reverse the payment"))
    res = g.report(al["id"]); srv.shutdown()
    assert res["sent"] and got and got[0]["schema"].startswith("attack-replay-report")
    ex = got[0]["message"]["excerpt"]; assert "me@home" not in ex and "[email]" in ex and "4567" not in ex
    assert (tmp_path / "outbox" / f"{al['id']}.json").exists() and g.store.get(al["id"])["status"] == "reported"


def test_report_without_channels_is_prepared_only(g):
    al = g.handle(mk("sms", "n", "", "Your payment has failed. Send your PIN now to reverse the transaction."))
    assert g.report(al["id"])["sent"] is False and g.store.get(al["id"])["status"] == "report_prepared"


def test_notify_never_crashes(monkeypatch):
    from ar.guardian import notify as N
    monkeypatch.setattr(N.subprocess, "Popen", lambda *a, **k: (_ for _ in ()).throw(OSError("no display")))
    assert N.notify("t", "b") is False


def test_dna_replay_trust_incident():
    a = analyze("URGENT: Your payment has failed. Send your PIN within 30 minutes so that our agent can reverse the transaction.")
    d = {x["tactic"]: x for x in a["dna"]}
    assert d["urgency"]["strength"] != "absent" and d["credential_request"]["evidence"] and a["replay"]["stages"][3]["recoverable"]["level"] == 3
    assert all(0 <= e["span"][0] < e["span"][1] for x in a["dna"] for e in x["evidence"])
    t = analyze(a["reason"] and "Your account will be suspended today. Verify your details immediately using the link below.", toggles={"expected": True})["trust_gap"]
    assert t["adjusted_band"] in ("Medium", "High") and t["warning_kept"] is True
    inc = analyze("I already sent the money after they said my payment failed.")
    assert inc["incident"]["kind"] == "money" and inc["replay"]["pointer"] == 3 and inc["risk"]["band"] == "High"
    assert analyze("Your OTP is 482913. Do not share this code with anyone.")["replay"] is None


def test_api_guardian_security_and_flow(client):
    assert client.post("/api/simulate", json={"sample": "sms_pin"}).status_code == 403            # no token
    assert client.get("/api/status", headers={"host": "evil.example.com"}).status_code == 403   # DNS rebinding
    tok = {"x-ar-token": client.get("/api/session").json()["token"]}
    r = client.post("/api/simulate", json={"sample": "exe_mail"}, headers=tok).json()
    assert r["flagged"] and r["alert"]["band"] == "High"
    assert client.post("/api/simulate", json={"sample": "benign"}, headers=tok).json()["flagged"] is False
    lst = client.get("/api/alerts").json(); assert lst and "payload" not in lst[0]
    full = client.get(f"/api/alerts/{lst[0]['id']}").json(); assert full["payload"]["analysis"]["dna"]
    assert client.post(f"/api/alerts/{lst[0]['id']}/report", headers=tok).json()["outbox"].startswith("ok")
    assert client.post(f"/api/alerts/{lst[0]['id']}/safe", headers=tok).json()["ok"]
    assert client.get("/api/status").json()["counts"]["scanned"] >= 2


def test_ingest_token_required(client):
    from ar.guardian import runtime
    tk = runtime.get().cfg["ingest_token"]
    body = {"text": "Your payment has failed. Send your PIN now to reverse the transaction.", "sender": "+000"}
    assert client.post("/ingest", json=body).status_code == 401
    r = client.post("/ingest", json=body, headers={"authorization": "Bearer " + tk}).json(); assert r["flagged"] and r["risk"] == "High"


def test_settings_webhook_validation(client):
    tok = {"x-ar-token": client.get("/api/session").json()["token"]}
    client.post("/api/settings", json={"report_webhook": "javascript:alert(1)"}, headers=tok)
    assert client.get("/api/status").json()["report_channels"]["webhook"] is False
    client.post("/api/settings", json={"report_webhook": "http://127.0.0.1:9/intake"}, headers=tok)
    assert client.get("/api/status").json()["report_channels"]["webhook"] is True
    client.post("/api/settings", json={"report_webhook": ""}, headers=tok)
