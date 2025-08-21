#!/usr/bin/env python3
"""
Real-time AI Chat Bridge Service
Enables real-time communication between multiple AI agents through WebSocket
"""
import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field, asdict
from enum import Enum
import uuid
from collections import defaultdict

logger = logging.getLogger(__name__)

class MessageType(Enum):
    """Message types for AI communication"""
    CHAT = "chat"
    COMMAND = "command"
    STATUS = "status"
    TASK = "task"
    RESPONSE = "response"
    ERROR = "error"
    HEARTBEAT = "heartbeat"
    BROADCAST = "broadcast"

class AIRole(Enum):
    """AI Agent roles"""
    PM = "pm"
    FRONTEND = "frontend"
    BACKEND = "backend"
    ARCHITECT = "architect"
    QA = "qa"

@dataclass
class AIAgent:
    """Represents an AI agent in the chat bridge"""
    agent_id: str
    name: str
    role: AIRole
    status: str = "online"
    last_seen: datetime = field(default_factory=datetime.now)
    current_task: Optional[str] = None
    websocket: Optional[Any] = None  # WebSocket connection
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "role": self.role.value,
            "status": self.status,
            "last_seen": self.last_seen.isoformat(),
            "current_task": self.current_task
        }

@dataclass
class ChatMessage:
    """Represents a chat message between AI agents"""
    message_id: str
    sender_id: str
    sender_name: str
    recipient_id: Optional[str]  # None for broadcast
    message_type: MessageType
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "message_id": self.message_id,
            "sender_id": self.sender_id,
            "sender_name": self.sender_name,
            "recipient_id": self.recipient_id,
            "message_type": self.message_type.value,
            "content": self.content,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat()
        }

class AIChatBridge:
    """Main service for managing AI agent communication"""
    
    def __init__(self):
        self.agents: Dict[str, AIAgent] = {}
        self.message_history: List[ChatMessage] = []
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.subscribers: Dict[str, Set[str]] = defaultdict(set)  # topic -> agent_ids
        self.active_tasks: Dict[str, Dict] = {}  # task_id -> task_info
        self.running = False
        self._lock = asyncio.Lock()
        
        logger.info("AI Chat Bridge initialized")
    
    async def register_agent(self, name: str, role: str, websocket: Any = None) -> AIAgent:
        """Register a new AI agent"""
        async with self._lock:
            agent_id = str(uuid.uuid4())
            agent = AIAgent(
                agent_id=agent_id,
                name=name,
                role=AIRole(role),
                websocket=websocket
            )
            self.agents[agent_id] = agent
            
            # Auto-subscribe to role-based topics
            self.subscribers[f"role:{role}"].add(agent_id)
            self.subscribers["broadcast"].add(agent_id)
            
            # Notify other agents
            await self._broadcast_status_update(agent, "joined")
            
            logger.info(f"Agent registered: {name} ({role}) - ID: {agent_id}")
            return agent
    
    async def unregister_agent(self, agent_id: str):
        """Unregister an AI agent"""
        async with self._lock:
            if agent_id in self.agents:
                agent = self.agents[agent_id]
                agent.status = "offline"
                
                # Remove from all subscriptions
                for topic_agents in self.subscribers.values():
                    topic_agents.discard(agent_id)
                
                # Notify other agents
                await self._broadcast_status_update(agent, "left")
                
                del self.agents[agent_id]
                logger.info(f"Agent unregistered: {agent.name} - ID: {agent_id}")
    
    async def send_message(self, sender_id: str, recipient_id: Optional[str], 
                          message_type: str, content: str, metadata: Dict = None) -> ChatMessage:
        """Send a message from one agent to another or broadcast"""
        if sender_id not in self.agents:
            raise ValueError(f"Unknown sender: {sender_id}")
        
        sender = self.agents[sender_id]
        message = ChatMessage(
            message_id=str(uuid.uuid4()),
            sender_id=sender_id,
            sender_name=sender.name,
            recipient_id=recipient_id,
            message_type=MessageType(message_type),
            content=content,
            metadata=metadata or {}
        )
        
        # Store in history
        self.message_history.append(message)
        
        # Queue for processing
        await self.message_queue.put(message)
        
        logger.info(f"Message queued: {sender.name} -> {recipient_id or 'broadcast'}: {content[:50]}...")
        return message
    
    async def _broadcast_status_update(self, agent: AIAgent, action: str):
        """Broadcast agent status update to all connected agents"""
        status_message = ChatMessage(
            message_id=str(uuid.uuid4()),
            sender_id="system",
            sender_name="System",
            recipient_id=None,
            message_type=MessageType.STATUS,
            content=f"{agent.name} has {action}",
            metadata={
                "agent_info": agent.to_dict(),
                "action": action
            }
        )
        
        await self.message_queue.put(status_message)
    
    async def process_messages(self):
        """Main message processing loop"""
        self.running = True
        logger.info("Message processing started")
        
        while self.running:
            try:
                # Get message from queue with timeout
                message = await asyncio.wait_for(self.message_queue.get(), timeout=1.0)
                
                # Route message
                await self._route_message(message)
                
                # Update sender activity
                if message.sender_id in self.agents:
                    self.agents[message.sender_id].last_seen = datetime.now()
                    
            except asyncio.TimeoutError:
                # Check for inactive agents
                await self._check_agent_health()
            except Exception as e:
                logger.error(f"Error processing message: {e}")
    
    async def _route_message(self, message: ChatMessage):
        """Route message to appropriate recipients"""
        if message.recipient_id:
            # Direct message
            if message.recipient_id in self.agents:
                await self._deliver_message(message.recipient_id, message)
        else:
            # Broadcast message
            for agent_id in self.subscribers["broadcast"]:
                if agent_id != message.sender_id:  # Don't send back to sender
                    await self._deliver_message(agent_id, message)
    
    async def _deliver_message(self, agent_id: str, message: ChatMessage):
        """Deliver message to specific agent"""
        if agent_id not in self.agents:
            return
        
        agent = self.agents[agent_id]
        
        # If agent has WebSocket connection, send through it
        if agent.websocket:
            try:
                await agent.websocket.send_text(json.dumps(message.to_dict()))
                logger.debug(f"Message delivered to {agent.name} via WebSocket")
            except Exception as e:
                logger.error(f"Failed to deliver message to {agent.name}: {e}")
                agent.status = "error"
        else:
            # Store for polling
            logger.debug(f"Message stored for {agent.name} (no WebSocket)")
    
    async def _check_agent_health(self):
        """Check health of all agents"""
        current_time = datetime.now()
        timeout_seconds = 60  # Consider agent offline after 60 seconds
        
        async with self._lock:
            for agent_id, agent in list(self.agents.items()):
                time_diff = (current_time - agent.last_seen).total_seconds()
                
                if time_diff > timeout_seconds and agent.status == "online":
                    agent.status = "offline"
                    await self._broadcast_status_update(agent, "timed out")
                    logger.warning(f"Agent {agent.name} marked as offline (timeout)")
    
    async def assign_task(self, task_id: str, agent_id: str, task_description: str, 
                         priority: str = "normal") -> Dict:
        """Assign a task to an AI agent"""
        if agent_id not in self.agents:
            raise ValueError(f"Unknown agent: {agent_id}")
        
        agent = self.agents[agent_id]
        
        # Create task
        task = {
            "task_id": task_id,
            "agent_id": agent_id,
            "agent_name": agent.name,
            "description": task_description,
            "priority": priority,
            "status": "assigned",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Store task
        self.active_tasks[task_id] = task
        
        # Update agent
        agent.current_task = task_id
        
        # Send task message
        await self.send_message(
            sender_id="system",
            recipient_id=agent_id,
            message_type="task",
            content=task_description,
            metadata=task
        )
        
        logger.info(f"Task {task_id} assigned to {agent.name}")
        return task
    
    async def update_task_status(self, task_id: str, status: str, metadata: Dict = None):
        """Update task status"""
        if task_id not in self.active_tasks:
            raise ValueError(f"Unknown task: {task_id}")
        
        task = self.active_tasks[task_id]
        task["status"] = status
        task["updated_at"] = datetime.now().isoformat()
        
        if metadata:
            task.update(metadata)
        
        # If task is completed, clear from agent
        if status in ["completed", "failed", "cancelled"]:
            agent_id = task["agent_id"]
            if agent_id in self.agents:
                self.agents[agent_id].current_task = None
        
        logger.info(f"Task {task_id} status updated to {status}")
    
    async def get_agent_status(self, agent_id: str) -> Dict:
        """Get current status of an agent"""
        if agent_id not in self.agents:
            raise ValueError(f"Unknown agent: {agent_id}")
        
        agent = self.agents[agent_id]
        return {
            **agent.to_dict(),
            "message_count": len([m for m in self.message_history if m.sender_id == agent_id]),
            "active_task": self.active_tasks.get(agent.current_task) if agent.current_task else None
        }
    
    async def get_team_status(self) -> Dict:
        """Get status of entire AI team"""
        return {
            "timestamp": datetime.now().isoformat(),
            "agents": {
                agent_id: await self.get_agent_status(agent_id)
                for agent_id in self.agents
            },
            "active_tasks": len([t for t in self.active_tasks.values() if t["status"] == "in_progress"]),
            "total_tasks": len(self.active_tasks),
            "message_count": len(self.message_history),
            "system_status": "running" if self.running else "stopped"
        }
    
    async def get_conversation_history(self, agent_id: Optional[str] = None, 
                                      limit: int = 50) -> List[Dict]:
        """Get conversation history, optionally filtered by agent"""
        messages = self.message_history
        
        if agent_id:
            messages = [
                m for m in messages 
                if m.sender_id == agent_id or m.recipient_id == agent_id
            ]
        
        # Return most recent messages
        return [m.to_dict() for m in messages[-limit:]]
    
    async def broadcast_command(self, command: str, metadata: Dict = None) -> List[str]:
        """Broadcast a command to all agents"""
        message = await self.send_message(
            sender_id="system",
            recipient_id=None,
            message_type="command",
            content=command,
            metadata=metadata or {}
        )
        
        # Return list of agent IDs that will receive the command
        return list(self.subscribers["broadcast"])
    
    async def stop(self):
        """Stop the chat bridge service"""
        self.running = False
        
        # Notify all agents
        await self.broadcast_command("shutdown", {"reason": "service_stop"})
        
        # Clear all agents
        for agent_id in list(self.agents.keys()):
            await self.unregister_agent(agent_id)
        
        logger.info("AI Chat Bridge stopped")

# WebSocket handler for FastAPI integration
class ChatBridgeWebSocketHandler:
    """WebSocket handler for AI Chat Bridge"""
    
    def __init__(self, chat_bridge: AIChatBridge):
        self.chat_bridge = chat_bridge
        self.agent_connections: Dict[str, str] = {}  # websocket -> agent_id
    
    async def handle_connection(self, websocket):
        """Handle new WebSocket connection"""
        agent_id = None
        try:
            # Wait for registration message
            data = await websocket.receive_text()
            registration = json.loads(data)
            
            if registration.get("type") != "register":
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": "First message must be registration"
                }))
                return
            
            # Register agent
            agent = await self.chat_bridge.register_agent(
                name=registration["name"],
                role=registration["role"],
                websocket=websocket
            )
            agent_id = agent.agent_id
            self.agent_connections[id(websocket)] = agent_id
            
            # Send registration confirmation
            await websocket.send_text(json.dumps({
                "type": "registered",
                "agent_id": agent_id,
                "team_status": await self.chat_bridge.get_team_status()
            }))
            
            # Handle messages
            while True:
                data = await websocket.receive_text()
                message_data = json.loads(data)
                
                await self._handle_message(agent_id, message_data)
                
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
        finally:
            # Clean up
            if agent_id:
                await self.chat_bridge.unregister_agent(agent_id)
            if id(websocket) in self.agent_connections:
                del self.agent_connections[id(websocket)]
    
    async def _handle_message(self, agent_id: str, message_data: Dict):
        """Handle incoming message from agent"""
        message_type = message_data.get("type", "chat")
        
        if message_type == "heartbeat":
            # Update last seen
            if agent_id in self.chat_bridge.agents:
                self.chat_bridge.agents[agent_id].last_seen = datetime.now()
        
        elif message_type == "task_update":
            # Update task status
            await self.chat_bridge.update_task_status(
                task_id=message_data["task_id"],
                status=message_data["status"],
                metadata=message_data.get("metadata")
            )
        
        else:
            # Regular message
            await self.chat_bridge.send_message(
                sender_id=agent_id,
                recipient_id=message_data.get("recipient_id"),
                message_type=message_type,
                content=message_data["content"],
                metadata=message_data.get("metadata", {})
            )

# Example usage
if __name__ == "__main__":
    async def demo():
        # Initialize bridge
        bridge = AIChatBridge()
        
        # Start message processor
        processor_task = asyncio.create_task(bridge.process_messages())
        
        # Register agents
        pm = await bridge.register_agent("Claude", "pm")
        frontend = await bridge.register_agent("Gemini", "frontend")
        backend = await bridge.register_agent("Codex", "backend")
        
        # Send messages
        await bridge.send_message(pm.agent_id, None, "chat", "Team, let's start the daily standup")
        await bridge.send_message(frontend.agent_id, pm.agent_id, "chat", "Ready for standup!")
        await bridge.send_message(backend.agent_id, pm.agent_id, "chat", "Backend ready")
        
        # Assign task
        task = await bridge.assign_task(
            task_id="TASK-001",
            agent_id=frontend.agent_id,
            task_description="Implement user dashboard component",
            priority="high"
        )
        
        # Get team status
        status = await bridge.get_team_status()
        print(json.dumps(status, indent=2))
        
        # Wait a bit
        await asyncio.sleep(2)
        
        # Stop bridge
        await bridge.stop()
        processor_task.cancel()
    
    # Run demo
    asyncio.run(demo())