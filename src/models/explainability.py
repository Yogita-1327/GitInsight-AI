import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.inspection import permutation_importance
from sklearn.metrics import roc_auc_score

from tabpfn import TabPFNClassifier


# ============================================================
# GitInsight-AI - TabPFN Explainability
# ============================================================

print("GitInsight-AI - TabPFN Explainability")
print("=" * 55)

# Load dataset
df = pd.read_csv("data/processed/ml_dataset_v1.csv")

X = df.drop(columns=["review_friction"])
y = df["review_friction"]

print(f"Dataset shape: {df.shape}")
print(f"Number of features: {X.shape[1]}")

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

print(f"Training samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")


# ------------------------------------------------------------
# Train TabPFN
# ------------------------------------------------------------

print("\nTraining TabPFN...")

model = TabPFNClassifier(
    random_state=42,
    device="auto"
)

model.fit(X_train, y_train)

print("Training completed.")


# ------------------------------------------------------------
# Baseline ROC-AUC
# ------------------------------------------------------------

y_probability = model.predict_proba(X_test)[:, 1]

baseline_auc = roc_auc_score(
    y_test,
    y_probability
)

print(f"\nBaseline ROC-AUC: {baseline_auc:.4f}")


# ------------------------------------------------------------
# Permutation Feature Importance
# ------------------------------------------------------------

print("\nCalculating feature importance...")

result = permutation_importance(
    model,
    X_test,
    y_test,
    scoring="roc_auc",
    n_repeats=10,
    random_state=42
)


# ------------------------------------------------------------
# Create importance table
# ------------------------------------------------------------

importance_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": result.importances_mean,
    "Std": result.importances_std
})

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

print("\nFeature Importance")
print("=" * 55)

for _, row in importance_df.iterrows():
    print(
        f"{row['Feature']:<30} "
        f"{row['Importance']:.4f}"
    )


# ------------------------------------------------------------
# Save results
# ------------------------------------------------------------

importance_df.to_csv(
    "data/processed/feature_importance.csv",
    index=False
)

print("\nFeature importance saved to:")
print("data/processed/feature_importance.csv")

print("\nTop 5 Features:")
print(importance_df.head(5).to_string(index=False))

print("\nExplainability analysis completed.")