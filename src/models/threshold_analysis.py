import pandas as pd

from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

from tabpfn import TabPFNClassifier


# Load dataset
data = pd.read_csv("data/processed/ml_dataset_v1.csv")

X = data.drop("review_friction", axis=1)
y = data["review_friction"]


# 5-fold stratified cross-validation
cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

# Store out-of-fold probabilities
oof_probabilities = [0.0] * len(y)


print("GitInsight-AI - TabPFN Threshold Analysis")
print("=" * 50)
print("Dataset shape:", data.shape)
print()


# Generate out-of-fold probabilities
for fold, (train_index, test_index) in enumerate(
    cv.split(X, y), start=1
):

    X_train = X.iloc[train_index]
    X_test = X.iloc[test_index]

    y_train = y.iloc[train_index]

    print(f"Training Fold {fold}...")

    model = TabPFNClassifier(
        random_state=42,
        device="auto"
    )

    model.fit(X_train, y_train)

    probabilities = model.predict_proba(X_test)[:, 1]

    for index, probability in zip(test_index, probabilities):
        oof_probabilities[index] = probability


print()
print("All folds completed.")
print()


# Convert probabilities to Series
probabilities = pd.Series(
    oof_probabilities,
    index=y.index
)


# Thresholds to test
thresholds = [
    0.10,
    0.15,
    0.20,
    0.25,
    0.30,
    0.35,
    0.40,
    0.45,
    0.50
]


print("Threshold Analysis")
print("=" * 75)

print(
    f"{'Threshold':<12}"
    f"{'Accuracy':<12}"
    f"{'Precision':<12}"
    f"{'Recall':<12}"
    f"{'F1 Score':<12}"
)

print("-" * 75)


for threshold in thresholds:

    predictions = (
        probabilities >= threshold
    ).astype(int)

    accuracy = accuracy_score(
        y,
        predictions
    )

    precision = precision_score(
        y,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y,
        predictions,
        zero_division=0
    )

    print(
        f"{threshold:<12.2f}"
        f"{accuracy:<12.4f}"
        f"{precision:<12.4f}"
        f"{recall:<12.4f}"
        f"{f1:<12.4f}"
    )


print()
print("Threshold analysis completed.")