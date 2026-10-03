import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    classification_report
)

from tabpfn import TabPFNClassifier


# Load ML dataset
data = pd.read_csv("data/processed/ml_dataset_v1.csv")

# Separate features and target
X = data.drop("review_friction", axis=1)
y = data["review_friction"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("GitInsight-AI - TabPFN Model")
print("=" * 40)
print("Dataset shape:", data.shape)
print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))
print("Training class distribution:")
print(y_train.value_counts().sort_index())
print()

# Create TabPFN model
model = TabPFNClassifier(
    random_state=42,
    device="auto"
)

# Train model
print("Training TabPFN...")
model.fit(X_train, y_train)

print("Training completed.")
print()

# Predictions
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

# Evaluation metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)
roc_auc = roc_auc_score(y_test, y_prob)
pr_auc = average_precision_score(y_test, y_prob)

print("Evaluation Results")
print("=" * 40)
print("Accuracy :", round(accuracy, 4))
print("Precision:", round(precision, 4))
print("Recall   :", round(recall, 4))
print("F1 Score :", round(f1, 4))
print("ROC-AUC  :", round(roc_auc, 4))
print("PR-AUC    :", round(pr_auc, 4))

print()
print("Predicted probabilities for class 1:")
for actual, probability, prediction in zip(y_test, y_prob, y_pred):
    print(
        "Actual:", actual,
        "| Probability:", round(probability, 4),
        "| Prediction:", prediction
    )

print()
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print()
print("Classification Report:")
print(classification_report(y_test, y_pred, zero_division=0))