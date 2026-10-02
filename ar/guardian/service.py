"""Core of the IDS-style flow: message in -> analyse -> fuse technical evidence -> store -> notify -> (auto) report. Content of benign mail is never stored."""
import hashlib
from .. import config as C
from ..pipeline import analyze
from ..mailsignals import signals, fuse
from . import config as G, reporter
from .notify import notify

RANK = {"Low": 0, "Medium": 1, "High": 2}


class Guardian:
    def __init__(self, cfg, store):
        self.cfg, self.store = cfg, store

    def handle(self, m: dict, raw: bytes | None = None):
        h = hashlib.sha256(f"{m['msg_id']}|{m['sender']}|{m['subject']}|{m['text'][:500]}".encode()).hexdigest()
        if self.store.seen(h):
            return None
        self.store.mark(h)
        text = (m["subject"] + ". " + m["text"][:1500]).strip(". ").strip()
        if not text and not m["attachments"] and not m["links"]:
            return None
        a = fuse(analyze(text or "(no text)", full=True), signals(m), text)
        self.store.scan(m["source"], a["label"])
        if a["label"] != "Suspicious":
            return None
        band, score = a["risk"]["band"], a["threat_score"]["percent"]
        alert = {"source": m["source"], "sender": m["sender"] or "unknown", "subject": m["subject"][:200], "label": a["label"], "threat_type": a["threat_type"], "band": band, "score": score, "reason": a["reason"], "action": a["action"]}
        payload = {"analysis": a, "analyzed_text": text, "message": {k: m[k] for k in ("source", "sender", "reply_to", "subject", "links", "attachments")}}
        aid = self.store.add_alert(alert, payload)
        if raw:
            d = G.HOME / "evidence"; d.mkdir(exist_ok=True); (d / f"{aid}.eml").write_bytes(raw)
        if RANK[band] >= RANK[self.cfg["notify_min_risk"]]:
            notify(f"Attack Replay: {score}% likely a threat — {band} risk, {a['threat_type']}", f"From {alert['sender']}: {a['reason']}")
        alert["id"] = aid
        if self.cfg["report_mode"] == "auto" and band == "High":
            self.report(aid)
        return alert

    def report(self, aid):
        al = self.store.get(aid)
        if not al: return None
        res = reporter.send(al, self.cfg)
        self.store.set_status(aid, "reported" if res["sent"] else "report_prepared")
        return res
