import json, os, secrets, stat
from pathlib import Path

HOME = Path(os.environ.get("AR_HOME") or (Path.home() / ".attack_replay"))
SERVICE = "attack-replay-guardian"


def default():
    return {"bind": "127.0.0.1", "port": 8787, "notify_min_risk": "Medium", "report_mode": "ask",
            "report": {"to": [], "webhook": "", "smtp": {"host": "", "port": 587, "user": "", "from": ""}, "attach_original": False},
            "watch_dirs": [str(HOME / "inbox_watch")], "imap": [], "backfill": 10, "ingest_token": secrets.token_urlsafe(16)}


def _merge(a, b):
    for k, v in b.items():
        a[k] = _merge(a[k], v) if isinstance(v, dict) and isinstance(a.get(k), dict) else v
    return a


def load():
    HOME.mkdir(parents=True, exist_ok=True)
    p, d = HOME / "config.json", default()
    if p.exists():
        d = _merge(d, json.loads(p.read_text()))
    else:
        save(d)
    return d


def save(cfg):
    HOME.mkdir(parents=True, exist_ok=True)
    (HOME / "config.json").write_text(json.dumps(cfg, indent=1))


def get_secret(name):
    try:
        import keyring
        v = keyring.get_password(SERVICE, name)
        if v:
            return v
    except Exception:
        pass
    f = HOME / "secrets.json"
    return json.loads(f.read_text()).get(name) if f.exists() else None


def set_secret(name, value):
    try:
        import keyring
        keyring.set_password(SERVICE, name, value)
        return "keyring"
    except Exception:
        f = HOME / "secrets.json"
        d = json.loads(f.read_text()) if f.exists() else {}
        d[name] = value
        f.write_text(json.dumps(d)); os.chmod(f, stat.S_IRUSR | stat.S_IWUSR)
        return "file (keyring unavailable — file is user-only readable)"
