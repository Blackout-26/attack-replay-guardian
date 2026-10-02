"""End-to-end analysis: normalize -> extract -> classify -> risk -> explain -> DNA -> replay -> trust gap -> incident (-> org). Deterministic, offline, no LLM."""
import threading
from . import config as C
from .normalize import normalize
from .extract import extract
from .model import load, prep
from .risk import risk
from .explain import explain
from .dna import dna as build_dna
from .replay import build_replay
from .trust import trust_gap
from .incident import detect_incident
from .org import org_view
from .score import threat_score

_lock, _art = threading.Lock(), None


def artifact():
    global _art
    with _lock:
        if _art is None:
            try:
                _art = load()
            except Exception:
                _art = False  # rules fallback
    return _art or None


def reload():
    global _art
    _art = None


def _rule_fallback(ents):
    keys = {a["key"] for a in ents["asks"]}
    if not ents["asks"]:
        return "Benign", 0.1
    t = ("Identity Fraud" if keys & {"identity", "password"} else "Financial Scam" if keys & {"money", "otp_pin"}
         else "Malicious Link" if keys & {"link", "attachment", "install"} else "Phishing")
    return t, 0.8


def analyze(text: str, full: bool = True, level: str = "normal", toggles: dict | None = None, mode: str = "citizen") -> dict:
    n = normalize(text)
    ents = extract(n)
    art, fallback = artifact(), False
    if art:
        classes = list(art["model"].classes_)
        p = art["model"].predict_proba([prep(text)])[0]
        p_susp = float(1 - p[classes.index("Benign")])
        best = max((c for c in classes if c != "Benign"), key=lambda c: p[classes.index(c)])
        suspicious = p_susp >= 0.5
        ttype = best if suspicious else "Benign"
        model_version = art["meta"]["version"]
    else:
        fallback, model_version = True, "rules-fallback"
        ttype, p_susp = _rule_fallback(ents)
        suspicious = ttype != "Benign"
    inc = detect_incident(n.text, text)
    if inc:  # DEC-024: a described incident is treated as Suspicious even if the wording alone looks benign
        if not suspicious:
            ttype, p_susp = inc["threat_type"], max(p_susp, 0.9)
        suspicious = True
    asks = ents["asks"] if suspicious else []
    rk = risk(p_susp, suspicious, asks)
    band = inc["band"] if inc else rk["band"]
    reason, action = explain(ttype, suspicious, p_susp, asks, rk["irreversibility"], level)
    if inc:
        reason = f"You describe harm that has already happened ({inc['title'].lower()}). Act now — follow the first-hour plan below." if level != "simple" else "It sounds like something bad already happened. Please follow the steps below right now."
        action = inc["plan"][0]["step"]
    out = {
        "label": "Suspicious" if suspicious else "Benign", "threat_type": ttype,
        "risk": {"band": band, "likelihood_x_irreversibility": rk["score"], "irreversibility": rk["irreversibility"]},
        "reason": reason, "action": action, "entities": {**ents, "asks": asks},
        "normalization": n.flags, "internal": {"p_suspicious": round(p_susp, 4)},
        "meta": {"model_version": model_version, "fallback_used": fallback, "llm_used": False, "deterministic": True, "reading_level": level},
    }
    if not full:
        return out
    tags = build_dna(n, ents)
    out["dna"] = tags
    ptr = inc["pointer"] if inc else 1
    out["replay"] = build_replay(ttype, text, tags, asks, ents, ptr) if suspicious else None
    out["trust_gap"] = trust_gap(out["label"], band, rk["irreversibility"], out["entities"], n.flags["evasion_signal"], toggles)
    out["incident"] = inc
    out["threat_score"] = threat_score(out)
    if mode == "org" and suspicious:
        out["org"] = org_view(ttype, ents)
    return out
