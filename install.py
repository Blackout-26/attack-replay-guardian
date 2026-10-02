#!/usr/bin/env python3
"""One-command installer.   python install.py install [--no-autostart] | uninstall | status
Creates a private virtualenv, installs dependencies, trains the model, registers Guardian to start at login (like an antivirus agent) and adds a shortcut."""
import os, plistlib, subprocess, sys, venv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WIN, MAC = sys.platform.startswith("win"), sys.platform == "darwin"
VPY = ROOT / ".venv" / ("Scripts/python.exe" if WIN else "bin/python")
VPYW = ROOT / ".venv" / "Scripts/pythonw.exe"
TASK = "AttackReplayGuardian"
HOME = Path(os.environ.get("AR_HOME") or Path.home() / ".attack_replay")
URL = "http://127.0.0.1:8787"


def sh(*a, **k): return subprocess.run(list(map(str, a)), check=k.pop("check", True), **k)


def autostart_on():
    if WIN:
        sh("schtasks", "/Create", "/TN", TASK, "/TR", f'"{VPYW}" "{ROOT / "guardian.py"}" run', "/SC", "ONLOGON", "/F")
        sh("schtasks", "/Run", "/TN", TASK, check=False)
    elif MAC:
        p = Path.home() / "Library/LaunchAgents/com.attackreplay.guardian.plist"
        p.write_bytes(plistlib.dumps({"Label": "com.attackreplay.guardian", "ProgramArguments": [str(VPY), str(ROOT / "guardian.py"), "run"], "RunAtLoad": True, "KeepAlive": True}))
        sh("launchctl", "load", p, check=False)
    else:
        d = Path.home() / ".config/autostart"; d.mkdir(parents=True, exist_ok=True)
        (d / "attack-replay.desktop").write_text(f"[Desktop Entry]\nType=Application\nName=Attack Replay Guardian\nExec={VPY} {ROOT / 'guardian.py'} run\nX-GNOME-Autostart-enabled=true\n")


def autostart_off():
    if WIN: sh("schtasks", "/End", "/TN", TASK, check=False); sh("schtasks", "/Delete", "/TN", TASK, "/F", check=False)
    elif MAC:
        p = Path.home() / "Library/LaunchAgents/com.attackreplay.guardian.plist"; sh("launchctl", "unload", p, check=False); p.unlink(missing_ok=True)
    else: (Path.home() / ".config/autostart/attack-replay.desktop").unlink(missing_ok=True)


def shortcut(add=True):
    desk = Path.home() / "Desktop"
    if desk.exists():
        f = desk / "Attack Replay Guardian.url"
        if add: f.write_text(f"[InternetShortcut]\nURL={URL}\n")
        else: f.unlink(missing_ok=True)


def install(args):
    if sys.version_info < (3, 10): sys.exit("Python 3.10+ required")
    if not VPY.exists():
        print("Creating virtual environment…"); venv.create(ROOT / ".venv", with_pip=True)
    print("Installing dependencies…"); sh(VPY, "-m", "pip", "install", "-q", "-r", ROOT / "requirements.txt", "keyring")
    print("Training detection model…"); sh(VPY, ROOT / "scripts/train.py")
    sh(VPY, "-c", "import sys;sys.path.insert(0,r'%s');from ar.guardian import config as G;G.load();print('Config:',G.HOME/'config.json')" % ROOT)
    shortcut(True)
    if "--no-autostart" not in args:
        autostart_on(); print("Guardian will now start automatically at login and is starting now.")
    print(f"\nInstalled. Dashboard: {URL}\nConnect your mailbox:   {VPY} guardian.py setup\nRun manually:           {VPY} guardian.py run --open")


def uninstall():
    autostart_off(); shortcut(False); print(f"Auto-start and shortcut removed. Your data stays in {HOME} (delete it to erase alerts/config). Delete this folder to remove the program.")


def status():
    print("venv:", VPY.exists(), "| model:", (ROOT / "models/attack_replay_v1.joblib").exists(), "| config:", (HOME / "config.json").exists())
    if WIN: sh("schtasks", "/Query", "/TN", TASK, check=False)


if __name__ == "__main__":
    c = sys.argv[1] if len(sys.argv) > 1 else ""
    {"install": lambda: install(sys.argv[2:]), "uninstall": uninstall, "status": status}.get(c, lambda: print(__doc__))()
