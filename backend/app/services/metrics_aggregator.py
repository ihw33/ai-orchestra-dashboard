# backend/app/services/metrics_aggregator.py

class MetricsAggregator:
    def aggregate_metrics(self, all_issues, all_prs, all_commit_activity, all_contributor_stats, repositories):
        metrics = {}

        for repo_name in repositories:
            repo_issues = all_issues.get(repo_name, [])
            repo_prs = all_prs.get(repo_name, [])
            commit_activity = all_commit_activity.get(repo_name, [])
            contributor_stats = all_contributor_stats.get(repo_name, [])

            metrics[repo_name] = {
                'issues': {
                    'open': len([i for i in repo_issues if i['state'] == 'open']),
                    'closed': len([i for i in repo_issues if i['state'] == 'closed']),
                },
                'prs': {
                    'open': len([p for p in repo_prs if p['state'] == 'open']),
                    'merged': len([p for p in repo_prs if p['merged']]),
                    'draft': len([p for p in repo_prs if p.get('draft')]),
                },
                'commit_frequency': {
                    'weekly_commits': commit_activity
                },
                'contributor_activity': {
                    'contributors': contributor_stats
                }
            }
        return metrics
