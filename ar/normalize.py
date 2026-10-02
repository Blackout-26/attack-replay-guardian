"""AR-014 baseline normalization with an offset map back to the user's original text."""
import re
import unicodedata
from dataclasses import dataclass, field

ZW = frozenset("\u200b\u200c\u200d\u2060\ufeff\u00ad\u200e\u200f")
HOMO = {  # Cyrillic / Greek look-alikes -> Latin
    "а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "х": "x", "у": "y", "і": "i", "ј": "j", "ѕ": "s",
    "к": "k", "м": "m", "н": "h", "т": "t", "в": "b", "α": "a", "ο": "o", "ε": "e", "ρ": "p", "ν": "v", "ι": "i", "κ": "k", "τ": "t",
}
_DEFANG = [
    (re.compile(r"h(?:xx|tt)p(s?)://"), lambda m: f"http{m.group(1)}://"),
    (re.compile(r"\[\s*://\s*\]"), lambda m: "://"),
    (re.compile(r"\[\s*\.\s*\]|\(\s*\.\s*\)|\{\s*\.\s*\}|\[\s*dot\s*\]|\(\s*dot\s*\)"), lambda m: "."),
    (re.compile(r"\s+"), lambda m: " "),
    (re.compile(r"^ | $"), lambda m: ""),
]


@dataclass
class Norm:
    raw: str
    text: str
    map: list = field(repr=False)
    flags: dict = field(default_factory=dict)

    def orig_span(self, s, e):
        """Map a span in normalized text back to (start, end) in the raw text."""
        return self.map[s], self.map[e - 1] + 1


def _sub(text, m, pat, fn):
    out, om, pos = [], [], 0
    for x in pat.finditer(text):
        s, e = x.span()
        out.append(text[pos:s]); om.extend(m[pos:s])
        r = fn(x); out.append(r)
        om.extend(m[min(s + k, e - 1)] for k in range(len(r)))
        pos = e
    out.append(text[pos:]); om.extend(m[pos:])
    return "".join(out), om


def normalize(raw: str) -> Norm:
    chars, m, zw, hg = [], [], 0, 0
    for i, ch in enumerate(raw):
        if ch in ZW:
            zw += 1
            continue
        for c in unicodedata.normalize("NFKC", ch):
            if c in HOMO:
                c, hg = HOMO[c], hg + 1
            for l in c.lower():
                chars.append(l); m.append(i)
    text = "".join(chars)
    for pat, fn in _DEFANG:
        text, m = _sub(text, m, pat, fn)
    return Norm(raw, text, m, {"zero_width": zw, "homoglyph": hg, "evasion_signal": bool(zw or hg)})
