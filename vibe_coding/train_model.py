from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "storepurchasedata_large.csv"
MODEL_PATH = ROOT / "model" / "purchase_model.joblib"
FEATURES = ["Age", "Salary"]
TARGET = "Purchased"


def main() -> None:
    data = pd.read_csv(DATA_PATH)
    required_columns = FEATURES + [TARGET]
    missing_columns = set(required_columns) - set(data.columns)
    if missing_columns:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing_columns)}")
    if data[required_columns].isnull().any().any():
        raise ValueError("Dataset contains missing values in the required columns.")

    X = data[FEATURES]
    y = data[TARGET]
    if set(y.unique()) != {0, 1}:
        raise ValueError(f"{TARGET} must contain both binary labels 0 and 1.")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    model = make_pipeline(
        StandardScaler(),
        LogisticRegression(random_state=42, max_iter=1000),
    )
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    print(f"Holdout accuracy: {accuracy_score(y_test, predictions):.3f}")
    print(classification_report(y_test, predictions, zero_division=0))

    model.fit(X, y)
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "features": FEATURES}, MODEL_PATH)
    print(f"Saved trained model to {MODEL_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
