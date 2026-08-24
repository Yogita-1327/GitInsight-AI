"""
target_builder.py

Purpose:
Create the ML target from post-PR review outcomes.

The target represents review friction/risk.
Outcome fields used here must NOT be used
as prediction features.
"""

import math


class TargetBuilder:

    @staticmethod
    def build(pr):

        change_requests = (
            pr.get("change_request_count") or 0
        )

        review_cycles = (
            pr.get("review_cycles") or 0
        )

        review_comments = (
            pr.get("review_comment_count") or 0
        )

        # --------------------------------
        # Review Friction Score
        # --------------------------------

        friction_score = (
            change_requests
            + review_cycles
            + math.log1p(review_comments)
        )

        return {
            "review_friction_score": friction_score
        }