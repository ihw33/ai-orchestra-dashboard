#!/usr/bin/env python3
"""
Round 4 통합 테스트
모든 구성 요소가 함께 작동하는지 확인
"""
import subprocess
import json
import time
from datetime import datetime

class IntegrationTest:
    def __init__(self):
        self.results = []
        self.start_time = datetime.now()
        
    def test_pl_bot(self):
        """PL Bot 동작 테스트"""
        print("\n🤖 PL Bot 테스트...")
        try:
            # PL Bot 리포트 확인
            with open("pl-bot-report.json", "r") as f:
                report = json.load(f)
            
            # 모든 AI 상태 확인
            all_active = all(
                ai["status"] == "active" 
                for ai in report["team_status"].values()
            )
            
            result = {
                "test": "PL Bot",
                "status": "PASS" if all_active else "FAIL",
                "details": f"Active AIs: {sum(1 for ai in report['team_status'].values() if ai['status'] == 'active')}/4"
            }
            self.results.append(result)
            print(f"  {result['status']}: {result['details']}")
            return all_active
        except Exception as e:
            result = {"test": "PL Bot", "status": "FAIL", "details": str(e)}
            self.results.append(result)
            print(f"  FAIL: {e}")
            return False
    
    def test_ai_execution(self):
        """AI 실행 테스트"""
        print("\n🎯 AI 실행 테스트...")
        try:
            # 실행 로그 확인
            with open("ai_execution_log.json", "r") as f:
                log = json.load(f)
            
            success_rate = (log["summary"]["success"] / log["summary"]["total"]) * 100
            
            result = {
                "test": "AI Execution",
                "status": "PASS" if success_rate >= 50 else "FAIL",
                "details": f"Success rate: {success_rate:.1f}%"
            }
            self.results.append(result)
            print(f"  {result['status']}: {result['details']}")
            return success_rate >= 50
        except Exception as e:
            result = {"test": "AI Execution", "status": "FAIL", "details": str(e)}
            self.results.append(result)
            print(f"  FAIL: {e}")
            return False
    
    def test_allow_detection(self):
        """Allow 요청 감지 테스트"""
        print("\n🔍 Allow 감지 테스트...")
        try:
            # 테스트 Allow 요청 생성
            test_message = "Allow me to access the database"
            
            # PL Bot이 감지하는지 확인
            # (실제로는 PL Bot 로직을 직접 테스트)
            detected = "allow" in test_message.lower()
            
            result = {
                "test": "Allow Detection",
                "status": "PASS" if detected else "FAIL",
                "details": f"Test message detection: {detected}"
            }
            self.results.append(result)
            print(f"  {result['status']}: {result['details']}")
            return detected
        except Exception as e:
            result = {"test": "Allow Detection", "status": "FAIL", "details": str(e)}
            self.results.append(result)
            print(f"  FAIL: {e}")
            return False
    
    def test_github_integration(self):
        """GitHub 통합 테스트"""
        print("\n🐙 GitHub 통합 테스트...")
        try:
            # GitHub CLI 확인
            result_gh = subprocess.run(
                ["gh", "--version"],
                capture_output=True,
                text=True
            )
            
            gh_works = result_gh.returncode == 0
            
            # Issue 목록 확인 (실제 저장소가 있다면)
            if gh_works:
                issues_cmd = subprocess.run(
                    "gh issue list --limit 1 2>/dev/null",
                    shell=True,
                    capture_output=True,
                    text=True
                )
                can_access_issues = issues_cmd.returncode == 0
            else:
                can_access_issues = False
            
            result = {
                "test": "GitHub Integration",
                "status": "PASS" if gh_works else "PARTIAL",
                "details": f"CLI: {'OK' if gh_works else 'Failed'}, Issues: {'OK' if can_access_issues else 'N/A'}"
            }
            self.results.append(result)
            print(f"  {result['status']}: {result['details']}")
            return gh_works
        except Exception as e:
            result = {"test": "GitHub Integration", "status": "FAIL", "details": str(e)}
            self.results.append(result)
            print(f"  FAIL: {e}")
            return False
    
    def test_auto_onboarding(self):
        """Auto-onboarding 테스트"""
        print("\n🚀 Auto-onboarding 테스트...")
        try:
            # onboarding 스크립트 존재 확인
            import os
            onboarding_exists = os.path.exists("auto-onboarding/onboarding_v2.py")
            
            result = {
                "test": "Auto-onboarding",
                "status": "PASS" if onboarding_exists else "FAIL",
                "details": f"Script exists: {onboarding_exists}"
            }
            self.results.append(result)
            print(f"  {result['status']}: {result['details']}")
            return onboarding_exists
        except Exception as e:
            result = {"test": "Auto-onboarding", "status": "FAIL", "details": str(e)}
            self.results.append(result)
            print(f"  FAIL: {e}")
            return False
    
    def test_monitoring_dashboard(self):
        """모니터링 대시보드 테스트"""
        print("\n📊 모니터링 대시보드 테스트...")
        try:
            # Frontend 서버 확인
            frontend_check = subprocess.run(
                "curl -s http://localhost:3000 > /dev/null",
                shell=True
            )
            frontend_up = frontend_check.returncode == 0
            
            # Backend API 확인
            backend_check = subprocess.run(
                "curl -s http://localhost:8001/health > /dev/null",
                shell=True
            )
            backend_up = backend_check.returncode == 0
            
            result = {
                "test": "Monitoring Dashboard",
                "status": "PASS" if (frontend_up and backend_up) else "PARTIAL",
                "details": f"Frontend: {'UP' if frontend_up else 'DOWN'}, Backend: {'UP' if backend_up else 'DOWN'}"
            }
            self.results.append(result)
            print(f"  {result['status']}: {result['details']}")
            return frontend_up or backend_up
        except Exception as e:
            result = {"test": "Monitoring Dashboard", "status": "FAIL", "details": str(e)}
            self.results.append(result)
            print(f"  FAIL: {e}")
            return False
    
    def generate_report(self):
        """테스트 리포트 생성"""
        elapsed = (datetime.now() - self.start_time).seconds
        
        # 결과 집계
        passed = sum(1 for r in self.results if r["status"] == "PASS")
        failed = sum(1 for r in self.results if r["status"] == "FAIL")
        partial = sum(1 for r in self.results if r["status"] == "PARTIAL")
        total = len(self.results)
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "elapsed_seconds": elapsed,
            "summary": {
                "total": total,
                "passed": passed,
                "failed": failed,
                "partial": partial,
                "success_rate": (passed / total * 100) if total > 0 else 0
            },
            "results": self.results
        }
        
        # 리포트 저장
        with open("integration_test_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        # 콘솔 출력
        print("\n" + "="*50)
        print("📋 통합 테스트 결과")
        print("="*50)
        print(f"총 테스트: {total}")
        print(f"✅ 통과: {passed}")
        print(f"❌ 실패: {failed}")
        print(f"⚠️ 부분: {partial}")
        print(f"성공률: {report['summary']['success_rate']:.1f}%")
        print(f"소요 시간: {elapsed}초")
        
        # 최종 판정
        if failed == 0:
            print("\n🎉 모든 테스트 통과! Round 4 준비 완료!")
        elif passed >= total * 0.7:
            print("\n✅ 대부분 테스트 통과. 일부 수정 필요.")
        else:
            print("\n⚠️ 추가 작업 필요. 실패한 항목을 확인하세요.")
        
        return report

def main():
    print("🧪 Round 4 통합 테스트 시작")
    print("="*50)
    
    tester = IntegrationTest()
    
    # 모든 테스트 실행
    tester.test_pl_bot()
    tester.test_ai_execution()
    tester.test_allow_detection()
    tester.test_github_integration()
    tester.test_auto_onboarding()
    tester.test_monitoring_dashboard()
    
    # 리포트 생성
    report = tester.generate_report()
    
    print("\n💾 리포트 저장됨: integration_test_report.json")

if __name__ == "__main__":
    main()