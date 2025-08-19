# backend/app/services/data_collector.py
from .github_service import github_service
from .metrics_aggregator import MetricsAggregator
from app.connection_manager import manager
import asyncio

class MultiProjectMonitor:
    def __init__(self, repositories):
        self.repositories = repositories
        self.metrics_aggregator = MetricsAggregator()
        self.is_streaming = False

    def fetch_all_issues(self):
        all_issues = {}
        for repo_name in self.repositories:
            issues = github_service.list_issues(repo_name, state='all')
            all_issues[repo_name] = issues
        return all_issues

    def fetch_all_prs(self):
        all_prs = {}
        for repo_name in self.repositories:
            prs = github_service.list_pull_requests(repo_name, state='all')
            all_prs[repo_name] = prs
        return all_prs

    def fetch_commit_activity(self):
        all_commit_activity = {}
        for repo_name in self.repositories:
            commit_activity = github_service.get_commit_activity(repo_name)
            all_commit_activity[repo_name] = commit_activity
        return all_commit_activity

    def fetch_contributor_stats(self):
        all_contributor_stats = {}
        for repo_name in self.repositories:
            contributor_stats = github_service.get_contributor_stats(repo_name)
            all_contributor_stats[repo_name] = contributor_stats
        return all_contributor_stats

    def get_aggregated_metrics(self):
        all_issues = self.fetch_all_issues()
        all_prs = self.fetch_all_prs()
        commit_activity = self.fetch_commit_activity()
        contributor_stats = self.fetch_contributor_stats()
        
        return self.metrics_aggregator.aggregate_metrics(
            all_issues,
            all_prs,
            commit_activity,
            contributor_stats,
            self.repositories
        )

    async def stream_updates(self):
        print("Getting aggregated metrics...")
        metrics = self.get_aggregated_metrics()
        print("Broadcasting metrics...")
        await manager.broadcast_json({"type": "metrics_update", "data": metrics})
        print("Metrics broadcasted.")

    async def start_streaming(self, interval_seconds=60):
        self.is_streaming = True
        print("Starting streaming...")
        while self.is_streaming:
            print("Streaming update...")
            await self.stream_updates()
            await asyncio.sleep(interval_seconds)

    def stop_streaming(self):
        self.is_streaming = False
