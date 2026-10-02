"""AR-013 loading, validation, dedup and frozen group-aware splits (DEC-019)."""
import hashlib
import json
import pandas as pd
from . import config as C
from .normalize import normalize

RISK = {"Low", "Medium", "High"}


def key(text):
    return hashlib.sha1(normalize(text).text.encode()).hexdigest()[:16]


def load_released():
    """Organiser dataset -> (all rows, unique-by-normalized-text rows). Fails loudly on schema/label problems."""
    df = pd.read_csv(C.RAW)
    need = {"incident_id", "channel", "content", "threat_label", "risk_level", "recommended_action"}
    if need - set(df.columns):
        raise ValueError(f"released dataset missing columns: {need - set(df.columns)}")
    df = df.dropna(subset=["content"])
    bad = set(df.threat_label) - set(C.TYPES)
    if bad or set(df.risk_level) - RISK:
        raise ValueError(f"unexpected labels: {bad or set(df.risk_level) - RISK}")
    df["group"] = df.content.map(key)
    if (df.groupby("group").threat_label.nunique() > 1).any():
        raise ValueError("conflicting labels for identical text")
    return df, df.drop_duplicates("group").reset_index(drop=True)


def load_supplement():
    df = pd.read_csv(C.SUPP)
    if set(df.threat_label) - set(C.TYPES):
        raise ValueError("unexpected supplement labels")
    df["group"] = df.content.map(key)
    return df


def build_splits():
    """train = released-unique + supplement(train); final_test = supplement(final_test), frozen by hash."""
    _, ru = load_released()
    sp = load_supplement()
    tr = pd.concat([ru[["content", "threat_label", "group"]].assign(source="released"),
                    sp[sp.partition == "train"][["content", "threat_label", "group"]].assign(source="developer-authored")], ignore_index=True)
    te = sp[sp.partition == "final_test"][["content", "threat_label", "group"]].assign(source="developer-authored").reset_index(drop=True)
    if tr.group.duplicated().any():
        raise ValueError("duplicate groups inside train")
    if set(tr.group) & set(te.group):
        raise ValueError("LEAKAGE: identical normalized text in train and final test")
    h = hashlib.sha256("\n".join(sorted(te.content)).encode()).hexdigest()
    if C.SPLIT_FILE.exists():
        if json.loads(C.SPLIT_FILE.read_text())["final_test_sha256"] != h:
            raise ValueError("final test set changed after being frozen")
    else:
        C.SPLIT_FILE.parent.mkdir(exist_ok=True)
        C.SPLIT_FILE.write_text(json.dumps({"final_test_sha256": h, "n_final_test": len(te), "seed": C.SEED}, indent=1))
    return tr, te
