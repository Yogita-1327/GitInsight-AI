"""
file_extractor.py

Extracts changed files from a GitHub Pull Request.
"""

from pathlib import Path


class FileExtractor:

    @staticmethod
    def extract(pr):

        files = []

        for file in pr.get_files():

            extension = Path(file.filename).suffix

            files.append({

                "filename": file.filename,

                "extension": extension,

                "status": file.status,

                "additions": file.additions,

                "deletions": file.deletions,

                "changes": file.changes

            })

        return files