from math import isfinite
from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, jsonify, render_template, request


MODEL_PATH = Path(__file__).resolve().parent / "model" / "purchase_model.joblib"


def create_app(model_path: Path = MODEL_PATH) -> Flask:
    if not model_path.is_file():
        raise FileNotFoundError(
            f"Trained model not found at {model_path}. Run `python train_model.py` first."
        )

    artifact = joblib.load(model_path)
    model = artifact["model"]
    features = artifact["features"]

    app = Flask(__name__)

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.post("/predict")
    def predict():
        customer = request.get_json(silent=True)
        if not isinstance(customer, dict):
            return jsonify({"error": "Request body must be a JSON object."}), 400

        values = {}
        for field in features:
            value = customer.get(field.lower())
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return jsonify({"error": f"'{field.lower()}' must be a number."}), 400
            if not isfinite(value) or value < 0:
                return jsonify(
                    {"error": f"'{field.lower()}' must be a finite, non-negative number."}
                ), 400
            values[field] = value

        row = pd.DataFrame([[values[field] for field in features]], columns=features)
        prediction = int(model.predict(row)[0])
        probability = float(model.predict_proba(row)[0, 1])
        return jsonify(
            {
                "prediction": prediction,
                "will_purchase": bool(prediction),
                "purchase_probability": probability,
            }
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
