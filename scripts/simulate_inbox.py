"""Drops realistic .eml files into the Guardian's watch folder, one every few seconds, as if mail were arriving.  python scripts/simulate_inbox.py [--delay 6]"""
import sys, time, uuid
from email.message import EmailMessage
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ar.guardian import config as G
from ar.guardian.samples import SAMPLES

delay = float(sys.argv[sys.argv.index("--delay") + 1]) if "--delay" in sys.argv else 6
cfg = G.load(); d = Path(cfg["watch_dirs"][0]); d.mkdir(parents=True, exist_ok=True)
for k, s in SAMPLES.items():
    m = EmailMessage(); m["From"] = s["sender"] if "@" in s["sender"] else "sms-gateway@phone.example.invalid"; m["To"] = "you@home.example.invalid"
    m["Subject"] = s["subject"] or f"SMS from {s['sender']}"; m["Message-ID"] = f"<{uuid.uuid4().hex}@sim>"
    if s.get("reply_to"): m["Reply-To"] = s["reply_to"]
    if s.get("auth"): m["Authentication-Results"] = "mx.example.invalid; " + s["auth"]
    m.set_content(s["text"])
    if s.get("links"): m.add_alternative("<p>" + s["text"] + " " + " ".join(f'<a href="{h}">{t}</a>' for t, h in s["links"]) + "</p>", subtype="html")
    for a in s.get("atts", []): m.add_attachment(b"MZ\x90\x00", maintype="application", subtype="octet-stream", filename=a)
    p = d / f"{int(time.time())}_{k}.eml"; p.write_bytes(m.as_bytes()); print("arrived:", s["label"]); time.sleep(delay)
