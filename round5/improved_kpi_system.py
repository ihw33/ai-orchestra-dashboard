#!/usr/bin/env python3
"""
Improved KPI Tracking System
Codex 리뷰 반영 버전 - 메모리 효율적이고 안정적인 구현
"""
import json
import logging
from logging.handlers import RotatingFileHandler
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, Optional
from pathlib import Path

# 로깅 설정
def setup_logging():
    """로깅 시스템 설정 with rotation"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logger = logging.getLogger("kpi_tracker")
    logger.setLevel(logging.INFO)
    
    # 파일 핸들러 with rotation (10MB, 5 backups)
    handler = RotatingFileHandler(
        log_dir / "kpi_tracker.log",
        maxBytes=10*1024*1024,
        backupCount=5
    )
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

logger = setup_logging()

@dataclass
class ResponseMetrics:
    """응답 성능 메트릭 - 메모리 효율적 집계"""
    total_calls: int = 0
    successful_responses: int = 0
    failed_responses: int = 0
    timeout_count: int = 0
    retry_count: int = 0
    
    # 집계 통계 (배열 대신)
    response_time_sum: float = 0.0
    response_time_count: int = 0
    response_time_max: float = 0.0
    
    @property
    def avg_response_time(self) -> float:
        """평균 응답 시간 계산"""
        if self.response_time_count == 0:
            return 0.0
        return self.response_time_sum / self.response_time_count
    
    @property
    def response_rate(self) -> float:
        """응답률 계산"""
        if self.total_calls == 0:
            return 0.0
        return (self.successful_responses / self.total_calls) * 100
    
    def add_response_time(self, time: float):
        """응답 시간 추가 (메모리 효율적)"""
        self.response_time_sum += time
        self.response_time_count += 1
        self.response_time_max = max(self.response_time_max, time)

@dataclass
class IssueMetrics:
    """이슈 관리 메트릭"""
    issues_assigned: int = 0
    issues_acknowledged: int = 0
    issues_started: int = 0
    issues_completed: int = 0
    issues_abandoned: int = 0
    
    # 시간 집계 (배열 대신)
    time_to_start_sum: float = 0.0
    time_to_start_count: int = 0
    time_to_complete_sum: float = 0.0
    time_to_complete_count: int = 0
    
    @property
    def completion_rate(self) -> float:
        """완료율 계산"""
        if self.issues_assigned == 0:
            return 0.0
        return (self.issues_completed / self.issues_assigned) * 100
    
    @property
    def avg_time_to_start(self) -> float:
        """평균 시작 시간"""
        if self.time_to_start_count == 0:
            return 0.0
        return self.time_to_start_sum / self.time_to_start_count
    
    @property
    def avg_time_to_complete(self) -> float:
        """평균 완료 시간"""
        if self.time_to_complete_count == 0:
            return 0.0
        return self.time_to_complete_sum / self.time_to_complete_count

@dataclass
class PRMetrics:
    """PR 프로세스 메트릭"""
    prs_created: int = 0
    prs_updated: int = 0
    pr_descriptions_written: int = 0
    review_requested: int = 0
    reviews_received: int = 0
    reviews_given: int = 0
    review_comments_addressed: int = 0
    pr_merged: int = 0
    pr_closed: int = 0
    
    @property
    def merge_rate(self) -> float:
        """머지율 계산"""
        if self.prs_created == 0:
            return 0.0
        return (self.pr_merged / self.prs_created) * 100
    
    @property
    def review_request_rate(self) -> float:
        """리뷰 요청률"""
        if self.prs_created == 0:
            return 0.0
        return (self.review_requested / self.prs_created) * 100

@dataclass
class BackupMetrics:
    """백업 시스템 메트릭"""
    times_backed_up: int = 0
    times_as_backup: int = 0
    backup_success: int = 0
    backup_failure: int = 0
    total_tasks: int = 0  # 전체 작업 수 추적
    
    @property
    def backup_activation_rate(self) -> float:
        """백업 활성화율 (퍼센트)"""
        if self.total_tasks == 0:
            return 0.0
        return (self.times_backed_up / self.total_tasks) * 100
    
    @property
    def backup_success_rate(self) -> float:
        """백업 성공률"""
        if self.times_as_backup == 0:
            return 100.0
        return (self.backup_success / self.times_as_backup) * 100

@dataclass
class AIKPIMetrics:
    """각 AI의 전체 KPI 메트릭"""
    ai_name: str
    role: str
    
    # 각 카테고리별 메트릭
    issues: IssueMetrics = field(default_factory=IssueMetrics)
    prs: PRMetrics = field(default_factory=PRMetrics)
    responses: ResponseMetrics = field(default_factory=ResponseMetrics)
    backup: BackupMetrics = field(default_factory=BackupMetrics)
    
    # 추가 메트릭
    errors_encountered: int = 0
    errors_resolved: int = 0
    workflow_followed: int = 0
    workflow_violated: int = 0
    
    @property
    def error_resolution_rate(self) -> float:
        """에러 해결률"""
        if self.errors_encountered == 0:
            return 100.0
        return (self.errors_resolved / self.errors_encountered) * 100
    
    @property
    def process_compliance_rate(self) -> float:
        """프로세스 준수율"""
        total = self.workflow_followed + self.workflow_violated
        if total == 0:
            return 100.0
        return (self.workflow_followed / total) * 100

class ImprovedKPITracker:
    """개선된 KPI 추적 시스템"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.start_time = datetime.now()
        self.team_kpis: Dict[str, AIKPIMetrics] = {}
        
        # 백업 매트릭스
        self.backup_matrix = {
            "Gemini": "Cursor",
            "Codex": "Gemini",
            "Cursor": "Codex",
            "Claude": None
        }
        
        # 설정 파일 로드
        self.baselines = self._load_baselines(config_path)
        
        # 팀 초기화
        self._initialize_team()
        
        logger.info("KPI Tracker initialized")
    
    def _load_baselines(self, config_path: Optional[str]) -> Dict:
        """기준값 로드 (JSON/YAML)"""
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                return json.load(f)
        
        # 기본값
        return {
            "issue_completion_rate": 80,
            "pr_merge_rate": 90,
            "response_rate": 95,
            "max_backup_activation_rate": 10,
            "process_compliance_rate": 95
        }
    
    def _initialize_team(self):
        """팀 멤버 초기화"""
        team_config = [
            ("Gemini", "Frontend Lead"),
            ("Codex", "Backend Engineer"),
            ("Claude", "PM & QA"),
            ("Cursor", "Architect")
        ]
        
        for name, role in team_config:
            self.team_kpis[name] = AIKPIMetrics(ai_name=name, role=role)
    
    def track_issue(self, ai_name: str, event_type: str, **kwargs):
        """이슈 관련 이벤트 추적"""
        if ai_name not in self.team_kpis:
            logger.warning(f"Unknown AI: {ai_name}")
            return
        
        metrics = self.team_kpis[ai_name].issues
        
        if event_type == "assigned":
            metrics.issues_assigned += 1
            self.team_kpis[ai_name].backup.total_tasks += 1
        elif event_type == "started":
            metrics.issues_started += 1
            if "time_to_start" in kwargs:
                metrics.time_to_start_sum += kwargs["time_to_start"]
                metrics.time_to_start_count += 1
        elif event_type == "completed":
            metrics.issues_completed += 1
            if "time_to_complete" in kwargs:
                metrics.time_to_complete_sum += kwargs["time_to_complete"]
                metrics.time_to_complete_count += 1
        elif event_type == "abandoned":
            metrics.issues_abandoned += 1
            self._activate_backup(ai_name)
        
        logger.info(f"Issue {event_type} for {ai_name}")
    
    def track_response(self, ai_name: str, success: bool, response_time: float):
        """응답 추적"""
        if ai_name not in self.team_kpis:
            return
        
        metrics = self.team_kpis[ai_name].responses
        metrics.total_calls += 1
        
        if success:
            metrics.successful_responses += 1
            metrics.add_response_time(response_time)
        else:
            metrics.failed_responses += 1
            if response_time > 30:  # 30초 이상이면 타임아웃
                metrics.timeout_count += 1
                self._activate_backup(ai_name)
        
        logger.info(f"Response tracked for {ai_name}: success={success}, time={response_time}s")
    
    def _activate_backup(self, primary: str):
        """백업 AI 활성화"""
        backup = self.backup_matrix.get(primary)
        if not backup:
            return
        
        self.team_kpis[primary].backup.times_backed_up += 1
        
        if backup in self.team_kpis:
            self.team_kpis[backup].backup.times_as_backup += 1
            logger.warning(f"Backup activated: {primary} -> {backup}")
    
    def generate_report(self) -> Dict:
        """종합 리포트 생성"""
        runtime = (datetime.now() - self.start_time).total_seconds()
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "runtime_minutes": runtime / 60,
            "team_performance": {}
        }
        
        for ai_name, metrics in self.team_kpis.items():
            report["team_performance"][ai_name] = {
                "role": metrics.role,
                "summary": {
                    "issue_completion_rate": metrics.issues.completion_rate,
                    "pr_merge_rate": metrics.prs.merge_rate,
                    "response_rate": metrics.responses.response_rate,
                    "backup_activation_rate": metrics.backup.backup_activation_rate,
                    "process_compliance_rate": metrics.process_compliance_rate,
                    "error_resolution_rate": metrics.error_resolution_rate
                },
                "detailed": asdict(metrics)
            }
        
        return report
    
    def analyze_performance(self) -> Dict:
        """성능 분석 및 권고사항"""
        analysis = {"timestamp": datetime.now().isoformat(), "issues": [], "recommendations": []}
        
        for ai_name, metrics in self.team_kpis.items():
            # 이슈 완료율 체크
            if metrics.issues.completion_rate < self.baselines["issue_completion_rate"]:
                analysis["issues"].append({
                    "ai": ai_name,
                    "metric": "issue_completion_rate",
                    "expected": self.baselines["issue_completion_rate"],
                    "actual": metrics.issues.completion_rate,
                    "severity": "HIGH"
                })
            
            # 백업 활성화율 체크
            if metrics.backup.backup_activation_rate > self.baselines["max_backup_activation_rate"]:
                analysis["issues"].append({
                    "ai": ai_name,
                    "metric": "backup_activation_rate",
                    "expected": f"<{self.baselines['max_backup_activation_rate']}%",
                    "actual": f"{metrics.backup.backup_activation_rate:.1f}%",
                    "severity": "MEDIUM"
                })
                analysis["recommendations"].append(
                    f"Consider retraining {ai_name} or adjusting timeout settings"
                )
        
        return analysis
    
    def save_report(self, filepath: str = "kpi_report.json"):
        """리포트 저장"""
        report = self.generate_report()
        analysis = self.analyze_performance()
        
        combined = {
            "report": report,
            "analysis": analysis
        }
        
        with open(filepath, 'w') as f:
            json.dump(combined, f, indent=2)
        
        logger.info(f"Report saved to {filepath}")
        return filepath

# 사용 예제
if __name__ == "__main__":
    tracker = ImprovedKPITracker()
    
    # 이슈 추적
    tracker.track_issue("Gemini", "assigned")
    tracker.track_issue("Gemini", "started", time_to_start=300)
    tracker.track_issue("Gemini", "completed", time_to_complete=7200)
    
    # 응답 추적
    tracker.track_response("Gemini", True, 3.5)
    tracker.track_response("Codex", False, 35.0)  # 타임아웃 - 백업 활성화
    
    # 리포트 생성
    report_path = tracker.save_report()
    print(f"Report saved: {report_path}")
    
    # 분석 결과 출력
    analysis = tracker.analyze_performance()
    print(json.dumps(analysis, indent=2))