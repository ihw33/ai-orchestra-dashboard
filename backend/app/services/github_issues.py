from typing import List, Dict, Optional
from github import Github
from datetime import datetime

class IssueCollector:
    def __init__(self, github_client: GitHubClient):
        self.client = github_client
    
    def get_issues(self, repo_name: str, state='open', limit=100):
        '''저장소의 Issue 목록 가져오기'''
        repo = self.client.get_repo(repo_name)
        issues = []
        
        for issue in repo.get_issues(state=state)[:limit]:
            if not issue.pull_request:  # PR 제외
                issues.append({
                    'number': issue.number,
                    'title': issue.title,
                    'body': issue.body,
                    'state': issue.state,
                    'labels': [l.name for l in issue.labels],
                    'assignees': [a.login for a in issue.assignees],
                    'created_at': issue.created_at,
                    'updated_at': issue.updated_at,
                    'comments': issue.comments,
                    'url': issue.html_url
                })
        return issues
    
    def get_issue_comments(self, repo_name: str, issue_number: int):
        '''특정 Issue의 댓글 가져오기'''
        repo = self.client.get_repo(repo_name)
        issue = repo.get_issue(number=issue_number)
        
        comments = []
        for comment in issue.get_comments():
            comments.append({
                'id': comment.id,
                'body': comment.body,
                'user': comment.user.login,
                'created_at': comment.created_at
            })
        return comments
