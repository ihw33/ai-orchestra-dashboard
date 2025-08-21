#!/usr/bin/env python3
"""
FastAPI Router for AI Chat Bridge
Provides WebSocket and REST endpoints for AI agent communication
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Dict, List, Optional, Any
import json
import logging
from datetime import datetime

from ..services.ai_chat_bridge import (
    AIChatBridge, 
    ChatBridgeWebSocketHandler,
    AIRole,
    MessageType
)

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/api/chat-bridge",
    tags=["chat-bridge"],
    responses={404: {"description": "Not found"}},
)

# Initialize chat bridge (singleton)
chat_bridge = AIChatBridge()
ws_handler = ChatBridgeWebSocketHandler(chat_bridge)

# Background task to process messages
import asyncio
message_processor_task = None

@router.on_event("startup")
async def startup_event():
    """Start message processor on startup"""
    global message_processor_task
    message_processor_task = asyncio.create_task(chat_bridge.process_messages())
    logger.info("Chat Bridge message processor started")

@router.on_event("shutdown")
async def shutdown_event():
    """Stop message processor on shutdown"""
    global message_processor_task
    if message_processor_task:
        await chat_bridge.stop()
        message_processor_task.cancel()
        logger.info("Chat Bridge message processor stopped")

# WebSocket endpoint
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time AI agent communication"""
    await websocket.accept()
    try:
        await ws_handler.handle_connection(websocket)
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close()

# REST endpoints

@router.post("/agents/register")
async def register_agent(name: str, role: str) -> Dict:
    """Register a new AI agent via REST API"""
    try:
        # Validate role
        if role not in [r.value for r in AIRole]:
            raise HTTPException(status_code=400, detail=f"Invalid role: {role}")
        
        agent = await chat_bridge.register_agent(name, role)
        return {
            "success": True,
            "agent": agent.to_dict(),
            "message": f"Agent {name} registered successfully"
        }
    except Exception as e:
        logger.error(f"Failed to register agent: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/agents/{agent_id}")
async def unregister_agent(agent_id: str) -> Dict:
    """Unregister an AI agent"""
    try:
        await chat_bridge.unregister_agent(agent_id)
        return {
            "success": True,
            "message": f"Agent {agent_id} unregistered successfully"
        }
    except Exception as e:
        logger.error(f"Failed to unregister agent: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/agents")
async def get_agents() -> Dict:
    """Get list of all registered agents"""
    agents = {
        agent_id: agent.to_dict() 
        for agent_id, agent in chat_bridge.agents.items()
    }
    return {
        "agents": agents,
        "count": len(agents),
        "timestamp": datetime.now().isoformat()
    }

@router.get("/agents/{agent_id}")
async def get_agent_status(agent_id: str) -> Dict:
    """Get status of a specific agent"""
    try:
        status = await chat_bridge.get_agent_status(agent_id)
        return {
            "success": True,
            "agent": status
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to get agent status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/messages/send")
async def send_message(
    sender_id: str,
    content: str,
    recipient_id: Optional[str] = None,
    message_type: str = "chat",
    metadata: Optional[Dict] = None
) -> Dict:
    """Send a message from one agent to another"""
    try:
        # Validate message type
        if message_type not in [t.value for t in MessageType]:
            raise HTTPException(status_code=400, detail=f"Invalid message type: {message_type}")
        
        message = await chat_bridge.send_message(
            sender_id=sender_id,
            recipient_id=recipient_id,
            message_type=message_type,
            content=content,
            metadata=metadata or {}
        )
        
        return {
            "success": True,
            "message": message.to_dict()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to send message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/messages/broadcast")
async def broadcast_message(
    content: str,
    message_type: str = "broadcast",
    metadata: Optional[Dict] = None
) -> Dict:
    """Broadcast a message to all agents"""
    try:
        recipient_ids = await chat_bridge.broadcast_command(content, metadata)
        return {
            "success": True,
            "recipients": recipient_ids,
            "count": len(recipient_ids),
            "message": content
        }
    except Exception as e:
        logger.error(f"Failed to broadcast message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/messages/history")
async def get_message_history(
    agent_id: Optional[str] = None,
    limit: int = 50
) -> Dict:
    """Get message history"""
    try:
        history = await chat_bridge.get_conversation_history(agent_id, limit)
        return {
            "messages": history,
            "count": len(history),
            "filtered_by": agent_id if agent_id else "all"
        }
    except Exception as e:
        logger.error(f"Failed to get message history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tasks/assign")
async def assign_task(
    task_id: str,
    agent_id: str,
    description: str,
    priority: str = "normal"
) -> Dict:
    """Assign a task to an AI agent"""
    try:
        task = await chat_bridge.assign_task(
            task_id=task_id,
            agent_id=agent_id,
            task_description=description,
            priority=priority
        )
        return {
            "success": True,
            "task": task
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to assign task: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/tasks/{task_id}/status")
async def update_task_status(
    task_id: str,
    status: str,
    metadata: Optional[Dict] = None
) -> Dict:
    """Update task status"""
    try:
        await chat_bridge.update_task_status(task_id, status, metadata)
        return {
            "success": True,
            "task_id": task_id,
            "status": status,
            "updated_at": datetime.now().isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to update task status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tasks")
async def get_tasks() -> Dict:
    """Get all tasks"""
    return {
        "tasks": chat_bridge.active_tasks,
        "count": len(chat_bridge.active_tasks),
        "active": len([t for t in chat_bridge.active_tasks.values() if t["status"] == "in_progress"])
    }

@router.get("/status")
async def get_system_status() -> Dict:
    """Get overall system status"""
    try:
        status = await chat_bridge.get_team_status()
        return {
            "success": True,
            "status": status
        }
    except Exception as e:
        logger.error(f"Failed to get system status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check() -> Dict:
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI Chat Bridge",
        "running": chat_bridge.running,
        "agents_online": len([a for a in chat_bridge.agents.values() if a.status == "online"]),
        "total_agents": len(chat_bridge.agents),
        "message_queue_size": chat_bridge.message_queue.qsize(),
        "timestamp": datetime.now().isoformat()
    }

# WebSocket client example documentation
@router.get("/ws/example")
async def websocket_example() -> Dict:
    """Get WebSocket client example"""
    return {
        "description": "WebSocket client example for AI agents",
        "endpoint": "ws://localhost:8000/api/chat-bridge/ws",
        "example_messages": {
            "register": {
                "type": "register",
                "name": "MyAI",
                "role": "backend"
            },
            "send_message": {
                "type": "chat",
                "recipient_id": None,  # null for broadcast
                "content": "Hello team!",
                "metadata": {}
            },
            "task_update": {
                "type": "task_update",
                "task_id": "TASK-001",
                "status": "in_progress",
                "metadata": {"progress": 50}
            },
            "heartbeat": {
                "type": "heartbeat"
            }
        },
        "expected_responses": {
            "registered": {
                "type": "registered",
                "agent_id": "uuid",
                "team_status": {}
            },
            "message": {
                "message_id": "uuid",
                "sender_id": "uuid",
                "sender_name": "AgentName",
                "recipient_id": "uuid or null",
                "message_type": "chat",
                "content": "message content",
                "metadata": {},
                "timestamp": "ISO 8601"
            },
            "error": {
                "type": "error",
                "message": "error description"
            }
        }
    }