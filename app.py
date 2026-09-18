import os
import re
from pathlib import Path

import joblib
from flask import Flask, jsonify, render_template, request


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "spam_classifier.pkl"
VECTORIZER_PATH = BASE_DIR / "models" / "tfidf_vectorizer.pkl"

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


def clean_message(message: str) -> str:
    return re.sub(r"[^a-zA-Z\s]", "", message.lower()).strip()


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/health")
def health():
    return jsonify({"status": "healthy", "model": "logistic_regression"})


@app.post("/predict")
def predict():
    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()

    if not message:
        return jsonify({"error": "Please enter a message to analyze."}), 400
    if len(message) > 5000:
        return jsonify({"error": "The message must contain 5,000 characters or fewer."}), 400

    cleaned = clean_message(message)
    if not cleaned:
        return jsonify({"error": "The message must contain some letters."}), 400

    features = vectorizer.transform([cleaned])
    prediction = int(model.predict(features)[0])
    probabilities = model.predict_proba(features)[0]
    class_probabilities = {
        int(label): float(probability)
        for label, probability in zip(model.classes_, probabilities)
    }
    spam_probability = class_probabilities.get(0, 0.0)
    ham_probability = class_probabilities.get(1, 0.0)

    return jsonify({
        "label": "spam" if prediction == 0 else "ham",
        "display_label": "Spam" if prediction == 0 else "Not spam",
        "confidence": round(max(spam_probability, ham_probability) * 100, 2),
        "spam_probability": round(spam_probability * 100, 2),
        "ham_probability": round(ham_probability * 100, 2),
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)
