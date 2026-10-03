import pandas as pd

from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score
)

from tabpfn import TabPFNClassifier


# Load dataset
data = pd.read_csv("data/processed/ml_dataset_v1.csv")

# Separate features and target
X = data.drop("review_friction", axis=1)
y = data["review_friction"]


# 5-fold stratified cross-validation
cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)


# Store results
accuracy_scores = []
precision_scores = []
recall_scores = []
f1_scores = []
roc_auc_scores = []
pr_auc_scores = []


print("GitInsight-AI - TabPFN 5-Fold Cross-Validation")
print("=" * 50)
print("Dataset shape:", data.shape)
print("Class distribution:")
print(y.value_counts().sort_index())
print()


# Run cross-validation
for fold, (train_index, test_index) in enumerate(cv.split(X, y), start=1):

    X_train = X.iloc[train_index]
    X_test = X.iloc[test_index]

    y_train = y.iloc[train_index]
    y_test = y.iloc[test_index]

    print(f"Training Fold {fold}...")

    # Create model
    model = TabPFNClassifier(
        random_state=42,
        device="auto"
    )

    # Train
    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(
        y_test, y_pred, zero_division=0
    )
    recall = recall_score(
        y_test, y_pred, zero_division=0
    )
    f1 = f1_score(
        y_test, y_pred, zero_division=0
    )
    roc_auc = roc_auc_score(y_test, y_prob)
    pr_auc = average_precision_score(y_test, y_prob)

    # Store results
    accuracy_scores.append(accuracy)
    precision_scores.append(precision)
    recall_scores.append(recall)
    f1_scores.append(f1)
    roc_auc_scores.append(roc_auc)
    pr_auc_scores.append(pr_auc)

    print(
        f"Fold {fold}: "
        f"Accuracy={accuracy:.4f}, "
        f"F1={f1:.4f}, "
        f"ROC-AUC={roc_auc:.4f}, "
        f"PR-AUC={pr_auc:.4f}"
    )

    print()


# Calculate average results
print("=" * 50)
print("Cross-Validation Results")
print("=" * 50)

print(
    "Accuracy :",
    round(sum(accuracy_scores) / len(accuracy_scores), 4)
)

print(
    "Precision:",
    round(sum(precision_scores) / len(precision_scores), 4)
)

print(
    "Recall   :",
    round(sum(recall_scores) / len(recall_scores), 4)
)

print(
    "F1 Score :",
    round(sum(f1_scores) / len(f1_scores), 4)
)

print(
    "ROC-AUC  :",
    round(sum(roc_auc_scores) / len(roc_auc_scores), 4)
)

print(
    "PR-AUC   :",
    round(sum(pr_auc_scores) / len(pr_auc_scores), 4)
)