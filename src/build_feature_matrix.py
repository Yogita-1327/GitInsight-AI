"""
build_feature_matrix.py

Purpose:
Build the ML-ready feature matrix from Dataset V2.
"""

import json
from pathlib import Path

import pandas as pd

from src.feature_engineering.feature_builder import FeatureBuilder


# --------------------------------
# Load Dataset
# --------------------------------

input_path = Path(
    "data/raw/dataset_v2.json"
)

with open(
    input_path,
    "r",
    encoding="utf-8"
) as file:

    dataset = json.load(file)


# --------------------------------
# Build Features
# --------------------------------

feature_rows = []

for pr in dataset:

    features = FeatureBuilder.build(pr)

    feature_rows.append(features)


df = pd.DataFrame(feature_rows)


# --------------------------------
# Create Output Directory
# --------------------------------

output_dir = Path(
    "data/features"
)

output_dir.mkdir(
    parents=True,
    exist_ok=True
)


# --------------------------------
# Save Feature Matrix
# --------------------------------

output_path = (
    output_dir /
    "feature_matrix_v1.csv"
)

df.to_csv(
    output_path,
    index=False
)


# --------------------------------
# Summary
# --------------------------------

print("\n✅ Feature matrix created")

print(
    f"Rows: {df.shape[0]}"
)

print(
    f"Features: {df.shape[1]}"
)

print(
    f"Saved to: {output_path}"
)

print("\nFeature columns:")

for column in df.columns:

    print(
        "-",
        column
    )