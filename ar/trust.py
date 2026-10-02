"""AR-009 Trust Gap. Toggles are transparent rule-based GUIDANCE, not learned effects (DEC-009, DEC-025 closes OD-019)."""

RULES = ("Each confirmation can lower the band by at most one step in total; a suspicious message never falls below Medium; "
         "the warning for an irreversible ask is never hidden. Guidance only — you cannot fully verify by toggling.")


def trust_gap(label, band, irr, ents, evasion, toggles):
    t = {"sender_verified": bool((toggles or {}).get("sender_verified")), "expected": bool((toggles or {}).get("expected"))}
    if label != "Suspicious":
        missing = ["Nothing alarming found. If you still feel unsure, confirm through the official channel."]
    else:
        missing = ["No independently verifiable sender."]
        if ents["asks"]:
            missing.append(f"It asks for {ents['asks'][0]['label']} — a legitimate service would not ask for this by message.")
        if ents["urls"]:
            missing.append("The link has not been confirmed through the official service.")
        if not t["expected"]:
            missing.append("You were not expecting this message.")
        if evasion:
            missing.append("The text contains hidden or look-alike characters — a common evasion trick.")
    adj = band
    if label == "Suspicious" and (t["sender_verified"] or t["expected"]) and band == "High":
        adj = "Medium"
    return {"missing_evidence": missing,
            "verify": ["Do not use the message's link or phone number.", "Open the official app or website yourself.", "Use a phone number you already had, not one from the message."],
            "toggles": t, "adjusted_band": adj, "band_changed": adj != band,
            "warning_kept": bool(label == "Suspicious" and irr == 3), "guidance_label": "Guidance (rule-based), not a learned effect", "rules": RULES}
