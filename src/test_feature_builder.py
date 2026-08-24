import json

from src.feature_engineering.feature_builder import FeatureBuilder


with open(
    "data/raw/dataset_v2.json",
    "r",
    encoding="utf-8"
) as file:

    dataset = json.load(file)


print("PRs loaded:", len(dataset))

features = FeatureBuilder.build(
    dataset[0]
)

print("\n===== FEATURE ENGINEERING =====")

for name, value in features.items():

    print(
        f"{name}: {value}"
    )