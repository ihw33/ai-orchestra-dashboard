"""
PM AI Router
대시보드에서 PM AI를 제어하기 위한 API 엔드포인트
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import asyncio

from app.services.pm_orchestrator import pm_agent, template_manager
from app.services.github_service import github_service

router = APIRouter(prefix="/api/pm", tags=["PM AI"])

# Request/Response Models
class IssueAssignmentRequest(BaseModel):
    issue_number: int
    repo_name: str
    auto_assign: bool = True

class DecisionRequest(BaseModel):
    type: str  # approve_completion, request_revision, initiate_collaboration
    issue_number: int
    repo_name: str
    details: Optional[Dict] = {}

class CollaborationRequest(BaseModel):
    topic: str
    template: str = "feature_planning"
    participants: List[str] = ["all"]
    repo_name: str

class CLICommandRequest(BaseModel):
    cli_name: str
    command: str
    issue_context: Optional[int] = None

# Endpoints

@router.post("/analyze-issue")
async def analyze_issue(request: IssueAssignmentRequest):
    """이슈 분석 및 업무 분배 계획 수립"""
    try:
        # GitHub에서 이슈 정보 가져오기
        issues = github_service.list_issues(request.repo_name)
        issue = next((i for i in issues if i["number"] == request.issue_number), None)
        
        if not issue:
            raise HTTPException(status_code=404, detail="Issue not found")
        
        # PM AI가 이슈 분석
        analysis = await pm_agent.analyze_issue(issue)
        
        # 자동 할당이 활성화된 경우
        if request.auto_assign:
            assignments = await pm_agent.assign_tasks(
                request.issue_number,
                request.repo_name,
                analysis
            )
            
            return {
                "status": "analyzed_and_assigned",
                "analysis": analysis,
                "assignments": assignments
            }
        
        return {
            "status": "analyzed",
            "analysis": analysis,
            "message": "Review the analysis and confirm to assign tasks"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/assign-tasks")
async def assign_tasks(request: IssueAssignmentRequest):
    """분석된 이슈에 대해 실제 업무 할당"""
    try:
        # 이슈 재분석 (이미 분석된 경우 캐시 사용 가능)
        issues = github_service.list_issues(request.repo_name)
        issue = next((i for i in issues if i["number"] == request.issue_number), None)
        
        if not issue:
            raise HTTPException(status_code=404, detail="Issue not found")
        
        analysis = await pm_agent.analyze_issue(issue)
        assignments = await pm_agent.assign_tasks(
            request.issue_number,
            request.repo_name,
            analysis
        )
        
        return {
            "status": "tasks_assigned",
            "assignments": assignments,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/monitor-progress/{issue_number}")
async def monitor_progress(issue_number: int, repo_name: str):
    """이슈 진행 상황 모니터링"""
    try:
        progress = await pm_agent.monitor_progress(issue_number, repo_name)
        
        return {
            "status": "success",
            "progress": progress,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/make-decision")
async def make_decision(request: DecisionRequest):
    """PM AI 의사결정 처리"""
    try:
        decision_data = {
            "type": request.type,
            "issue_number": request.issue_number,
            "repo_name": request.repo_name,
            **request.details
        }
        
        result = await pm_agent.make_decision(decision_data)
        
        return {
            "status": "decision_made",
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/start-collaboration")
async def start_collaboration(request: CollaborationRequest):
    """협업 워크플로우 시작"""
    try:
        collaboration_data = {
            "topic": request.topic,
            "template": request.template,
            "participants": request.participants,
            "repo_name": request.repo_name
        }
        
        result = await pm_agent.initiate_collaboration(collaboration_data)
        
        return {
            "status": "collaboration_started",
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send-to-cli")
async def send_to_cli(request: CLICommandRequest):
    """특정 CLI에 명령 전송"""
    try:
        success = pm_agent.cli_manager.send_to_cli(
            request.cli_name,
            request.command
        )
        
        if success:
            return {
                "status": "command_sent",
                "cli": request.cli_name,
                "command": request.command,
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to send command")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/broadcast-to-all")
async def broadcast_to_all(message: str):
    """모든 CLI에 메시지 브로드캐스트"""
    try:
        pm_agent.cli_manager.broadcast_to_all_clis(message)
        
        return {
            "status": "broadcast_sent",
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/task-assignments")
async def get_task_assignments():
    """현재 할당된 모든 작업 조회"""
    try:
        return {
            "status": "success",
            "assignments": pm_agent.task_assignments,
            "total": len(pm_agent.task_assignments)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/pending-decisions")
async def get_pending_decisions():
    """대기 중인 의사결정 사항 조회"""
    try:
        return {
            "status": "success",
            "pending": pm_agent.pending_decisions,
            "total": len(pm_agent.pending_decisions)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/detect-clis")
async def detect_clis():
    """현재 사용 가능한 CLI 감지"""
    try:
        # 새로운 V2 감지기 사용
        import sys
        sys.path.append('/Users/m4_macbook/ai-orchestra-dashboard/scripts')
        from cli_detector_v2 import CLIDetectorV2
        
        detector = CLIDetectorV2()
        status = detector.get_full_status()
        
        # 기존 형식으로 변환
        active_clis = {}
        for cli_name, info in status['cli_status'].items():
            active_clis[cli_name] = {
                "available": info['available'],
                "main_process": info['main_process'],
                "monitor_connected": info['monitor_connected'],
                "monitor_status": info['monitor_status'],
                "pending_tasks": info['pending_tasks'],
                "completed_tasks": info['completed_tasks'],
                "connection_type": "monitor" if info['monitor_connected'] else "app_only",
                "capabilities": ["ready"] if info['available'] else ["offline"]
            }
        
        return {
            "status": "success",
            "detected": {
                "active_clis": active_clis,
                "summary": status['summary']
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ping-all")
async def ping_all_clis():
    """모든 연결된 CLI에 핑 전송"""
    try:
        import sys
        sys.path.append('/Users/m4_macbook/ai-orchestra-dashboard/scripts')
        from ping_cli import ping_all_connected
        
        connected_clis = ping_all_connected()
        
        return {
            "status": "success",
            "pinged_count": len(connected_clis),
            "pinged_clis": connected_clis,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ping-cli/{cli_name}")
async def ping_specific_cli(cli_name: str):
    """특정 CLI에 핑 전송"""
    try:
        import sys
        sys.path.append('/Users/m4_macbook/ai-orchestra-dashboard/scripts')
        from ping_cli import ping_cli
        
        ping_id = ping_cli(cli_name)
        
        return {
            "status": "success",
            "cli": cli_name,
            "ping_id": ping_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/manual-assign")
async def manual_assign_task(request: Dict):
    """수동으로 특정 CLI에 작업 할당"""
    try:
        cli_name = request.get("cli_name")
        task_description = request.get("description")
        priority = request.get("priority", "normal")
        
        if not cli_name or not task_description:
            raise HTTPException(status_code=400, detail="CLI name and description required")
        
        # 파일 브릿지를 통해 작업 생성
        if pm_agent.task_bridge:
            task_data = {
                "type": "manual",
                "description": task_description,
                "priority": priority,
                "created_from": "dashboard",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            task_id = pm_agent.task_bridge.create_task(cli_name.lower(), task_data)
            
            return {
                "status": "success",
                "task_id": task_id,
                "cli": cli_name,
                "message": f"Task assigned to {cli_name}"
            }
        else:
            raise HTTPException(status_code=500, detail="Task bridge not initialized")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/templates")
async def get_templates():
    """사용 가능한 협업 템플릿 조회"""
    try:
        return {
            "status": "success",
            "templates": template_manager.templates
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/gather-opinions/{template_name}/{chapter_index}")
async def gather_opinions(template_name: str, chapter_index: int):
    """챕터별 의견 수집 시작"""
    try:
        opinions = await template_manager.gather_opinions(template_name, chapter_index)
        
        return {
            "status": "opinions_requested",
            "template": template_name,
            "chapter_index": chapter_index,
            "opinions": opinions
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/synthesize-chapter")
async def synthesize_chapter(opinions: List[Dict]):
    """수집된 의견을 종합하여 챕터 작성"""
    try:
        synthesized = await template_manager.synthesize_chapter(opinions)
        
        return {
            "status": "chapter_synthesized",
            "content": synthesized,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket endpoint for real-time PM updates
from fastapi import WebSocket, WebSocketDisconnect

@router.websocket("/ws/pm-updates")
async def pm_updates_websocket(websocket: WebSocket):
    """PM AI 실시간 업데이트 WebSocket"""
    await websocket.accept()
    
    try:
        while True:
            # PM 상태 업데이트 전송
            update = {
                "type": "pm_status",
                "assignments": len(pm_agent.task_assignments),
                "pending_decisions": len(pm_agent.pending_decisions),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            await websocket.send_json(update)
            await asyncio.sleep(5)  # 5초마다 업데이트
            
    except WebSocketDisconnect:
        print("PM WebSocket disconnected")