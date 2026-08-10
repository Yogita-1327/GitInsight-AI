"""
pr_parser.py

Purpose:
Combines outputs from different extractors
into one ML-ready dataset record.
"""

from src.ingestion.extractors.file_extractor import FileExtractor
from src.ingestion.extractors.diff_extractor import DiffExtractor
from src.ingestion.extractors.review_extractor import ReviewExtractor
from src.ingestion.extractors.timeline_extractor import TimelineExtractor


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
        # Review Intelligence
        # --------------------------------

        review_data = ReviewExtractor.extract(pr)

        # --------------------------------
        # Timeline Intelligence
        # --------------------------------

        timeline_data = TimelineExtractor.extract(pr)

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
            # Basic PR Comments
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

            "code_diff": code_diff,

            # ============================
            # Review Intelligence
            # ============================

            "review_count":
            review_data["review_count"],

            "unique_reviewer_count":
            review_data["unique_reviewer_count"],

            "reviewers":
            review_data["reviewers"],

            "approval_count":
            review_data["approval_count"],

            "change_request_count":
            review_data["change_request_count"],

            "commented_review_count":
            review_data["commented_review_count"],

            "dismissed_review_count":
            review_data["dismissed_review_count"],

            "first_review_at":
            review_data["first_review_at"],

            "last_review_at":
            review_data["last_review_at"],

            "time_to_first_review_hours":
            review_data["time_to_first_review_hours"],

            "review_cycles":
            review_data["review_cycles"],

            "reviews":
            review_data["reviews"],

            "review_comment_count":
            review_data["review_comment_count"],

            "review_comments_detail":
            review_data["review_comments"],

            # ============================
            # Timeline Intelligence
            # ============================

            "timeline_created_at":
            timeline_data["created_at"],

            "timeline_first_commit_at":
            timeline_data["first_commit_at"],

            "timeline_first_review_at":
            timeline_data["first_review_at"],

            "timeline_last_review_at":
            timeline_data["last_review_at"],

            "timeline_closed_at":
            timeline_data["closed_at"],

            "timeline_merged_at":
            timeline_data["merged_at"],

            "time_to_first_commit_hours":
            timeline_data["time_to_first_commit_hours"],

            "time_to_first_review_hours":
            timeline_data["time_to_first_review_hours"],

            "time_to_close_hours":
            timeline_data["time_to_close_hours"],

            "time_to_merge_hours":
            timeline_data["time_to_merge_hours"],

            "timeline_commit_count":
            timeline_data["commit_count"],

            "timeline_review_count":
            timeline_data["review_count"],

            "timeline_comment_count":
            timeline_data["comment_count"]

        }

        return data