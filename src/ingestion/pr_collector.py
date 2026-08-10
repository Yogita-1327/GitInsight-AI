"""
pr_collector.py

Purpose:
Downloads Pull Requests from a GitHub repository.
"""

from src.ingestion.github_client import github_client


class PRCollector:

    def __init__(self, repository_name):
        self.repository_name = repository_name
        self.repository = github_client.get_repo(repository_name)

    def get_repository(self):
        return self.repository

    def get_pull_requests(
        self,
        state="closed",
        sort="updated",
        direction="desc",
        limit=None,
    ):
        """
        Returns GitHub Pull Request objects.
        """

        return self.repository.get_pulls(
            state=state,
            sort=sort,
            direction=direction,
        )
        if limit is None:
          return pulls

        return [pr for _, pr in zip(range(limit), pulls)]