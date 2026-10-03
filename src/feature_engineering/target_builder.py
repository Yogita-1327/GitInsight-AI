"""
target_builder.py

Purpose:
Creates the binary review-friction target for GitInsight-AI.

Target:
0 -> No significant review friction
1 -> Review friction detected
"""


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
        # Review Friction Target
        # --------------------------------
        #
        # A PR is considered to have
        # review friction if meaningful
        # review-related friction signals exist.

        review_friction = (
            change_requests > 0
            or review_cycles > 0
            or review_comments > 0
        )

        return {
            "review_friction": int(review_friction)
        }