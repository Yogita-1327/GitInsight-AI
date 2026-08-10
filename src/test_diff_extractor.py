from src.ingestion.pr_collector import PRCollector
from src.ingestion.extractors.diff_extractor import DiffExtractor

collector = PRCollector("facebook/react")

pr = next(iter(collector.get_pull_requests(limit=1)))

diff = DiffExtractor.extract(pr)

print(diff)