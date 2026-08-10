"""
dataset_builder.py

Purpose:
Builds dataset_v2.json by coordinating
all ingestion modules.
"""

from pathlib import Path

from src.ingestion.pr_collector import PRCollector
from src.ingestion.pr_parser import PRParser
from src.ingestion.dataset_writer import DatasetWriter


class DatasetBuilder:

    def __init__(self, repository_name):

        self.collector = PRCollector(repository_name)

        self.repository = self.collector.get_repository()

    def build(
        self,
        limit=100
    ):

        dataset = []

        pull_requests = self.collector.get_pull_requests()

        for index, pr in enumerate(pull_requests):

            if index >= limit:
                break

            data = PRParser.parse(
                pr,
                self.repository
            )

            dataset.append(data)

        # --------------------------------
        # Dataset V2 Output
        # --------------------------------

        output_path = (
            Path("data")
            / "raw"
            / "dataset_v2.json"
        )

        DatasetWriter.save_json(
            dataset,
            output_path
        )

        print(
            f"\nCollected {len(dataset)} Pull Requests"
        )