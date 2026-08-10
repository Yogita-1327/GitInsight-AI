from src.ingestion.github_client import github_client
from src.ingestion.extractors.review_extractor import ReviewExtractor


repo = github_client.get_repo("facebook/react")

print("Searching for a PR with reviews...\n")

for pr in repo.get_pulls(
    state="closed",
    sort="updated",
    direction="desc"
):

    review_data = ReviewExtractor.extract(pr)

    if review_data["review_count"] > 0:

        print("===== FOUND PR WITH REVIEWS =====")

        print("PR Number:", pr.number)
        print("Title:", pr.title)

        print(
            "Review Count:",
            review_data["review_count"]
        )

        print(
            "Unique Reviewers:",
            review_data["unique_reviewer_count"]
        )

        print(
            "Approvals:",
            review_data["approval_count"]
        )

        print(
            "Changes Requested:",
            review_data["change_request_count"]
        )

        print(
            "Commented Reviews:",
            review_data["commented_review_count"]
        )

        print(
            "Review Comments:",
            review_data["review_comment_count"]
        )

        print(
            "Time To First Review:",
            review_data["time_to_first_review_hours"],
            "hours"
        )

        print(
            "Review Cycles:",
            review_data["review_cycles"]
        )

        print("\n===== REVIEWS =====")

        for review in review_data["reviews"]:
            print(review)

        break