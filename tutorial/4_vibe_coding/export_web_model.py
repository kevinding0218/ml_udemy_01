import json
from pathlib import Path

import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "model" / "purchase_model.joblib"
WEB_MODEL_PATH = ROOT / "docs" / "model.json"


def main() -> None:
    if not MODEL_PATH.is_file():
        raise FileNotFoundError(
            f"Trained model not found at {MODEL_PATH}. Run `python train_model.py` first."
        )

    artifact = joblib.load(MODEL_PATH)
    pipeline = artifact["model"]
    scaler = next(
        (step for _, step in pipeline.steps if isinstance(step, StandardScaler)), None
    )
    classifier = next(
        (step for _, step in pipeline.steps if isinstance(step, LogisticRegression)), None
    )
    if scaler is None or classifier is None or classifier.classes_.tolist() != [0, 1]:
        raise ValueError("Expected a StandardScaler and binary LogisticRegression model.")

    WEB_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    web_model = {
        "features": artifact["features"],
        "means": scaler.mean_.tolist(),
        "scales": scaler.scale_.tolist(),
        "coefficients": classifier.coef_[0].tolist(),
        "intercept": float(classifier.intercept_[0]),
    }
    WEB_MODEL_PATH.write_text(json.dumps(web_model, indent=2) + "\n", encoding="utf-8")
    print(f"Exported browser model to {WEB_MODEL_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
