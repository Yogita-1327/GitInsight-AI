from src.ingestion.github_client import github_client
from src.ingestion.extractors.issue_extractor import IssueExtractor


repo = github_client.get_repo("facebook/react")

print("Searching for a PR with issue references...\n")

for pr in repo.get_pulls(
    state="closed",
    sort="updated",
    direction="desc"
):

    issue_data = IssueExtractor.extract(pr)

    if issue_data["linked_issue_count"] > 0:

        print("===== ISSUE INTELLIGENCE =====")

        print(
            "PR Number:",
            pr.number
        )

        print(
            "Title:",
            pr.title
        )

        print(
            "Linked Issue Count:",
            issue_data["linked_issue_count"]
        )

        print(
            "Open Issues:",
            issue_data["open_linked_issue_count"]
        )

        print(
            "Closed Issues:",
            issue_data["closed_linked_issue_count"]
        )

        print(
            "Issue Numbers:",
            issue_data["linked_issue_numbers"]
        )

        print("\nLinked Issues:")

        for issue in issue_data["linked_issues"]:

            print(issue)

        break