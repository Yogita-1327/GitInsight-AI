"""
pr_parser.py

Purpose:
Combines outputs from different extractors
into one ML-ready dataset record.
"""

from src.ingestion.extractors.file_extractor import FileExtractor
from src.ingestion.extractors.diff_extractor import DiffExtractor


class PRParser:

    @staticmethod
    def parse(pr, repository):

        # --------------------------------
        # Commit Metadata
        # --------------------------------

        commits = []

        for commit in pr.get_commits():

            commits.append({

                "sha": commit.sha,

                "message": commit.commit.message,

                "author":
                commit.author.login
                if commit.author
                else None,

                "date":
                str(commit.commit.author.date)

            })

        # --------------------------------
        # Changed Files
        # --------------------------------

        changed_files = FileExtractor.extract(pr)

        # --------------------------------
        # Raw Code Diff
        # --------------------------------

        code_diff = DiffExtractor.extract(pr)

        # --------------------------------
        # Dataset Row
        # --------------------------------

        data = {

            # ============================
            # Repository Metadata
            # ============================

            "repository_name": repository.full_name,

            "repository_language": repository.language,

            "repository_stars": repository.stargazers_count,

            "repository_forks": repository.forks_count,

            "repository_watchers": repository.subscribers_count,

            "repository_open_issues": repository.open_issues_count,

            "repository_default_branch": repository.default_branch,

            "repository_topics": repository.get_topics(),

            "repository_license":
            repository.license.name
            if repository.license
            else None,

            # ============================
            # Pull Request Metadata
            # ============================

            "pr_number": pr.number,

            "title": pr.title,

            "description": pr.body,

            "author":
            pr.user.login
            if pr.user
            else None,

            "created_at": str(pr.created_at),

            "closed_at": str(pr.closed_at),

            "merged_at": str(pr.merged_at),

            "merged": pr.merged,

            # ============================
            # Review Metadata
            # ============================

            "comments": pr.comments,

            "review_comments": pr.review_comments,

            "labels": [
                label.name
                for label in pr.labels
            ],

            # ============================
            # Commit Metadata
            # ============================

            "commit_count": len(commits),

            "commits": commits,

            # ============================
            # File Metadata
            # ============================

            "files_changed": pr.changed_files,

            "changed_files": changed_files,

            # ============================
            # Code Statistics
            # ============================

            "lines_added": pr.additions,

            "lines_deleted": pr.deletions,

            # ============================
            # Raw Code Diff
            # ============================

            "code_diff": code_diff

        }

        return data