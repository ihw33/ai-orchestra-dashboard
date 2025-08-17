#!/usr/bin/env python3
"""
Workflow Automation Script
Manages automated workflows for AI Orchestra Dashboard
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from backend.app.services.github_service import github_service
from backend.app.services.ai_orchestrator import orchestrator

class WorkflowEngine:
    """Engine for running automated workflows"""
    
    def __init__(self):
        self.workflows = {
            "document_creation": self.document_creation_workflow,
            "code_review": self.code_review_workflow,
            "issue_triage": self.issue_triage_workflow,
            "sprint_planning": self.sprint_planning_workflow
        }
        self.active_workflows = {}
    
    async def document_creation_workflow(self, params: Dict) -> Dict:
        """
        Workflow for creating documentation with AI assistance
        """
        workflow_id = f"doc_{datetime.utcnow().timestamp()}"
        
        print(f"🚀 Starting Document Creation Workflow: {workflow_id}")
        
        # Step 1: Start AI discussion about document structure
        discussion_id = await orchestrator.start_discussion(
            topic=f"Creating documentation for: {params.get('topic', 'Unknown')}",
            participants=["pm", "dev"]
        )
        
        # Step 2: Generate document outline
        outline_task = {
            "type": "planning",
            "title": "Generate document outline",
            "description": f"Create an outline for: {params.get('topic')}",
            "context": params
        }
        outline_result = await orchestrator.assign_task(outline_task)
        
        # Step 3: Generate content for each section
        sections = params.get("sections", ["Introduction", "Implementation", "Usage", "Examples"])
        content_results = []
        
        for section in sections:
            content_task = {
                "type": "development",
                "title": f"Write content for section: {section}",
                "description": f"Generate detailed content for the {section} section",
                "context": {
                    "topic": params.get("topic"),
                    "outline": outline_result.get("response"),
                    "section": section
                }
            }
            result = await orchestrator.assign_task(content_task)
            content_results.append(result)
        
        # Step 4: Review and finalize
        review_task = {
            "type": "review",
            "title": "Review and finalize documentation",
            "description": "Review the generated documentation for completeness and accuracy",
            "context": {
                "outline": outline_result,
                "content": content_results
            }
        }
        final_result = await orchestrator.assign_task(review_task)
        
        # Step 5: Create GitHub issue with documentation
        if params.get("create_issue", True):
            issue = github_service.create_issue(
                repo_name=params.get("repo", "ai-orchestra-dashboard"),
                title=f"Documentation: {params.get('topic')}",
                body=final_result.get("response", "Documentation generated"),
                labels=["documentation", "ai-generated"]
            )
            print(f"✅ Documentation issue created: {issue['html_url']}")
        
        return {
            "workflow_id": workflow_id,
            "status": "completed",
            "discussion_id": discussion_id,
            "results": {
                "outline": outline_result,
                "content": content_results,
                "final": final_result
            }
        }
    
    async def code_review_workflow(self, params: Dict) -> Dict:
        """
        Workflow for automated code review
        """
        pr_number = params.get("pr_number")
        repo_name = params.get("repo", "ai-orchestra-dashboard")
        
        print(f"🔍 Starting Code Review Workflow for PR #{pr_number}")
        
        # Step 1: Fetch PR details
        prs = github_service.list_pull_requests(repo_name)
        pr = next((pr for pr in prs if pr["number"] == pr_number), None)
        
        if not pr:
            return {"error": f"PR #{pr_number} not found"}
        
        # Step 2: AI review
        review_task = {
            "type": "review",
            "title": f"Review PR #{pr_number}: {pr['title']}",
            "description": "Perform code review and provide feedback",
            "context": pr
        }
        review_result = await orchestrator.assign_task(review_task)
        
        # Step 3: Post review comment
        if review_result.get("status") == "completed":
            comment = github_service.comment_on_issue(
                repo_name=repo_name,
                issue_number=pr_number,
                comment=f"🤖 **AI Code Review**\n\n{review_result.get('response', 'Review completed')}"
            )
            print(f"✅ Review comment posted on PR #{pr_number}")
        
        return {
            "workflow": "code_review",
            "pr_number": pr_number,
            "status": review_result.get("status"),
            "review": review_result
        }
    
    async def issue_triage_workflow(self, params: Dict) -> Dict:
        """
        Workflow for triaging new issues
        """
        repo_name = params.get("repo", "ai-orchestra-dashboard")
        
        print(f"📋 Starting Issue Triage Workflow")
        
        # Step 1: Fetch open issues without labels
        issues = github_service.list_issues(repo_name, state="open")
        untriaged_issues = [i for i in issues if not i["labels"]]
        
        results = []
        
        for issue in untriaged_issues:
            # Step 2: AI analysis
            triage_task = {
                "type": "management",
                "title": f"Triage issue #{issue['number']}",
                "description": f"Analyze and categorize: {issue['title']}",
                "context": issue
            }
            triage_result = await orchestrator.assign_task(triage_task)
            
            # Step 3: Apply labels based on analysis
            if triage_result.get("status") == "completed":
                # Parse AI response to determine labels
                response = triage_result.get("response", "")
                labels = []
                
                if "bug" in response.lower():
                    labels.append("bug")
                elif "feature" in response.lower():
                    labels.append("enhancement")
                elif "documentation" in response.lower():
                    labels.append("documentation")
                
                if "high priority" in response.lower() or "urgent" in response.lower():
                    labels.append("priority-high")
                elif "low priority" in response.lower():
                    labels.append("priority-low")
                else:
                    labels.append("priority-medium")
                
                # Apply labels
                if labels:
                    github_service.add_labels_to_issue(
                        repo_name=repo_name,
                        issue_number=issue["number"],
                        labels=labels
                    )
                    print(f"✅ Labels applied to issue #{issue['number']}: {labels}")
                
                results.append({
                    "issue_number": issue["number"],
                    "labels": labels,
                    "analysis": triage_result
                })
        
        return {
            "workflow": "issue_triage",
            "issues_processed": len(results),
            "results": results
        }
    
    async def sprint_planning_workflow(self, params: Dict) -> Dict:
        """
        Workflow for sprint planning with AI assistance
        """
        sprint_name = params.get("sprint_name", f"Sprint {datetime.utcnow().strftime('%Y-%m-%d')}")
        repo_name = params.get("repo", "ai-orchestra-dashboard")
        
        print(f"📅 Starting Sprint Planning Workflow: {sprint_name}")
        
        # Step 1: Create milestone
        milestone = github_service.create_milestone(
            repo_name=repo_name,
            title=sprint_name,
            description=f"Sprint planned with AI assistance on {datetime.utcnow().isoformat()}"
        )
        
        # Step 2: Start AI discussion for sprint planning
        discussion_id = await orchestrator.start_discussion(
            topic=f"Sprint planning for: {sprint_name}",
            participants=["pm", "dev"]
        )
        
        # Step 3: Analyze backlog and prioritize
        issues = github_service.list_issues(repo_name, state="open")
        
        prioritization_task = {
            "type": "planning",
            "title": "Prioritize backlog for sprint",
            "description": f"Analyze and prioritize issues for {sprint_name}",
            "context": {
                "issues": issues[:10],  # Limit to first 10 issues
                "sprint_capacity": params.get("capacity", 5)
            }
        }
        priority_result = await orchestrator.assign_task(prioritization_task)
        
        # Step 4: Assign issues to sprint (milestone)
        # This would normally parse the AI response to determine which issues to include
        # For demo purposes, we'll assign the first few high-priority issues
        high_priority_issues = [i for i in issues if any("priority-high" in label for label in i["labels"])][:3]
        
        for issue in high_priority_issues:
            # Assign to milestone (would need to implement this in github_service)
            print(f"📌 Assigning issue #{issue['number']} to {sprint_name}")
        
        # Step 5: Generate sprint report
        report_task = {
            "type": "management",
            "title": "Generate sprint report",
            "description": f"Create sprint planning report for {sprint_name}",
            "context": {
                "milestone": milestone,
                "assigned_issues": high_priority_issues,
                "prioritization": priority_result
            }
        }
        report_result = await orchestrator.assign_task(report_task)
        
        return {
            "workflow": "sprint_planning",
            "sprint_name": sprint_name,
            "milestone": milestone,
            "discussion_id": discussion_id,
            "assigned_issues": len(high_priority_issues),
            "report": report_result
        }
    
    async def run_workflow(self, workflow_name: str, params: Dict = None) -> Dict:
        """Run a specific workflow"""
        if workflow_name not in self.workflows:
            return {"error": f"Unknown workflow: {workflow_name}"}
        
        workflow_func = self.workflows[workflow_name]
        
        try:
            result = await workflow_func(params or {})
            return result
        except Exception as e:
            return {
                "error": f"Workflow failed: {str(e)}",
                "workflow": workflow_name,
                "status": "failed"
            }

async def main():
    """Main entry point for CLI usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Orchestra Workflow Automation")
    parser.add_argument("workflow", choices=["document", "review", "triage", "sprint"],
                       help="Workflow to run")
    parser.add_argument("--repo", default="ai-orchestra-dashboard",
                       help="GitHub repository")
    parser.add_argument("--pr", type=int, help="PR number for review workflow")
    parser.add_argument("--topic", help="Topic for documentation workflow")
    parser.add_argument("--sprint", help="Sprint name for planning workflow")
    
    args = parser.parse_args()
    
    engine = WorkflowEngine()
    
    # Prepare parameters based on workflow
    params = {"repo": args.repo}
    
    if args.workflow == "document":
        params["topic"] = args.topic or "API Documentation"
        result = await engine.run_workflow("document_creation", params)
    elif args.workflow == "review" and args.pr:
        params["pr_number"] = args.pr
        result = await engine.run_workflow("code_review", params)
    elif args.workflow == "triage":
        result = await engine.run_workflow("issue_triage", params)
    elif args.workflow == "sprint":
        params["sprint_name"] = args.sprint or f"Sprint {datetime.utcnow().strftime('%Y-%m-%d')}"
        result = await engine.run_workflow("sprint_planning", params)
    else:
        print("❌ Invalid workflow or missing parameters")
        return
    
    print("\n📊 Workflow Result:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(main())