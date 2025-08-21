#!/usr/bin/env python3
"""
KPI 분석 및 원인 진단 시스템
예상값 대비 실제값 분석 및 자동 코멘트 생성
"""
import json
from datetime import datetime
from typing import Dict, List, Tuple

class KPIAnalyzer:
    def __init__(self):
        # 프로세스별 예상 기준값 (1일 기준)
        self.expected_baselines = {
            "issue_management": {
                "issues_assigned": 5,                    # 하루 5개 이슈 예상
                "issue_completion_rate": 80,             # 80% 완료율 목표
                "avg_time_to_start_minutes": 10,         # 10분 내 시작
                "avg_time_to_complete_hours": 2,         # 2시간 내 완료
                "start_report_rate": 100,                # 100% 시작 보고
                "completion_report_rate": 100,           # 100% 완료 보고
            },
            "pr_process": {
                "prs_per_issue": 1,                      # 이슈당 1개 PR
                "pr_description_rate": 100,              # 100% 설명 작성
                "review_request_rate": 100,              # 100% 리뷰 요청
                "review_response_time_hours": 1,         # 1시간 내 리뷰
                "pr_merge_rate": 90,                     # 90% 머지 성공
                "review_comments_per_pr": 3,             # PR당 평균 3개 코멘트
            },
            "code_quality": {
                "commits_per_pr": 3,                     # PR당 3개 커밋
                "lines_per_commit": 50,                  # 커밋당 50줄
                "test_pass_rate": 95,                    # 95% 테스트 통과
                "bug_introduction_rate": 5,              # 5% 이하 버그 발생
                "error_self_resolution_rate": 80,        # 80% 자체 해결
            },
            "communication": {
                "response_rate": 95,                     # 95% 응답률
                "avg_response_time_seconds": 5,          # 5초 내 응답
                "status_updates_per_issue": 3,           # 이슈당 3번 상태 업데이트
                "questions_answered_rate": 90,           # 90% 질문 답변
            },
            "process_compliance": {
                "workflow_compliance_rate": 95,          # 95% 워크플로우 준수
                "branch_naming_compliance": 100,         # 100% 브랜치 규칙
                "commit_format_compliance": 100,         # 100% 커밋 형식
                "checklist_completion_rate": 100,        # 100% 체크리스트
            },
            "backup_system": {
                "max_backup_activation_rate": 10,        # 최대 10% 백업 활성화
                "backup_success_rate": 100,              # 백업 100% 성공
                "primary_success_rate": 90,              # 주담당 90% 성공
            }
        }
        
        self.analysis_results = []
        
    def analyze_kpi(self, actual_kpis: Dict, ai_name: str) -> Dict:
        """실제 KPI vs 예상 기준값 분석"""
        analysis = {
            "ai_name": ai_name,
            "timestamp": datetime.now().isoformat(),
            "deviations": [],
            "root_causes": [],
            "recommendations": []
        }
        
        # 1. 이슈 관리 분석
        issue_analysis = self._analyze_issue_management(actual_kpis.get("issue_management", {}))
        analysis["deviations"].extend(issue_analysis["deviations"])
        analysis["root_causes"].extend(issue_analysis["causes"])
        
        # 2. PR 프로세스 분석
        pr_analysis = self._analyze_pr_process(actual_kpis.get("pr_process", {}), actual_kpis.get("issue_management", {}))
        analysis["deviations"].extend(pr_analysis["deviations"])
        analysis["root_causes"].extend(pr_analysis["causes"])
        
        # 3. 코드 품질 분석
        quality_analysis = self._analyze_code_quality(actual_kpis.get("code_work", {}), actual_kpis.get("quality_metrics", {}))
        analysis["deviations"].extend(quality_analysis["deviations"])
        analysis["root_causes"].extend(quality_analysis["causes"])
        
        # 4. 통신 분석
        comm_analysis = self._analyze_communication(actual_kpis.get("communication", {}), actual_kpis.get("response_performance", {}))
        analysis["deviations"].extend(comm_analysis["deviations"])
        analysis["root_causes"].extend(comm_analysis["causes"])
        
        # 5. 프로세스 준수 분석
        compliance_analysis = self._analyze_compliance(actual_kpis.get("process_compliance", {}))
        analysis["deviations"].extend(compliance_analysis["deviations"])
        analysis["root_causes"].extend(compliance_analysis["causes"])
        
        # 6. 백업 시스템 분석
        backup_analysis = self._analyze_backup(actual_kpis.get("backup_system", {}))
        analysis["deviations"].extend(backup_analysis["deviations"])
        analysis["root_causes"].extend(backup_analysis["causes"])
        
        # 7. 종합 권고사항 생성
        analysis["recommendations"] = self._generate_recommendations(analysis["deviations"], analysis["root_causes"])
        
        return analysis
    
    def _analyze_issue_management(self, issue_kpis: Dict) -> Dict:
        """이슈 관리 분석"""
        result = {"deviations": [], "causes": []}
        expected = self.expected_baselines["issue_management"]
        
        # 완료율 체크
        if issue_kpis.get("issues_assigned", 0) > 0:
            completion_rate = (issue_kpis.get("issues_completed", 0) / issue_kpis["issues_assigned"]) * 100
            
            if completion_rate < expected["issue_completion_rate"]:
                deviation = {
                    "metric": "이슈 완료율",
                    "expected": expected["issue_completion_rate"],
                    "actual": round(completion_rate, 1),
                    "severity": "HIGH" if completion_rate < 50 else "MEDIUM"
                }
                result["deviations"].append(deviation)
                
                # 원인 분석
                if issue_kpis.get("issues_started", 0) < issue_kpis.get("issues_assigned", 0):
                    result["causes"].append({
                        "issue": "시작하지 못한 이슈 존재",
                        "detail": f"{issue_kpis['issues_assigned'] - issue_kpis.get('issues_started', 0)}개 이슈 미시작",
                        "impact": "완료율 저하"
                    })
                
                if issue_kpis.get("issues_abandoned", 0) > 0:
                    result["causes"].append({
                        "issue": "포기한 이슈 존재",
                        "detail": f"{issue_kpis['issues_abandoned']}개 이슈 포기",
                        "impact": "완료율 저하, 재할당 필요"
                    })
        
        # 시작 시간 체크
        if issue_kpis.get("avg_time_to_start", []):
            avg_start_time = sum(issue_kpis["avg_time_to_start"]) / len(issue_kpis["avg_time_to_start"])
            if avg_start_time > expected["avg_time_to_start_minutes"] * 60:  # 초 단위로 변환
                result["deviations"].append({
                    "metric": "평균 시작 시간",
                    "expected": f"{expected['avg_time_to_start_minutes']}분",
                    "actual": f"{avg_start_time/60:.1f}분",
                    "severity": "LOW"
                })
                result["causes"].append({
                    "issue": "이슈 시작 지연",
                    "detail": "할당 후 시작까지 시간 초과",
                    "impact": "전체 프로세스 지연"
                })
        
        return result
    
    def _analyze_pr_process(self, pr_kpis: Dict, issue_kpis: Dict) -> Dict:
        """PR 프로세스 분석"""
        result = {"deviations": [], "causes": []}
        expected = self.expected_baselines["pr_process"]
        
        # PR 생성률 체크
        completed_issues = issue_kpis.get("issues_completed", 0)
        if completed_issues > 0:
            prs_created = pr_kpis.get("prs_created", 0)
            pr_per_issue = prs_created / completed_issues
            
            if pr_per_issue < expected["prs_per_issue"]:
                result["deviations"].append({
                    "metric": "이슈당 PR 수",
                    "expected": expected["prs_per_issue"],
                    "actual": round(pr_per_issue, 2),
                    "severity": "HIGH"
                })
                result["causes"].append({
                    "issue": "PR 생성 누락",
                    "detail": "완료된 이슈에 대한 PR 미생성",
                    "impact": "코드 리뷰 프로세스 누락"
                })
        
        # PR 머지율 체크
        if pr_kpis.get("prs_created", 0) > 0:
            merge_rate = (pr_kpis.get("pr_merged", 0) / pr_kpis["prs_created"]) * 100
            
            if merge_rate < expected["pr_merge_rate"]:
                result["deviations"].append({
                    "metric": "PR 머지율",
                    "expected": f"{expected['pr_merge_rate']}%",
                    "actual": f"{merge_rate:.1f}%",
                    "severity": "MEDIUM"
                })
                
                # 머지 실패 원인 분석
                if pr_kpis.get("review_comments_addressed", 0) < pr_kpis.get("reviews_received", 0) * 3:
                    result["causes"].append({
                        "issue": "리뷰 코멘트 미처리",
                        "detail": "받은 리뷰에 대한 대응 부족",
                        "impact": "PR 머지 지연 또는 실패"
                    })
        
        # 리뷰 프로세스 체크
        if pr_kpis.get("review_requested", 0) < pr_kpis.get("prs_created", 0):
            result["deviations"].append({
                "metric": "리뷰 요청률",
                "expected": "100%",
                "actual": f"{(pr_kpis.get('review_requested', 0) / max(pr_kpis.get('prs_created', 1), 1)) * 100:.1f}%",
                "severity": "HIGH"
            })
            result["causes"].append({
                "issue": "리뷰 요청 누락",
                "detail": "PR 생성 후 리뷰 요청 안 함",
                "impact": "코드 품질 검증 누락"
            })
        
        return result
    
    def _analyze_code_quality(self, code_kpis: Dict, quality_kpis: Dict) -> Dict:
        """코드 품질 분석"""
        result = {"deviations": [], "causes": []}
        expected = self.expected_baselines["code_quality"]
        
        # 테스트 통과율 체크
        total_tests = quality_kpis.get("test_passed", 0) + quality_kpis.get("test_failed", 0)
        if total_tests > 0:
            test_pass_rate = (quality_kpis["test_passed"] / total_tests) * 100
            
            if test_pass_rate < expected["test_pass_rate"]:
                result["deviations"].append({
                    "metric": "테스트 통과율",
                    "expected": f"{expected['test_pass_rate']}%",
                    "actual": f"{test_pass_rate:.1f}%",
                    "severity": "HIGH"
                })
                result["causes"].append({
                    "issue": "테스트 실패",
                    "detail": f"{quality_kpis.get('test_failed', 0)}개 테스트 실패",
                    "impact": "배포 불가, 품질 저하"
                })
        
        # 버그 발생률 체크
        if code_kpis.get("commits_made", 0) > 0:
            bug_rate = (quality_kpis.get("bugs_introduced", 0) / code_kpis["commits_made"]) * 100
            
            if bug_rate > expected["bug_introduction_rate"]:
                result["deviations"].append({
                    "metric": "버그 발생률",
                    "expected": f"<{expected['bug_introduction_rate']}%",
                    "actual": f"{bug_rate:.1f}%",
                    "severity": "HIGH"
                })
                result["causes"].append({
                    "issue": "높은 버그 발생률",
                    "detail": f"커밋당 {bug_rate:.1f}% 버그 발생",
                    "impact": "추가 수정 작업 필요, 안정성 저하"
                })
        
        # 에러 해결률 체크
        if quality_kpis.get("errors_encountered", 0) > 0:
            resolution_rate = (quality_kpis.get("errors_resolved", 0) / quality_kpis["errors_encountered"]) * 100
            
            if resolution_rate < expected["error_self_resolution_rate"]:
                result["deviations"].append({
                    "metric": "에러 자체 해결률",
                    "expected": f"{expected['error_self_resolution_rate']}%",
                    "actual": f"{resolution_rate:.1f}%",
                    "severity": "MEDIUM"
                })
                result["causes"].append({
                    "issue": "에러 해결 능력 부족",
                    "detail": "발생한 에러를 자체적으로 해결하지 못함",
                    "impact": "외부 도움 필요, 생산성 저하"
                })
        
        return result
    
    def _analyze_communication(self, comm_kpis: Dict, response_kpis: Dict) -> Dict:
        """커뮤니케이션 분석"""
        result = {"deviations": [], "causes": []}
        expected = self.expected_baselines["communication"]
        
        # 응답률 체크
        if response_kpis.get("total_calls", 0) > 0:
            response_rate = (response_kpis.get("successful_responses", 0) / response_kpis["total_calls"]) * 100
            
            if response_rate < expected["response_rate"]:
                result["deviations"].append({
                    "metric": "응답률",
                    "expected": f"{expected['response_rate']}%",
                    "actual": f"{response_rate:.1f}%",
                    "severity": "HIGH"
                })
                
                # 응답 실패 원인 분석
                if response_kpis.get("timeout_count", 0) > 0:
                    result["causes"].append({
                        "issue": "타임아웃 발생",
                        "detail": f"{response_kpis['timeout_count']}회 타임아웃",
                        "impact": "작업 지연, 백업 AI 활성화"
                    })
                
                if response_kpis.get("failed_responses", 0) > 0:
                    result["causes"].append({
                        "issue": "응답 실패",
                        "detail": f"{response_kpis['failed_responses']}회 실패",
                        "impact": "재시도 필요, 효율성 저하"
                    })
        
        # 평균 응답 시간 체크
        if response_kpis.get("avg_response_time", []):
            avg_time = sum(response_kpis["avg_response_time"]) / len(response_kpis["avg_response_time"])
            
            if avg_time > expected["avg_response_time_seconds"]:
                result["deviations"].append({
                    "metric": "평균 응답 시간",
                    "expected": f"{expected['avg_response_time_seconds']}초",
                    "actual": f"{avg_time:.1f}초",
                    "severity": "MEDIUM"
                })
                result["causes"].append({
                    "issue": "느린 응답 속도",
                    "detail": f"평균 {avg_time:.1f}초 응답 시간",
                    "impact": "전체 프로세스 지연"
                })
        
        return result
    
    def _analyze_compliance(self, compliance_kpis: Dict) -> Dict:
        """프로세스 준수 분석"""
        result = {"deviations": [], "causes": []}
        expected = self.expected_baselines["process_compliance"]
        
        # 워크플로우 준수율
        total_workflows = compliance_kpis.get("workflow_followed", 0) + compliance_kpis.get("workflow_violated", 0)
        if total_workflows > 0:
            compliance_rate = (compliance_kpis["workflow_followed"] / total_workflows) * 100
            
            if compliance_rate < expected["workflow_compliance_rate"]:
                result["deviations"].append({
                    "metric": "워크플로우 준수율",
                    "expected": f"{expected['workflow_compliance_rate']}%",
                    "actual": f"{compliance_rate:.1f}%",
                    "severity": "HIGH"
                })
                result["causes"].append({
                    "issue": "프로세스 위반",
                    "detail": f"{compliance_kpis.get('workflow_violated', 0)}회 위반",
                    "impact": "품질 일관성 저하, 재작업 필요"
                })
        
        # 브랜치 규칙 준수
        if compliance_kpis.get("proper_branch_usage", 0) == 0 and compliance_kpis.get("workflow_followed", 0) > 0:
            result["deviations"].append({
                "metric": "브랜치 규칙 준수",
                "expected": "100%",
                "actual": "0%",
                "severity": "HIGH"
            })
            result["causes"].append({
                "issue": "브랜치 규칙 미준수",
                "detail": "올바른 브랜치 사용 기록 없음",
                "impact": "코드 관리 혼란, 머지 충돌 가능성"
            })
        
        return result
    
    def _analyze_backup(self, backup_kpis: Dict) -> Dict:
        """백업 시스템 분석"""
        result = {"deviations": [], "causes": []}
        expected = self.expected_baselines["backup_system"]
        
        # 백업 활성화율
        if backup_kpis.get("times_backed_up", 0) > 0:
            # 전체 작업 대비 백업 활성화 비율 계산 필요
            backup_activation_rate = backup_kpis["times_backed_up"]  # 단순 횟수로 일단 체크
            
            if backup_activation_rate > expected["max_backup_activation_rate"]:
                result["deviations"].append({
                    "metric": "백업 활성화 횟수",
                    "expected": f"<{expected['max_backup_activation_rate']}회",
                    "actual": f"{backup_activation_rate}회",
                    "severity": "MEDIUM"
                })
                result["causes"].append({
                    "issue": "주 담당 AI 불안정",
                    "detail": f"{backup_activation_rate}회 백업 AI 활성화",
                    "impact": "효율성 저하, AI 재교육 필요"
                })
        
        # 백업 성공률
        if backup_kpis.get("times_as_backup", 0) > 0:
            backup_success_rate = (backup_kpis.get("backup_success", 0) / backup_kpis["times_as_backup"]) * 100
            
            if backup_success_rate < expected["backup_success_rate"]:
                result["deviations"].append({
                    "metric": "백업 성공률",
                    "expected": f"{expected['backup_success_rate']}%",
                    "actual": f"{backup_success_rate:.1f}%",
                    "severity": "HIGH"
                })
                result["causes"].append({
                    "issue": "백업 시스템 실패",
                    "detail": "백업 AI도 작업 처리 실패",
                    "impact": "작업 완전 실패, 수동 개입 필요"
                })
        
        return result
    
    def _generate_recommendations(self, deviations: List, causes: List) -> List[Dict]:
        """종합 권고사항 생성"""
        recommendations = []
        
        # 심각도별 분류
        high_severity = [d for d in deviations if d.get("severity") == "HIGH"]
        medium_severity = [d for d in deviations if d.get("severity") == "MEDIUM"]
        
        # HIGH 심각도 권고사항
        if high_severity:
            recommendations.append({
                "priority": "URGENT",
                "action": "즉시 조치 필요",
                "items": [f"{d['metric']}: 예상 {d['expected']} → 실제 {d['actual']}" for d in high_severity],
                "suggestion": "프로세스 재설계 또는 AI 재교육 필요"
            })
        
        # MEDIUM 심각도 권고사항
        if medium_severity:
            recommendations.append({
                "priority": "IMPORTANT",
                "action": "개선 필요",
                "items": [f"{d['metric']}: 예상 {d['expected']} → 실제 {d['actual']}" for d in medium_severity],
                "suggestion": "모니터링 강화 및 점진적 개선"
            })
        
        # 원인별 권고사항
        timeout_issues = [c for c in causes if "타임아웃" in c.get("issue", "")]
        if timeout_issues:
            recommendations.append({
                "priority": "HIGH",
                "action": "응답 시간 최적화",
                "items": [c["detail"] for c in timeout_issues],
                "suggestion": "AI 모델 최적화 또는 타임아웃 설정 조정"
            })
        
        process_violations = [c for c in causes if "프로세스" in c.get("issue", "") or "규칙" in c.get("issue", "")]
        if process_violations:
            recommendations.append({
                "priority": "HIGH",
                "action": "프로세스 교육 강화",
                "items": [c["detail"] for c in process_violations],
                "suggestion": "워크플로우 가이드 재교육 및 자동화 도구 도입"
            })
        
        return recommendations
    
    def generate_analysis_report(self, all_team_kpis: Dict) -> Dict:
        """전체 팀 분석 리포트 생성"""
        full_report = {
            "timestamp": datetime.now().isoformat(),
            "team_analysis": {},
            "summary": {
                "total_deviations": 0,
                "high_severity_count": 0,
                "top_issues": [],
                "overall_health": ""
            }
        }
        
        # 각 AI별 분석
        for ai_name, kpis in all_team_kpis.items():
            analysis = self.analyze_kpi(kpis, ai_name)
            full_report["team_analysis"][ai_name] = analysis
            
            # 전체 집계
            full_report["summary"]["total_deviations"] += len(analysis["deviations"])
            full_report["summary"]["high_severity_count"] += len([d for d in analysis["deviations"] if d.get("severity") == "HIGH"])
        
        # 상위 이슈 추출
        all_causes = []
        for ai_name, analysis in full_report["team_analysis"].items():
            for cause in analysis.get("root_causes", []):
                cause["ai"] = ai_name
                all_causes.append(cause)
        
        # 가장 많이 발생한 이슈
        issue_counts = {}
        for cause in all_causes:
            issue = cause.get("issue", "")
            issue_counts[issue] = issue_counts.get(issue, 0) + 1
        
        sorted_issues = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)
        full_report["summary"]["top_issues"] = [{"issue": issue, "count": count} for issue, count in sorted_issues[:5]]
        
        # 전체 건강도 평가
        if full_report["summary"]["high_severity_count"] > 10:
            full_report["summary"]["overall_health"] = "CRITICAL - 즉시 개입 필요"
        elif full_report["summary"]["high_severity_count"] > 5:
            full_report["summary"]["overall_health"] = "WARNING - 주의 필요"
        elif full_report["summary"]["total_deviations"] > 20:
            full_report["summary"]["overall_health"] = "CAUTION - 모니터링 필요"
        else:
            full_report["summary"]["overall_health"] = "GOOD - 정상 운영"
        
        return full_report
    
    def print_analysis_dashboard(self, report: Dict):
        """분석 대시보드 출력"""
        print("\n" + "="*80)
        print("🔍 KPI 분석 대시보드")
        print("="*80)
        
        # 전체 요약
        summary = report["summary"]
        print(f"\n📊 전체 상태: {summary['overall_health']}")
        print(f"   총 편차: {summary['total_deviations']}개")
        print(f"   심각 이슈: {summary['high_severity_count']}개")
        
        # 상위 이슈
        if summary["top_issues"]:
            print("\n🔝 주요 이슈:")
            for issue in summary["top_issues"][:3]:
                print(f"   • {issue['issue']} ({issue['count']}회 발생)")
        
        # AI별 분석
        print("\n" + "-"*80)
        for ai_name, analysis in report["team_analysis"].items():
            print(f"\n🤖 {ai_name} 분석")
            
            # 주요 편차
            high_deviations = [d for d in analysis["deviations"] if d.get("severity") == "HIGH"]
            if high_deviations:
                print("   ⚠️ 심각 편차:")
                for dev in high_deviations[:3]:
                    print(f"      • {dev['metric']}: 예상 {dev['expected']} → 실제 {dev['actual']}")
            
            # 주요 원인
            if analysis["root_causes"]:
                print("   🔍 원인:")
                for cause in analysis["root_causes"][:2]:
                    print(f"      • {cause['issue']}: {cause['detail']}")
            
            # 권고사항
            urgent_recs = [r for r in analysis["recommendations"] if r.get("priority") == "URGENT"]
            if urgent_recs:
                print("   💡 긴급 조치:")
                for rec in urgent_recs[:1]:
                    print(f"      • {rec['suggestion']}")
        
        print("\n" + "="*80)

# 사용 예제
if __name__ == "__main__":
    analyzer = KPIAnalyzer()
    
    # 테스트용 실제 KPI 데이터
    test_kpis = {
        "issue_management": {
            "issues_assigned": 5,
            "issues_completed": 2,  # 40% 완료율 - 예상보다 낮음
            "issues_started": 3,
            "issues_abandoned": 1,
            "avg_time_to_start": [600, 1200, 900],  # 평균 15분 - 예상보다 늦음
        },
        "pr_process": {
            "prs_created": 1,  # 2개 완료 이슈에 1개 PR - 예상보다 적음
            "pr_merged": 0,
            "review_requested": 0,  # 리뷰 요청 안 함 - 문제
        },
        "response_performance": {
            "total_calls": 10,
            "successful_responses": 7,  # 70% 응답률 - 예상보다 낮음
            "timeout_count": 2,
            "avg_response_time": [3, 8, 12, 5],  # 평균 7초 - 예상보다 느림
        }
    }
    
    # 분석 실행
    analysis = analyzer.analyze_kpi(test_kpis, "Gemini")
    
    # 결과 출력
    print(json.dumps(analysis, indent=2, ensure_ascii=False))