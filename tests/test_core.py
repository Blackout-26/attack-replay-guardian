import csv, io, socket
import pytest
from ar.normalize import normalize
from ar.extract import extract
from ar.risk import risk
from ar.explain import explain, ACTION
from ar.pipeline import analyze
from ar import config as C
from ar.data import build_splits, load_released

SAMPLES = ["Cl\u200bick hxxp://wallet-verify[.]example NOW", "Your аccоunt is  locked", "Ｓｅｎｄ your PIN", "plain text", "  spaced   out  ", "ﬁle \u00a0 x"]


@pytest.mark.parametrize("s", SAMPLES)
def test_normalize_idempotent(s):
    a = normalize(s)
    assert normalize(a.text).text == a.text


@pytest.mark.parametrize("s", SAMPLES)
def test_offsets_valid_and_monotonic(s):
    n = normalize(s)
    assert len(n.map) == len(n.text)
    assert all(0 <= i < len(s) for i in n.map) and n.map == sorted(n.map)


def test_offsets_point_at_original_words():
    raw = "Please  SEND your PIN now"
    n = normalize(raw); s = n.text.index("pin")
    a, b = n.orig_span(s, s + 3)
    assert raw[a:b] == "PIN"


def test_evasion_flags_and_defang():
    n = normalize("Cl\u200bick hxxp://a[.]example and аpple")
    assert n.flags["zero_width"] == 1 and n.flags["homoglyph"] >= 1
    assert "http://a.example" in n.text


def test_extraction_entities_and_no_fetch():
    e = extract(normalize("Pay US$50 to +263 77 123 4567 or visit hxxp://pay-now[.]example/x"))
    assert e["amounts"] and e["phones"] and e["urls"][0]["value"].startswith("http://pay-now.example")


@pytest.mark.parametrize("txt,key", [
    ("Send your PIN so that our agent can reverse the transaction.", "otp_pin"),
    ("Reply with your password.", "password"),
    ("Please send it back to this number.", "money"),
    ("Install the security update now.", "install"),
])
def test_asks_detected(txt, key):
    assert key in [a["key"] for a in extract(normalize(txt))["asks"]]


@pytest.mark.parametrize("txt", ["Your OTP is 482913. Do not share this code with anyone.", "Never share your PIN with anyone.",
                                  "Please bring your identification.", "Log in through the usual student portal."])
def test_legitimate_mentions_are_not_asks(txt):
    assert [a for a in extract(normalize(txt))["asks"] if a["irr"] == 3 and a["key"] != "login"] == []


def _ask(k, irr): return [{"key": k, "irr": irr, "label": "x"}]


def test_risk_rule_consistency_otp_ge_click_ge_reply():
    b = {"Low": 0, "Medium": 1, "High": 2}
    for p in (0.5, 0.7, 0.9, 0.99):
        o, c, r = (b[risk(p, True, _ask(k, i))["band"]] for k, i in (("otp_pin", 3), ("link", 2), ("reply", 1)))
        assert o >= c >= r


def test_risk_monotonic_and_bounds():
    s = [risk(p / 10, True, _ask("otp_pin", 3))["score"] for p in range(5, 11)]
    assert s == sorted(s)
    assert risk(0.01, False, [])["band"] == "Low"
    assert risk(0.5, True, [])["band"] in ("Medium", "High")   # suspicious is never Low


@pytest.mark.parametrize("t", [t for t in C.TYPES if t != "Benign"])
def test_explanation_names_both_factors_and_action_exists(t):
    reason, action = explain(t, True, 0.9, [{"key": "money", "label": "money", "irr": 3}], 3)
    assert "Likely" in reason and "can't take back" in reason and action == ACTION[t]


def test_every_type_has_action():
    assert set(ACTION) == set(C.TYPES)


REG = [("URGENT: Your mobile wallet has been flagged. Confirm your PIN within 30 minutes or it will be suspended: hxxp://wallet-verify[.]example", "Suspicious", "High"),
       ("Sorry, I sent you money by mistake. Please send it back to this number, I am in a hurry.", "Suspicious", None),
       ("Your electricity account is overdue. Pay now to avoid disconnection: hxxp://pay-utility[.]example", "Suspicious", None),
       ("Your appointment at the clinic is confirmed for Tuesday at 10:00. Please bring your identification.", "Benign", "Low"),
       ("Your OTP is 482913. Do not share this code with anyone. It expires in 5 minutes.", "Benign", "Low")]


@pytest.mark.parametrize("t,label,band", REG)
def test_regression_demo_messages(t, label, band):
    a = analyze(t)
    assert a["label"] == label and (band is None or a["risk"]["band"] == band)
    assert analyze(t) == a  # deterministic


def test_released_dataset_shape_and_split_integrity():
    allr, uniq = load_released()
    assert len(allr) == 100 and len(uniq) == 12
    tr, te = build_splits()
    assert not (set(tr.group) & set(te.group)) and len(te) == 30


def test_pipeline_offline(monkeypatch):
    def boom(*a, **k): raise AssertionError("network access attempted")
    monkeypatch.setattr(socket.socket, "connect", boom)
    a = analyze("Click http://example.invalid/security-check to restore your account immediately.")
    assert a["meta"]["llm_used"] is False and a["label"] == "Suspicious"


def test_hostile_and_non_latin_inputs_do_not_crash():
    for t in ["<script>alert(1)</script>", "'; DROP TABLE x;--", "Здравствуйте, ваш счёт заблокирован", "مرحبا", "\u200b" * 50 + "hi", "a" * 4000, "😀" * 300]:
        assert analyze(t)["label"] in ("Suspicious", "Benign")
