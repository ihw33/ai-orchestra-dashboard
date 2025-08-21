from typing import List, Dict, Optional
from github import Github
from datetime import datetime

from .github_client import GitHubClient

class PullRequestCollector:
    def __init__(self, github_client: GitHubClient):
        self.client = github_client
    
    def get_pull_requests(self, repo_name: str, state='open', limit=100) -> List[Dict]:
        '''저장소의 Pull Request 목록 가져오기'''
        repo = self.client.get_repo(repo_name)
        pulls = []
        
        for pull in repo.get_pulls(state=state)[:limit]:
            pulls.append({
                'number': pull.number,
                'title': pull.title,
                'body': pull.body,
                'state': pull.state,
                'head': pull.head.ref,
                'base': pull.base.ref,
                'created_at': pull.created_at.isoformat(),
                'updated_at': pull.updated_at.isoformat(),
                'html_url': pull.html_url,
                'mergeable': pull.mergeable,
                'merged': pull.merged
            })
        return pulls

    def get_pull_request_reviews(self, repo_name: str, pr_number: int) -> List[Dict]:
        '''특정 Pull Request의 리뷰 가져오기'''
        repo = self.client.get_repo(repo_name)
        pull = repo.get_pull(pr_number)
        
        reviews = []
        for review in pull.get_reviews():
            reviews.append({
                'id': review.id,
                'user': review.user.login,
                'body': review.body,
                'state': review.state,
                'submitted_at': review.submitted_at.isoformat()
            })
        return reviews

    def get_pull_request_merge_status(self, repo_name: str, pr_number: int) -> Dict:
        '''특정 Pull Request의 머지 상태 가져오기'''
        repo = self.client.get_repo(repo_name)
        pull = repo.get_pull(pr_number)
        
        return {
            'merged': pull.merged,
            'mergeable': pull.mergeable,
            'merged_by': pull.merged_by.login if pull.merged_by else None,
            'merged_at': pull.merged_at.isoformat() if pull.merged_at else None
        }
