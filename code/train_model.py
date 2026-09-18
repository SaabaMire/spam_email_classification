import json
import re
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split


BASE_DIR = Path(__file__).resolve().parents[1]
DATASET_PATH = BASE_DIR / "dataset" / "spam.csv"
MODELS_DIR = BASE_DIR / "models"


def clean_message(message: str) -> str:
    return re.sub(r"[^a-zA-Z\s]", "", str(message).lower())


df = pd.read_csv(DATASET_PATH)
df["Category"] = df["Category"].fillna("").astype(str).str.lower().str.strip()
df["Message"] = df["Message"].apply(clean_message)
df["Category"] = df["Category"].map({"spam": 0, "ham": 1})
df = df.dropna(subset=["Category"])

X_train, X_test, y_train, y_test = train_test_split(
    df["Message"],
    df["Category"],
    test_size=0.2,
    random_state=42,
)

vectorizer = TfidfVectorizer(stop_words="english", lowercase=True, min_df=1)
X_train_features = vectorizer.fit_transform(X_train)
X_test_features = vectorizer.transform(X_test)

model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train_features, y_train)
predictions = model.predict(X_test_features)

metrics = {
    "accuracy": round(accuracy_score(y_test, predictions), 4),
    "precision": round(precision_score(y_test, predictions, pos_label=0), 4),
    "recall": round(recall_score(y_test, predictions, pos_label=0), 4),
    "f1_score": round(f1_score(y_test, predictions, pos_label=0), 4),
}

MODELS_DIR.mkdir(exist_ok=True)
joblib.dump(model, MODELS_DIR / "spam_classifier.pkl", compress=3)
joblib.dump(vectorizer, MODELS_DIR / "tfidf_vectorizer.pkl", compress=3)
(MODELS_DIR / "model_metrics.json").write_text(
    json.dumps(metrics, indent=2),
    encoding="utf-8",
)

print(json.dumps(metrics, indent=2))
