"""AR-004 risk = likelihood x irreversibility of the ask (DEC-008). Transparent, rule-based; not fit to risk labels (only 12 unique messages)."""
from . import config as C

IRR_PHRASE = {3: "something you can't take back", 2: "something that is costly to undo", 1: "a reply that keeps you talking to the sender"}


def risk(p_susp: float, suspicious: bool, asks: list) -> dict:
    if not suspicious:
        return {"band": "Low", "irreversibility": 0, "score": 0.0}
    irr = max((a["irr"] for a in asks), default=1)
    score = ((p_susp * irr) / 3)
    band = "High" if score >= C.BAND_HIGH else "Medium"  # a suspicious message is never rated Low
    return {"band": band, "irreversibility": irr, "score": round(score, 3)}
