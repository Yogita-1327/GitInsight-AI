"""
dataset_writer.py

Purpose:
Saves datasets to disk.
"""

import json
from pathlib import Path


class DatasetWriter:

    @staticmethod
    def save_json(dataset, output_path):
        """
        Save dataset as JSON.
        """

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                dataset,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(f"\n✅ Dataset saved successfully")
        print(output_path)