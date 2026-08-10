"""
issue_extractor.py

Purpose:
Extract issue context and issue references
associated with a GitHub Pull Request.
"""

import re


class IssueExtractor:

    @staticmethod
    def extract(pr):

        repository = pr.base.repo

        # --------------------------------
        # PR Text
        # --------------------------------

        title = pr.title or ""
        body = pr.body or ""

        text = f"{title}\n{body}"

        # --------------------------------
        # Extract Issue References
        # --------------------------------

        issue_numbers = set()

        # Matches references such as:
        # #123
        # fixes #123
        # closes #456

        matches = re.findall(
            r"(?<![\w/])#(\d+)",
            text
        )

        for match in matches:
            issue_numbers.add(int(match))

        # --------------------------------
        # Collect Issue Information
        # --------------------------------

        issues = []

        for issue_number in sorted(issue_numbers):

            # Don't treat the PR itself as an issue.
            if issue_number == pr.number:
                continue

            try:

                issue = repository.get_issue(
                    issue_number
                )

                issues.append({

                    "issue_number":
                    issue.number,

                    "title":
                    issue.title,

                    "state":
                    issue.state,

                    "labels": [
                        label.name
                        for label in issue.labels
                    ],

                    "author":
                    issue.user.login
                    if issue.user
                    else None,

                    "created_at":
                    str(issue.created_at),

                    "closed_at":
                    str(issue.closed_at)
                    if issue.closed_at
                    else None,

                    "comments":
                    issue.comments,

                    "url":
                    issue.html_url

                })

            except Exception:

                # Ignore references that cannot
                # be retrieved from the repository.
                continue

        # --------------------------------
        # Issue Statistics
        # --------------------------------

        open_issue_count = sum(
            1
            for issue in issues
            if issue["state"] == "open"
        )

        closed_issue_count = sum(
            1
            for issue in issues
            if issue["state"] == "closed"
        )

        # --------------------------------
        # Output
        # --------------------------------

        return {

            "linked_issue_count":
            len(issues),

            "open_linked_issue_count":
            open_issue_count,

            "closed_linked_issue_count":
            closed_issue_count,

            "linked_issue_numbers":
            [
                issue["issue_number"]
                for issue in issues
            ],

            "linked_issues":
            issues

        }