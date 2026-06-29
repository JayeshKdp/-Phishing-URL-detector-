"""Train and save the local phishing URL detection model."""

from __future__ import annotations

import csv
from pathlib import Path

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

from feature_extraction import FEATURE_NAMES, extract_features


BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "dataset" / "phishing.csv"
MODEL_PATH = BASE_DIR / "model.pkl"


def load_dataset() -> list[dict[str, str]]:
    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATASET_PATH}")

    with DATASET_PATH.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        required_columns = {"url", "label"}
        missing = required_columns - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Dataset is missing required columns: {', '.join(sorted(missing))}")

        dataset = []
        for row in reader:
            url = (row.get("url") or "").strip()
            label = (row.get("label") or "").strip().lower()
            if url and label in {"safe", "phishing"}:
                dataset.append({"url": url, "label": label})

    if not dataset:
        raise ValueError("Dataset does not contain any usable safe/phishing rows.")

    return dataset


def build_feature_matrix(dataset: list[dict[str, str]]) -> tuple[list[list[int]], list[int]]:
    feature_rows = [extract_features(row["url"]) for row in dataset]
    features = [[row[name] for name in FEATURE_NAMES] for row in feature_rows]
    labels = [0 if row["label"] == "safe" else 1 for row in dataset]
    return features, labels


def train_model() -> None:
    dataset = load_dataset()
    features, labels = build_feature_matrix(dataset)

    stratify = labels if len(set(labels)) > 1 else None
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        labels,
        test_size=0.25,
        random_state=42,
        stratify=stratify,
    )

    model = RandomForestClassifier(
        n_estimators=250,
        max_depth=12,
        min_samples_leaf=2,
        random_state=42,
        class_weight="balanced",
    )
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    accuracy = accuracy_score(y_test, predictions)

    print(f"Training samples: {len(x_train)}")
    print(f"Testing samples: {len(x_test)}")
    print(f"Model accuracy: {accuracy:.2%}")
    print("\nClassification report:")
    print(classification_report(y_test, predictions, target_names=["Safe", "Phishing"]))

    joblib.dump(
        {
            "model": model,
            "feature_names": FEATURE_NAMES,
            "accuracy": accuracy,
        },
        MODEL_PATH,
    )
    print(f"\nSaved trained model to: {MODEL_PATH}")


if __name__ == "__main__":
    train_model()
