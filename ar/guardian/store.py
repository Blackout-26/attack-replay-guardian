"""Local SQLite store. Privacy: full detail kept ONLY for flagged messages; benign messages leave a content-free scan record."""
import json, sqlite3, threading, time, uuid
from datetime import date, datetime, timedelta
from ..score import threat_score


class Store:
    def __init__(self, path):
        self.db = sqlite3.connect(str(path), check_same_thread=False); self.lk = threading.Lock()
        self.db.executescript("""CREATE TABLE IF NOT EXISTS alerts(id TEXT PRIMARY KEY, ts REAL, source TEXT, sender TEXT, subject TEXT, label TEXT, ttype TEXT, band TEXT, reason TEXT, action TEXT, status TEXT, reported_at REAL, payload TEXT);
        CREATE TABLE IF NOT EXISTS seen(h TEXT PRIMARY KEY, ts REAL); CREATE TABLE IF NOT EXISTS scans(ts REAL, source TEXT, verdict TEXT); CREATE TABLE IF NOT EXISTS kv(k TEXT PRIMARY KEY, v TEXT);""")
        self._migrate()

    def _q(self, sql, a=()):
        with self.lk:
            c = self.db.execute(sql, a); self.db.commit(); return c.fetchall()

    def _migrate(self):
        """v0.2: alerts gain a threat-likelihood score. Databases created by older versions are upgraded in place and old alerts are scored from their stored analysis."""
        if "score" not in {r[1] for r in self._q("PRAGMA table_info(alerts)")}:
            self._q("ALTER TABLE alerts ADD COLUMN score INTEGER")
        self._q("CREATE INDEX IF NOT EXISTS alerts_ts ON alerts(ts)")
        for aid, payload in self._q("SELECT id, payload FROM alerts WHERE score IS NULL"):
            try:
                an = json.loads(payload)["analysis"]; s = (an.get("threat_score") or threat_score(an))["percent"]
            except Exception:
                s = 50
            self._q("UPDATE alerts SET score=? WHERE id=?", (s, aid))

    def seen(self, h): return bool(self._q("SELECT 1 FROM seen WHERE h=?", (h,)))
    def mark(self, h): self._q("INSERT OR IGNORE INTO seen VALUES(?,?)", (h, time.time()))
    def scan(self, source, verdict): self._q("INSERT INTO scans VALUES(?,?,?)", (time.time(), source, verdict))
    def kv_get(self, k):
        r = self._q("SELECT v FROM kv WHERE k=?", (k,)); return r[0][0] if r else None
    def kv_set(self, k, v): self._q("INSERT OR REPLACE INTO kv VALUES(?,?)", (k, str(v)))

    def add_alert(self, a, payload):
        aid = uuid.uuid4().hex[:10]
        self._q("INSERT INTO alerts(id,ts,source,sender,subject,label,ttype,band,reason,action,status,reported_at,payload,score) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (aid, time.time(), a["source"], a["sender"], a["subject"], a["label"], a["threat_type"], a["band"], a["reason"], a["action"], "new", None, json.dumps(payload), a.get("score")))
        return aid

    _COLS = "id,ts,source,sender,subject,label,ttype,band,reason,action,status,reported_at,score"

    def _row(self, r):
        k = self._COLS.split(","); d = dict(zip(k, r)); d["threat_type"] = d.pop("ttype"); d["risk"] = d.pop("band"); return d

    def list(self, limit=100, status=None):
        rows = self._q(f"SELECT {self._COLS} FROM alerts" + (" WHERE status=?" if status else "") + " ORDER BY ts DESC LIMIT ?", ((status, limit) if status else (limit,)))
        return [self._row(r) for r in rows]

    def get(self, aid):
        r = self._q(f"SELECT {self._COLS},payload FROM alerts WHERE id=?", (aid,))
        if not r: return None
        d = self._row(r[0][:-1]); d["payload"] = json.loads(r[0][-1])
        an = d["payload"]["analysis"]
        if "threat_score" not in an: an["threat_score"] = threat_score(an)   # alert stored by an older version
        return d

    def set_status(self, aid, status):
        self._q("UPDATE alerts SET status=?, reported_at=? WHERE id=?", (status, time.time() if status == "reported" else None, aid))

    def counts(self):
        day = time.time() - 86400
        sc = self._q("SELECT COUNT(*), SUM(verdict='Suspicious') FROM scans")[0]; t = self._q("SELECT COUNT(*), SUM(verdict='Suspicious') FROM scans WHERE ts>?", (day,))[0]
        return {"scanned": sc[0] or 0, "flagged": sc[1] or 0, "scanned_24h": t[0] or 0, "flagged_24h": t[1] or 0}

    def overview(self, days=14):
        """Numbers behind the dashboard charts. Alerts marked safe by the user are left out of the threat tallies."""
        today = date.today(); first = today - timedelta(days=days - 1)
        t0 = datetime.combine(first, datetime.min.time()).timestamp()
        got = {r[0]: (r[1] or 0, r[2] or 0) for r in self._q("SELECT date(ts,'unixepoch','localtime'), COUNT(*), SUM(verdict='Suspicious') FROM scans WHERE ts>=? GROUP BY 1", (t0,))}
        daily = []
        for i in range(days):
            d = (first + timedelta(days=i)).isoformat(); s, f = got.get(d, (0, 0)); daily.append({"date": d, "scanned": s, "flagged": f})
        st = {r[0]: r[1] for r in self._q("SELECT status, COUNT(*) FROM alerts GROUP BY status")}
        live = "status != 'safe'"
        avg = self._q(f"SELECT AVG(score), MAX(score) FROM alerts WHERE {live}")[0]
        bands = {r[0]: r[1] for r in self._q(f"SELECT band, COUNT(*) FROM alerts WHERE {live} GROUP BY band")}
        types = [{"type": r[0], "count": r[1], "avg_score": round(r[2] or 0)} for r in self._q(f"SELECT ttype, COUNT(*), AVG(score) FROM alerts WHERE {live} GROUP BY ttype ORDER BY 2 DESC")]
        senders = [{"sender": r[0], "count": r[1], "max_score": r[2] or 0} for r in self._q(f"SELECT sender, COUNT(*), MAX(score) FROM alerts WHERE {live} GROUP BY sender HAVING COUNT(*) > 1 ORDER BY 2 DESC, 3 DESC LIMIT 5")]
        return {"daily": daily, "alerts": {"total": sum(st.values()), "needs_review": st.get("new", 0), "reported": st.get("reported", 0) + st.get("report_prepared", 0), "marked_safe": st.get("safe", 0),
                                          "avg_score": round(avg[0] or 0), "top_score": avg[1] or 0, "high": bands.get("High", 0), "medium": bands.get("Medium", 0)},
                "types": types, "repeat_senders": senders}
