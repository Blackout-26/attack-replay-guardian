import secrets
from . import config as G
from .store import Store
from .service import Guardian
from .monitors import FolderWatch, ImapWatch


class Runtime:
    def __init__(self):
        self.cfg = G.load(); self.store = Store(G.HOME / "guardian.db"); self.g = Guardian(self.cfg, self.store)
        self.token, self.monitors = secrets.token_urlsafe(16), []

    def start_monitors(self):
        for d in self.cfg["watch_dirs"]: self.monitors.append(FolderWatch(d, self.g))
        for a in self.cfg["imap"]: self.monitors.append(ImapWatch(a, self.g, backfill=self.cfg["backfill"]))
        for m in self.monitors: m.start()

    def stop(self):
        for m in self.monitors: m.stop()


_rt = None


def get():
    global _rt
    if _rt is None: _rt = Runtime()
    return _rt
