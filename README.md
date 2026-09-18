# Spam Email Classification

A machine-learning application that classifies an email or SMS as **spam** or **not spam**. Its free GitHub Pages version runs TF-IDF and Logistic Regression directly in the browser, so it does not need a paid server.

## Features

- Analyze emails and SMS messages from a browser
- Return spam/not-spam classification with confidence scores
- Display spam and ham probabilities
- Provide ready-made examples for testing
- Expose health and prediction API endpoints
- Use a responsive interface suitable for desktop and mobile
- Run privately in the browser without sending message text to a server

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
├── docs/                          # Free GitHub Pages application
│   ├── index.html
│   ├── app.js
│   ├── style.css
│   └── model.json
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

## Deploy free with GitHub Pages

1. Open this repository on GitHub.
2. Select **Settings → Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**.
4. Select the `main` branch and the `/docs` folder.
5. Click **Save**.
6. Wait for GitHub to publish the site at:

   ```text
   https://saabamire.github.io/spam_email_classification/
   ```

GitHub Pages is the recommended deployment for this project because it is free and the exported model runs entirely in JavaScript. The Flask version remains available for local use or optional server deployment.

## Disclaimer

This application is an educational machine-learning project. Automated classifiers can make mistakes, so suspicious messages should still be reviewed carefully.

## Author

[SaabaMire](https://github.com/SaabaMire)
