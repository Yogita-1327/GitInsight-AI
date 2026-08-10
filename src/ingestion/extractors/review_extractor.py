"""
review_extractor.py

Purpose:
Extract review intelligence from a GitHub Pull Request.
"""

from datetime import datetime, timezone


class ReviewExtractor:

    @staticmethod
    def extract(pr):
        """
        Extract review-related information from a GitHub Pull Request.
        """

        # --------------------------------
        # Pull Request Reviews
        # --------------------------------

        reviews = []

        for review in pr.get_reviews():

            reviews.append({
                "review_id": review.id,

                "reviewer":
                    review.user.login
                    if review.user
                    else None,

                "state": review.state,

                "submitted_at":
                    str(review.submitted_at)
                    if review.submitted_at
                    else None,

                "body": review.body,

                "commit_id": review.commit_id
            })

        # --------------------------------
        # Review Statistics
        # --------------------------------

        review_count = len(reviews)

        reviewers = list({
            review["reviewer"]
            for review in reviews
            if review["reviewer"]
        })

        approvals = sum(
            1
            for review in reviews
            if review["state"] == "APPROVED"
        )

        change_requests = sum(
            1
            for review in reviews
            if review["state"] == "CHANGES_REQUESTED"
        )

        commented_reviews = sum(
            1
            for review in reviews
            if review["state"] == "COMMENTED"
        )

        dismissed_reviews = sum(
            1
            for review in reviews
            if review["state"] == "DISMISSED"
        )

        # --------------------------------
        # Review Timing
        # --------------------------------

        submitted_times = [
            review["submitted_at"]
            for review in reviews
            if review["submitted_at"]
        ]

        submitted_dates = []

        for timestamp in submitted_times:

            try:
                submitted_dates.append(
                    datetime.fromisoformat(
                        timestamp.replace("Z", "+00:00")
                    )
                )

            except ValueError:
                pass

        first_review_at = None
        last_review_at = None
        time_to_first_review_hours = None

        if submitted_dates:

            submitted_dates.sort()

            first_review_at = str(submitted_dates[0])
            last_review_at = str(submitted_dates[-1])

            if pr.created_at:

                created_at = pr.created_at

                if created_at.tzinfo is None:
                    created_at = created_at.replace(
                        tzinfo=timezone.utc
                    )

                time_difference = (
                    submitted_dates[0] - created_at
                )

                time_to_first_review_hours = round(
                    time_difference.total_seconds() / 3600,
                    2
                )

        # --------------------------------
        # Review Cycles
        # --------------------------------

        review_cycles = 0

        for review in reviews:

            if review["state"] == "CHANGES_REQUESTED":
                review_cycles += 1

        # --------------------------------
        # Review Comments
        # --------------------------------

        review_comments = []

        for comment in pr.get_review_comments():

            review_comments.append({

                "comment_id": comment.id,

                "author":
                    comment.user.login
                    if comment.user
                    else None,

                "body": comment.body,

                "created_at":
                    str(comment.created_at)
                    if comment.created_at
                    else None,

                "updated_at":
                    str(comment.updated_at)
                    if comment.updated_at
                    else None,

                "path": comment.path,

                "line": comment.line,

                "side": comment.side,

                "commit_id": comment.commit_id
            })

        # --------------------------------
        # Final Structured Output
        # --------------------------------

        return {

            # Review counts
            "review_count": review_count,

            "unique_reviewer_count": len(reviewers),

            "reviewers": reviewers,

            "approval_count": approvals,

            "change_request_count": change_requests,

            "commented_review_count": commented_reviews,

            "dismissed_review_count": dismissed_reviews,

            # Review timing
            "first_review_at": first_review_at,

            "last_review_at": last_review_at,

            "time_to_first_review_hours":
                time_to_first_review_hours,

            # Review cycles
            "review_cycles": review_cycles,

            # Detailed reviews
            "reviews": reviews,

            # Inline review comments
            "review_comment_count": len(review_comments),

            "review_comments": review_comments
        }