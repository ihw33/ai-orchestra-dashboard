#!/usr/bin/env python3
"""
AI Orchestra 상세 KPI 추적 시스템
모든 프로세스 단계별 수치 추적
"""
import json
import time
from datetime import datetime
from typing import Dict, List, Optional

class DetailedKPITracker:
    def __init__(self):
        self.team_kpis = {
            "Gemini": self._create_kpi_template(),
            "Codex": self._create_kpi_template(),
            "Claude": self._create_kpi_template(),
            "Cursor": self._create_kpi_template()
        }
        self.backup_matrix = {
            "Gemini": "Cursor",  # Gemini 실패시 Cursor
            "Codex": "Gemini",   # Codex 실패시 Gemini
            "Cursor": "Codex",   # Cursor 실패시 Codex
            "Claude": None       # PM은 백업 없음
        }
        self.start_time = datetime.now()
        
    def _create_kpi_template(self) -> Dict:
        """각 AI별 KPI 템플릿"""
        return {
            # 1. 이슈/작업 관리
            "issue_management": {
                "issues_assigned": 0,          # 할당받은 이슈 수
                "issues_acknowledged": 0,       # 확인한 이슈 수
                "issues_started": 0,           # 시작 보고한 이슈 수
                "issues_completed": 0,         # 완료 보고한 이슈 수
                "issues_abandoned": 0,         # 포기한 이슈 수
                "avg_time_to_start": [],      # 할당~시작 시간
                "avg_time_to_complete": [],   # 시작~완료 시간
            },
            
            # 2. 코드 작업
            "code_work": {
                "files_created": 0,           # 생성한 파일 수
                "files_modified": 0,          # 수정한 파일 수
                "lines_added": 0,             # 추가한 코드 라인
                "lines_deleted": 0,           # 삭제한 코드 라인
                "commits_made": 0,            # 커밋 횟수
                "commit_messages_quality": [] # 커밋 메시지 품질 (1-5)
            },
            
            # 3. PR 프로세스
            "pr_process": {
                "prs_created": 0,             # 생성한 PR 수
                "prs_updated": 0,             # 업데이트한 PR 수
                "pr_descriptions_written": 0,  # PR 설명 작성 수
                "review_requested": 0,         # 리뷰 요청 횟수
                "reviews_received": 0,         # 받은 리뷰 수
                "reviews_given": 0,           # 준 리뷰 수
                "review_comments_addressed": 0, # 처리한 리뷰 코멘트
                "pr_merged": 0,               # 머지된 PR 수
                "pr_closed": 0,               # 닫힌 PR 수
            },
            
            # 4. 커뮤니케이션
            "communication": {
                "messages_sent": 0,           # 보낸 메시지 수
                "messages_received": 0,       # 받은 메시지 수
                "questions_asked": 0,         # 질문한 횟수
                "questions_answered": 0,      # 답변한 횟수
                "help_requests": 0,           # 도움 요청 횟수
                "status_updates": 0,          # 상태 업데이트 횟수
                "allow_requests": 0,          # Allow 요청 횟수
            },
            
            # 5. 응답 성능
            "response_performance": {
                "total_calls": 0,             # 총 호출 횟수
                "successful_responses": 0,     # 성공 응답 횟수
                "failed_responses": 0,        # 실패 응답 횟수
                "timeout_count": 0,           # 타임아웃 횟수
                "retry_count": 0,             # 재시도 횟수
                "avg_response_time": [],      # 평균 응답 시간
                "max_response_time": 0,       # 최대 응답 시간
            },
            
            # 6. 백업 시스템
            "backup_system": {
                "times_backed_up": 0,         # 백업된 횟수
                "times_as_backup": 0,         # 백업으로 활동한 횟수
                "backup_success": 0,          # 백업 성공 횟수
                "backup_failure": 0,          # 백업 실패 횟수
                "primary_failure_rate": 0,    # 주 담당 실패율
            },
            
            # 7. 품질 지표
            "quality_metrics": {
                "errors_encountered": 0,      # 발생한 에러 수
                "errors_resolved": 0,         # 해결한 에러 수
                "bugs_introduced": 0,         # 발생시킨 버그 수
                "bugs_fixed": 0,              # 수정한 버그 수
                "test_passed": 0,             # 통과한 테스트 수
                "test_failed": 0,             # 실패한 테스트 수
                "code_quality_score": [],     # 코드 품질 점수
            },
            
            # 8. 프로세스 준수
            "process_compliance": {
                "workflow_followed": 0,        # 워크플로우 준수 횟수
                "workflow_violated": 0,        # 워크플로우 위반 횟수
                "checklist_completed": 0,      # 체크리스트 완료 횟수
                "documentation_created": 0,    # 문서 작성 횟수
                "proper_branch_usage": 0,      # 올바른 브랜치 사용
                "proper_commit_format": 0,     # 올바른 커밋 형식
            }
        }
    
    def track_issue_assignment(self, ai_name: str, issue_id: str):
        """이슈 할당 추적"""
        if ai_name in self.team_kpis:
            self.team_kpis[ai_name]["issue_management"]["issues_assigned"] += 1
            self._log_event(ai_name, "issue_assigned", issue_id)
    
    def track_issue_start(self, ai_name: str, issue_id: str, time_to_start: float):
        """이슈 시작 추적"""
        if ai_name in self.team_kpis:
            kpi = self.team_kpis[ai_name]["issue_management"]
            kpi["issues_started"] += 1
            kpi["avg_time_to_start"].append(time_to_start)
            self._log_event(ai_name, "issue_started", issue_id)
    
    def track_pr_creation(self, ai_name: str, pr_number: int, has_description: bool = True):
        """PR 생성 추적"""
        if ai_name in self.team_kpis:
            pr_kpi = self.team_kpis[ai_name]["pr_process"]
            pr_kpi["prs_created"] += 1
            if has_description:
                pr_kpi["pr_descriptions_written"] += 1
            self._log_event(ai_name, "pr_created", f"PR #{pr_number}")
    
    def track_code_review(self, reviewer: str, pr_owner: str, comments: int):
        """코드 리뷰 추적"""
        if reviewer in self.team_kpis:
            self.team_kpis[reviewer]["pr_process"]["reviews_given"] += 1
        if pr_owner in self.team_kpis:
            self.team_kpis[pr_owner]["pr_process"]["reviews_received"] += 1
            self.team_kpis[pr_owner]["pr_process"]["review_comments_addressed"] += comments
    
    def track_backup_activation(self, primary: str, backup: str, success: bool):
        """백업 활성화 추적"""
        if primary in self.team_kpis:
            self.team_kpis[primary]["backup_system"]["times_backed_up"] += 1
        if backup in self.team_kpis:
            self.team_kpis[backup]["backup_system"]["times_as_backup"] += 1
            if success:
                self.team_kpis[backup]["backup_system"]["backup_success"] += 1
            else:
                self.team_kpis[backup]["backup_system"]["backup_failure"] += 1
    
    def track_process_compliance(self, ai_name: str, compliant: bool, process_type: str):
        """프로세스 준수 추적"""
        if ai_name in self.team_kpis:
            compliance = self.team_kpis[ai_name]["process_compliance"]
            if compliant:
                compliance["workflow_followed"] += 1
                if process_type == "branch":
                    compliance["proper_branch_usage"] += 1
                elif process_type == "commit":
                    compliance["proper_commit_format"] += 1
            else:
                compliance["workflow_violated"] += 1
    
    def _log_event(self, ai_name: str, event_type: str, details: str):
        """이벤트 로깅"""
        timestamp = datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "ai": ai_name,
            "event": event_type,
            "details": details
        }
        # 로그를 파일에 추가
        with open("kpi_events.jsonl", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    
    def generate_report(self) -> Dict:
        """종합 리포트 생성"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "runtime_minutes": (datetime.now() - self.start_time).seconds // 60,
            "team_performance": {}
        }
        
        for ai_name, kpis in self.team_kpis.items():
            # 주요 지표 계산
            issue_completion_rate = 0
            if kpis["issue_management"]["issues_assigned"] > 0:
                issue_completion_rate = (
                    kpis["issue_management"]["issues_completed"] / 
                    kpis["issue_management"]["issues_assigned"] * 100
                )
            
            pr_success_rate = 0
            if kpis["pr_process"]["prs_created"] > 0:
                pr_success_rate = (
                    kpis["pr_process"]["pr_merged"] / 
                    kpis["pr_process"]["prs_created"] * 100
                )
            
            process_compliance_rate = 0
            total_processes = (
                kpis["process_compliance"]["workflow_followed"] + 
                kpis["process_compliance"]["workflow_violated"]
            )
            if total_processes > 0:
                process_compliance_rate = (
                    kpis["process_compliance"]["workflow_followed"] / 
                    total_processes * 100
                )
            
            report["team_performance"][ai_name] = {
                "summary": {
                    "issue_completion_rate": round(issue_completion_rate, 1),
                    "pr_success_rate": round(pr_success_rate, 1),
                    "process_compliance_rate": round(process_compliance_rate, 1),
                    "backup_dependency": kpis["backup_system"]["times_backed_up"]
                },
                "detailed_kpis": kpis
            }
        
        return report
    
    def print_dashboard(self):
        """대시보드 출력"""
        print("\n" + "="*80)
        print("📊 AI Orchestra 상세 KPI 대시보드")
        print("="*80)
        
        report = self.generate_report()
        
        for ai_name, perf in report["team_performance"].items():
            print(f"\n🤖 {ai_name}")
            print("-"*40)
            
            summary = perf["summary"]
            kpis = perf["detailed_kpis"]
            
            # 이슈 관리
            print(f"📋 이슈: {kpis['issue_management']['issues_completed']}/{kpis['issue_management']['issues_assigned']} 완료")
            print(f"   시작보고: {kpis['issue_management']['issues_started']}")
            
            # PR 프로세스
            print(f"🔄 PR: {kpis['pr_process']['prs_created']} 생성, {kpis['pr_process']['pr_merged']} 머지")
            print(f"   리뷰: {kpis['pr_process']['reviews_given']} 제공, {kpis['pr_process']['reviews_received']} 받음")
            
            # 코드 작업
            print(f"💻 코드: +{kpis['code_work']['lines_added']} -{kpis['code_work']['lines_deleted']} 라인")
            print(f"   커밋: {kpis['code_work']['commits_made']}회")
            
            # 프로세스 준수
            print(f"✅ 프로세스 준수율: {summary['process_compliance_rate']}%")
            
            # 백업
            if summary["backup_dependency"] > 0:
                print(f"⚠️ 백업 의존: {summary['backup_dependency']}회")
    
    def save_report(self, filename: str = "detailed_kpi_report.json"):
        """리포트 저장"""
        report = self.generate_report()
        with open(filename, "w") as f:
            json.dump(report, f, indent=2)
        return filename

# 테스트 및 사용 예제
if __name__ == "__main__":
    tracker = DetailedKPITracker()
    
    # 예제: 이슈 할당 및 시작
    tracker.track_issue_assignment("Gemini", "ORCH-101")
    tracker.track_issue_start("Gemini", "ORCH-101", 5.2)  # 5.2초 후 시작
    
    # 예제: PR 생성 및 리뷰
    tracker.track_pr_creation("Gemini", 42, has_description=True)
    tracker.track_code_review("Claude", "Gemini", comments=3)
    
    # 예제: 백업 활성화
    tracker.track_backup_activation("Codex", "Gemini", success=True)
    
    # 예제: 프로세스 준수
    tracker.track_process_compliance("Gemini", compliant=True, process_type="branch")
    
    # 대시보드 출력
    tracker.print_dashboard()
    
    # 리포트 저장
    report_file = tracker.save_report()
    print(f"\n💾 상세 KPI 리포트 저장: {report_file}")