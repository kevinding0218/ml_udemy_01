import argparse
from pathlib import Path

import joblib
import pandas as pd


MODEL_PATH = Path(__file__).resolve().parent / "model" / "purchase_model.joblib"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Predict whether a customer will make a purchase."
    )
    parser.add_argument("age", type=float, help="Customer age")
    parser.add_argument("salary", type=float, help="Customer salary")
    args = parser.parse_args()

    if args.age < 0:
        parser.error("age must be non-negative")
    if args.salary < 0:
        parser.error("salary must be non-negative")
    if not MODEL_PATH.exists():
        parser.error("trained model not found; run `python train_model.py` first")

    artifact = joblib.load(MODEL_PATH)
    features = artifact["features"]
    customer = pd.DataFrame([[args.age, args.salary]], columns=features)
    model = artifact["model"]
    prediction = int(model.predict(customer)[0])
    probability = float(model.predict_proba(customer)[0, 1])

    outcome = "will purchase" if prediction == 1 else "will not purchase"
    print(f"Prediction: customer {outcome}")
    print(f"Purchase probability: {probability:.1%}")


if __name__ == "__main__":
    main()
