from src.ingestion.dataset_builder import DatasetBuilder

builder = DatasetBuilder(
    "facebook/react"
)

builder.build(limit=100)