"""AR-006 grounded template explanations and actions; AR-026 reading levels via pre-written variants. No LLM (DEC-002/014)."""
from .risk import IRR_PHRASE

ACTION = {
    "Phishing": "Do not click the link. Verify through the organisation's official channel.",
    "Financial Scam": "Do not provide financial information. Verify the promotion independently.",
    "Identity Fraud": "Do not share credentials or identity information. Verify the request independently.",
    "AI-Enabled Threat": "Verify the request using an independent communication channel.",
    "Malicious Link": "Do not open the link. Use the official service website.",
    "Benign": "No action required. If you are unsure, verify through an official channel.",
}
PHRASE = {"Phishing": "phishing", "Financial Scam": "a financial scam", "Identity Fraud": "identity fraud",
          "AI-Enabled Threat": "an AI-enabled impersonation", "Malicious Link": "a malicious link or file"}
SIMPLE_T = {"Phishing": "a trick to steal your login", "Financial Scam": "a money scam", "Identity Fraud": "a trick to steal your identity",
            "AI-Enabled Threat": "a fake voice or video pretending to be someone you trust", "Malicious Link": "a dangerous link or file"}
SIMPLE_A = {"otp_pin": "your secret PIN or code", "identity": "your ID details", "money": "your money", "install": "you to install something",
            "login": "your login details", "password": "your password", "attachment": "you to open a file", "link": "you to click a link", "reply": "you to reply"}


def explain(ttype, suspicious, p_susp, asks, irr, level="normal"):
    if not suspicious:
        return ("Looks routine: no request for secrets, money or links was found. If unsure, confirm through the organisation's official channel."
                if level != "simple" else "This looks like a normal message. If you feel unsure, check with the sender using a number you already have.", ACTION["Benign"])
    conf = "high" if p_susp >= 0.85 else "moderate"
    top = asks[0] if asks else None
    if level == "simple":
        reason = f"This looks like {SIMPLE_T[ttype]}." + (f" It wants {SIMPLE_A[top['key']]}, which you cannot easily get back." if top else " Be careful with any link or number in it.")
    elif level == "technical":
        reason = (f"Classifier: {ttype} ({conf} calibrated likelihood). " + (f"Strongest ask: {top['key']} (irreversibility {irr}/3). " if top else "No explicit ask extracted. ") + "Risk = likelihood × irreversibility.")
    elif top:
        what = top["label"] if top["label"].startswith("you to") else "for " + top["label"]
        reason = f"Likely {PHRASE[ttype]} ({conf} confidence), and it asks {what} — {IRR_PHRASE[irr]}."
    else:
        reason = f"Likely {PHRASE[ttype]} ({conf} confidence); no direct request was found, so treat any link, number or attachment in it with care."
    action = ACTION[ttype]
    if any(a["key"] == "otp_pin" for a in asks):
        action += " Never share a PIN or OTP."
    return reason, action
