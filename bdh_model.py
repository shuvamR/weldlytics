# bdh_model.py
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

MODEL_PATH = "bdh_model.pkl"


def train_bdh_model():
    """Train a Random Forest classifier on synthetic welding current data."""
    np.random.seed(42)
    X = []
    y = []
    for _ in range(1000):
        if np.random.rand() > 0.3:
            current = np.random.normal(100, 15, 10)
            y.append(1)
        else:
            if np.random.rand() > 0.5:
                current = np.random.normal(160, 20, 10)
            else:
                current = np.random.normal(50, 15, 10)
            y.append(0)
        X.append(current)
    model = RandomForestClassifier(n_estimators=30, max_depth=5, random_state=42)
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
    return model


def load_or_train_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    else:
        return train_bdh_model()


model = load_or_train_model()
training_accuracy = 0.70  # Starts at 70%, improves over time
days_trained = 1


def predict_quality(current_window):
    global training_accuracy, days_trained
    if len(current_window) < 10:
        return "WAITING", 0.0, "Collecting 10 samples...", "⚙️ Initializing..."

    proba = model.predict_proba([current_window])[0]
    pred_class = 1 if proba[1] > 0.5 else 0
    confidence = proba[pred_class]
    quality = "GOOD" if pred_class == 1 else "REJECTED"

    # Simulate learning - accuracy improves over time
    if len(current_window) > 0 and np.random.rand() < 0.01:  # Slowly improve
        if training_accuracy < 0.92:
            training_accuracy = min(0.92, training_accuracy + 0.002)
            days_trained = min(30, days_trained + 1)

    # Enhanced explanation with root cause
    ideal = [100] * 10
    diffs = [abs(c - i) for c, i in zip(current_window, ideal)]
    worst_idx = np.argmax(diffs)
    deviation = current_window[worst_idx] - 100

    if quality == "REJECTED":
        if deviation > 0:
            root_cause = f"Current spike to {current_window[worst_idx]:.0f}A at {worst_idx + 1}.{worst_idx + 2}s"
            suggestion = "REDUCE CURRENT"
        else:
            root_cause = f"Current drop to {current_window[worst_idx]:.0f}A at {worst_idx + 1}.{worst_idx + 2}s"
            suggestion = "INCREASE CURRENT"
    else:
        root_cause = f"Stable arc maintained (avg {np.mean(current_window):.0f}A)"
        suggestion = "MAINTAIN STEADY ARC"

    explanation = f"{root_cause}. {suggestion}"

    return quality, confidence, explanation, suggestion