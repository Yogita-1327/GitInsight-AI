"""
test_feature_quality.py

Purpose:
Audit feature quality across the complete
GitInsight-AI Dataset V2.
"""

import json
import pandas as pd

from src.feature_engineering.feature_builder import FeatureBuilder


# --------------------------------
# Load Dataset
# --------------------------------

with open(
    "data/raw/dataset_v2.json",
    "r",
    encoding="utf-8"
) as file:

    dataset = json.load(file)


# --------------------------------
# Build Feature Matrix
# --------------------------------

feature_rows = []

for pr in dataset:

    features = FeatureBuilder.build(pr)

    feature_rows.append(features)


df = pd.DataFrame(feature_rows)


# --------------------------------
# Basic Dataset Information
# --------------------------------

print("\n===== FEATURE QUALITY AUDIT =====")

print(
    "PR records:",
    len(df)
)

print(
    "Feature count:",
    len(df.columns)
)

print(
    "\nFeatures:"
)

for column in df.columns:

    print(
        "-",
        column
    )


# --------------------------------
# Missing Values
# --------------------------------

print(
    "\n===== MISSING VALUES ====="
)

missing = df.isnull().sum()

for column, count in missing.items():

    print(
        f"{column}: {count}"
    )


# --------------------------------
# Zero Values
# --------------------------------

print(
    "\n===== ZERO VALUES ====="
)

for column in df.columns:

    zero_count = (
        df[column] == 0
    ).sum()

    print(
        f"{column}: {zero_count}"
    )


# --------------------------------
# Descriptive Statistics
# --------------------------------

print(
    "\n===== STATISTICS ====="
)

print(
    df.describe()
)