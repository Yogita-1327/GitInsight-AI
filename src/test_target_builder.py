"""
test_target_builder.py

Purpose:
Test the binary review-friction target.
"""

import json
import pandas as pd

from src.feature_engineering.target_builder import TargetBuilder


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
# Build Targets
# --------------------------------

targets = []

for pr in dataset:

    target = TargetBuilder.build(pr)

    targets.append(
        target["review_friction"]
    )


df = pd.DataFrame({
    "review_friction": targets
})


# --------------------------------
# Display Results
# --------------------------------

print("\n===== REVIEW FRICTION TARGET =====")

print(
    "Total PRs:",
    len(df)
)

print("\nTarget distribution:")

print(
    df["review_friction"]
    .value_counts()
    .sort_index()
)

print("\nTarget percentages:")

print(
    (
        df["review_friction"]
        .value_counts(normalize=True)
        .sort_index()
        * 100
    ).round(2)
)