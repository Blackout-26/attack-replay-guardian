"""Mock SERVICE-PROVIDER intake console for demos (what a mobile operator / ISP / mail provider would see).  python scripts/provider_console.py  -> http://127.0.0.1:8788"""
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import uvicorn

app, R = FastAPI(), []


@app.post("/intake")
async def intake(req: Request):
    d = await req.json(); R.insert(0, d); return {"received": True, "case_id": f"CASE-{len(R):04d}"}


@app.get("/reports")
def reports(): return R


@app.get("/", response_class=HTMLResponse)
def page():
    return """<!doctype html><meta charset=utf-8><title>Provider intake</title><body style="font:15px system-ui;background:#0b1020;color:#e8ecf8;max-width:900px;margin:20px auto">
<h2>Service-provider fraud desk — incoming reports</h2><div id=r></div><script>
const e=s=>String(s??'').replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
async function L(){const d=await fetch('/reports').then(r=>r.json());document.getElementById('r').innerHTML=d.length?d.map(x=>`<div style="background:#141b33;border:1px solid #2a3563;border-radius:10px;padding:10px;margin:8px 0"><b>${e(x.verdict.threat_type)}</b> — ${e(x.verdict.risk)} risk · ${e(x.message.source)} · ${e(x.generated_at)}<br>${e(x.verdict.reason)}<br><small>Sender: ${e(x.evidence.indicators.sender)} · domains: ${e((x.evidence.indicators.domains||[]).join(', ')||'—')}<br>Evidence: ${e((x.evidence.technical_signals||[]).join('; ')||'text analysis')}<br>Excerpt (redacted): ${e(x.message.excerpt)}</small></div>`).join(''):'<p>No reports yet.</p>'}L();setInterval(L,3000)</script>"""


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8788, log_level="warning")
