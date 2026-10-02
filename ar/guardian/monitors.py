"""Background sources. IMAP is opened READ-ONLY with BODY.PEEK (never marks mail read, never deletes/moves). Folder watcher reads dropped .eml/.txt/.json files."""
import imaplib, json, threading, time
from datetime import datetime
from pathlib import Path
from ..emailparse import parse_email, mk
from . import config as G

MAX_BYTES = 5_000_000


class Monitor(threading.Thread):
    def __init__(self, name, guardian, interval):
        super().__init__(daemon=True, name=name)
        self.g, self.interval, self.stop_ev = guardian, interval, threading.Event()
        self.status = {"name": name, "state": "starting", "last_check": None, "error": None, "processed": 0}

    def run(self):
        back = 5
        while not self.stop_ev.is_set():
            try:
                self.poll_once()
                self.status.update(state="watching", error=None, last_check=datetime.now().isoformat(timespec="seconds")); back = 5
                self.stop_ev.wait(self.interval)
            except Exception as e:  # never die: report and retry with backoff
                self.status.update(state="error", error=f"{type(e).__name__}: {str(e)[:120]}")
                self.stop_ev.wait(back); back = min(back * 2, 300)

    def stop(self): self.stop_ev.set()


class FolderWatch(Monitor):
    def __init__(self, path, guardian, interval=2):
        super().__init__(f"folder:{Path(path).name}", guardian, interval); self.path = Path(path); self.path.mkdir(parents=True, exist_ok=True)

    def poll_once(self):
        for f in sorted(self.path.iterdir()):
            if not f.is_file() or f.suffix.lower() not in (".eml", ".txt", ".json"): continue
            st = f.stat(); key = f"file:{f}:{st.st_mtime_ns}:{st.st_size}"
            if self.g.store.seen(key) or st.st_size > MAX_BYTES: continue
            self.g.store.mark(key)
            raw = f.read_bytes(); src = "folder"
            if f.suffix.lower() == ".eml":
                m = parse_email(raw, src)
            elif f.suffix.lower() == ".json":
                d = json.loads(raw.decode("utf-8", "replace")); m = mk(src, str(d.get("sender") or d.get("from") or ""), str(d.get("subject") or ""), str(d.get("text") or d.get("message") or d.get("body") or ""))
            else:
                m = mk(src, "", "", raw.decode("utf-8", "replace"))
            self.g.handle(m, raw if f.suffix.lower() == ".eml" else None); self.status["processed"] += 1


class ImapWatch(Monitor):
    def __init__(self, acct, guardian, connect=None, backfill=10):
        super().__init__(f"imap:{acct.get('name') or acct['user']}", guardian, int(acct.get("poll_seconds", 60)))
        self.a, self.backfill = acct, backfill
        self.key = f"imap:{acct['user']}@{acct['host']}:{acct.get('folder', 'INBOX')}"
        self.connect = connect or self._connect

    def _connect(self):
        pw = G.get_secret(f"imap:{self.a['user']}@{self.a['host']}")
        if not pw: raise RuntimeError("no password stored — run: python guardian.py setup")
        M = imaplib.IMAP4_SSL(self.a["host"], int(self.a.get("port", 993)), timeout=30); M.login(self.a["user"], pw); return M

    def poll_once(self):
        M = self.connect()
        try:
            M.select(self.a.get("folder", "INBOX"), readonly=True)
            last = self.g.store.kv_get(self.key)
            if last is None:
                typ, d = M.uid("SEARCH", None, "ALL"); uids = sorted(int(x) for x in d[0].split())
                new, top = (uids[-self.backfill:] if self.backfill else []), (uids[-1] if uids else 0)
            else:
                typ, d = M.uid("SEARCH", None, f"UID {int(last) + 1}:*"); uids = sorted(int(x) for x in d[0].split())
                new = [u for u in uids if u > int(last)][:200]; top = max(new + [int(last)])
            for u in new:
                typ, data = M.uid("FETCH", str(u), "(BODY.PEEK[])")
                raw = data[0][1] if data and isinstance(data[0], tuple) else b""
                if raw and len(raw) <= MAX_BYTES:
                    self.g.handle(parse_email(raw, f"email:{self.a.get('name') or self.a['user']}"), raw); self.status["processed"] += 1
            self.g.store.kv_set(self.key, top)
        finally:
            try: M.logout()
            except Exception: pass
