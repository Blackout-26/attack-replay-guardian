from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data/raw/Cyber_Shield_Training_Dataset.csv"
SUPP = ROOT / "data/supplement/dev_supplement.csv"
SPLIT_FILE = ROOT / "data/splits/split_v1.json"
MODEL_FILE = ROOT / "models/attack_replay_v1.joblib"
REPORTS = ROOT / "reports"

VERSION = "0.1.0-sprint1"
SEED = 42
TYPES = ["Phishing", "Financial Scam", "Identity Fraud", "Malicious Link", "AI-Enabled Threat", "Benign"]  # frozen: DEC-018
MAX_CHARS = 5000            # provisional (OD-018)
MAX_BATCH_BYTES = 5_000_000
MAX_BATCH_ROWS = 20_000
# Risk engine (DEC-008): score = ((P(suspicious) * irreversibility) / 3)
BAND_HIGH, BAND_MED = 0.70, 0.25
