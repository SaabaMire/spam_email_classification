# Spam Email Classification

A full-stack machine-learning application that classifies an email or SMS as **spam** or **not spam**. It combines TF-IDF text features, Logistic Regression, a Flask prediction API, and a responsive browser interface.

## Features

- Analyze emails and SMS messages from a browser
- Return spam/not-spam classification with confidence scores
- Display spam and ham probabilities
- Provide ready-made examples for testing
- Expose health and prediction API endpoints
- Use a responsive interface suitable for desktop and mobile

## Model performance

The included model was evaluated on a 20% test split of the UCI SMS Spam Collection dataset.

| Metric | Score |
| --- | ---: |
| Accuracy | 96.32% |
| Spam precision | 100.00% |
| Spam recall | 72.48% |
| Spam F1 score | 84.05% |

## Technology stack

- Python and Flask
- pandas and scikit-learn
- TF-IDF text vectorization
- Logistic Regression
- Joblib model persistence
- HTML, CSS, and JavaScript
- Gunicorn for production serving

## Project structure

```text
.
├── app.py                         # Flask website and prediction API
├── code/
│   ├── spam_detection.ipynb       # Original analysis notebook
│   └── train_model.py             # Reproducible training script
├── dataset/
│   └── spam.csv                   # Training dataset
├── models/
│   ├── model_metrics.json
│   ├── spam_classifier.pkl
│   └── tfidf_vectorizer.pkl
├── static/
│   ├── app.js
│   └── style.css
├── templates/
│   └── index.html
├── Procfile
└── requirements.txt
```

## Run locally

### 1. Clone the repository

```bash
git clone https://github.com/SaabaMire/spam_email_classification.git
cd spam_email_classification
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
source .venv/bin/activate
```

### 3. Install the dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Start the application

```bash
python app.py
```

Open `http://127.0.0.1:8000`.

## Retrain the model

```bash
python code/train_model.py
```

This recreates the classifier, vectorizer, and evaluation metrics in `models/`.

## API

### Health check

```http
GET /health
```

### Classify a message

```http
POST /predict
Content-Type: application/json
```

Example request:

```json
{
  "message": "Congratulations! You have won a free cash prize. Click now."
}
```

Example response:

```json
{
  "label": "spam",
  "display_label": "Spam",
  "confidence": 92.8,
  "spam_probability": 92.8,
  "ham_probability": 7.2
}
```

## Deploy on Railway

1. Create a Railway service from this GitHub repository.
2. Leave the root directory empty.
3. Railway installs `requirements.txt` and uses the included `Procfile`:

   ```text
   web: gunicorn --bind 0.0.0.0:$PORT app:app
   ```

4. Wait for the deployment to become active.
5. Generate a public domain under **Settings → Networking**.
6. Open `/health` on the public domain to verify the model is running.

## Disclaimer

This application is an educational machine-learning project. Automated classifiers can make mistakes, so suspicious messages should still be reviewed carefully.

## Author

[SaabaMire](https://github.com/SaabaMire)
