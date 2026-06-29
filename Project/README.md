# PhishGuard ML - Offline Phishing URL Detector

PhishGuard ML is a Flask web application that predicts whether a URL is safe or phishing using a locally trained Scikit-learn Random Forest model. It does not use external phishing detection APIs or paid services.

## Features

- Flask routing for Home, About, How It Works, Contact, and scan results
- Local CSV dataset in `dataset/phishing.csv`
- URL feature extraction in `feature_extraction.py`
- Random Forest training script in `train_model.py`
- Saved local model artifact: `model.pkl`
- Confidence score, risk level, and feature table
- Dark cybersecurity UI with responsive Bootstrap 5-compatible local assets
- JavaScript form validation and loading animation
- Render-friendly project structure

## Project Structure

```text
project/
├── app.py
├── requirements.txt
├── model.pkl
├── train_model.py
├── feature_extraction.py
├── dataset/
│   └── phishing.csv
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── about.html
│   ├── how.html
│   ├── result.html
│   ├── contact.html
│   ├── 404.html
│   └── 500.html
├── static/
│   ├── css/
│   ├── js/
│   └── images/
└── README.md
```

## Installation

1. Open a terminal in the `project` folder.

2. Create and activate a virtual environment.

```bash
python -m venv .venv
.venv\Scripts\activate
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies.

```bash
pip install -r requirements.txt
```

4. Train the local model.

```bash
python train_model.py
```

The script loads `dataset/phishing.csv`, extracts URL features, trains a Random Forest classifier, prints accuracy in the terminal, and saves `model.pkl`.

5. Run the Flask app.

```bash
python app.py
```

6. Visit:

```text
http://127.0.0.1:5000
```

## Render Deployment

Use these settings on Render:

- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`

For Render, add `gunicorn` to `requirements.txt` if you deploy with Gunicorn:

```text
gunicorn==22.0.0
```

Run `python train_model.py` locally before deployment so `model.pkl` is included with the project.

## Dataset Format

The CSV must contain:

```csv
url,label
https://example.com,safe
http://verify-account-example.com/login,phishing
```

Accepted labels are `safe` and `phishing`.

## Important Note

This is a portfolio and educational project. Real-world phishing defense should combine multiple signals, continuous dataset updates, user reporting, domain reputation, sandboxing, and security monitoring.
