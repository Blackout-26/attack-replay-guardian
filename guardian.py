#!/usr/bin/env python3
"""Attack Replay Guardian launcher.   python guardian.py run [--open] | setup | demo | status"""
import getpass, os, subprocess, sys, threading, webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT); sys.path.insert(0, str(ROOT))


def ensure_model():
    from ar import config as C
    if not C.MODEL_FILE.exists():
        print("First run: training the detection model (about a minute)…"); subprocess.check_call([sys.executable, str(ROOT / "scripts/train.py")])


def run(args):
    os.environ["AR_GUARDIAN"] = "1"
    from ar.guardian import config as G
    if sys.stdout is None or sys.stderr is None:          # pythonw / background: no console
        log = open(G.HOME / "guardian.log", "a", buffering=1); sys.stdout = sys.stderr = log
    ensure_model(); cfg = G.load(); url = f"http://{cfg['bind']}:{cfg['port']}"
    if "--open" in args: threading.Timer(2.5, lambda: webbrowser.open(url)).start()
    print(f"Attack Replay Guardian running at {url}  (config: {G.HOME / 'config.json'})", flush=True)
    import uvicorn
    uvicorn.run("ar.api:app", host=cfg["bind"], port=cfg["port"], log_level="warning")


def ask(q, d=""):
    v = input(f"{q}{f' [{d}]' if d else ''}: ").strip(); return v or d


def setup():
    from ar.guardian import config as G
    cfg = G.load(); print("Attack Replay Guardian setup (Enter to skip any step)\n")
    if ask("Watch an email account via IMAP? (y/n)", "n").lower().startswith("y"):
        host = ask("IMAP server", "imap.gmail.com"); user = ask("Email address / username")
        print("  Use an APP PASSWORD (Gmail: enable IMAP + 2-step verification, then create an app password).")
        pw = getpass.getpass("  Password (hidden): ")
        where = G.set_secret(f"imap:{user}@{host}", pw); print("  Password stored in:", where)
        cfg["imap"] = [a for a in cfg["imap"] if not (a["user"] == user and a["host"] == host)] + [{"name": user.split("@")[0], "host": host, "port": 993, "user": user, "folder": "INBOX", "poll_seconds": 60}]
    w = ask("Report webhook URL (your provider/SOC intake; blank = none)", cfg["report"]["webhook"])
    cfg["report"]["webhook"] = w
    to = ask("Report by email to (comma-separated abuse/fraud addresses; blank = none)", ",".join(cfg["report"]["to"]))
    cfg["report"]["to"] = [x.strip() for x in to.split(",") if x.strip()]
    if cfg["report"]["to"]:
        s = cfg["report"]["smtp"]; s["host"] = ask("SMTP server for sending reports", s["host"] or "smtp.gmail.com"); s["user"] = ask("SMTP username", s["user"]); s["from"] = s["user"]
        if s["user"]: G.set_secret(f"smtp:{s['user']}@{s['host']}", getpass.getpass("  SMTP password (hidden): "))
    cfg["report_mode"] = ask("Reporting mode: ask / auto / off", cfg["report_mode"])
    G.save(cfg); print("\nSaved. Start with:  python guardian.py run --open")


def demo():
    from ar.guardian import config as G
    cfg = G.load(); cfg["report"]["webhook"] = "http://127.0.0.1:8788/intake"; cfg["report_mode"] = "ask"; G.save(cfg)
    print("Demo configured. Terminal 1: python scripts/provider_console.py   Terminal 2: python guardian.py run --open   Terminal 3: python scripts/simulate_inbox.py")


if __name__ == "__main__":
    c = sys.argv[1] if len(sys.argv) > 1 else "run"
    {"run": lambda: run(sys.argv[2:]), "setup": setup, "demo": demo}.get(c, lambda: print(__doc__))()
