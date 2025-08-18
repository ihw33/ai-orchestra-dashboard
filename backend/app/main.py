"""
AI Orchestra Dashboard Backend
FastAPI 메인 애플리케이션
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 라우터 임포트
from app.routers import pm_router

# FastAPI 앱 생성
app = FastAPI(
    title="AI Orchestra Dashboard API",
    description="PM AI가 GitHub와 CLI들을 관리하는 대시보드 API",
    version="1.0.0"
)

# CORS 설정
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(pm_router.router)

# WebSocket 연결 관리
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

# 기본 엔드포인트
@app.get("/")
async def root():
    """API 상태 확인"""
    return {
        "status": "online",
        "service": "AI Orchestra Dashboard API",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "pm_api": "/api/pm",
            "websocket": "/ws"
        }
    }

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    # API 키 존재 여부 확인
    github_ok = bool(os.getenv("GITHUB_TOKEN"))
    anthropic_ok = bool(os.getenv("ANTHROPIC_API_KEY"))
    openai_ok = bool(os.getenv("OPENAI_API_KEY"))
    
    return {
        "status": "healthy",
        "services": {
            "github": "connected" if github_ok else "missing_token",
            "anthropic": "connected" if anthropic_ok else "missing_key",
            "openai": "connected" if openai_ok else "missing_key"
        }
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """실시간 업데이트를 위한 WebSocket 엔드포인트"""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # 받은 메시지를 모든 연결된 클라이언트에게 브로드캐스트
            await manager.broadcast(f"Message: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("Client disconnected")

# 시작 시 메시지
@app.on_event("startup")
async def startup_event():
    """서버 시작 시 실행"""
    print("🚀 AI Orchestra Dashboard Backend Started")
    print(f"📖 Documentation: http://localhost:8000/docs")
    print(f"🔌 WebSocket: ws://localhost:8000/ws")
    
    # API 키 상태 확인
    if not os.getenv("GITHUB_TOKEN"):
        print("⚠️  WARNING: GITHUB_TOKEN not configured")
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  WARNING: ANTHROPIC_API_KEY not configured")
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  WARNING: OPENAI_API_KEY not configured")

@app.on_event("shutdown")
async def shutdown_event():
    """서버 종료 시 실행"""
    print("👋 AI Orchestra Dashboard Backend Stopped")