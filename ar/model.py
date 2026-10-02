"""AR-002 / AR-019 baseline: char n-gram + word TF-IDF -> logistic regression, sigmoid-calibrated."""
import joblib
import numpy as np
import sklearn
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import FeatureUnion, Pipeline
from . import config as C
from .normalize import normalize
from .extract import extract, cue_tokens


def basic_prep(raw: str) -> str:
    """Un-hardened preprocessing (lowercase + whitespace only). Used ONLY as the Arena 'before patch' baseline."""
    return " ".join(raw.lower().split())


def prep(raw: str, hardened: bool = True) -> str:
    if not hardened:
        return basic_prep(raw)
    n = normalize(raw)
    return n.text + " ||| " + cue_tokens(n, extract(n))


def make(C_=10.0, calibrate=True):
    pipe = Pipeline([
        ("f", FeatureUnion([("c", TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), sublinear_tf=True)),
                            ("w", TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True))])),
        ("lr", LogisticRegression(C=C_, max_iter=3000, class_weight="balanced", random_state=C.SEED))])
    return CalibratedClassifierCV(pipe, method="sigmoid", cv=StratifiedKFold(3, shuffle=True, random_state=C.SEED)) if calibrate else pipe


def fit(texts, labels, C_=10.0, calibrate=True, hardened=True):
    m = make(C_, calibrate)
    m.fit([prep(t, hardened) for t in texts], list(labels))
    return m


def proba(model, texts, hardened=True):
    return model.predict_proba([prep(t, hardened) for t in texts]), list(model.classes_)


def save(model, meta):
    C.MODEL_FILE.parent.mkdir(exist_ok=True)
    joblib.dump({"model": model, "meta": {**meta, "sklearn": sklearn.__version__, "seed": C.SEED, "version": C.VERSION}}, C.MODEL_FILE)


def load():
    return joblib.load(C.MODEL_FILE)
