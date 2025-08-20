"""
AI Orchestra Dashboard - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from typing import Dict, List
import json

# Load environment variables
load_dotenv()

# Import routers
from app.routers import pm_router
from app.routers import projects_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    print("🚀 Starting AI Orchestra Dashboard Backend...")
    
    # Validate configuration on startup
    from app.config import settings
    try:
        settings.validate()
        print(f"✅ Configuration validated: {settings}")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        raise
    
    yield
    print("👋 Shutting down AI Orchestra Dashboard Backend...")

# Create FastAPI app
app = FastAPI(
    title="AI Orchestra Dashboard API",
    description="Backend API for managing AI agents and GitHub workflows",
    version="0.1.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "AI Orchestra Dashboard API",
        "version": "0.1.0",
        "status": "operational"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "database": "connected",
            "github": "connected",
            "ai_services": "connected"
        }
    }

# WebSocket endpoint for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Process received data
            message = json.loads(data)
            
            # Broadcast updates to all connected clients
            await manager.broadcast(json.dumps({
                "type": "update",
                "data": message
            }))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(json.dumps({
            "type": "client_disconnected"
        }))

# GitHub webhook endpoint
@app.post("/webhooks/github")
async def github_webhook(payload: dict):
    """Handle GitHub webhook events"""
    event_type = payload.get("action")
    
    # Broadcast GitHub event to all connected clients
    await manager.broadcast(json.dumps({
        "type": "github_event",
        "event": event_type,
        "data": payload
    }))
    
    return {"status": "received"}

# Include routers
app.include_router(pm_router.router)
app.include_router(projects_router.router)
# app.include_router(github.router, prefix="/api/github", tags=["github"])
# app.include_router(ai.router, prefix="/api/ai", tags=["ai"])
# app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
# app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("APP_PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
