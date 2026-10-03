"""
test_ml_dataset.py

Purpose:
Audit the ML dataset for missing values,
target distribution, and potential data leakage.
"""

import pandas as pd


# --------------------------------
# Load ML Dataset
# --------------------------------

df = pd.read_csv(
    "data/processed/ml_dataset_v1.csv"
)


# --------------------------------
# Basic Information
# --------------------------------

print("\n===== ML DATASET AUDIT =====")

print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nColumns:")

for column in df.columns:
    print("-", column)


# --------------------------------
# Missing Values
# --------------------------------

print("\n===== MISSING VALUES =====")

print(
    df.isnull().sum()
)


# --------------------------------
# Target Distribution
# --------------------------------

print("\n===== TARGET DISTRIBUTION =====")

print(
    df["review_friction"]
    .value_counts()
    .sort_index()
)

print("\nTarget Percentage:")

print(
    (
        df["review_friction"]
        .value_counts(normalize=True)
        .sort_index()
        * 100
    ).round(2)
)


# --------------------------------
# Potential Leakage Check
# --------------------------------

print("\n===== POTENTIAL LEAKAGE CHECK =====")

leakage_keywords = [
    "review_count",
    "review_comment",
    "approval",
    "change_request",
    "review_cycle",
    "time_to_review",
    "time_to_merge",
    "merged",
    "closed"
]

found = []

for column in df.columns:

    if column == "review_friction":
        continue

    if any(
        keyword in column.lower()
        for keyword in leakage_keywords
    ):
        found.append(column)


if found:

    print("⚠️ Columns requiring review:")

    for column in found:
        print("-", column)

else:

    print("✅ No obvious leakage columns found.")


# --------------------------------
# Data Types
# --------------------------------

print("\n===== DATA TYPES =====")

print(df.dtypes)