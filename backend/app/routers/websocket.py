"""
WebSocket endpoints for real-time metrics and notifications
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Dict
import json
import asyncio
import logging
from datetime import datetime

from app.services.iterm2_advanced import (
    pattern_analyzer,
    time_tracker,
    notification_system,
    collaboration_manager
)

logger = logging.getLogger(__name__)

router = APIRouter()

class ConnectionManager:
    """WebSocket 연결 관리"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.metrics_task = None
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Client connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"Client disconnected. Total connections: {len(self.active_connections)}")
    
    async def broadcast(self, message: Dict):
        """모든 연결된 클라이언트에게 메시지 전송"""
        if self.active_connections:
            message_json = json.dumps(message)
            for connection in self.active_connections:
                try:
                    await connection.send_text(message_json)
                except:
                    # 연결이 끊긴 경우 제거
                    await self._remove_failed_connection(connection)
    
    async def _remove_failed_connection(self, websocket: WebSocket):
        try:
            self.active_connections.remove(websocket)
        except ValueError:
            pass

manager = ConnectionManager()

@router.websocket("/ws/metrics")
async def websocket_endpoint(websocket: WebSocket):
    """실시간 메트릭 WebSocket 엔드포인트"""
    await manager.connect(websocket)
    
    try:
        # 메트릭 브로드캐스트 태스크 시작
        if manager.metrics_task is None:
            manager.metrics_task = asyncio.create_task(broadcast_metrics())
        
        # 연결 유지
        while True:
            # 클라이언트로부터 메시지 대기 (ping/pong)
            data = await websocket.receive_text()
            
            # 필요한 경우 클라이언트 요청 처리
            if data == "ping":
                await websocket.send_text("pong")
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)

async def broadcast_metrics():
    """1초마다 메트릭 브로드캐스트"""
    while True:
        try:
            # 실제 세션 상태 수집 (예시 데이터)
            metrics = await collect_session_metrics()
            
            await manager.broadcast({
                "type": "metrics",
                "payload": metrics,
                "timestamp": datetime.now().isoformat()
            })
            
            # 알림 확인
            notifications = await check_for_notifications(metrics)
            for notification in notifications:
                await manager.broadcast({
                    "type": "notification", 
                    "payload": notification,
                    "timestamp": datetime.now().isoformat()
                })
            
            await asyncio.sleep(1)
            
        except Exception as e:
            logger.error(f"Error broadcasting metrics: {e}")
            await asyncio.sleep(5)

async def collect_session_metrics() -> List[Dict]:
    """세션 메트릭 수집"""
    # 실제 구현에서는 iTerm2 세션에서 데이터 수집
    # 여기서는 예시 데이터 반환
    
    sessions = [
        {
            "agent": "Claude",
            "status": "working",
            "currentTask": "Reviewing PR #55",
            "tasksCompleted": 15,
            "averageTime": 245,
            "successRate": 93,
            "lastActivity": datetime.now().isoformat(),
            "cpuUsage": 35,
            "memoryUsage": 42
        },
        {
            "agent": "Gemini", 
            "status": "idle",
            "currentTask": None,
            "tasksCompleted": 12,
            "averageTime": 180,
            "successRate": 88,
            "lastActivity": datetime.now().isoformat(),
            "cpuUsage": 5,
            "memoryUsage": 28
        },
        {
            "agent": "Codex",
            "status": "thinking",
            "currentTask": "Implementing Issue #58",
            "tasksCompleted": 18,
            "averageTime": 320,
            "successRate": 95,
            "lastActivity": datetime.now().isoformat(),
            "cpuUsage": 78,
            "memoryUsage": 65
        }
    ]
    
    return sessions

async def check_for_notifications(metrics: List[Dict]) -> List[Dict]:
    """메트릭 기반 알림 생성"""
    notifications = []
    
    for session in metrics:
        # CPU 사용량 높음
        if session["cpuUsage"] > 80:
            notifications.append({
                "id": f"notif_{datetime.now().timestamp()}",
                "type": "high_resource",
                "severity": "warning",
                "message": f"⚠️ {session['agent']} CPU usage high: {session['cpuUsage']}%",
                "timestamp": datetime.now().isoformat()
            })
        
        # 성공률 낮음
        if session["successRate"] < 80:
            notifications.append({
                "id": f"notif_{datetime.now().timestamp()}",
                "type": "low_success_rate",
                "severity": "critical",
                "message": f"🚨 {session['agent']} success rate low: {session['successRate']}%",
                "timestamp": datetime.now().isoformat()
            })
    
    return notifications

@router.get("/api/metrics/summary")
async def get_metrics_summary():
    """메트릭 요약 API"""
    all_metrics = await time_tracker.get_all_metrics()
    
    return {
        "status": "success",
        "data": all_metrics,
        "timestamp": datetime.now().isoformat()
    }

@router.post("/api/collaboration/start")
async def start_collaboration(task_type: str, issue_number: int, context: Dict = {}):
    """AI 협업 작업 시작"""
    result = await collaboration_manager.coordinate_task(
        task_type=task_type,
        issue_number=issue_number,
        context=context
    )
    
    return {
        "status": "success",
        "data": result,
        "timestamp": datetime.now().isoformat()
    }
