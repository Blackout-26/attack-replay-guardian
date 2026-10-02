#!/usr/bin/env python3
"""Fill a DEMO Guardian database with two weeks of fictional history so the dashboard charts look alive for a presentation.

Safe by design: it writes to its own folder (default ~/.attack_replay_demo) and refuses to touch the real one
(~/.attack_replay) unless you pass --force. Everything it creates is fictional (example.invalid, no real brands).

  PowerShell:
    $env:AR_HOME = "$HOME\\.attack_replay_demo"
    .venv\\Scripts\\python scripts\\seed_demo.py
    .venv\\Scripts\\python guardian.py run --open        # same $env:AR_HOME in this terminal
"""
import os, random, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
REAL = Path.home() / ".attack_replay"
home = Path(os.environ.get("AR_HOME") or (Path.home() / ".attack_replay_demo"))
if home.resolve() == REAL.resolve() and "--force" not in sys.argv:
    sys.exit(f"Refusing to write demo data into your real Guardian folder ({REAL}).\nSet AR_HOME to another folder, e.g.  $env:AR_HOME = \"$HOME\\.attack_replay_demo\"   (or pass --force).")
os.environ["AR_HOME"] = str(home)

from ar.guardian import config as G
from ar.guardian.store import Store
from ar.guardian.service import Guardian
from ar.guardian.samples import SAMPLES
from ar.emailparse import mk

EXTRA = [
    ("sms", "+263 77 000 0101", "", "Congratulations! You won a cash prize. Reply with your ID number and send a processing fee to claim it today."),
    ("sms", "Unknown number", "", "Your mobile wallet has been limited. Confirm your PIN now at secure-wallet.example.invalid or lose access."),
    ("email", "hr-notice@payroll.example.invalid", "Salary update", "Your salary payment is on hold. Verify your bank account number and password immediately to release it."),
    ("whatsapp-export", "Unknown number", "", "This voice message from the director asks you to urgently buy vouchers and tell no one."),
    ("email", "delivery@parcels.example.invalid", "Parcel held at customs", "Your parcel is held at customs. Pay the release fee today using the link below or it will be returned."),
    ("sms", "Unknown number", "", "Hi, I am your relative and I am in trouble. Send airtime money urgently and do not tell anyone."),
]


def main():
    home.mkdir(parents=True, exist_ok=True)
    cfg = G.default(); cfg["watch_dirs"] = [str(home / "inbox_watch")]
    st = Store(home / "guardian.db"); g = Guardian(cfg, st)
    import ar.guardian.service as svc
    svc.notify = lambda *a, **k: True          # never pop notifications while seeding
    rnd = random.Random(7)
    pool = [(sp["source"], sp["sender"], sp["subject"], sp["text"], sp) for k, sp in SAMPLES.items() if k != "benign"] + [(s, f, j, t, {}) for s, f, j, t in EXTRA]
    flagged_per_day = [2, 1, 3, 2, 4, 1, 2, 3, 2, 5, 3, 4, 6, 2]          # oldest -> today
    now = time.time(); n_alerts = 0
    for back, nflag in zip(range(13, -1, -1), flagged_per_day):
        day = now - back * 86400
        scanned = nflag + rnd.randint(9, 24)
        for _ in range(scanned - nflag):
            st._q("INSERT INTO scans VALUES(?,?,?)", (day - rnd.randint(0, 40000), "email", "Benign"))
        for _ in range(nflag):
            src, sender, subj, text, sp = rnd.choice(pool)
            m = mk("simulated:" + src, sender, subj, text, sp.get("links"), sp.get("atts"), {"auth": sp.get("auth", ""), "received_spf": ""}, sp.get("reply_to", ""), msg_id=f"seed-{back}-{rnd.random()}")
            al = g.handle(m)
            if not al: continue
            ts = day - rnd.randint(0, 40000) if back else now - rnd.randint(300, 20000)
            st._q("UPDATE alerts SET ts=? WHERE id=?", (ts, al["id"])); st._q("UPDATE scans SET ts=? WHERE rowid=(SELECT MAX(rowid) FROM scans)", (ts,))
            n_alerts += 1
            r = rnd.random()
            if back > 1 and r < .30: st.set_status(al["id"], "reported")
            elif back > 1 and r < .45: st.set_status(al["id"], "safe")
    print(f"Demo data written to {home}\n  {n_alerts} fictional alerts over 14 days.\nStart the dashboard with the same AR_HOME:  python guardian.py run --open")


if __name__ == "__main__":
    main()
