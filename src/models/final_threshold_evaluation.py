import pandas as pd
import numpy as np

from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

from tabpfn import TabPFNClassifier


# ============================================================
# GitInsight-AI - Final Threshold Evaluation
# ============================================================

print("GitInsight-AI - Final Threshold Evaluation")
print("=" * 55)

# Load dataset
df = pd.read_csv("data/processed/ml_dataset_v1.csv")

X = df.drop(columns=["review_friction"])
y = df["review_friction"]

print(f"Dataset shape: {df.shape}")
print(f"Features: {X.shape[1]}")
print(f"Target: review_friction")

print("\nClass distribution:")
print(y.value_counts())


# ------------------------------------------------------------
# 5-Fold Stratified Cross Validation
# ------------------------------------------------------------

skf = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

all_y_true = []
all_y_prob = []

print("\nRunning 5-Fold TabPFN evaluation...")

for fold, (train_idx, test_idx) in enumerate(
    skf.split(X, y), start=1
):

    print(f"Training Fold {fold}...")

    X_train = X.iloc[train_idx]
    X_test = X.iloc[test_idx]

    y_train = y.iloc[train_idx]
    y_test = y.iloc[test_idx]

    model = TabPFNClassifier(
        random_state=42,
        device="auto"
    )

    model.fit(X_train, y_train)

    probabilities = model.predict_proba(X_test)[:, 1]

    all_y_true.extend(y_test.tolist())
    all_y_prob.extend(probabilities.tolist())


# Convert to arrays
all_y_true = np.array(all_y_true)
all_y_prob = np.array(all_y_prob)


# ------------------------------------------------------------
# Final threshold
# ------------------------------------------------------------

threshold = 0.25

all_y_pred = (
    all_y_prob >= threshold
).astype(int)


# ------------------------------------------------------------
# Evaluation
# ------------------------------------------------------------

accuracy = accuracy_score(
    all_y_true,
    all_y_pred
)

precision = precision_score(
    all_y_true,
    all_y_pred,
    zero_division=0
)

recall = recall_score(
    all_y_true,
    all_y_pred,
    zero_division=0
)

f1 = f1_score(
    all_y_true,
    all_y_pred,
    zero_division=0
)

cm = confusion_matrix(
    all_y_true,
    all_y_pred
)


# ------------------------------------------------------------
# Results
# ------------------------------------------------------------

print("\n" + "=" * 55)
print("FINAL THRESHOLD RESULTS")
print("=" * 55)

print(f"Threshold : {threshold}")
print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")


print("\nConfusion Matrix:")
print(cm)


print("\nClassification Report:")
print(
    classification_report(
        all_y_true,
        all_y_pred,
        zero_division=0
    )
)

print("\nFinal threshold evaluation completed.")