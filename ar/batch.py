"""AR-017 /batch: CSV in -> CSV out (label,type,risk,explanation,action). Row count preserved; malformed rows survive; formula-injection safe."""
import csv
import io
from . import config as C
from .pipeline import analyze

COLS = ["label", "type", "risk", "explanation", "action"]
NAMES = ("content", "text", "message", "body", "sms", "narrative")


class BatchError(ValueError):
    def __init__(self, msg, status=400):
        super().__init__(msg); self.status = status


def safe(v):
    v = str(v)
    return "'" + v if v[:1] in ("=", "+", "-", "@", "\t", "\r") else v


def _decode(b):
    for enc in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return b.decode(enc)
        except UnicodeDecodeError:
            continue


def run_batch(data: bytes, include_input=False):
    if len(data) > C.MAX_BATCH_BYTES:
        raise BatchError("file too large", 413)
    text = _decode(data)
    if not text or not text.strip():
        raise BatchError("empty file")
    csv.field_size_limit(1_000_000)
    try:
        rows = [r for r in csv.reader(io.StringIO(text, newline="")) if r]
    except csv.Error:
        raise BatchError("could not parse CSV")
    head = [h.strip().lower() for h in rows[0]]
    ci = next((i for i, h in enumerate(head) if h in NAMES), None)
    if ci is None:
        if len(head) == 1:
            ci, body = 0, rows            # single column, no header
        else:
            raise BatchError("no content/text/message column found")
    else:
        body = rows[1:]
    if len(body) > C.MAX_BATCH_ROWS:
        raise BatchError("too many rows", 413)
    out = io.StringIO()
    w = csv.writer(out, lineterminator="\n")
    w.writerow(COLS + (["input_row"] if include_input else []))
    for r in body:
        t = r[ci].strip() if ci < len(r) else ""
        if not t or len(t) > C.MAX_CHARS:
            res = ["Unknown", "Unknown", "Low", "Input was empty, unreadable or too long to analyse.", "Review this item manually."]
        else:
            a = analyze(t, full=False)
            res = [a["label"], a["threat_type"], a["risk"]["band"], a["reason"], a["action"]]
        w.writerow([safe(x) for x in res] + ([safe(",".join(r))] if include_input else []))
    return out.getvalue().encode("utf-8"), len(body)
