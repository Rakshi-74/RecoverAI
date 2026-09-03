import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load dataset
df = pd.read_csv("ml_dataset.csv")

# Features used by the model
features = [
    "amount",
    "attempt_number",
    "checkout_started",
    "checkout_duration_seconds",
    "customer_age_days",
    "lifetime_value",
    "successful_payments",
    "failed_payments",
    "previous_recoveries",
    "contact_opted_out",
    "failure_rate",
    "recovery_history_rate",
    "high_value_customer",
    "high_amount",
    "multiple_attempt"
]

X = df[features]
y = df["recovery_success"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Create model
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=8,
    random_state=42,
    class_weight="balanced"
)

# Train
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
accuracy = accuracy_score(y_test, y_pred)

print("====================================")
print("       RecoverAI ML MODEL")
print("====================================")
print(f"Training records: {len(X_train)}")
print(f"Testing records:  {len(X_test)}")
print(f"Accuracy: {accuracy:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Feature importance
importance = pd.DataFrame({
    "feature": features,
    "importance": model.feature_importances_
})

importance = importance.sort_values(
    by="importance",
    ascending=False
)

print("\nFeature Importance:")
print(importance.to_string(index=False))

# Save model
joblib.dump(
    {
        "model": model,
        "features": features
    },
    "ml/recovery_model.joblib"
)

print("\nModel saved successfully!")
print("File: ml/recovery_model.joblib")