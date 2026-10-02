"""Threat likelihood score (0-100 %) for one analysed message.  DEC-028.

What it is: a transparent blend of independent pieces of evidence -- the text classifier, the manipulation
tactics found (Threat DNA), technical email evidence and a described incident. Every piece contributes a
strength between 0 and 1 and they are combined with a noisy-OR:  score = 1 - prod(1 - strength_i).
So several weak signs add up, one very strong sign (a hidden .exe, a described incident) can carry the score alone,
and a message with no evidence stays low.

What it is NOT: a calibrated probability. The classifier was trained on very little data (see reports/BASELINE_EVALUATION.md),
so the percentage is a ranking and triage aid. It never contradicts the verdict: Suspicious >= 50 %, Benign <= 49 %.
Weights below are transparent config, hand-set, and have not been fit to any held-out labels.
"""

# classifier weight: even a 100 % classifier output alone never reaches certainty
MODEL_W = 0.80
# (strength when "strong", strength when "present") per Threat-DNA tactic
TACTIC_W = {
    "credential_request": (0.55, 0.40), "payment_request": (0.50, 0.35), "suspicious_link": (0.40, 0.25),
    "secrecy": (0.35, 0.22), "synthetic_media": (0.30, 0.18), "urgency": (0.28, 0.14), "fear_loss": (0.28, 0.14),
    "reward_lure": (0.28, 0.14), "authority": (0.22, 0.12), "call_to_action": (0.06, 0.03),
}
SIGNAL_W = {3: 0.75, 2: 0.35, 1: 0.10}   # technical email evidence by severity
INCIDENT_W = 0.90                        # the person describes harm that already happened
SIGNAL_LABEL = {
    "auth_fail": "Sender checks failed", "reply_to": "Replies go to another domain", "display_spoof": "Display name shows another address",
    "link_mismatch": "Link hides its real destination", "url_ip": "Link points to a raw IP address", "url_punycode": "Look-alike domain in a link",
    "url_short": "Shortened link", "attach_double_ext": "Hidden executable attachment", "attach_danger": "Executable attachment",
    "attach_macro": "Attachment can run macros", "attach_html": "Web-page attachment", "attach_archive": "Archive attachment",
}

LEVELS = [(85, "Very likely a threat", "high"), (65, "Likely a threat", "high"), (50, "Possibly a threat", "medium"),
          (25, "Probably fine", "low"), (0, "Looks safe", "safe")]


def level_of(percent: int):
    for floor, name, tone in LEVELS:
        if percent >= floor:
            return name, tone
    return LEVELS[-1][1], LEVELS[-1][2]


def threat_score(a: dict) -> dict:
    """a = an analysis dict (needs label, internal.p_suspicious, dna, threat_type; uses email_signals / incident when present)."""
    parts = []   # (strength, key, label, detail)
    p = float((a.get("internal") or {}).get("p_suspicious") or 0.0)
    parts.append((MODEL_W * p, "classifier", "Message wording",
                  f"The text classifier leans {a.get('threat_type', 'Benign')} ({round(p * 100)}% raw model output)" if p >= 0.5
                  else f"The text classifier finds the wording mostly ordinary ({round(p * 100)}% raw model output)"))
    for d in a.get("dna") or []:
        w = TACTIC_W.get(d["tactic"])
        if w and d["strength"] != "absent":
            hits = ", ".join(sorted({e["text"].lower() for e in d["evidence"]})[:3])
            parts.append((w[0] if d["strength"] == "strong" else w[1], "tactic:" + d["tactic"], d["name"],
                          f"{d['strength'].capitalize()} in the wording: {hits}"))
    seen = set()
    for s in a.get("email_signals") or []:
        if s["id"] in seen:
            continue
        seen.add(s["id"])
        parts.append((SIGNAL_W.get(s["severity"], 0.1), "signal:" + s["id"], SIGNAL_LABEL.get(s["id"], "Technical evidence"), s["text"][0].upper() + s["text"][1:]))
    inc = a.get("incident")
    if inc:
        parts.append((INCIDENT_W, "incident", "Described incident", inc["title"]))

    miss = 1.0
    for st, *_ in parts:
        miss *= 1.0 - st
    raw = 1.0 - miss
    pct = round(raw * 100)
    suspicious = a.get("label") == "Suspicious"
    adjusted = None
    if suspicious and pct < 50:
        pct, adjusted = 50, "floor"
    elif not suspicious and pct > 49:
        pct, adjusted = 49, "cap"
    pct = max(0, min(100, pct))
    name, tone = level_of(pct)
    factors = [{"key": k, "label": lb, "detail": dt, "strength": round(st * 100)} for st, k, lb, dt in sorted(parts, key=lambda x: -x[0]) if st >= 0.05]
    return {"percent": pct, "level": name, "tone": tone, "factors": factors, "adjusted": adjusted, "method": "evidence-blend/v1",
            "note": "Evidence-based likelihood from the classifier, the tactics found and any technical evidence. A triage aid, not a guarantee."}
