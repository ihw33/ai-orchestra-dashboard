#!/usr/bin/env python3
"""
Round 4 빠른 통합 테스트
"""
import json
import os
import subprocess
from datetime import datetime

def quick_test():
    print("🧪 Round 4 빠른 통합 테스트")
    print("="*50)
    
    results = []
    
    # 1. PL Bot 리포트 확인
    print("\n✅ PL Bot 체크...")
    if os.path.exists("pl-bot-report.json"):
        with open("pl-bot-report.json", "r") as f:
            report = json.load(f)
        active_count = sum(1 for ai in report["team_status"].values() if ai["status"] == "active")
        print(f"  활성 AI: {active_count}/4")
        results.append({"test": "PL Bot", "pass": active_count == 4})
    else:
        print("  ❌ 리포트 없음")
        results.append({"test": "PL Bot", "pass": False})
    
    # 2. AI 실행 로그 확인
    print("\n✅ AI 실행 로그 체크...")
    if os.path.exists("ai_execution_log.json"):
        with open("ai_execution_log.json", "r") as f:
            log = json.load(f)
        success_rate = (log["summary"]["success"] / log["summary"]["total"]) * 100
        print(f"  성공률: {success_rate:.1f}%")
        results.append({"test": "AI Execution", "pass": success_rate >= 50})
    else:
        print("  ❌ 로그 없음")
        results.append({"test": "AI Execution", "pass": False})
    
    # 3. Auto-onboarding 스크립트 확인
    print("\n✅ Auto-onboarding 체크...")
    onboarding_exists = os.path.exists("auto-onboarding/onboarding_v2.py")
    print(f"  스크립트: {'있음' if onboarding_exists else '없음'}")
    results.append({"test": "Auto-onboarding", "pass": onboarding_exists})
    
    # 4. GitHub CLI 확인
    print("\n✅ GitHub CLI 체크...")
    try:
        result = subprocess.run(["gh", "--version"], capture_output=True, timeout=2)
        gh_works = result.returncode == 0
        print(f"  GitHub CLI: {'정상' if gh_works else '오류'}")
        results.append({"test": "GitHub CLI", "pass": gh_works})
    except:
        print("  ❌ GitHub CLI 실행 실패")
        results.append({"test": "GitHub CLI", "pass": False})
    
    # 5. 서버 상태 확인
    print("\n✅ 서버 상태 체크...")
    try:
        # Frontend
        frontend = subprocess.run(
            "curl -s -o /dev/null -w '%{http_code}' http://localhost:3000",
            shell=True,
            capture_output=True,
            text=True,
            timeout=2
        )
        frontend_up = frontend.stdout.strip() != "000"
        
        # Backend
        backend = subprocess.run(
            "curl -s -o /dev/null -w '%{http_code}' http://localhost:8001/health",
            shell=True,
            capture_output=True,
            text=True,
            timeout=2
        )
        backend_up = backend.stdout.strip() == "200"
        
        print(f"  Frontend: {'UP' if frontend_up else 'DOWN'}")
        print(f"  Backend: {'UP' if backend_up else 'DOWN'}")
        results.append({"test": "Servers", "pass": frontend_up or backend_up})
    except:
        print("  ⚠️ 서버 체크 실패")
        results.append({"test": "Servers", "pass": False})
    
    # 결과 요약
    print("\n" + "="*50)
    print("📊 테스트 결과 요약")
    print("="*50)
    
    passed = sum(1 for r in results if r["pass"])
    total = len(results)
    
    for r in results:
        status = "✅" if r["pass"] else "❌"
        print(f"{status} {r['test']}")
    
    print(f"\n통과: {passed}/{total} ({passed/total*100:.0f}%)")
    
    # 최종 판정
    if passed == total:
        print("\n🎉 모든 테스트 통과!")
    elif passed >= total * 0.7:
        print("\n✅ 대부분 통과. Round 4 준비됨!")
    else:
        print("\n⚠️ 추가 작업 필요")
    
    # 결과 저장
    with open("quick_test_result.json", "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "passed": passed,
            "total": total,
            "success_rate": passed/total*100,
            "results": results
        }, f, indent=2)
    
    print("\n💾 결과 저장됨: quick_test_result.json")

if __name__ == "__main__":
    quick_test()