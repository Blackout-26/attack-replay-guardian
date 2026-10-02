"""Threat-likelihood score (DEC-027), its storage/migration, and the dashboard endpoints added with it."""
import csv, io, json, sqlite3
from ar.pipeline import analyze
from ar.score import threat_score
from ar.guardian.store import Store
from ar.guardian.samples import SAMPLES
from ar.api import _cell

PIN = "URGENT: Your payment has failed. Send your PIN within 30 minutes so that our agent can reverse the transaction."
ROUTINE = "Reminder: the team meeting is at 14:00 tomorrow in the boardroom. Please bring your reports."


def _a(label="Suspicious", p=0.6, **kw):
    return {"label": label, "threat_type": "Phishing", "internal": {"p_suspicious": p}, "dna": [], **kw}


def test_score_never_contradicts_the_verdict():
    for t in (PIN, ROUTINE, "Congratulations you won a prize! Reply with your ID number to claim.", "Please find attached the minutes of Monday's meeting. Regards, Tendai"):
        a = analyze(t); s = a["threat_score"]["percent"]
        assert 0 <= s <= 100
        assert (s >= 50) == (a["label"] == "Suspicious"), (t, s, a["label"])


def test_clear_scam_scores_high_and_routine_mail_low():
    assert analyze(PIN)["threat_score"]["percent"] >= 85
    r = analyze(ROUTINE)["threat_score"]
    assert r["percent"] < 25 and r["tone"] == "safe"


def test_more_evidence_never_lowers_the_score():
    base = threat_score(_a())["percent"]
    with_sig = threat_score(_a(email_signals=[{"id": "auth_fail", "severity": 2, "text": "the sender's authentication checks failed"}]))["percent"]
    with_hard = threat_score(_a(email_signals=[{"id": "attach_double_ext", "severity": 3, "text": "hidden executable"}]))["percent"]
    with_inc = threat_score(_a(incident={"title": "Money already sent"}))["percent"]
    assert base < with_sig < with_hard and with_inc > base


def test_factors_explain_the_number():
    s = analyze(PIN)["threat_score"]
    assert s["factors"] and s["factors"][0]["strength"] >= s["factors"][-1]["strength"]
    assert {"label", "detail", "strength"} <= set(s["factors"][0]) and "not a guarantee" in s["note"]


def test_guardian_alert_carries_score_and_it_is_stored(tmp_path, monkeypatch):
    from ar.guardian import config as G
    from ar.guardian.service import Guardian
    from ar.emailparse import mk
    monkeypatch.setattr("ar.guardian.service.notify", lambda *a, **k: True); monkeypatch.setattr(G, "HOME", tmp_path)
    g = Guardian(G.default(), Store(tmp_path / "t.db"))
    sp = SAMPLES["exe_mail"]
    al = g.handle(mk("email", sp["sender"], sp["subject"], sp["text"], None, sp["atts"], {}, "", "id-1"))
    assert al and al["score"] >= 80                       # a hidden .exe lifts a plain-looking message
    row = g.store.get(al["id"]); assert row["score"] == al["score"] == row["payload"]["analysis"]["threat_score"]["percent"]


def test_old_database_is_upgraded_and_old_alerts_are_scored(tmp_path):
    db = tmp_path / "old.db"; c = sqlite3.connect(db)
    c.executescript("CREATE TABLE alerts(id TEXT PRIMARY KEY, ts REAL, source TEXT, sender TEXT, subject TEXT, label TEXT, ttype TEXT, band TEXT, reason TEXT, action TEXT, status TEXT, reported_at REAL, payload TEXT);")
    a = analyze(PIN); a.pop("threat_score")                # what a v0.1 alert looked like
    c.execute("INSERT INTO alerts VALUES('old1',1.0,'sms','x','','Suspicious','Financial Scam','High','r','a','new',NULL,?)", (json.dumps({"analysis": a, "analyzed_text": PIN, "message": {}}),)); c.commit(); c.close()
    st = Store(db)
    assert st.list()[0]["score"] >= 85 and st.get("old1")["payload"]["analysis"]["threat_score"]["percent"] >= 85


def _token(client): return client.get("/api/session").json()["token"]


def test_api_alert_list_has_scores_and_overview_shape(client):
    t = _token(client)
    for k in ("sms_pin", "phish_mail", "benign"): client.post("/api/simulate", json={"sample": k}, headers={"x-ar-token": t})
    L = client.get("/api/alerts").json()
    assert L and all(isinstance(a["score"], int) and 50 <= a["score"] <= 100 for a in L)
    o = client.get("/api/overview").json()
    assert len(o["daily"]) == 14 and {"scanned", "flagged", "date"} <= set(o["daily"][0])
    assert o["alerts"]["total"] >= 2 and o["alerts"]["needs_review"] >= 1 and 50 <= o["alerts"]["avg_score"] <= 100 and o["types"]


def test_trust_endpoint_keeps_the_email_evidence_band(client):
    t = {"x-ar-token": _token(client)}
    client.post("/api/simulate", json={"sample": "phish_mail"}, headers=t)
    al = next(a for a in client.get("/api/alerts").json() if a["subject"].startswith("Action required"))
    assert al["risk"] == "High"
    off = client.post(f"/api/alerts/{al['id']}/trust", json={}, headers=t).json()
    on = client.post(f"/api/alerts/{al['id']}/trust", json={"sender_verified": True}, headers=t).json()
    assert off["adjusted_band"] == "High" and on["adjusted_band"] == "Medium" and on["toggles"]["sender_verified"] is True
    assert client.post("/api/alerts/nope/trust", json={}, headers=t).status_code == 404


def test_reopen_after_mark_safe(client):
    t = {"x-ar-token": _token(client)}
    client.post("/api/simulate", json={"sample": "voice"}, headers=t)
    aid = client.get("/api/alerts").json()[0]["id"]
    client.post(f"/api/alerts/{aid}/safe", headers=t); assert client.get(f"/api/alerts/{aid}").json()["status"] == "safe"
    client.post(f"/api/alerts/{aid}/reopen", headers=t); assert client.get(f"/api/alerts/{aid}").json()["status"] == "new"


def test_csv_export_and_formula_guard(client):
    assert [_cell(x) for x in ("=cmd|' /C calc'!A0", "+1", "-1", "@SUM(1)", "plain", None)] == ["'=cmd|' /C calc'!A0", "'+1", "'-1", "'@SUM(1)", "plain", ""]
    r = client.get("/api/alerts.csv"); rows = list(csv.reader(io.StringIO(r.text)))
    assert r.headers["content-type"].startswith("text/csv") and rows[0][6] == "threat_likelihood_percent" and len(rows) > 1 and rows[1][6].isdigit()
