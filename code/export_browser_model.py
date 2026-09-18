import json
from pathlib import Path

import joblib


BASE_DIR = Path(__file__).resolve().parents[1]
MODELS_DIR = BASE_DIR / "models"
OUTPUT_DIR = BASE_DIR / "docs"

model = joblib.load(MODELS_DIR / "spam_classifier.pkl")
vectorizer = joblib.load(MODELS_DIR / "tfidf_vectorizer.pkl")

payload = {
    "vocabulary": vectorizer.vocabulary_,
    "idf": vectorizer.idf_.tolist(),
    "coefficients": model.coef_[0].tolist(),
    "intercept": float(model.intercept_[0]),
    "classes": [int(value) for value in model.classes_],
}

OUTPUT_DIR.mkdir(exist_ok=True)
(OUTPUT_DIR / "model.json").write_text(
    json.dumps(payload, separators=(",", ":")),
    encoding="utf-8",
)

print(f"Exported browser model to {OUTPUT_DIR / 'model.json'}")
