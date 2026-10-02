"""AR-016 /analyze, AR-017 /batch. Stateless; never logs message bodies; never fetches URLs from input (AR-030)."""
from pathlib import Path
import os, secrets, time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
import csv, io
from datetime import datetime
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from . import config as C
from .batch import run_batch, BatchError
from .pipeline import analyze, artifact

from .guardian import runtime as RT, config as G
from .guardian.samples import SAMPLES
from .emailparse import mk
from .trust import trust_gap


@asynccontextmanager
async def lifespan(app):
    if os.environ.get("AR_GUARDIAN") == "1":
        RT.get().start_monitors()
    yield
    if RT._rt: RT._rt.stop()


app = FastAPI(title="Attack Replay Guardian", version=C.VERSION, docs_url="/docs", lifespan=lifespan)


class AnalyzeIn(BaseModel):
    text: str
    sender: str | None = None     # optional; not used by the baseline (dataset has no reliable sender field)
    channel: str | None = None
    expected: bool | None = None
    sender_verified: bool | None = None
    reading_level: str = "normal"   # technical | normal | simple
    mode: str = "citizen"           # citizen | org


def err(msg, status=400):  # noqa
    return JSONResponse({"error": msg}, status_code=status)


@app.exception_handler(RequestValidationError)
async def _v(request, exc):  # deliberately does NOT echo the submitted input
    return err("invalid request: 'text' (string) is required")


@app.get("/health")
def health():
    a = artifact()
    return {"status": "ok", "model": a["meta"]["version"] if a else "rules-fallback", "llm_used": False, "offline": True}


@app.post("/analyze")
def analyze_ep(body: AnalyzeIn):
    t = body.text.strip()
    if not t:
        return err("text is empty")
    if len(t) > C.MAX_CHARS:
        return err(f"text exceeds {C.MAX_CHARS} characters", 413)
    lv = body.reading_level if body.reading_level in ("technical", "normal", "simple") else "normal"
    return analyze(t, level=lv, toggles={"expected": body.expected, "sender_verified": body.sender_verified}, mode="org" if body.mode == "org" else "citizen")


@app.middleware("http")
async def guard(request: Request, call_next):
    host = (request.headers.get("host") or "").split(":")[0]
    if RT.get().cfg["bind"] in ("127.0.0.1", "localhost") and host not in ("127.0.0.1", "localhost", "testserver"):
        return JSONResponse({"error": "bad host"}, status_code=403)   # DNS-rebinding defence
    if request.method == "POST" and request.url.path.startswith("/api/") and request.headers.get("x-ar-token") != RT.get().token:
        return JSONResponse({"error": "missing or bad token"}, status_code=403)   # CSRF defence: token is only readable same-origin
    r = await call_next(request)
    r.headers.update({"X-Content-Type-Options": "nosniff", "Referrer-Policy": "no-referrer", "X-Frame-Options": "DENY",
                      "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self'; img-src 'self' data:"})
    return r


def _pub(a): return {k: v for k, v in a.items() if k != "payload"}


@app.get("/api/session")
def session(): return {"token": RT.get().token}


@app.get("/api/status")
def status():
    r = RT.get()
    return {"protection": "on" if r.monitors else "manual", "version": C.VERSION, "monitors": [m.status for m in r.monitors], "counts": r.store.counts(),
            "report_mode": r.cfg["report_mode"], "notify_min_risk": r.cfg["notify_min_risk"], "report_channels": {"webhook": bool(r.cfg["report"]["webhook"]), "email": bool(r.cfg["report"]["to"])},
            "watch_dirs": r.cfg["watch_dirs"], "llm_used": False, "offline": True}


@app.get("/api/alerts")
def alerts(status: str | None = None, limit: int = 100): return [_pub(a) for a in RT.get().store.list(min(limit, 500), status)]


@app.get("/api/alerts/{aid}")
def alert(aid: str):
    a = RT.get().store.get(aid)
    return a if a else err("not found", 404)


def _cell(v):   # CSV-injection guard: sender/subject are attacker-controlled and the file will be opened in a spreadsheet
    v = "" if v is None else str(v)
    return "'" + v if v[:1] in ("=", "+", "-", "@", "\t", "\r") else v


@app.get("/api/alerts.csv")
def alerts_csv():
    out = io.StringIO(); w = csv.writer(out)
    w.writerow(["id", "time", "source", "sender", "subject", "threat_type", "threat_likelihood_percent", "risk", "status", "reason", "action"])
    for a in RT.get().store.list(5000):
        w.writerow([a["id"], datetime.fromtimestamp(a["ts"]).isoformat(timespec="seconds"), *(_cell(a[k]) for k in ("source", "sender", "subject", "threat_type", "score", "risk", "status", "reason", "action"))])
    return Response(out.getvalue(), media_type="text/csv", headers={"Content-Disposition": 'attachment; filename="attack-replay-alerts.csv"'})


@app.get("/api/overview")
def overview(): return RT.get().store.overview()


@app.post("/api/alerts/{aid}/trust")
async def alert_trust(aid: str, request: Request):
    """Re-run the Trust Gap what-if for a STORED alert. Uses the stored (email-evidence-aware) band, so toggles never lose the technical evidence."""
    al = RT.get().store.get(aid)
    if not al: return err("not found", 404)
    d, a = await request.json(), al["payload"]["analysis"]
    tg = trust_gap(a["label"], a["risk"]["band"], a["risk"]["irreversibility"], a["entities"], a["normalization"]["evasion_signal"], {"expected": d.get("expected"), "sender_verified": d.get("sender_verified")})
    return tg


@app.post("/api/alerts/{aid}/reopen")
def reopen(aid: str):
    if not RT.get().store.get(aid): return err("not found", 404)
    RT.get().store.set_status(aid, "new"); return {"ok": True}


@app.post("/api/alerts/{aid}/safe")
def safe(aid: str):
    RT.get().store.set_status(aid, "safe"); return {"ok": True}


@app.post("/api/alerts/{aid}/report")
def report(aid: str):
    res = RT.get().g.report(aid)
    return res if res else err("not found", 404)


@app.post("/api/settings")
async def settings(request: Request):
    r, d = RT.get(), await request.json()
    if d.get("report_mode") in ("ask", "auto", "off"): r.cfg["report_mode"] = d["report_mode"]
    if d.get("notify_min_risk") in ("Medium", "High"): r.cfg["notify_min_risk"] = d["notify_min_risk"]
    w = d.get("report_webhook")
    if isinstance(w, str) and (w == "" or w.startswith(("http://", "https://"))): r.cfg["report"]["webhook"] = w.strip()
    G.save(r.cfg); return {"ok": True}


@app.post("/api/simulate")
async def simulate(request: Request):
    d = await request.json(); sp = SAMPLES.get(d.get("sample"))
    if not sp: return err("unknown sample")
    m = mk("simulated:" + sp["source"], sp["sender"], sp["subject"], sp["text"], sp.get("links"), sp.get("atts"), {"auth": sp.get("auth", ""), "received_spf": ""}, sp.get("reply_to", ""), msg_id=secrets.token_hex(6))
    al = RT.get().g.handle(m)
    return {"flagged": bool(al), "alert": al}


@app.get("/api/samples")
def samples(): return {k: v["label"] for k, v in SAMPLES.items()}


class IngestIn(BaseModel):
    text: str
    sender: str = ""
    subject: str = ""
    source: str = "ingest"


@app.post("/ingest")
def ingest(body: IngestIn, request: Request):
    """Webhook for phone SMS-forwarder apps and other tools. Bearer token from config.json -> ingest_token."""
    if request.headers.get("authorization", "") != "Bearer " + RT.get().cfg["ingest_token"]:
        return err("unauthorized", 401)
    if len(body.text) > C.MAX_CHARS: return err("text too long", 413)
    al = RT.get().g.handle(mk("ingest:" + body.source[:30], body.sender[:200], body.subject[:200], body.text, msg_id=secrets.token_hex(6)))
    return {"flagged": bool(al), "alert_id": al["id"] if al else None, "risk": al["band"] if al else None}


@app.post("/batch")
async def batch_ep(request: Request, include_input: bool = False):
    cl = request.headers.get("content-length")
    if cl and cl.isdigit() and int(cl) > C.MAX_BATCH_BYTES + 10_000:
        return err("file too large", 413)
    ct = request.headers.get("content-type", "")
    if ct.startswith("multipart/"):
        form = await request.form()
        f = form.get("file")
        if f is None or not hasattr(f, "read"):
            return err("multipart upload needs a 'file' field")
        data = await f.read()
    else:
        data = await request.body()
    try:
        out, n = run_batch(data, include_input)
    except BatchError as e:
        return err(str(e), e.status)
    return Response(out, media_type="text/csv", headers={"Content-Disposition": 'attachment; filename="results.csv"', "X-Row-Count": str(n)})


WEB = Path(C.ROOT) / "web"
if WEB.exists():
    app.mount("/", StaticFiles(directory=WEB, html=True), name="web")
