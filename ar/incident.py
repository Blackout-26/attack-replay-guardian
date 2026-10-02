"""AR-010 Incident Mode: detects harm-already-happened language, jumps the replay pointer, first-hour plan, evidence list, report draft.
Never claims to contact anyone; local channels are TO BE VERIFIED (no contact details invented)."""
import re

_I = r"\bi(?:'ve| have)?\s+(?:(?:already|just|also|accidentally|have)\s+)*"
PATS = [
    ("money", "Money already sent", 3, "Financial Scam", "High", _I + r"(?:sent|paid|transferred|wired|deposited)\b[^.!?]{0,40}(?:money|cash|funds|fee|\$\s?\d|us\$|airtime|them|it)|money (?:was|has been) (?:deducted|taken|stolen)|(?:took|stole) my money"),
    ("credentials", "Credentials or codes already shared", 2, "Identity Fraud", "High", _I + r"(?:entered|typed|shared|gave|given|told|submitted|provided|replied with)\b[^.!?]{0,30}(?:otp|pin|password|code|details|id|login|card|number)"),
    ("clicked", "Link or file already opened", 2, "Malicious Link", "Medium", _I + r"(?:clicked|opened|tapped|followed|downloaded|installed)\b"),
    ("replied", "Already replied", 1, "Phishing", "Medium", _I + r"(?:replied|responded|texted back|answered|called (?:them|back))\b"),
]
PLAN = {
 "money": [("Right now", "Call your mobile-money provider or bank using the number in its official app, on your card, or on its official website — not a number from the message."),
           ("Right now", "Ask them to flag or hold the transaction and note the reference number they give you."),
           ("Within 15 minutes", "Stop all contact with the sender. Do not send more money, even for a 'refund' or 'release fee'."),
           ("Within the hour", "Change your PIN and passwords through the official app and check for other transactions."),
           ("Within the hour", "Report it to your provider and the police (local reporting channels: TO BE VERIFIED)."),
           ("Today", "Warn family or colleagues who may be targeted next.")],
 "credentials": [("Right now", "Change the PIN or password through the official service — open it yourself, not via the message."),
                 ("Right now", "Sign out other sessions and devices; turn on two-step verification."),
                 ("Within 15 minutes", "Call your provider on an official number and ask them to watch the account."),
                 ("Within the hour", "Check for transactions or changes you did not make; report any."),
                 ("Today", "Warn your contacts in case the account is used to message them.")],
 "clicked": [("Right now", "Close the page and enter nothing more. If you typed anything, treat it as shared credentials."),
             ("Right now", "If a file downloaded or an app installed, disconnect from the network."),
             ("Within the hour", "From a different, clean device change your important passwords."),
             ("Within the hour", "Scan the phone or PC with trusted security software and remove unknown apps."),
             ("Today", "Watch for follow-up calls or messages.")],
 "replied": [("Right now", "Stop replying. Block and report the sender."),
             ("Within the hour", "Do not click links or send anything; check any claim through official channels."),
             ("Today", "Expect follow-up pressure — it is part of the pattern, not a sign you owe anything.")]}
KEEP = ["The message itself (do not delete it)", "Sender number or address", "Date and time received", "Any transaction reference or receipt", "Screenshots taken on your own device", "Call logs"]
REPORT = ("On [date/time] I received a message via [channel] from [sender number/address]. It said: \"{snip}\". I [describe what you did]. "
          "Transaction reference / details: [reference]. Please advise on next steps and record this report.")
NOTICE = "Local reporting channels and provider procedures are TO BE VERIFIED — no contact details are invented here."


def detect_incident(norm_text, raw):
    for kind, title, ptr, ttype, band, rx in PATS:
        if re.search(rx, norm_text):
            snip = raw[:120].replace('"', "'")
            return {"kind": kind, "title": title, "pointer": ptr, "threat_type": ttype, "band": band,
                    "plan": [{"when": w, "step": s} for w, s in PLAN[kind]], "evidence": KEEP, "report_draft": REPORT.format(snip=snip), "notice": NOTICE}
    return None
