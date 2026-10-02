"""Email -> normalized message dict (visible text, links, attachments, auth headers). Stdlib only. Never fetches anything."""
import email
import re
from email import policy
from email.utils import parseaddr
from html.parser import HTMLParser


class _H(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True); s.t, s.links, s._a, s.skip = [], [], None, 0

    def handle_starttag(s, tag, a):
        if tag in ("script", "style"): s.skip += 1
        if tag == "a": s._a = [dict(a).get("href") or "", []]
        if tag in ("br", "p", "div", "tr", "li"): s.t.append("\n")

    def handle_endtag(s, tag):
        if tag in ("script", "style") and s.skip: s.skip -= 1
        if tag == "a" and s._a:
            s.links.append((" ".join("".join(s._a[1]).split()), s._a[0])); s._a = None

    def handle_data(s, d):
        if s.skip: return
        s.t.append(d)
        if s._a: s._a[1].append(d)


def mk(source, sender="", subject="", text="", links=None, atts=None, headers=None, reply_to="", msg_id="", display=""):
    return {"source": source, "sender": sender, "display": display, "reply_to": reply_to, "subject": subject, "text": " ".join(str(text).split()),
            "links": links or [], "attachments": atts or [], "headers": headers or {}, "msg_id": msg_id}


def parse_email(raw: bytes, source="email") -> dict:
    m = email.message_from_bytes(raw, policy=policy.default)
    text = html_text = ""
    links, atts = [], []
    for part in m.walk():
        if part.is_multipart():
            continue
        fn = part.get_filename()
        if fn or part.get_content_disposition() == "attachment":
            atts.append(str(fn or "")); continue
        try:
            body = part.get_content()
        except Exception:
            body = (part.get_payload(decode=True) or b"").decode("utf-8", "replace")
        if not isinstance(body, str):
            continue
        ct = part.get_content_type()
        if ct == "text/plain" and not text:
            text = body
        elif ct == "text/html":
            h = _H(); h.feed(body); links += h.links; html_text = html_text or "".join(h.t)
    name, addr = parseaddr(str(m.get("from") or ""))
    hdr = {"auth": " ".join(str(x) for x in m.get_all("Authentication-Results", [])).lower(), "received_spf": str(m.get("Received-SPF") or "").lower()}
    return mk(source, addr.lower(), str(m.get("subject") or ""), text or html_text, links, atts, hdr,
              parseaddr(str(m.get("reply-to") or ""))[1].lower(), str(m.get("message-id") or ""), name)
