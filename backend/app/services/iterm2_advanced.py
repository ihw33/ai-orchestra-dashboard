"""
iTerm2 Advanced Automation Services
Real-time monitoring, pattern analysis, and automatic recovery
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class SessionState(Enum):
    READY = "ready"
    BUSY = "busy" 
    THINKING = "thinking"
    ERROR = "error"
    PAUSED = "paused"
    CRASHED = "crashed"

class AIResponsePatternAnalyzer:
    """AI 응답 패턴을 분석하여 작업 완료 자동 감지"""
    
    def __init__(self):
        self.patterns = {
            "claude": {
                "thinking": ["Let me", "I'll", "I need to", "I'm analyzing"],
                "completion": ["Done", "Completed", "Finished", "Created successfully"],
                "error": ["Error:", "Failed:", "Unable to", "Cannot"],
                "waiting": ["What would you", "Is there anything", "How can I"]
            },
            "gemini": {
                "processing": ["Processing", "Analyzing", "Searching"],
                "completion": ["Task completed", "All done", "Successfully"],
                "error": ["Exception", "Failed", "Error occurred"],
                "waiting": ["Ready for", "Please provide", "What's next"]
            },
            "codex": {
                "working": ["Generating", "Creating", "Building"],
                "completion": ["Generated", "Created", "Built successfully"],
                "error": ["Syntax error", "Failed to", "Could not"],
                "waiting": ["Enter command", "Ready", ">"]
            }
        }
    
    async def analyze_output(self, output: str, agent_type: str) -> Dict:
        """AI 출력 분석하여 상태 판단"""
        output_lower = output.lower()
        last_lines = output.split('\n')[-10:]  # 마지막 10줄 분석
        
        result = {
            "state": "unknown",
            "confidence": 0.0,
            "matched_patterns": [],
            "suggested_action": None
        }
        
        # 패턴 매칭
        for state, patterns in self.patterns.get(agent_type, {}).items():
            matches = []
            for pattern in patterns:
                pattern_lower = pattern.lower()
                for line in last_lines:
                    if pattern_lower in line.lower():
                        matches.append(pattern)
                        break
            
            if matches:
                confidence = len(matches) / len(patterns)
                if confidence > result["confidence"]:
                    result["state"] = state
                    result["confidence"] = confidence
                    result["matched_patterns"] = matches
        
        # 상태별 액션 제안
        if result["state"] == "completion":
            result["suggested_action"] = "assign_next_task"
        elif result["state"] == "error":
            result["suggested_action"] = "investigate_error"
        elif result["state"] == "waiting":
            result["suggested_action"] = "send_task"
        
        return result

class TaskTimeTracker:
    """각 AI의 작업 시간을 추적하여 성능 분석"""
    
    def __init__(self):
        self.active_tasks = {}
        self.completed_tasks = []
        self.performance_metrics = {}
    
    async def start_task(self, agent_name: str, issue_number: int, task_description: str):
        """작업 시작 추적"""
        task_id = f"{agent_name}_{issue_number}_{datetime.now().timestamp()}"
        
        self.active_tasks[task_id] = {
            "agent": agent_name,
            "issue": issue_number,
            "description": task_description,
            "start_time": datetime.now(),
            "status": "active"
        }
        
        logger.info(f"Task started: {task_id}")
        return task_id
    
    async def end_task(self, task_id: str, status: str = "completed"):
        """작업 완료 추적"""
        if task_id not in self.active_tasks:
            logger.warning(f"Task not found: {task_id}")
            return None
        
        task = self.active_tasks.pop(task_id)
        task["end_time"] = datetime.now()
        task["duration"] = (task["end_time"] - task["start_time"]).total_seconds()
        task["status"] = status
        
        self.completed_tasks.append(task)
        
        # 성능 메트릭 업데이트
        agent = task["agent"]
        if agent not in self.performance_metrics:
            self.performance_metrics[agent] = {
                "total_tasks": 0,
                "completed_tasks": 0,
                "failed_tasks": 0,
                "total_time": 0,
                "average_time": 0
            }
        
        metrics = self.performance_metrics[agent]
        metrics["total_tasks"] += 1
        
        if status == "completed":
            metrics["completed_tasks"] += 1
            metrics["total_time"] += task["duration"]
            metrics["average_time"] = metrics["total_time"] / metrics["completed_tasks"]
        else:
            metrics["failed_tasks"] += 1
        
        logger.info(f"Task completed: {task_id} in {task['duration']:.2f}s")
        return task
    
    async def get_agent_performance(self, agent_name: str) -> Dict:
        """특정 AI의 성능 메트릭 조회"""
        return self.performance_metrics.get(agent_name, {})
    
    async def get_all_metrics(self) -> Dict:
        """전체 성능 메트릭 조회"""
        return {
            "agents": self.performance_metrics,
            "active_tasks": len(self.active_tasks),
            "completed_tasks": len(self.completed_tasks),
            "summary": {
                "total_tasks": sum(m["total_tasks"] for m in self.performance_metrics.values()),
                "success_rate": self._calculate_success_rate()
            }
        }
    
    def _calculate_success_rate(self) -> float:
        """전체 성공률 계산"""
        total = sum(m["total_tasks"] for m in self.performance_metrics.values())
        completed = sum(m["completed_tasks"] for m in self.performance_metrics.values())
        
        return (completed / total * 100) if total > 0 else 0

class SmartNotificationSystem:
    """컨텍스트 기반 스마트 알림 시스템"""
    
    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url
        self.notification_history = []
        self.alert_thresholds = {
            "task_stuck_minutes": 30,
            "error_rate_percent": 20,
            "response_time_seconds": 300
        }
    
    async def check_and_notify(self, session_states: Dict, metrics: Dict):
        """세션 상태와 메트릭을 확인하여 알림 전송"""
        notifications = []
        
        # 1. Stuck task 확인
        for session_id, state in session_states.items():
            if state.get("duration_minutes", 0) > self.alert_thresholds["task_stuck_minutes"]:
                notifications.append({
                    "type": "task_stuck",
                    "severity": "warning",
                    "message": f"⚠️ {state['agent']} stuck on Issue #{state['issue']} for {state['duration_minutes']}min",
                    "suggested_action": "interrupt_and_reassign"
                })
        
        # 2. 높은 에러율 확인
        for agent, agent_metrics in metrics.get("agents", {}).items():
            error_rate = self._calculate_error_rate(agent_metrics)
            if error_rate > self.alert_thresholds["error_rate_percent"]:
                notifications.append({
                    "type": "high_error_rate",
                    "severity": "critical",
                    "message": f"🚨 {agent} error rate: {error_rate:.1f}%",
                    "suggested_action": "investigate_logs"
                })
        
        # 3. 느린 응답시간 확인
        for agent, agent_metrics in metrics.get("agents", {}).items():
            avg_time = agent_metrics.get("average_time", 0)
            if avg_time > self.alert_thresholds["response_time_seconds"]:
                notifications.append({
                    "type": "slow_response",
                    "severity": "info",
                    "message": f"🐌 {agent} avg response time: {avg_time:.0f}s",
                    "suggested_action": "optimize_prompts"
                })
        
        # 알림 전송
        for notification in notifications:
            await self._send_notification(notification)
        
        return notifications
    
    def _calculate_error_rate(self, metrics: Dict) -> float:
        """에러율 계산"""
        total = metrics.get("total_tasks", 0)
        failed = metrics.get("failed_tasks", 0)
        
        return (failed / total * 100) if total > 0 else 0
    
    async def _send_notification(self, notification: Dict):
        """실제 알림 전송"""
        notification["timestamp"] = datetime.now().isoformat()
        self.notification_history.append(notification)
        
        # 웹훅이 설정되어 있으면 전송
        if self.webhook_url:
            # 실제 구현에서는 aiohttp 등을 사용
            logger.info(f"Notification sent: {notification}")
        
        # 대시보드 웹소켓으로 브로드캐스트
        # await websocket_manager.broadcast(notification)

class AICollaborationManager:
    """여러 AI가 협업할 때 조율하는 매니저"""
    
    def __init__(self):
        self.collaboration_patterns = {
            "code_review": {
                "sequence": [
                    {"agent": "claude", "action": "review_code", "timeout": 600},
                    {"agent": "codex", "action": "fix_issues", "timeout": 900},
                    {"agent": "claude", "action": "verify_fixes", "timeout": 300}
                ]
            },
            "data_analysis": {
                "sequence": [
                    {"agent": "gemini", "action": "collect_data", "timeout": 600},
                    {"agent": "claude", "action": "analyze_data", "timeout": 900},
                    {"agent": "gemini", "action": "visualize_results", "timeout": 600}
                ]
            },
            "feature_development": {
                "sequence": [
                    {"agent": "claude", "action": "design_architecture", "timeout": 600},
                    {"agent": "codex", "action": "implement_code", "timeout": 1200},
                    {"agent": "claude", "action": "write_tests", "timeout": 600},
                    {"agent": "gemini", "action": "run_tests", "timeout": 300}
                ]
            }
        }
    
    async def coordinate_task(self, task_type: str, issue_number: int, context: Dict) -> Dict:
        """작업 유형에 따라 AI들을 조율"""
        if task_type not in self.collaboration_patterns:
            logger.warning(f"Unknown task type: {task_type}")
            return {"status": "error", "message": "Unknown task type"}
        
        pattern = self.collaboration_patterns[task_type]
        results = []
        
        for step in pattern["sequence"]:
            logger.info(f"Executing step: {step['agent']} - {step['action']}")
            
            result = await self._execute_step(
                agent=step["agent"],
                action=step["action"],
                timeout=step["timeout"],
                context=context,
                previous_results=results
            )
            
            results.append(result)
            
            # 실패 시 중단
            if result["status"] != "success":
                logger.error(f"Step failed: {result}")
                break
            
            # 다음 단계를 위한 컨텍스트 업데이트
            context["previous_step"] = result
        
        return {
            "task_type": task_type,
            "issue_number": issue_number,
            "steps_completed": len([r for r in results if r["status"] == "success"]),
            "total_steps": len(pattern["sequence"]),
            "results": results
        }
    
    async def _execute_step(self, agent: str, action: str, timeout: int, 
                          context: Dict, previous_results: List) -> Dict:
        """개별 협업 단계 실행"""
        # 실제 구현에서는 iTerm2 세션에 명령 전송
        start_time = datetime.now()
        
        try:
            # 여기서 실제 AI에게 작업 할당
            # await iterm2_service.send_to_agent(agent, self._build_prompt(action, context))
            
            # 작업 완료 대기
            # result = await iterm2_service.wait_for_completion(agent, timeout)
            
            duration = (datetime.now() - start_time).total_seconds()
            
            return {
                "status": "success",
                "agent": agent,
                "action": action,
                "duration": duration,
                "output": "Sample output"  # 실제 AI 출력
            }
            
        except Exception as e:
            return {
                "status": "error",
                "agent": agent,
                "action": action,
                "error": str(e)
            }
    
    def _build_prompt(self, action: str, context: Dict) -> str:
        """액션과 컨텍스트를 기반으로 프롬프트 생성"""
        prompts = {
            "review_code": f"Please review the code in PR #{context.get('pr_number')}",
            "fix_issues": f"Fix the issues mentioned in: {context.get('previous_step', {}).get('output')}",
            "analyze_data": f"Analyze the data: {context.get('data_source')}",
            # ... 더 많은 프롬프트 템플릿
        }
        
        return prompts.get(action, f"Execute {action}")

class SessionSnapshot:
    """세션 상태를 저장하고 복구하는 클래스"""
    
    def __init__(self, storage_path: str = "./snapshots"):
        self.storage_path = storage_path
        self.snapshots = {}
    
    async def create_snapshot(self, session_id: str, session_data: Dict) -> str:
        """현재 세션 상태의 스냅샷 생성"""
        snapshot_id = f"{session_id}_{datetime.now().timestamp()}"
        
        snapshot = {
            "id": snapshot_id,
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "agent_name": session_data.get("agent_name"),
            "working_directory": session_data.get("cwd"),
            "environment": session_data.get("env", {}),
            "command_history": session_data.get("history", [])[-50:],  # 최근 50개 명령
            "last_output": session_data.get("output", ""),
            "active_task": session_data.get("active_task")
        }
        
        # 파일로 저장
        snapshot_file = f"{self.storage_path}/{snapshot_id}.json"
        with open(snapshot_file, 'w') as f:
            json.dump(snapshot, f, indent=2)
        
        self.snapshots[snapshot_id] = snapshot
        logger.info(f"Snapshot created: {snapshot_id}")
        
        return snapshot_id
    
    async def restore_snapshot(self, snapshot_id: str) -> Dict:
        """스냅샷에서 세션 복구"""
        snapshot_file = f"{self.storage_path}/{snapshot_id}.json"
        
        try:
            with open(snapshot_file, 'r') as f:
                snapshot = json.load(f)
            
            # 실제 구현에서는 iTerm2 세션 복구
            restore_commands = [
                f"cd {snapshot['working_directory']}",
                # 환경 변수 복구
                *[f"export {k}={v}" for k, v in snapshot['environment'].items()],
                # 히스토리 복구 (선택적)
                "echo 'Session restored from snapshot'"
            ]
            
            return {
                "status": "success",
                "snapshot_id": snapshot_id,
                "restored_at": datetime.now().isoformat(),
                "commands": restore_commands
            }
            
        except Exception as e:
            logger.error(f"Failed to restore snapshot: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def list_snapshots(self, session_id: Optional[str] = None) -> List[Dict]:
        """저장된 스냅샷 목록 조회"""
        snapshots = []
        
        for snapshot_id, snapshot in self.snapshots.items():
            if session_id is None or snapshot["session_id"] == session_id:
                snapshots.append({
                    "id": snapshot["id"],
                    "session_id": snapshot["session_id"],
                    "agent_name": snapshot["agent_name"],
                    "timestamp": snapshot["timestamp"],
                    "active_task": snapshot.get("active_task")
                })
        
        return sorted(snapshots, key=lambda x: x["timestamp"], reverse=True)

class AutoRecoverySystem:
    """세션 오류 시 자동 복구 시스템"""
    
    def __init__(self):
        self.recovery_attempts = {}
        self.max_recovery_attempts = 3
        self.health_check_interval = 30  # seconds
    
    async def monitor_sessions(self, sessions: Dict):
        """지속적으로 세션 상태를 모니터링하고 복구"""
        while True:
            for session_id, session_info in sessions.items():
                try:
                    health = await self._check_session_health(session_info)
                    
                    if not health["is_healthy"]:
                        logger.warning(f"Unhealthy session detected: {session_id}")
                        await self._attempt_recovery(session_id, session_info, health)
                    else:
                        # 복구 시도 카운터 리셋
                        self.recovery_attempts[session_id] = 0
                        
                except Exception as e:
                    logger.error(f"Error monitoring session {session_id}: {e}")
            
            await asyncio.sleep(self.health_check_interval)
    
    async def _check_session_health(self, session_info: Dict) -> Dict:
        """세션 상태 체크"""
        health = {
            "is_healthy": True,
            "issues": [],
            "checks": {
                "responsive": False,
                "memory_ok": False,
                "cpu_ok": False,
                "no_errors": False
            }
        }
        
        # 1. 응답성 체크
        try:
            # echo 테스트 등으로 응답 확인
            health["checks"]["responsive"] = True
        except:
            health["is_healthy"] = False
            health["issues"].append("Not responsive")
        
        # 2. 리소스 사용량 체크
        memory_usage = session_info.get("memory_usage", 0)
        cpu_usage = session_info.get("cpu_usage", 0)
        
        if memory_usage < 90:
            health["checks"]["memory_ok"] = True
        else:
            health["is_healthy"] = False
            health["issues"].append(f"High memory: {memory_usage}%")
        
        if cpu_usage < 80:
            health["checks"]["cpu_ok"] = True
        else:
            health["is_healthy"] = False
            health["issues"].append(f"High CPU: {cpu_usage}%")
        
        # 3. 에러 체크
        recent_output = session_info.get("recent_output", "")
        if "error" not in recent_output.lower():
            health["checks"]["no_errors"] = True
        else:
            health["issues"].append("Errors in output")
        
        return health
    
    async def _attempt_recovery(self, session_id: str, session_info: Dict, health: Dict):
        """세션 복구 시도"""
        attempt = self.recovery_attempts.get(session_id, 0) + 1
        self.recovery_attempts[session_id] = attempt
        
        if attempt > self.max_recovery_attempts:
            logger.error(f"Max recovery attempts reached for {session_id}")
            # 새 세션 생성 또는 알림
            return
        
        logger.info(f"Recovery attempt {attempt} for {session_id}")
        
        # 복구 전략
        if "Not responsive" in health["issues"]:
            # Ctrl+C 전송
            logger.info("Sending interrupt signal")
            # await send_ctrl_c(session_id)
            
        if "High memory" in health["issues"]:
            # 메모리 정리
            logger.info("Attempting memory cleanup")
            # await send_command(session_id, "clear")
            
        if "Errors in output" in health["issues"]:
            # 에러 복구
            logger.info("Attempting error recovery")
            # await send_command(session_id, "reset")

# 전역 인스턴스
pattern_analyzer = AIResponsePatternAnalyzer()
time_tracker = TaskTimeTracker()
notification_system = SmartNotificationSystem()
collaboration_manager = AICollaborationManager()
snapshot_manager = SessionSnapshot()
recovery_system = AutoRecoverySystem()
