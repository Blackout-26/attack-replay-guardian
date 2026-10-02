"""Email-specific technical evidence that text classification cannot see. Severity 1-3. Transparent rules, no allow/deny brand lists."""
import re
from urllib.parse import urlparse

SHORT = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "ow.ly", "cutt.ly", "rb.gy"}
DANGER = {".exe", ".scr", ".bat", ".cmd", ".js", ".vbs", ".ps1", ".jar", ".lnk", ".iso", ".img", ".msi", ".hta", ".apk"}
MACRO = {".docm", ".xlsm", ".pptm"}
_LOOKS_URL = re.compile(r"^(?:https?://)?[\w.-]+\.[a-z]{2,}(?:/\S*)?$", re.I)


def _host(u):
    try:
        return (urlparse(u if "://" in u else "http://" + u).hostname or "").lower()
    except ValueError:
        return ""


def _reg(h):
    p = h.split(".")
    return ".".join(p[-3:]) if len(p) >= 3 and len(p[-1]) == 2 and p[-2] in {"co", "com", "org", "net", "ac", "gov"} else ".".join(p[-2:])


def signals(m: dict) -> list:
    out = []
    add = lambda i, sev, t: out.append({"id": i, "severity": sev, "text": t})
    h = m.get("headers", {})
    if re.search(r"\b(?:spf|dkim|dmarc)=(?:fail|softfail|permerror)", h.get("auth", "") + " " + h.get("received_spf", "")):
        add("auth_fail", 2, "the sender's authentication checks (SPF/DKIM/DMARC) failed")
    fd, rd = _reg(m.get("sender", "").split("@")[-1]), _reg(m.get("reply_to", "").split("@")[-1])
    if m.get("reply_to") and m.get("sender") and fd != rd:
        add("reply_to", 2, "replies would go to a different domain than the sender's")
    dn = m.get("display", "")
    if "@" in dn and _reg(dn.split("@")[-1].strip(" >)")) != fd and fd:
        add("display_spoof", 2, "the display name shows a different address than the real sender")
    for text, href in m.get("links", []):
        hh = _host(href)
        if _LOOKS_URL.match(text or "") and hh and _reg(_host(text)) != _reg(hh):
            add("link_mismatch", 3, f"a link shows “{text[:40]}” but actually goes to {hh}"); break
    urls = [u for _, u in m.get("links", [])]
    for u in urls:
        hh = _host(u)
        if re.fullmatch(r"\d{1,3}(?:\.\d{1,3}){3}", hh):
            add("url_ip", 2, "a link points to a raw IP address"); break
    if any("xn--" in _host(u) for u in urls):
        add("url_punycode", 2, "a link uses a look-alike (punycode) domain")
    if any(_host(u) in SHORT for u in urls):
        add("url_short", 1, "a link uses a URL shortener that hides the destination")
    for fn in m.get("attachments", []):
        f = fn.lower(); ext = "." + f.rsplit(".", 1)[-1] if "." in f else ""
        if re.search(r"\.(?:pdf|docx?|xlsx?|jpe?g|png|txt)\.(?:exe|scr|js|bat|vbs|lnk|cmd)$", f):
            add("attach_double_ext", 3, f"attachment “{fn}” hides an executable behind a document name")
        elif ext in DANGER:
            add("attach_danger", 3, f"attachment “{fn}” is an executable/script file type")
        elif ext in MACRO:
            add("attach_macro", 2, f"attachment “{fn}” can contain macros")
        elif ext in {".html", ".htm"}:
            add("attach_html", 2, f"attachment “{fn}” is a web page that can capture logins")
        elif ext in {".zip", ".rar", ".7z"}:
            add("attach_archive", 1, f"attachment “{fn}” is an archive that can hide files")
    return out


def fuse(a: dict, sigs: list, text: str) -> dict:
    """Combine text verdict with technical evidence. hard = any severity-3, or two severity-2."""
    from .explain import ACTION
    from .replay import build_replay
    from .trust import trust_gap
    a["email_signals"] = sigs
    if not sigs:
        return a
    hard = any(s["severity"] == 3 for s in sigs) or sum(s["severity"] == 2 for s in sigs) >= 2
    ev = "; ".join(s["text"] for s in sigs if s["severity"] >= 2)
    if a["label"] == "Benign" and hard:
        t = "Malicious Link" if any(s["id"].startswith(("attach", "link", "url")) for s in sigs) else "Phishing"
        band = "High" if any(s["severity"] == 3 for s in sigs) else "Medium"
        a.update(label="Suspicious", threat_type=t, reason=f"The wording looks routine, but technical evidence points to trouble: {ev}.", action=ACTION[t])
        a["risk"] = {**a["risk"], "band": band, "irreversibility": 2}
        a["replay"] = build_replay(t, text, a["dna"], [], a["entities"], 1)
        a["trust_gap"] = trust_gap("Suspicious", band, 2, a["entities"], False, None)
    elif a["label"] == "Suspicious" and ev:
        a["reason"] += f" Technical evidence: {ev}."
        if hard and a["risk"]["band"] == "Medium":
            a["risk"]["band"] = "High"
    from .score import threat_score   # technical evidence changes the evidence blend, so re-score
    a["threat_score"] = threat_score(a)
    return a
