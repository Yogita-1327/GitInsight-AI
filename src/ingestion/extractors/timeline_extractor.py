"""
timeline_extractor.py

Purpose:
Extract lifecycle and timing intelligence
from a GitHub Pull Request.
"""

class TimelineExtractor:

    @staticmethod
    def extract(pr):

        # --------------------------------
        # PR Creation
        # --------------------------------

        created_at = pr.created_at

        # --------------------------------
        # PR Closed / Merged
        # --------------------------------

        closed_at = pr.closed_at
        merged_at = pr.merged_at

        # --------------------------------
        # Commits
        # --------------------------------

        commits = list(pr.get_commits())

        commit_dates = []

        for commit in commits:

            if commit.commit.author:

                commit_date = commit.commit.author.date

                if commit_date:

                    # Ignore commits authored before
                    # the PR was created.
                    if not created_at or commit_date >= created_at:
                        commit_dates.append(commit_date)

        # --------------------------------
        # First Commit
        # --------------------------------

        first_commit_at = None
        time_to_first_commit_hours = None

        if commit_dates:

            commit_dates.sort()

            first_commit_at = commit_dates[0]

            if created_at:

                time_difference = (
                    first_commit_at - created_at
                )

                time_to_first_commit_hours = round(
                    time_difference.total_seconds() / 3600,
                    2
                )

        # --------------------------------
        # Time To Close
        # --------------------------------

        time_to_close_hours = None

        if created_at and closed_at:

            time_difference = (
                closed_at - created_at
            )

            time_to_close_hours = round(
                time_difference.total_seconds() / 3600,
                2
            )

        # --------------------------------
        # Time To Merge
        # --------------------------------

        time_to_merge_hours = None

        if created_at and merged_at:

            time_difference = (
                merged_at - created_at
            )

            time_to_merge_hours = round(
                time_difference.total_seconds() / 3600,
                2
            )

        # --------------------------------
        # Review Timeline
        # --------------------------------

        reviews = list(pr.get_reviews())

        review_dates = []

        for review in reviews:

            if review.submitted_at:
                review_dates.append(
                    review.submitted_at
                )

        review_dates.sort()

        first_review_at = None
        last_review_at = None
        time_to_first_review_hours = None

        if review_dates:

            first_review_at = review_dates[0]

            last_review_at = review_dates[-1]

            if created_at:

                time_difference = (
                    first_review_at - created_at
                )

                time_to_first_review_hours = round(
                    time_difference.total_seconds() / 3600,
                    2
                )

        # --------------------------------
        # Activity Counts
        # --------------------------------

        commit_count = len(commits)

        review_count = len(reviews)

        comment_count = pr.comments

        # --------------------------------
        # Timeline Output
        # --------------------------------

        return {

            "created_at":
                str(created_at)
                if created_at
                else None,

            "first_commit_at":
                str(first_commit_at)
                if first_commit_at
                else None,

            "first_review_at":
                str(first_review_at)
                if first_review_at
                else None,

            "last_review_at":
                str(last_review_at)
                if last_review_at
                else None,

            "closed_at":
                str(closed_at)
                if closed_at
                else None,

            "merged_at":
                str(merged_at)
                if merged_at
                else None,

            "time_to_first_commit_hours":
                time_to_first_commit_hours,

            "time_to_first_review_hours":
                time_to_first_review_hours,

            "time_to_close_hours":
                time_to_close_hours,

            "time_to_merge_hours":
                time_to_merge_hours,

            "commit_count":
                commit_count,

            "review_count":
                review_count,

            "comment_count":
                comment_count
        }