"""
feature_builder.py

Purpose:
Convert raw GitHub PR records into
ML-ready numerical features.
"""

import math


class FeatureBuilder:

    @staticmethod
    def safe_ratio(numerator, denominator):

        if denominator == 0:
            return 0.0

        return numerator / denominator

    @staticmethod
    def build(pr):

        lines_added = pr.get("lines_added") or 0
        lines_deleted = pr.get("lines_deleted") or 0
        files_changed = pr.get("files_changed") or 0
        commit_count = pr.get("commit_count") or 0

        repository_stars = (
            pr.get("repository_stars") or 0
        )

        repository_forks = (
            pr.get("repository_forks") or 0
        )

        repository_open_issues = (
            pr.get("repository_open_issues") or 0
        )

        linked_issue_count = (
            pr.get("linked_issue_count") or 0
        )

        open_linked_issue_count = (
            pr.get("open_linked_issue_count") or 0
        )

        closed_linked_issue_count = (
            pr.get("closed_linked_issue_count") or 0
        )

        # --------------------------------
        # PR Size Features
        # --------------------------------

        total_changes = (
            lines_added + lines_deleted
        )

        deletion_ratio = FeatureBuilder.safe_ratio(
            lines_deleted,
            total_changes
        )

        addition_ratio = FeatureBuilder.safe_ratio(
            lines_added,
            total_changes
        )

        changes_per_file = FeatureBuilder.safe_ratio(
            total_changes,
            files_changed
        )

        commits_per_file = FeatureBuilder.safe_ratio(
            commit_count,
            files_changed
        )

        # --------------------------------
        # Issue Context
        # --------------------------------

        issue_density = FeatureBuilder.safe_ratio(
            linked_issue_count,
            files_changed
        )

        # --------------------------------
        # Log-scaled Repository Features
        # --------------------------------

        log_stars = math.log1p(
            repository_stars
        )

        log_forks = math.log1p(
            repository_forks
        )

        log_open_issues = math.log1p(
            repository_open_issues
        )

        # --------------------------------
        # Feature Vector
        # --------------------------------

        features = {

            "lines_added": lines_added,

            "lines_deleted": lines_deleted,

            "total_changes": total_changes,

            "files_changed": files_changed,

            "commit_count": commit_count,

            "addition_ratio": addition_ratio,

            "deletion_ratio": deletion_ratio,

            "changes_per_file": changes_per_file,

            "commits_per_file": commits_per_file,

            "repository_stars_log": log_stars,

            "repository_forks_log": log_forks,

            "repository_open_issues_log":
                log_open_issues,

            "linked_issue_count":
                linked_issue_count,

            "open_linked_issue_count":
                open_linked_issue_count,

            "closed_linked_issue_count":
                closed_linked_issue_count,

            "issue_density":
                issue_density
        }

        return features