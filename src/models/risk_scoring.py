import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from tabpfn import TabPFNClassifier


# ============================================================
# GitInsight-AI - Risk Scoring
# ============================================================

print("GitInsight-AI - PR Risk Scoring")
print("=" * 55)

# ------------------------------------------------------------
# Load dataset
# ------------------------------------------------------------

df = pd.read_csv("data/processed/ml_dataset_v1.csv")

X = df.drop(columns=["review_friction"])
y = df["review_friction"]

print(f"Dataset shape: {df.shape}")


# ------------------------------------------------------------
# Train / Test Split
# ------------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    stratify=y,
    random_state=42
)


# ------------------------------------------------------------
# Train TabPFN
# ------------------------------------------------------------

print("\nTraining TabPFN...")

model = TabPFNClassifier(
    random_state=42,
    device="auto"
)

model.fit(X_train, y_train)

print("Model training completed.")


# ------------------------------------------------------------
# Select one PR from test data
# ------------------------------------------------------------

pr_index = X_test.index[0]

pr_features = X_test.loc[[pr_index]]

probability = model.predict_proba(pr_features)[0][1]


# ------------------------------------------------------------
# Risk Score
# ------------------------------------------------------------

risk_score = probability * 100


if probability < 0.25:
    risk_level = "LOW"
elif probability < 0.50:
    risk_level = "MEDIUM"
else:
    risk_level = "HIGH"


# ------------------------------------------------------------
# Display PR information
# ------------------------------------------------------------

print("\n" + "=" * 55)
print("PR RISK ASSESSMENT")
print("=" * 55)

print(f"PR Index                  : {pr_index}")
print(f"Review Friction Probability: {probability:.4f}")
print(f"Risk Score                : {risk_score:.2f}/100")
print(f"Risk Level                : {risk_level}")


# ------------------------------------------------------------
# Feature values
# ------------------------------------------------------------

print("\nPR Feature Values")
print("-" * 55)

for feature in X.columns:
    print(
        f"{feature:<30}: "
        f"{pr_features.iloc[0][feature]}"
    )


# ------------------------------------------------------------
# Save assessment
# ------------------------------------------------------------

assessment = pd.DataFrame({
    "pr_index": [pr_index],
    "review_friction_probability": [probability],
    "risk_score": [risk_score],
    "risk_level": [risk_level]
})

assessment.to_csv(
    "data/processed/pr_risk_assessment.csv",
    index=False
)

print("\nRisk assessment saved to:")
print("data/processed/pr_risk_assessment.csv")

print("\nRisk scoring completed.")