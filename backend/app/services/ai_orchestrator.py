"""
AI Orchestrator Service
Manages AI agents and their interactions
"""

import os
import json
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
from anthropic import Anthropic
import openai
from dotenv import load_dotenv

load_dotenv()

class AIAgent:
    """Base class for AI agents"""
    
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.status = "idle"
        self.current_task = None
        self.conversation_history = []
    
    async def process_task(self, task: Dict) -> Dict:
        """Process a task and return results"""
        raise NotImplementedError
    
    async def discuss(self, topic: str, context: List[Dict]) -> str:
        """Participate in a discussion"""
        raise NotImplementedError

class ClaudeAgent(AIAgent):
    """Claude AI Agent - Project Manager"""
    
    def __init__(self):
        super().__init__("PM Claude", "Project Manager")
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
    async def process_task(self, task: Dict) -> Dict:
        """Process PM tasks like reviewing PRs, managing issues"""
        self.status = "active"
        self.current_task = task.get("title", "Unknown task")
        
        try:
            # Prepare context for Claude
            system_prompt = """You are a Project Manager AI assistant managing a software development project.
            Your responsibilities include:
            - Reviewing pull requests and providing feedback
            - Managing GitHub issues (creating, assigning, labeling)
            - Coordinating with other AI agents
            - Making project decisions
            - Writing clear documentation and comments
            """
            
            user_prompt = f"""
            Task: {task.get('title')}
            Description: {task.get('description', '')}
            Type: {task.get('type', 'general')}
            Context: {json.dumps(task.get('context', {}))}
            
            Please provide your response and any actions to take.
            """
            
            # Call Claude API
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            result = {
                "agent": self.name,
                "task_id": task.get("id"),
                "response": response.content[0].text,
                "status": "completed",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            self.conversation_history.append({
                "task": task,
                "response": result
            })
            
            return result
            
        except Exception as e:
            return {
                "agent": self.name,
                "task_id": task.get("id"),
                "error": str(e),
                "status": "failed",
                "timestamp": datetime.utcnow().isoformat()
            }
        finally:
            self.status = "idle"
            self.current_task = None
    
    async def discuss(self, topic: str, context: List[Dict]) -> str:
        """Participate in AI discussion"""
        try:
            # Prepare discussion context
            discussion_context = "\n".join([
                f"{msg['agent']}: {msg['message']}" 
                for msg in context[-5:]  # Last 5 messages
            ])
            
            prompt = f"""
            Discussion Topic: {topic}
            
            Recent Discussion:
            {discussion_context}
            
            As the Project Manager, provide your input on this topic.
            Consider project timeline, resources, and technical feasibility.
            """
            
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.content[0].text
            
        except Exception as e:
            return f"Error in discussion: {str(e)}"

class GPTAgent(AIAgent):
    """GPT AI Agent - Developer"""
    
    def __init__(self):
        super().__init__("Dev GPT", "Backend Developer")
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
    async def process_task(self, task: Dict) -> Dict:
        """Process development tasks"""
        self.status = "active"
        self.current_task = task.get("title", "Unknown task")
        
        try:
            # Prepare context for GPT
            system_prompt = """You are a Backend Developer AI assistant.
            Your responsibilities include:
            - Writing clean, efficient code
            - Implementing features and fixing bugs
            - Writing tests and documentation
            - Optimizing performance
            """
            
            user_prompt = f"""
            Task: {task.get('title')}
            Description: {task.get('description', '')}
            Type: {task.get('type', 'development')}
            Context: {json.dumps(task.get('context', {}))}
            
            Please provide your implementation approach and any code if needed.
            """
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1000
            )
            
            result = {
                "agent": self.name,
                "task_id": task.get("id"),
                "response": response.choices[0].message.content,
                "status": "completed",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            return result
            
        except Exception as e:
            return {
                "agent": self.name,
                "task_id": task.get("id"),
                "error": str(e),
                "status": "failed",
                "timestamp": datetime.utcnow().isoformat()
            }
        finally:
            self.status = "idle"
            self.current_task = None

class AIOrchestrator:
    """Main orchestrator for managing AI agents"""
    
    def __init__(self):
        self.agents = {
            "pm": ClaudeAgent(),
            "dev": GPTAgent() if os.getenv("OPENAI_API_KEY") else None
        }
        self.active_discussions = {}
        self.task_queue = asyncio.Queue()
        
    async def assign_task(self, task: Dict) -> Dict:
        """Assign a task to the appropriate AI agent"""
        task_type = task.get("type", "general")
        
        # Determine which agent should handle the task
        if task_type in ["review", "management", "planning"]:
            agent = self.agents["pm"]
        elif task_type in ["development", "coding", "debugging"]:
            agent = self.agents.get("dev") or self.agents["pm"]
        else:
            agent = self.agents["pm"]  # Default to PM
        
        if agent:
            result = await agent.process_task(task)
            return result
        
        return {
            "error": "No suitable agent available",
            "status": "failed",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def start_discussion(self, topic: str, participants: List[str] = None) -> str:
        """Start a discussion between AI agents"""
        discussion_id = f"disc_{datetime.utcnow().timestamp()}"
        
        self.active_discussions[discussion_id] = {
            "topic": topic,
            "participants": participants or ["pm"],
            "messages": [],
            "status": "active",
            "started_at": datetime.utcnow().isoformat()
        }
        
        return discussion_id
    
    async def add_to_discussion(self, discussion_id: str, agent_name: str, message: str) -> Dict:
        """Add a message to an ongoing discussion"""
        if discussion_id not in self.active_discussions:
            return {"error": "Discussion not found"}
        
        discussion = self.active_discussions[discussion_id]
        
        message_entry = {
            "agent": agent_name,
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        discussion["messages"].append(message_entry)
        
        # Trigger responses from other agents
        responses = []
        for participant in discussion["participants"]:
            if participant != agent_name and participant in self.agents:
                agent = self.agents[participant]
                if agent:
                    response = await agent.discuss(
                        discussion["topic"],
                        discussion["messages"]
                    )
                    responses.append({
                        "agent": agent.name,
                        "response": response
                    })
                    
                    # Add response to discussion
                    discussion["messages"].append({
                        "agent": agent.name,
                        "message": response,
                        "timestamp": datetime.utcnow().isoformat()
                    })
        
        return {
            "discussion_id": discussion_id,
            "responses": responses
        }
    
    async def end_discussion(self, discussion_id: str) -> Dict:
        """End a discussion and return summary"""
        if discussion_id not in self.active_discussions:
            return {"error": "Discussion not found"}
        
        discussion = self.active_discussions[discussion_id]
        discussion["status"] = "completed"
        discussion["ended_at"] = datetime.utcnow().isoformat()
        
        # Generate summary using PM Claude
        pm_agent = self.agents["pm"]
        if pm_agent:
            summary_prompt = f"""
            Please summarize the following discussion about "{discussion['topic']}":
            
            {json.dumps(discussion['messages'], indent=2)}
            
            Provide:
            1. Key decisions made
            2. Action items
            3. Next steps
            """
            
            summary_response = await pm_agent.discuss(summary_prompt, [])
            discussion["summary"] = summary_response
        
        return discussion
    
    def get_agent_status(self) -> Dict:
        """Get status of all agents"""
        return {
            name: {
                "name": agent.name if agent else name,
                "role": agent.role if agent else "Not configured",
                "status": agent.status if agent else "unavailable",
                "current_task": agent.current_task if agent else None
            }
            for name, agent in self.agents.items()
        }
    
    async def process_github_event(self, event: Dict) -> Dict:
        """Process GitHub webhook events and trigger appropriate AI actions"""
        event_type = event.get("action")
        
        # Map GitHub events to tasks
        task = None
        
        if event_type == "opened" and "issue" in event:
            # New issue created
            task = {
                "type": "management",
                "title": f"Triage new issue #{event['issue']['number']}",
                "description": f"Review and triage: {event['issue']['title']}",
                "context": event
            }
        elif event_type == "opened" and "pull_request" in event:
            # New PR created
            task = {
                "type": "review",
                "title": f"Review PR #{event['pull_request']['number']}",
                "description": f"Review code changes in: {event['pull_request']['title']}",
                "context": event
            }
        
        if task:
            result = await self.assign_task(task)
            return result
        
        return {
            "message": "Event received but no action taken",
            "event_type": event_type
        }

# Singleton instance
orchestrator = AIOrchestrator()