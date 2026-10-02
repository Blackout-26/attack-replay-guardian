"""AR-007 replay engine: instantiates a curated playbook with the message's own entities. Selected by threat type; never generative."""
from .playbooks import PB, SAFE, STOP, NOTICE, LOCAL
from .dna import NAMES


def build_replay(ttype, raw, dna_tags, asks, ents, pointer=1):
    pb = PB.get(ttype)
    if not pb:
        return None
    ask = asks[0]["label"] if asks else "a decision from you"
    snippet = (raw[:140] + "…") if len(raw) > 140 else raw
    used = [t["name"] for t in dna_tags if t["strength"] != "absent" and t["tactic"] in ("urgency", "authority", "fear_loss", "reward_lure", "secrecy")]
    rec = lambda t: {"level": t[0], "text": t[1], "local": bool(t[2]) if len(t) > 2 else False}
    stages = [
        {"i": 0, "name": "Hook", "text": f"The message itself: “{snippet}” {pb['hook']}" + (f" Tactics seen: {', '.join(used)}." if used else ""), "recoverable": rec(SAFE)},
        {"i": 1, "name": "Action point", "text": pb["act"].format(ask=ask), "recoverable": rec(STOP)},
        {"i": 2, "name": "Extraction", "text": pb["ext"].format(ask=ask), "recoverable": rec(pb["r2"])},
        {"i": 3, "name": "Takeover / cash-out", "text": pb["out"], "recoverable": rec(pb["r3"])}]
    end = "You stop here: the attack needs your action to continue. Nothing lost."
    choices = {
        "click": {"pointer": 2, "text": pb["click"]},
        "reply": {"pointer": 1, "text": f"{pb['nxt']} {pb['press']}"},
        "ignore": {"pointer": 0, "text": f"You ignore it. {end}"},
        "report": {"pointer": 0, "text": f"You block and report it (to your provider or the authorities; local channels TO BE VERIFIED) and warn others. {end}"}}
    return {"playbook": ttype, "title": pb["title"], "label": NOTICE, "notice": LOCAL, "pointer": pointer, "stages": stages, "choices": choices,
            "interrupt": ["Do not act on the message.", "Open the official service yourself, or call an independently sourced number.", "Block and report the sender."]}
