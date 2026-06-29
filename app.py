"""Flask application for local phishing URL detection."""

from __future__ import annotations

from pathlib import Path

import joblib
from flask import Flask, flash, redirect, render_template, request, url_for

from feature_extraction import FEATURE_NAMES, extract_features, is_valid_url, normalize_url


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model.pkl"

app = Flask(__name__)
app.config["SECRET_KEY"] = "replace-this-secret-before-production"


def load_model_artifact() -> dict:
    if not MODEL_PATH.exists():
        raise FileNotFoundError("model.pkl was not found. Run `python train_model.py` first.")
    return joblib.load(MODEL_PATH)


MODEL_ARTIFACT = load_model_artifact()
MODEL = MODEL_ARTIFACT["model"]
MODEL_ACCURACY = MODEL_ARTIFACT.get("accuracy")


def classify_risk(prediction: str, confidence: float) -> tuple[str, str]:
    if prediction == "Safe" and confidence >= 0.70:
        return "Safe", "green"
    if confidence < 0.75:
        return "Suspicious", "yellow"
    return "Dangerous", "red"


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        raw_url = request.form.get("url", "").strip()
        if not raw_url:
            flash("Please enter a URL before scanning.", "warning")
            return redirect(url_for("home"))

        if len(raw_url) > 2048 or not is_valid_url(raw_url):
            flash("Enter a valid URL such as https://example.com/login.", "danger")
            return redirect(url_for("home"))

        normalized_url = normalize_url(raw_url)
        features = extract_features(normalized_url)
        feature_vector = [[features[name] for name in FEATURE_NAMES]]

        probabilities = MODEL.predict_proba(feature_vector)[0]
        phishing_probability = float(probabilities[1])
        safe_probability = float(probabilities[0])

        prediction = "Phishing" if phishing_probability >= 0.50 else "Safe"
        confidence = phishing_probability if prediction == "Phishing" else safe_probability
        risk_label, risk_color = classify_risk(prediction, confidence)

        return render_template(
            "result.html",
            url=normalized_url,
            prediction=prediction,
            confidence=round(confidence * 100, 2),
            phishing_probability=round(phishing_probability * 100, 2),
            safe_probability=round(safe_probability * 100, 2),
            risk_label=risk_label,
            risk_color=risk_color,
            features=features,
            model_accuracy=round(MODEL_ACCURACY * 100, 2) if MODEL_ACCURACY is not None else None,
        )

    return render_template("index.html", model_accuracy=round(MODEL_ACCURACY * 100, 2) if MODEL_ACCURACY else None)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/how-it-works")
def how_it_works():
    return render_template("how.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True)
