"""
build_ml_dataset.py

Purpose:
Combine leakage-safe engineered features with
the review-friction target.
"""

import json
from pathlib import Path

import pandas as pd

from src.feature_engineering.feature_builder import FeatureBuilder
from src.feature_engineering.target_builder import TargetBuilder


# --------------------------------
# Load Dataset V2
# --------------------------------

with open(
    "data/raw/dataset_v2.json",
    "r",
    encoding="utf-8"
) as file:

    dataset = json.load(file)


# --------------------------------
# Build Features + Target
# --------------------------------

rows = []

for pr in dataset:

    features = FeatureBuilder.build(pr)

    target = TargetBuilder.build(pr)

    row = {
        **features,
        **target
    }

    rows.append(row)


df = pd.DataFrame(rows)


# --------------------------------
# Save ML Dataset
# --------------------------------

output_dir = Path(
    "data/processed"
)

output_dir.mkdir(
    parents=True,
    exist_ok=True
)

output_path = (
    output_dir /
    "ml_dataset_v1.csv"
)

df.to_csv(
    output_path,
    index=False
)


# --------------------------------
# Summary
# --------------------------------

print("\n✅ ML dataset created")

print("Rows:", len(df))

print("Features:", len(df.columns) - 1)

print("Target: review_friction")

print("\nTarget distribution:")

print(
    df["review_friction"]
    .value_counts()
    .sort_index()
)

print("\nSaved to:")

print(output_path)