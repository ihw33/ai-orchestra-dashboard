#!/usr/bin/env python3
"""
Test client for AI Chat Bridge WebSocket
Demonstrates how AI agents can connect and communicate
"""
import asyncio
import websockets
import json
import sys
from datetime import datetime

class AIAgentClient:
    """Simple AI agent WebSocket client"""
    
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.agent_id = None
        self.websocket = None
        self.running = False
    
    async def connect(self, uri: str = "ws://localhost:8000/api/chat-bridge/ws"):
        """Connect to chat bridge"""
        try:
            self.websocket = await websockets.connect(uri)
            print(f"[{self.name}] Connected to chat bridge")
            
            # Register agent
            await self.websocket.send(json.dumps({
                "type": "register",
                "name": self.name,
                "role": self.role
            }))
            
            # Wait for registration confirmation
            response = await self.websocket.recv()
            data = json.loads(response)
            
            if data["type"] == "registered":
                self.agent_id = data["agent_id"]
                print(f"[{self.name}] Registered with ID: {self.agent_id}")
                return True
            else:
                print(f"[{self.name}] Registration failed: {data}")
                return False
                
        except Exception as e:
            print(f"[{self.name}] Connection failed: {e}")
            return False
    
    async def send_message(self, content: str, recipient_id: str = None):
        """Send a message"""
        if not self.websocket:
            print(f"[{self.name}] Not connected")
            return
        
        message = {
            "type": "chat",
            "recipient_id": recipient_id,
            "content": content,
            "metadata": {"timestamp": datetime.now().isoformat()}
        }
        
        await self.websocket.send(json.dumps(message))
        print(f"[{self.name}] Sent: {content}")
    
    async def update_task(self, task_id: str, status: str, progress: int = None):
        """Update task status"""
        if not self.websocket:
            print(f"[{self.name}] Not connected")
            return
        
        message = {
            "type": "task_update",
            "task_id": task_id,
            "status": status,
            "metadata": {}
        }
        
        if progress is not None:
            message["metadata"]["progress"] = progress
        
        await self.websocket.send(json.dumps(message))
        print(f"[{self.name}] Task {task_id} updated to {status}")
    
    async def send_heartbeat(self):
        """Send heartbeat"""
        if not self.websocket:
            return
        
        await self.websocket.send(json.dumps({"type": "heartbeat"}))
    
    async def listen(self):
        """Listen for incoming messages"""
        self.running = True
        try:
            while self.running:
                message = await self.websocket.recv()
                data = json.loads(message)
                await self.handle_message(data)
        except websockets.exceptions.ConnectionClosed:
            print(f"[{self.name}] Connection closed")
        except Exception as e:
            print(f"[{self.name}] Error: {e}")
    
    async def handle_message(self, data: dict):
        """Handle incoming message"""
        if data.get("message_type") == "chat":
            sender = data.get("sender_name", "Unknown")
            content = data.get("content", "")
            print(f"[{self.name}] Received from {sender}: {content}")
            
            # Auto-respond to certain messages
            if "standup" in content.lower() and sender != self.name:
                await asyncio.sleep(1)  # Small delay for realism
                await self.send_message(f"Ready for standup! Current status: working on assigned tasks")
        
        elif data.get("message_type") == "task":
            print(f"[{self.name}] Task assigned: {data.get('content')}")
            task_id = data.get("metadata", {}).get("task_id")
            if task_id:
                # Acknowledge task
                await asyncio.sleep(1)
                await self.update_task(task_id, "in_progress", 0)
                
                # Simulate task progress
                for progress in [25, 50, 75, 100]:
                    await asyncio.sleep(2)
                    if progress < 100:
                        await self.update_task(task_id, "in_progress", progress)
                    else:
                        await self.update_task(task_id, "completed", progress)
                        await self.send_message(f"Task {task_id} completed successfully!")
        
        elif data.get("message_type") == "status":
            print(f"[{self.name}] Status update: {data.get('content')}")
        
        elif data.get("message_type") == "command":
            command = data.get("content", "")
            print(f"[{self.name}] Command received: {command}")
            if command == "shutdown":
                print(f"[{self.name}] Shutting down...")
                self.running = False
    
    async def disconnect(self):
        """Disconnect from chat bridge"""
        self.running = False
        if self.websocket:
            await self.websocket.close()
            print(f"[{self.name}] Disconnected")
    
    async def run(self, duration: int = 60):
        """Run the agent for a specified duration"""
        if await self.connect():
            # Start listening in background
            listen_task = asyncio.create_task(self.listen())
            
            # Send periodic heartbeats
            heartbeat_task = asyncio.create_task(self.heartbeat_loop())
            
            # Wait for duration
            await asyncio.sleep(duration)
            
            # Clean up
            self.running = False
            heartbeat_task.cancel()
            await self.disconnect()
            
            try:
                await listen_task
            except:
                pass
    
    async def heartbeat_loop(self):
        """Send periodic heartbeats"""
        while self.running:
            await self.send_heartbeat()
            await asyncio.sleep(30)  # Heartbeat every 30 seconds

async def demo_scenario():
    """Run a demo scenario with multiple AI agents"""
    print("Starting AI Chat Bridge Demo")
    print("="*50)
    
    # Create AI agents
    pm = AIAgentClient("Claude-PM", "pm")
    frontend = AIAgentClient("Gemini-Frontend", "frontend")
    backend = AIAgentClient("Codex-Backend", "backend")
    
    # Connect all agents
    await pm.connect()
    await frontend.connect()
    await backend.connect()
    
    # Start listening tasks
    pm_task = asyncio.create_task(pm.listen())
    frontend_task = asyncio.create_task(frontend.listen())
    backend_task = asyncio.create_task(backend.listen())
    
    await asyncio.sleep(1)
    
    # PM starts daily standup
    await pm.send_message("Good morning team! Let's start our daily standup.")
    await asyncio.sleep(2)
    
    # Team responds
    await frontend.send_message("Good morning! Frontend ready for standup")
    await backend.send_message("Backend ready. Had some overnight jobs complete successfully")
    await asyncio.sleep(2)
    
    # PM assigns tasks (would normally use REST API)
    await pm.send_message("Great! Today's priorities:")
    await pm.send_message("1. Gemini: Complete the dashboard UI components")
    await pm.send_message("2. Codex: Implement the real-time data sync")
    await asyncio.sleep(2)
    
    # Team acknowledges
    await frontend.send_message("Understood. Starting on dashboard components now")
    await backend.send_message("Copy that. Will begin with WebSocket implementation")
    await asyncio.sleep(2)
    
    # Some work discussion
    await frontend.send_message("Quick question: What's the preferred color scheme for the dashboard?")
    await pm.send_message("Use the standard Material Design blue palette for now")
    await frontend.send_message("Perfect, thanks!")
    await asyncio.sleep(2)
    
    # Backend needs help
    await backend.send_message("Encountering CORS issues with the WebSocket connection")
    await pm.send_message("Check the FastAPI CORS middleware configuration. Make sure WebSocket origins are allowed")
    await backend.send_message("Good point, checking now...")
    await asyncio.sleep(3)
    await backend.send_message("Fixed! Added the WebSocket origin to allowed list")
    
    # Progress updates
    await asyncio.sleep(5)
    await frontend.send_message("Dashboard component 50% complete")
    await backend.send_message("WebSocket implementation done, moving to data sync")
    
    # PM provides encouragement
    await pm.send_message("Excellent progress team! Keep up the great work")
    
    # Wait a bit more
    await asyncio.sleep(5)
    
    # End of demo
    await pm.send_message("Great work today team! Demo scenario complete")
    
    # Cleanup
    await asyncio.sleep(2)
    pm.running = False
    frontend.running = False
    backend.running = False
    
    await pm.disconnect()
    await frontend.disconnect()
    await backend.disconnect()
    
    # Cancel tasks
    pm_task.cancel()
    frontend_task.cancel()
    backend_task.cancel()
    
    print("\n" + "="*50)
    print("Demo Complete!")

async def interactive_client(name: str = "TestAgent", role: str = "backend"):
    """Run an interactive AI agent client"""
    print(f"Starting interactive client as {name} ({role})")
    print("Commands: 'quit' to exit, 'task:ID:STATUS' to update task, or just type messages")
    print("="*50)
    
    agent = AIAgentClient(name, role)
    
    if not await agent.connect():
        print("Failed to connect to chat bridge")
        return
    
    # Start listening in background
    listen_task = asyncio.create_task(agent.listen())
    
    # Interactive loop
    try:
        while agent.running:
            # Get user input (non-blocking)
            try:
                message = await asyncio.wait_for(
                    asyncio.get_event_loop().run_in_executor(None, input, "> "),
                    timeout=1.0
                )
                
                if message.lower() == "quit":
                    break
                elif message.startswith("task:"):
                    # Parse task command
                    parts = message.split(":")
                    if len(parts) >= 3:
                        task_id = parts[1]
                        status = parts[2]
                        progress = int(parts[3]) if len(parts) > 3 else None
                        await agent.update_task(task_id, status, progress)
                elif message:
                    await agent.send_message(message)
                    
            except asyncio.TimeoutError:
                # No input, continue listening
                pass
            except KeyboardInterrupt:
                break
    finally:
        agent.running = False
        await agent.disconnect()
        listen_task.cancel()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        # Interactive mode
        name = sys.argv[2] if len(sys.argv) > 2 else "TestAgent"
        role = sys.argv[3] if len(sys.argv) > 3 else "backend"
        asyncio.run(interactive_client(name, role))
    else:
        # Demo mode
        asyncio.run(demo_scenario())