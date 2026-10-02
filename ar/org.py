"""AR-027 Organisation mode: ATT&CK-style tags, indicators, containment. Mapping is INDICATIVE — verify technique IDs before publishing."""
from urllib.parse import urlparse

TAGS = {
 "Phishing": [("Initial Access", "TA0001"), ("Phishing", "T1566"), ("Credential Access", "TA0006")],
 "Financial Scam": [("Initial Access", "TA0001"), ("Phishing", "T1566"), ("Financial Theft", "T1657")],
 "Identity Fraud": [("Initial Access", "TA0001"), ("Phishing for Information", "T1598"), ("Credential Access", "TA0006")],
 "Malicious Link": [("Initial Access", "TA0001"), ("Phishing: Link/Attachment", "T1566.001/.002"), ("User Execution", "T1204")],
 "AI-Enabled Threat": [("Initial Access", "TA0001"), ("Impersonation", "T1656"), ("Financial Theft", "T1657")]}
CONTAIN = ["Block the listed domains/numbers at the mail, web and SMS gateways.", "Reset credentials of any user who interacted; revoke active sessions.",
           "Search mailboxes/logs for the same sender, wording and URL; remove matches.", "Notify staff with the Replay view so they recognise the pattern.", "Preserve the original message and headers before deleting anything."]


def org_view(ttype, ents):
    doms = sorted({urlparse(u["value"] if "://" in u["value"] else "http://" + u["value"]).netloc for u in ents["urls"]})
    return {"note": "ATT&CK-style, indicative mapping; verify IDs before publishing.",
            "tags": [{"name": n, "id": i} for n, i in TAGS.get(ttype, [])],
            "indicators": {"domains": doms, "phones": [p["value"] for p in ents["phones"]], "asks": [a["key"] for a in ents["asks"]]},
            "containment": CONTAIN}
