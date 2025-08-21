"""
Lightweight GitHub API client wrapper (PyGithub)
Issue #13: GitHub API 클라이언트 구현
"""

from github import Github
from github.GithubException import GithubException
import os
from typing import Optional, List, Dict, Any


class GitHubClient:
    def __init__(self, token: Optional[str] = None, *, per_page: int = 50):
        self.token = token or os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("GITHUB_TOKEN is not configured")
        self.client = Github(self.token, per_page=per_page)

    def get_repo(self, repo_name: str):
        """Return repository object for 'owner/repo'."""
        try:
            return self.client.get_repo(repo_name)
        except GithubException as e:
            raise RuntimeError(f"Failed to get repo {repo_name}: {e}")

    def test_connection(self) -> Dict[str, Any]:
        """Validate token and return basic identity info."""
        try:
            user = self.client.get_user()
            return {"status": "connected", "user": user.login}
        except GithubException as e:
            return {"status": "error", "message": str(e)}

    def list_issues(self, repo_name: str, state: str = "open") -> List[Dict[str, Any]]:
        repo = self.get_repo(repo_name)
        issues = repo.get_issues(state=state)
        return [
            {
                "number": i.number,
                "title": i.title,
                "body": i.body,
                "state": i.state,
                "labels": [l.name for l in i.labels],
                "assignees": [a.login for a in i.assignees],
                "created_at": i.created_at.isoformat(),
                "updated_at": i.updated_at.isoformat(),
                "comments": i.comments,
                "html_url": i.html_url,
            }
            for i in issues
        ]

    def list_pull_requests(self, repo_name: str, state: str = "open") -> List[Dict[str, Any]]:
        repo = self.get_repo(repo_name)
        pulls = repo.get_pulls(state=state)
        return [
            {
                "number": pr.number,
                "title": pr.title,
                "state": pr.state,
                "head": pr.head.ref,
                "base": pr.base.ref,
                "created_at": pr.created_at.isoformat(),
                "updated_at": pr.updated_at.isoformat(),
                "html_url": pr.html_url,
            }
            for pr in pulls
        ]

    def rate_limit(self) -> Dict[str, Any]:
        rl = self.client.get_rate_limit()
        return {
            "core_remaining": rl.core.remaining,
            "core_reset": rl.core.reset.isoformat(),
            "search_remaining": rl.search.remaining,
            "search_reset": rl.search.reset.isoformat(),
        }
