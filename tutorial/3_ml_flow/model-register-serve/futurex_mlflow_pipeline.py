import numpy as np
import pandas as pd
import mlflow
import mlflow.sklearn

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

# ============================================================
# Configure MLflow
# ============================================================
mlflow.set_tracking_uri("http://127.0.0.1:5000/")
mlflow.set_experiment("futurexskill mlflow demo 4")

# Enable automatic logging
mlflow.sklearn.autolog()

# ============================================================
# Load Dataset
# ============================================================
DATA_URL = "https://raw.githubusercontent.com/futurexskill/ml-model-deployment/main/storepurchasedata.csv"

training_data = pd.read_csv(DATA_URL)
print("Loaded training data from GitHub")

# Features and Target
X = training_data.iloc[:, :-1].values
y = training_data.iloc[:, -1].values

# ============================================================
# Split Dataset
# ============================================================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.60,
    random_state=0
)

# ============================================================
# Feature Scaling
# ============================================================
sc = StandardScaler()

X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

print("Completed Feature Scaling")

# ============================================================
# Models to Compare
# ============================================================
models = {
    "Logistic Regression": LogisticRegression(
        max_iter=500,
        random_state=0
    ),

    "K-Nearest Neighbors": KNeighborsClassifier(
        n_neighbors=5,
        metric="minkowski",
        p=2
    ),

    "Decision Tree": DecisionTreeClassifier(
        random_state=0
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        random_state=0
    )
}

# ============================================================
# Variables to Track Best Model
# ============================================================
results = {}

best_model = None
best_model_name = None
best_accuracy = 0.0

# ============================================================
# Train Models and Track with MLflow
# ============================================================
for model_name, model in models.items():

    with mlflow.start_run(run_name=model_name):

        print(f"\nTraining {model_name}...")

        # Train
        model.fit(X_train, y_train)

        # Predict
        y_pred = model.predict(X_test)

        # Evaluate
        accuracy = accuracy_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)

        # Log additional metrics
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_text(
            np.array2string(cm),
            "confusion_matrix.txt"
        )

        mlflow.set_tag("Classifier", model_name)

        print(f"Accuracy : {accuracy:.4f}")
        print(cm)

        results[model_name] = accuracy

        # Keep track of best model
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_model = model
            best_model_name = model_name

# ============================================================
# Print Model Comparison
# ============================================================
print("\n" + "=" * 60)
print("MODEL COMPARISON")
print("=" * 60)

for name, score in sorted(results.items(), key=lambda x: x[1], reverse=True):
    print(f"{name:25s}: {score:.4f}")

print("\n" + "=" * 60)
print("BEST MODEL")
print("=" * 60)
print(f"Model    : {best_model_name}")
print(f"Accuracy : {best_accuracy:.4f}")

# ============================================================
# Register Best Model in MLflow Model Registry
# ============================================================
with mlflow.start_run(run_name="Register Best Model"):

    model_info = mlflow.sklearn.log_model(
        sk_model=best_model,
        name="best_model",
        registered_model_name="CustomerPurchasePredictionModel"
    )

    mlflow.log_metric("best_accuracy", best_accuracy)
    mlflow.set_tag("Best Model", best_model_name)

print("\n" + "=" * 60)
print("MODEL REGISTERED SUCCESSFULLY")
print("=" * 60)
print(f"Registered Model : CustomerPurchasePredictionModel")
print(f"Winning Model    : {best_model_name}")
print(f"Accuracy         : {best_accuracy:.4f}")
print(f"Model URI        : {model_info.model_uri}")