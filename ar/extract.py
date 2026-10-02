"""AR-015 rule-based extraction. URLs are treated as strings only: never resolved or fetched."""
import re
from .normalize import Norm

_TLD = r"(?:com|org|net|info|xyz|top|link|io|ly|co\.zw|zw|invalid|example)"
URL = re.compile(r"(?:https?://|www\.)[^\s<>\"']+|\b(?:[a-z0-9-]+\.)+" + _TLD + r"\b(?:/[^\s<>\"']*)?")
PHONE = re.compile(r"(?:\+?263|\b0)[\s-]?7[1-9](?:[\s-]?\d){7}\b|\+\d{1,3}[\s-]?\d{8,12}\b")  # ZW formats: TO BE VERIFIED
AMOUNT = re.compile(r"(?:us\$|\$|usd|zwg|zig)\s?\d[\d,]*(?:\.\d+)?|\d[\d,]*(?:\.\d+)?\s?(?:usd|zwg|dollars)")
SECTORS = {  # context lexicon, not brand lists (DEC-005)
    "mobile money": r"mobile (?:money|wallet)|\bwallet\b|airtime",
    "bank": r"\bbank(?:ing)?\b|\bcard\b",
    "utility": r"electricity|water supply|\butility\b|\btoken",
    "government": r"government|minister|ministry|public official|tax authority",
    "university": r"universit|student|lecture|\bexam\b|timetable",
    "employer": r"\b(?:manager|director|supervisor|ceo|boss|payroll|employer|staff|hr)\b",
    "courier": r"parcel|delivery|package|courier|customs",
    "investment": r"\binvest|returns|trading|double your money",
    "sim/account": r"\bsim\b|\baccount\b|mailbox|\bemail\b",
}
VERB = re.compile(r"\b(?:send|share|reply(?: with)?|provide|give|enter|confirm|read out|submit|tell|type|supply|text|request\w*|register)\b")
NEG = re.compile(r"\b(?:do not|don't|dont|never|won't|not)\b")
URGE = re.compile(r"\b(?:link|below|click|now|immediately|today|urgent(?:ly)?|within \d+|warning|suspend\w*|block\w*|deactivat\w*|delet\w*|locked|expire\w*|avoid|prevent|limited)\b")
# (key, label, irreversibility 1-3, regex, needs_request_verb)  -- ordering OTP/PIN/money/install >= click >= reply (KNOWN); others PROPOSED (DEC-018)
ASKS = [
    ("otp_pin", "your PIN or OTP", 3, r"\b(?:otp|pin|cvv|passcode|one[- ]time (?:pin|password|code)|six[- ]digit code|(?:verification|recovery|reset|security) code|the code (?:you|we|that)|code you (?:just )?(?:received|got))\b", True),
    ("identity", "your ID or personal identity details", 3, r"\b(?:national id|id number|id card|copy of your id|photo of your (?:national )?id|passport(?: details| number)?|date of birth|card number|bank account number|tax number|personal details)\b", True),
    ("money", "money", 3, r"\b(?:send|transfer|pay|deposit|wire|remit|approve|buy|move)\b[^.!?]{0,40}?\b(?:money|funds|cash|fees?|airtime|vouchers?|payment|savings|us\$\s?\d[\d,]*|\$\s?\d[\d,]*|(?:it|them|this) back)\b|\b(?:reverse|refund|return)\b\s+(?:it|the money|the funds|the transaction)\b", False),
    ("install", "you to install software", 3, r"\binstall\b|\bdownload (?:the |this )?[\w ]{0,15}app\b|enable macros", False),
    ("login", "your login details", 3, r"\b(?:sign[- ]?in|log[- ]?in|login|verify your (?:details|identity|account)|confirm your (?:identity|details)|(?:re-?)?validate|re-?activate|restore your account|update your (?:\w+ )?(?:details|login|password))\b", "login"),
    ("password", "your password or account details", 2, r"\b(?:password|username|login credentials|account login|account details|account number)\b", True),
    ("attachment", "you to open a file", 2, r"\battach(?:ed|ment)?\b|\bopen the (?:zip|file|document)\b|\.(?:zip|exe|apk|docm|xlsm|scr)\b|\bdownload\b", False),
    ("link", "you to open a link", 2, None, False),
    ("reply", "you to reply", 1, r"\breply\b|\bcall (?:us|back|this number)\b", False),
]


def _requested(t, s):
    w = re.split(r"[.!?;:]\s", t[max(0, s - 60):s])[-1]
    return bool(VERB.search(w)) and not NEG.search(w)


def _negated(t, s):
    return bool(NEG.search(re.split(r"[.!?;:]\s", t[max(0, s - 30):s])[-1]))


def extract(n: Norm) -> dict:
    t = n.text
    ents = {"urls": [], "phones": [], "amounts": [], "sectors": [], "asks": []}
    for key, rx in (("urls", URL), ("phones", PHONE), ("amounts", AMOUNT)):
        for x in rx.finditer(t):
            v = x.group().rstrip(".,;)")
            ents[key].append({"value": v, "span": list(n.orig_span(x.start(), x.start() + len(v)))})
    ents["sectors"] = [k for k, rx in SECTORS.items() if re.search(rx, t)]
    urge = bool(URGE.search(t)) or bool(ents["urls"])
    for key, label, irr, rx, need in ASKS:
        if key == "link":
            if ents["urls"]:
                u = ents["urls"][0]
                ents["asks"].append({"key": key, "label": label, "irr": irr, "span": u["span"]})
            continue
        for x in re.finditer(rx, t):
            if need is True and not _requested(t, x.start()):
                continue
            if need == "login" and not urge:
                continue
            if need is False and _negated(t, x.start()):
                continue
            ents["asks"].append({"key": key, "label": label, "irr": irr, "span": list(n.orig_span(x.start(), x.end()))})
            break
    ents["asks"].sort(key=lambda a: -a["irr"])
    return ents


def cue_tokens(n: Norm, ents: dict) -> str:
    """Deterministic cue tokens appended to the model input so structured evidence reaches the classifier."""
    c = [f"__ask_{a['key']}__" for a in ents["asks"]]
    if ents["urls"]:
        c.append("__url__")
    if n.flags["evasion_signal"]:
        c.append("__evasion__")
    return " ".join(c)
