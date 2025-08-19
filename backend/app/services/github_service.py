"""
GitHub API Service
Handles all interactions with GitHub API
"""

from github import Github, GithubException
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv
import json

load_dotenv()

class GitHubService:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("GITHUB_TOKEN not found in environment variables")
        self.client = Github(self.token)
        
    def get_user_info(self) -> Dict:
        """Get authenticated user information"""
        user = self.client.get_user()
        return {
            "login": user.login,
            "name": user.name,
            "email": user.email,
            "avatar_url": user.avatar_url
        }
    
    def get_repository(self, repo_name: str):
        """Get repository object"""
        try:
            return self.client.get_repo(repo_name)
        except GithubException as e:
            raise Exception(f"Repository not found: {repo_name}")
    
    def list_issues(self, repo_name: str, state: str = "open") -> List[Dict]:
        """List issues for a repository"""
        repo = self.get_repository(repo_name)
        issues = repo.get_issues(state=state)
        
        return [{
            "number": issue.number,
            "title": issue.title,
            "body": issue.body,
            "state": issue.state,
            "labels": [label.name for label in issue.labels],
            "assignees": [assignee.login for assignee in issue.assignees],
            "created_at": issue.created_at.isoformat(),
            "updated_at": issue.updated_at.isoformat(),
            "comments": issue.comments,
            "html_url": issue.html_url
        } for issue in issues]
    
    def create_issue(self, repo_name: str, title: str, body: str, labels: List[str] = None) -> Dict:
        """Create a new issue"""
        repo = self.get_repository(repo_name)
        issue = repo.create_issue(
            title=title,
            body=body,
            labels=labels or []
        )
        
        return {
            "number": issue.number,
            "title": issue.title,
            "html_url": issue.html_url,
            "created": True
        }
    
    def comment_on_issue(self, repo_name: str, issue_number: int, comment: str) -> Dict:
        """Add a comment to an issue"""
        repo = self.get_repository(repo_name)
        issue = repo.get_issue(issue_number)
        comment = issue.create_comment(comment)
        
        return {
            "id": comment.id,
            "body": comment.body,
            "created_at": comment.created_at.isoformat()
        }
    
    def list_pull_requests(self, repo_name: str, state: str = "open") -> List[Dict]:
        """List pull requests for a repository"""
        repo = self.get_repository(repo_name)
        pulls = repo.get_pulls(state=state)
        
        return [{
            "number": pr.number,
            "title": pr.title,
            "body": pr.body,
            "state": pr.state,
            "head": pr.head.ref,
            "base": pr.base.ref,
            "created_at": pr.created_at.isoformat(),
            "updated_at": pr.updated_at.isoformat(),
            "html_url": pr.html_url,
            "mergeable": pr.mergeable,
            "merged": pr.merged
        } for pr in pulls]
    
    def create_pull_request(self, repo_name: str, title: str, body: str, head: str, base: str = "main") -> Dict:
        """Create a new pull request"""
        repo = self.get_repository(repo_name)
        pr = repo.create_pull(
            title=title,
            body=body,
            head=head,
            base=base
        )
        
        return {
            "number": pr.number,
            "title": pr.title,
            "html_url": pr.html_url,
            "created": True
        }
    
    def get_workflow_runs(self, repo_name: str, limit: int = 10) -> List[Dict]:
        """Get recent workflow runs"""
        repo = self.get_repository(repo_name)
        workflows = repo.get_workflow_runs()
        
        runs = []
        for i, run in enumerate(workflows):
            if i >= limit:
                break
            runs.append({
                "id": run.id,
                "name": run.name,
                "status": run.status,
                "conclusion": run.conclusion,
                "created_at": run.created_at.isoformat(),
                "html_url": run.html_url
            })
        
        return runs
    
    def get_milestones(self, repo_name: str, state: str = "open") -> List[Dict]:
        """Get milestones for a repository"""
        repo = self.get_repository(repo_name)
        milestones = repo.get_milestones(state=state)
        
        return [{
            "number": milestone.number,
            "title": milestone.title,
            "description": milestone.description,
            "state": milestone.state,
            "open_issues": milestone.open_issues,
            "closed_issues": milestone.closed_issues,
            "due_on": milestone.due_on.isoformat() if milestone.due_on else None,
            "created_at": milestone.created_at.isoformat(),
            "updated_at": milestone.updated_at.isoformat()
        } for milestone in milestones]
    
    def create_milestone(self, repo_name: str, title: str, description: str = None, due_on: str = None) -> Dict:
        """Create a new milestone"""
        repo = self.get_repository(repo_name)
        milestone = repo.create_milestone(
            title=title,
            description=description,
            due_on=due_on
        )
        
        return {
            "number": milestone.number,
            "title": milestone.title,
            "created": True
        }
    
    def assign_issue(self, repo_name: str, issue_number: int, assignees: List[str]) -> Dict:
        """Assign users to an issue"""
        repo = self.get_repository(repo_name)
        issue = repo.get_issue(issue_number)
        issue.add_to_assignees(*assignees)
        
        return {
            "issue_number": issue_number,
            "assignees": assignees,
            "assigned": True
        }
    
    def add_labels_to_issue(self, repo_name: str, issue_number: int, labels: List[str]) -> Dict:
        """Add labels to an issue"""
        repo = self.get_repository(repo_name)
        issue = repo.get_issue(issue_number)
        issue.add_to_labels(*labels)
        
        return {
            "issue_number": issue_number,
            "labels": labels,
            "added": True
        }

    def get_commit_activity(self, repo_name: str) -> List[Dict]:
        """Get commit activity for a repository"""
        repo = self.get_repository(repo_name)
        try:
            stats = repo.get_stats_commit_activity()
            if stats is None:
                return []
            return [{"week": s.week.isoformat(), "days": s.days, "total": s.total} for s in stats]
        except GithubException as e:
            if e.status == 202:
                return [] # Data not cached yet
            raise

    def get_contributor_stats(self, repo_name: str) -> List[Dict]:
        """Get contributor statistics for a repository"""
        repo = self.get_repository(repo_name)
        try:
            stats = repo.get_stats_contributors()
            if stats is None:
                return []
            return [{
                "author": s.author.login,
                "total": s.total,
                "weeks": [{"w": w.w.isoformat(), "a": w.a, "d": w.d, "c": w.c} for w in s.weeks]
            } for s in stats]
        except GithubException as e:
            if e.status == 202:
                return [] # Data not cached yet
            raise

# Singleton instance
github_service = GitHubService()