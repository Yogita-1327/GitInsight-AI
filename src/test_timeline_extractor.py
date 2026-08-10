from src.ingestion.github_client import github_client
from src.ingestion.extractors.timeline_extractor import TimelineExtractor


repo = github_client.get_repo("facebook/react")

print("Searching for a closed PR...\n")

for pr in repo.get_pulls(
    state="closed",
    sort="updated",
    direction="desc"
):

    timeline = TimelineExtractor.extract(pr)

    print("===== TIMELINE INTELLIGENCE =====")

    print("PR Number:", pr.number)
    print("Title:", pr.title)

    print(
        "Created:",
        timeline["created_at"]
    )

    print(
        "First Commit:",
        timeline["first_commit_at"]
    )

    print(
        "First Review:",
        timeline["first_review_at"]
    )

    print(
        "Last Review:",
        timeline["last_review_at"]
    )

    print(
        "Closed:",
        timeline["closed_at"]
    )

    print(
        "Merged:",
        timeline["merged_at"]
    )

    print(
        "Time To First Commit:",
        timeline["time_to_first_commit_hours"],
        "hours"
    )

    print(
        "Time To First Review:",
        timeline["time_to_first_review_hours"],
        "hours"
    )

    print(
        "Time To Close:",
        timeline["time_to_close_hours"],
        "hours"
    )

    print(
        "Time To Merge:",
        timeline["time_to_merge_hours"],
        "hours"
    )

    print(
        "Commit Count:",
        timeline["commit_count"]
    )

    print(
        "Review Count:",
        timeline["review_count"]
    )

    print(
        "Comment Count:",
        timeline["comment_count"]
    )

    break