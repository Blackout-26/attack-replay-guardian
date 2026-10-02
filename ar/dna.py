"""AR-005 Threat DNA: tactic detectors with evidence spans on the ORIGINAL text; strength strong/present/absent (no percentages, DEC-003).
Rule: strong = 2+ distinct evidence items; present = 1; absent = 0. English lexicons only — Shona lexicon needs a Shona-speaking reviewer (R-005)."""
import re
from .normalize import Norm

LEX = [
    ("urgency", "Urgency", r"\b(?:urgent(?:ly)?|immediately|right now|asap|within \d+ (?:minutes?|hours?|days?)|today|end of day|expires?|last chance|final warning|hurry|at once|quickly|now)\b"),
    ("authority", "Authority impersonation", r"\b(?:your (?:manager|director|supervisor|boss|ceo|bank manager|bank officer|principal)|public official|government|minister|ministry|our agent|security team|helpdesk|customer (?:care|service|support)|hr notice|bank officer|support team|(?:your )?relative|sibling|sounds like)\b"),
    ("fear_loss", "Fear / loss", r"\b(?:suspend\w*|block\w*|deactivat\w*|delet\w*|lock(?:ed)?|clos(?:ure|ed)|disabled|penalt\w+|arrest\w*|legal action|los(?:e|ing|t)|disconnect\w*|infected|limited|in trouble|returned)\b"),
    ("reward_lure", "Reward / lure", r"\b(?:won|winner|prize|congratulations|lottery|refund|reward|grant|free loan|loan|guaranteed returns|double your money|earn daily|cash grant|relief fund|scholarship|selected|payment programme|outstanding payment)\b"),
    ("secrecy", "Secrecy", r"\b(?:don'?t tell|do not tell|keep (?:this )?(?:secret|confidential|between us)|tell no one|confidential|without telling)\b"),
    ("call_to_action", "Call to action", r"\b(?:click|reply|download|open|install|sign in|log in|login|verify|confirm|call|send|update|transfer|pay|submit|enter|validate|register|watch|deposit|approve)\b"),
    ("synthetic_media", "Synthetic media cue", r"\b(?:voice (?:message|note)|video (?:message|call)|audio (?:clip|message)|recording|deepfake|ai-generated|synthetic voice|appears to show|a video (?:of|appears)|looks like|what looks like)\b"),
]
ORDER = [k for k, _, _ in LEX[:5]] + ["credential_request", "payment_request", "call_to_action", "suspicious_link", "synthetic_media"]
NAMES = {k: n for k, n, _ in LEX} | {"credential_request": "Credential / identity request", "payment_request": "Payment request", "suspicious_link": "Suspicious link or file"}


def _strength(ev):
    return "strong" if len({e["text"].lower() for e in ev}) >= 2 else "present" if ev else "absent"


def dna(n: Norm, ents: dict) -> list:
    found = {}
    for k, _, rx in LEX:
        ev, seen = [], set()
        for x in re.finditer(rx, n.text):
            sp = n.orig_span(x.start(), x.end())
            if sp not in seen:
                seen.add(sp); ev.append({"text": n.raw[sp[0]:sp[1]], "span": list(sp)})
        found[k] = ev[:6]
    asks = ents["asks"]
    mk = lambda keys: [{"text": n.raw[a["span"][0]:a["span"][1]], "span": a["span"]} for a in asks if a["key"] in keys]
    found["credential_request"] = mk({"otp_pin", "identity", "password", "login"})
    found["payment_request"] = mk({"money"}) + [{"text": a["value"], "span": a["span"]} for a in ents["amounts"]]
    link = [{"text": u["value"], "span": u["span"]} for u in ents["urls"]] + mk({"attachment", "install"})
    found["suspicious_link"] = link
    out = []
    for k in ORDER:
        ev = found[k]
        st = _strength(ev)
        if k == "suspicious_link" and ev and (n.flags["evasion_signal"] or re.search(r"hxxp|\[\.\]", n.raw.lower())):
            st = "strong"
        out.append({"tactic": k, "name": NAMES[k], "strength": st, "evidence": ev})
    return out
