"""Standard abuse report: always written to a local outbox; sent to a webhook and/or SMTP address ONLY if the user configured them.
No provider addresses are invented. Excerpts are redacted; the original .eml is attached only if attach_original=true."""
import json, re, smtplib, urllib.request
from datetime import datetime, timezone
from email.message import EmailMessage
from urllib.parse import urlparse
from .. import config as C
from . import config as G

_EM, _PH = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"), re.compile(r"\+?\d[\d \-]{8,}\d")


def redact(t, keep=""):
    return _PH.sub("[phone]", _EM.sub(lambda m: m.group() if keep and m.group().lower() == keep.lower() else "[email]", t))


def build_report(alert):
    p, a = alert["payload"], alert["payload"]["analysis"]
    msg = p["message"]
    doms = sorted({urlparse(u["value"] if "://" in u["value"] else "http://" + u["value"]).netloc for u in a["entities"]["urls"]} | {urlparse(h).netloc for _, h in msg["links"] if h})
    return {"schema": "attack-replay-report/1", "report_id": alert["id"], "generated_at": datetime.now(timezone.utc).isoformat(),
            "reporter": {"tool": "Attack Replay Guardian", "version": C.VERSION, "note": "Automated first-pass analysis; verify before acting."},
            "verdict": {"label": alert["label"], "threat_type": alert["threat_type"], "risk": alert["risk"], "reason": alert["reason"]},
            "evidence": {"technical_signals": [s["text"] for s in a.get("email_signals", [])],
                         "tactics": [{"name": d["name"], "strength": d["strength"], "examples": [e["text"] for e in d["evidence"][:3]]} for d in a.get("dna", []) if d["strength"] != "absent"],
                         "indicators": {"domains": [d for d in doms if d], "phones": [x["value"] for x in a["entities"]["phones"]], "sender": msg["sender"], "reply_to": msg["reply_to"]}},
            "message": {"source": msg["source"], "subject": msg["subject"], "excerpt": redact(p["analyzed_text"][:400], msg["sender"])}}


def send(alert, cfg):
    rep, res = build_report(alert), {}
    out = G.HOME / "outbox"; out.mkdir(exist_ok=True)
    (out / f"{alert['id']}.json").write_text(json.dumps(rep, indent=1)); res["outbox"] = "ok: " + str(out / f"{alert['id']}.json")
    rc = cfg["report"]
    if rc.get("webhook"):
        try:
            req = urllib.request.Request(rc["webhook"], json.dumps(rep).encode(), {"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=10) as r:
                res["webhook"] = "ok" if 200 <= r.status < 300 else f"error: HTTP {r.status}"
        except Exception as e:
            res["webhook"] = f"error: {type(e).__name__}"
    else:
        res["webhook"] = "not configured"
    s = rc.get("smtp", {})
    if rc.get("to") and s.get("host"):
        try:
            m = EmailMessage(); m["To"] = ", ".join(rc["to"]); m["From"] = s.get("from") or s.get("user"); m["Subject"] = f"[Attack Replay] Suspicious message report {alert['id']}"
            m.set_content(f"{rep['verdict']['threat_type']} — {rep['verdict']['risk']} risk\n{rep['verdict']['reason']}\n\nIndicators: {json.dumps(rep['evidence']['indicators'])}\n\nFull report attached.")
            m.add_attachment(json.dumps(rep, indent=1).encode(), maintype="application", subtype="json", filename="report.json")
            ev = G.HOME / "evidence" / f"{alert['id']}.eml"
            if rc.get("attach_original") and ev.exists():
                m.add_attachment(ev.read_bytes(), maintype="message", subtype="rfc822", filename="original.eml")
            cls = smtplib.SMTP_SSL if int(s["port"]) == 465 else smtplib.SMTP
            with cls(s["host"], int(s["port"]), timeout=15) as sm:
                if cls is smtplib.SMTP: sm.starttls()
                pw = G.get_secret(f"smtp:{s['user']}@{s['host']}")
                if s.get("user") and pw: sm.login(s["user"], pw)
                sm.send_message(m)
            res["email"] = "ok"
        except Exception as e:
            res["email"] = f"error: {type(e).__name__}"
    else:
        res["email"] = "not configured"
    res["sent"] = res["webhook"] == "ok" or res["email"] == "ok"
    return res
