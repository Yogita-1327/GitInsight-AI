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

rows = []

for pr in dataset:

    target = TargetBuilder.build(pr)

    rows.append(target)


df = pd.DataFrame(rows)


# --------------------------------
# Display Results
# --------------------------------

print("\n===== TARGET AUDIT =====")

print(
    "PR records:",
    len(df)
)

print(
    "\nReview friction statistics:"
)

print(
    df["review_friction_score"].describe()
)

print(
    "\nUnique scores:",
    df["review_friction_score"].nunique()
)

print(
    "\nLowest scores:"
)

print(
    df["review_friction_score"]
    .sort_values()
    .head(10)
    .to_list()
)

print(
    "\nHighest scores:"
)

print(
    df["review_friction_score"]
    .sort_values(
        ascending=False
    )
    .head(10)
    .to_list()
)