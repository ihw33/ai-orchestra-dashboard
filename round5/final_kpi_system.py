#!/usr/bin/env python3
"""
Final KPI System
- 메모리 효율 집계(배열 대신 합/개수/최댓값)
- 백업 활성화율: 총 작업 대비 퍼센트
- @dataclass 사용, 로깅/에러 처리 강화
- Detailed/KPIAnalyzer 호환을 고려한 직렬화 키 유지
"""
from __future__ import annotations

import json
import logging
from logging.handlers import RotatingFileHandler
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Any


# ------------------------------
# Logging
# ------------------------------
def setup_logging() -> logging.Logger:
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(exist_ok=True)
    logger = logging.getLogger("final_kpi_system")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(log_dir / "kpi_system.log", maxBytes=5 * 1024 * 1024, backupCount=3)
    fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    return logger


logger = setup_logging()


# ------------------------------
# Metric dataclasses (memory-efficient)
# ------------------------------
@dataclass
class ResponseMetrics:
    total_calls: int = 0
    successful_responses: int = 0
    failed_responses: int = 0
    timeout_count: int = 0
    retry_count: int = 0

    response_time_sum: float = 0.0
    response_time_count: int = 0
    response_time_max: float = 0.0

    @property
    def avg_response_time(self) -> float:
        return 0.0 if self.response_time_count == 0 else self.response_time_sum / self.response_time_count

    def add_response_time(self, t: float) -> None:
        self.response_time_sum += t
        self.response_time_count += 1
        if t > self.response_time_max:
            self.response_time_max = t

    def to_analyzer_dict(self) -> Dict[str, Any]:
        # Analyzer 호환을 위해 avg를 단일 리스트로 제공
        return {
            "total_calls": self.total_calls,
            "successful_responses": self.successful_responses,
            "failed_responses": self.failed_responses,
            "timeout_count": self.timeout_count,
            "retry_count": self.retry_count,
            "avg_response_time": ([self.avg_response_time] if self.response_time_count else []),
            "max_response_time": self.response_time_max,
        }


@dataclass
class IssueMetrics:
    issues_assigned: int = 0
    issues_acknowledged: int = 0
    issues_started: int = 0
    issues_completed: int = 0
    issues_abandoned: int = 0

    time_to_start_sum: float = 0.0
    time_to_start_count: int = 0
    time_to_complete_sum: float = 0.0
    time_to_complete_count: int = 0

    @property
    def completion_rate(self) -> float:
        return 0.0 if self.issues_assigned == 0 else (self.issues_completed / self.issues_assigned) * 100

    @property
    def avg_time_to_start(self) -> float:
        return 0.0 if self.time_to_start_count == 0 else self.time_to_start_sum / self.time_to_start_count

    @property
    def avg_time_to_complete(self) -> float:
        return 0.0 if self.time_to_complete_count == 0 else self.time_to_complete_sum / self.time_to_complete_count

    def to_analyzer_dict(self) -> Dict[str, Any]:
        # Analyzer는 리스트를 평균으로 처리하므로 단일 샘플 형태로 제공
        return {
            "issues_assigned": self.issues_assigned,
            "issues_acknowledged": self.issues_acknowledged,
            "issues_started": self.issues_started,
            "issues_completed": self.issues_completed,
            "issues_abandoned": self.issues_abandoned,
            "avg_time_to_start": ([self.avg_time_to_start] if self.time_to_start_count else []),
            "avg_time_to_complete": ([self.avg_time_to_complete] if self.time_to_complete_count else []),
        }


@dataclass
class PRMetrics:
    prs_created: int = 0
    prs_updated: int = 0
    pr_descriptions_written: int = 0
    review_requested: int = 0
    reviews_received: int = 0
    reviews_given: int = 0
    review_comments_addressed: int = 0
    pr_merged: int = 0
    pr_closed: int = 0


@dataclass
class CommunicationMetrics:
    messages_sent: int = 0
    messages_received: int = 0
    questions_asked: int = 0
    questions_answered: int = 0
    help_requests: int = 0
    status_updates: int = 0
    allow_requests: int = 0


@dataclass
class CodeWorkMetrics:
    files_created: int = 0
    files_modified: int = 0
    lines_added: int = 0
    lines_deleted: int = 0
    commits_made: int = 0
    commit_messages_quality_sum: int = 0
    commit_messages_quality_count: int = 0

    @property
    def commit_messages_quality_avg(self) -> float:
        c = self.commit_messages_quality_count
        return 0.0 if c == 0 else self.commit_messages_quality_sum / c


@dataclass
class QualityMetrics:
    errors_encountered: int = 0
    errors_resolved: int = 0
    bugs_introduced: int = 0
    bugs_fixed: int = 0
    test_passed: int = 0
    test_failed: int = 0
    code_quality_score_sum: int = 0
    code_quality_score_count: int = 0

    @property
    def code_quality_score_avg(self) -> float:
        c = self.code_quality_score_count
        return 0.0 if c == 0 else self.code_quality_score_sum / c


@dataclass
class ProcessCompliance:
    workflow_followed: int = 0
    workflow_violated: int = 0
    checklist_completed: int = 0
    documentation_created: int = 0
    proper_branch_usage: int = 0
    proper_commit_format: int = 0

    @property
    def process_compliance_rate(self) -> float:
        total = self.workflow_followed + self.workflow_violated
        return 100.0 if total == 0 else (self.workflow_followed / total) * 100


@dataclass
class BackupMetrics:
    times_backed_up: int = 0
    times_as_backup: int = 0
    backup_success: int = 0
    backup_failure: int = 0
    total_tasks: int = 0

    @property
    def backup_activation_rate(self) -> float:
        return 0.0 if self.total_tasks == 0 else (self.times_backed_up / self.total_tasks) * 100

    @property
    def backup_success_rate(self) -> float:
        return 100.0 if self.times_as_backup == 0 else (self.backup_success / self.times_as_backup) * 100


@dataclass
class AIKPIMetrics:
    ai_name: str
    role: str

    issue_management: IssueMetrics = field(default_factory=IssueMetrics)
    pr_process: PRMetrics = field(default_factory=PRMetrics)
    communication: CommunicationMetrics = field(default_factory=CommunicationMetrics)
    response_performance: ResponseMetrics = field(default_factory=ResponseMetrics)
    backup_system: BackupMetrics = field(default_factory=BackupMetrics)
    quality_metrics: QualityMetrics = field(default_factory=QualityMetrics)
    process_compliance: ProcessCompliance = field(default_factory=ProcessCompliance)
    code_work: CodeWorkMetrics = field(default_factory=CodeWorkMetrics)

    def summary(self) -> Dict[str, Any]:
        return {
            "issue_completion_rate": self.issue_management.completion_rate,
            "pr_merge_rate": 0.0 if self.pr_process.prs_created == 0 else (self.pr_process.pr_merged / self.pr_process.prs_created) * 100,
            "response_rate": 0.0 if self.response_performance.total_calls == 0 else (self.response_performance.successful_responses / self.response_performance.total_calls) * 100,
            "backup_activation_rate": self.backup_system.backup_activation_rate,
            "process_compliance_rate": self.process_compliance.process_compliance_rate,
            "error_resolution_rate": 100.0 if self.quality_metrics.errors_encountered == 0 else (self.quality_metrics.errors_resolved / self.quality_metrics.errors_encountered) * 100,
        }

    def to_analyzer_payload(self) -> Dict[str, Any]:
        # KPIAnalyzer가 기대하는 키 네임으로 직렬화
        return {
            "issue_management": self.issue_management.to_analyzer_dict(),
            "pr_process": asdict(self.pr_process),
            "communication": asdict(self.communication),
            "response_performance": self.response_performance.to_analyzer_dict(),
            "backup_system": asdict(self.backup_system),
            "quality_metrics": {
                **asdict(self.quality_metrics),
                "code_quality_score": ([self.quality_metrics.code_quality_score_avg] if self.quality_metrics.code_quality_score_count else []),
            },
            "process_compliance": asdict(self.process_compliance),
            "code_work": {
                **asdict(self.code_work),
                "commit_messages_quality": ([self.code_work.commit_messages_quality_avg] if self.code_work.commit_messages_quality_count else []),
            },
        }


# ------------------------------
# Tracker
# ------------------------------
class FinalKPITracker:
    def __init__(self, config_path: Optional[str] = None) -> None:
        self.start_time = datetime.now()
        self.team_kpis: Dict[str, AIKPIMetrics] = {}

        self.backup_matrix = {
            "Gemini": "Cursor",
            "Codex": "Gemini",
            "Cursor": "Codex",
            "Claude": None,
        }

        self.baselines = self._load_baselines(config_path)
        self._initialize_team()
        logger.info("FinalKPITracker initialized")

    def _load_baselines(self, config_path: Optional[str]) -> Dict[str, Any]:
        if config_path and Path(config_path).exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:  # noqa: BLE001
                logger.error(f"Failed to load baselines: {e}")
        return {
            "issue_completion_rate": 80,
            "pr_merge_rate": 90,
            "response_rate": 95,
            "max_backup_activation_rate": 10,
            "process_compliance_rate": 95,
        }

    def _initialize_team(self) -> None:
        for name, role in (
            ("Gemini", "Frontend Lead"),
            ("Codex", "Backend Engineer"),
            ("Claude", "PM & QA"),
            ("Cursor", "Architect"),
        ):
            self.team_kpis[name] = AIKPIMetrics(ai_name=name, role=role)

    # ---- Issue tracking
    def track_issue(self, ai_name: str, event: str, **kwargs: Any) -> None:
        m = self.team_kpis.get(ai_name)
        if not m:
            logger.warning(f"Unknown AI: {ai_name}")
            return
        im = m.issue_management
        if event == "assigned":
            im.issues_assigned += 1
            m.backup_system.total_tasks += 1
        elif event == "acknowledged":
            im.issues_acknowledged += 1
        elif event == "started":
            im.issues_started += 1
            if "time_to_start" in kwargs:
                im.time_to_start_sum += float(kwargs["time_to_start"])  # seconds
                im.time_to_start_count += 1
        elif event == "completed":
            im.issues_completed += 1
            if "time_to_complete" in kwargs:
                im.time_to_complete_sum += float(kwargs["time_to_complete"])  # seconds
                im.time_to_complete_count += 1
        elif event == "abandoned":
            im.issues_abandoned += 1
            self._activate_backup(ai_name)
        logger.info(f"Issue event={event} ai={ai_name}")

    # ---- Responses
    def track_response(self, ai_name: str, success: bool, response_time: float, timeout_threshold: float = 30.0) -> None:
        m = self.team_kpis.get(ai_name)
        if not m:
            logger.warning(f"Unknown AI: {ai_name}")
            return
        rm = m.response_performance
        rm.total_calls += 1
        if success:
            rm.successful_responses += 1
            rm.add_response_time(response_time)
        else:
            rm.failed_responses += 1
            if response_time >= timeout_threshold:
                rm.timeout_count += 1
                self._activate_backup(ai_name)
        logger.info(f"Response ai={ai_name} success={success} time={response_time}")

    # ---- PR process
    def track_pr(self, ai_name: str, action: str, **kwargs: Any) -> None:
        m = self.team_kpis.get(ai_name)
        if not m:
            logger.warning(f"Unknown AI: {ai_name}")
            return
        pr = m.pr_process
        if action == "created":
            pr.prs_created += 1
            if kwargs.get("has_description"):
                pr.pr_descriptions_written += 1
        elif action == "updated":
            pr.prs_updated += 1
        elif action == "review_requested":
            pr.review_requested += 1
        elif action == "review_received":
            pr.reviews_received += 1
        elif action == "review_given":
            pr.reviews_given += 1
            pr.review_comments_addressed += int(kwargs.get("comments", 0))
        elif action == "merged":
            pr.pr_merged += 1
        elif action == "closed":
            pr.pr_closed += 1
        logger.info(f"PR action={action} ai={ai_name}")

    # ---- Communication
    def track_comm(self, ai_name: str, kind: str) -> None:
        m = self.team_kpis.get(ai_name)
        if not m:
            logger.warning(f"Unknown AI: {ai_name}")
            return
        c = m.communication
        if kind == "sent":
            c.messages_sent += 1
        elif kind == "received":
            c.messages_received += 1
        elif kind == "asked":
            c.questions_asked += 1
        elif kind == "answered":
            c.questions_answered += 1
        elif kind == "help":
            c.help_requests += 1
        elif kind == "status":
            c.status_updates += 1
        elif kind == "allow":
            c.allow_requests += 1
        logger.info(f"Comm kind={kind} ai={ai_name}")

    # ---- Code work
    def track_code(self, ai_name: str, action: str, **kwargs: Any) -> None:
        m = self.team_kpis.get(ai_name)
        if not m:
            logger.warning(f"Unknown AI: {ai_name}")
            return
        cw = m.code_work
        if action == "file_created":
            cw.files_created += 1
        elif action == "file_modified":
            cw.files_modified += 1
        elif action == "commit":
            cw.commits_made += 1
            cw.lines_added += int(kwargs.get("lines_added", 0))
            cw.lines_deleted += int(kwargs.get("lines_deleted", 0))
            q = kwargs.get("message_quality")
            if isinstance(q, (int, float)):
                cw.commit_messages_quality_sum += int(q)
                cw.commit_messages_quality_count += 1
        logger.info(f"Code action={action} ai={ai_name}")

    # ---- Process compliance
    def track_compliance(self, ai_name: str, compliant: bool, process_type: Optional[str] = None) -> None:
        m = self.team_kpis.get(ai_name)
        if not m:
            logger.warning(f"Unknown AI: {ai_name}")
            return
        pc = m.process_compliance
        if compliant:
            pc.workflow_followed += 1
            if process_type == "branch":
                pc.proper_branch_usage += 1
            elif process_type == "commit":
                pc.proper_commit_format += 1
            elif process_type == "checklist":
                pc.checklist_completed += 1
            elif process_type == "doc":
                pc.documentation_created += 1
        else:
            pc.workflow_violated += 1
        logger.info(f"Compliance ai={ai_name} compliant={compliant} type={process_type}")

    # ---- Quality
    def track_quality(self, ai_name: str, event: str) -> None:
        m = self.team_kpis.get(ai_name)
        if not m:
            logger.warning(f"Unknown AI: {ai_name}")
            return
        q = m.quality_metrics
        if event == "error":
            q.errors_encountered += 1
        elif event == "error_resolved":
            q.errors_resolved += 1
        elif event == "bug":
            q.bugs_introduced += 1
        elif event == "bug_fixed":
            q.bugs_fixed += 1
        elif event == "test_pass":
            q.test_passed += 1
        elif event == "test_fail":
            q.test_failed += 1
        logger.info(f"Quality ai={ai_name} event={event}")

    # ---- Backup
    def _activate_backup(self, primary: str) -> None:
        backup = self.backup_matrix.get(primary)
        if not backup:
            return
        p = self.team_kpis.get(primary)
        if p:
            p.backup_system.times_backed_up += 1
        b = self.team_kpis.get(backup)
        if b:
            b.backup_system.times_as_backup += 1
        logger.warning(f"Backup activated: {primary} -> {backup}")

    def track_backup_result(self, backup_ai: str, success: bool) -> None:
        m = self.team_kpis.get(backup_ai)
        if not m:
            return
        if success:
            m.backup_system.backup_success += 1
        else:
            m.backup_system.backup_failure += 1

    # ------------------------------
    # Reporting
    # ------------------------------
    def generate_report(self) -> Dict[str, Any]:
        runtime = (datetime.now() - self.start_time).total_seconds()
        out: Dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "runtime_minutes": runtime / 60,
            "team_performance": {},
        }
        for name, m in self.team_kpis.items():
            out["team_performance"][name] = {
                "role": m.role,
                "summary": m.summary(),
                # Analyzer 호환을 위한 상세 필드 네이밍 유지
                "detailed_kpis": m.to_analyzer_payload(),
            }
        return out

    def analyze(self) -> Dict[str, Any]:
        # 간단한 내장 분석 (상세 Analyzer와 병행 사용 가능)
        analysis = {"timestamp": datetime.now().isoformat(), "issues": [], "recommendations": []}
        for name, m in self.team_kpis.items():
            if m.issue_management.completion_rate < self.baselines["issue_completion_rate"]:
                analysis["issues"].append({
                    "ai": name,
                    "metric": "issue_completion_rate",
                    "expected": self.baselines["issue_completion_rate"],
                    "actual": round(m.issue_management.completion_rate, 1),
                    "severity": "HIGH",
                })
            if m.backup_system.backup_activation_rate > self.baselines["max_backup_activation_rate"]:
                analysis["issues"].append({
                    "ai": name,
                    "metric": "backup_activation_rate",
                    "expected": f"<{self.baselines['max_backup_activation_rate']}%",
                    "actual": f"{m.backup_system.backup_activation_rate:.1f}%",
                    "severity": "MEDIUM",
                })
                analysis["recommendations"].append(f"Consider tuning timeouts or retraining {name}")
        return analysis

    def save_report(self, filepath: str = "kpi_report.json") -> str:
        data = {"report": self.generate_report(), "analysis": self.analyze()}
        try:
            with open(Path(__file__).parent / filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Report saved: {filepath}")
        except Exception as e:  # noqa: BLE001
            logger.error(f"Failed to save report: {e}")
            raise
        return str(Path(__file__).parent / filepath)


# ------------------------------
# Example
# ------------------------------
if __name__ == "__main__":
    t = FinalKPITracker()
    # Issues
    t.track_issue("Gemini", "assigned")
    t.track_issue("Gemini", "started", time_to_start=300)
    t.track_issue("Gemini", "completed", time_to_complete=3600)
    # Responses
    t.track_response("Gemini", True, 2.5)
    t.track_response("Codex", False, 35.0)
    # PRs
    t.track_pr("Gemini", "created", has_description=True)
    t.track_pr("Claude", "review_given", comments=2)
    # Communication
    t.track_comm("Gemini", "status")
    # Compliance
    t.track_compliance("Gemini", True, "branch")
    # Save report
    path = t.save_report()
    print(f"Saved report to: {path}")

