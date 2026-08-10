from src.ingestion.pr_collector import PRCollector
from src.ingestion.extractors.file_extractor import FileExtractor

collector = PRCollector("facebook/react")

repository = collector.get_repository()

pr = next(iter(collector.get_pull_requests(limit=1)))

files = FileExtractor.extract(pr)

print(files)