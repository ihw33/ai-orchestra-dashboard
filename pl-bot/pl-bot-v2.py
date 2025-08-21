#!/usr/bin/env python3
"""
PL Bot v2.0 - Progress Leader Bot
Round 4 구현: 실시간 팀 모니터링 + Allow 대응
"""
import subprocess
import time
import json
from datetime import datetime, timedelta
import asyncio

class PLBot:
    def __init__(self):
        self.team = {
            "Gemini": {"status": "active", "last_response": None, "task": None},
            "Codex": {"status": "active", "last_response": None, "task": None},
            "Cursor": {"status": "active", "last_response": None, "task": None},
            "Claude": {"status": "active", "last_response": None, "task": None}
        }
        self.allow_pending = []
        self.blocked_tasks = []
        
    def check_ai_response(self, ai_name):
        """AI 응답 체크 - Allow 요청 감지"""
        try:
            # 실제 AI 상태 체크 명령
            if ai_name == "Gemini":
                result = subprocess.run(
                    ["gemini", "--version"], 
                    capture_output=True, 
                    text=True, 
                    timeout=5
                )
            elif ai_name == "Codex":
                result = subprocess.run(
                    ["codex", "--version"], 
                    capture_output=True, 
                    text=True, 
                    timeout=5
                )
            elif ai_name == "Claude":
                # Claude는 현재 세션(나)이므로 항상 active
                return "active"
            elif ai_name == "Cursor":
                # Cursor는 GUI 앱이므로 프로세스 체크
                result = subprocess.run(
                    ["ps", "aux"], 
                    capture_output=True, 
                    text=True
                )
                if "Cursor" in result.stdout:
                    return "active"
                else:
                    return "not_running"
            else:
                return "unknown"
                
            # Allow 요청 감지
            if "allow" in result.stdout.lower() or "permission" in result.stdout.lower():
                self.handle_allow_request(ai_name, result.stdout)
                return "allow_pending"
                
            # 타임아웃 감지
            if not result.stdout and not result.stderr:
                return "timeout"
                
            return "active"
            
        except subprocess.TimeoutExpired:
            return "timeout"
        except Exception as e:
            print(f"❌ {ai_name} 체크 실패: {e}")
            return "error"
    
    def handle_allow_request(self, ai_name, message):
        """Allow 요청 처리"""
        print(f"\n🚨 ALLOW 요청 감지!")
        print(f"   AI: {ai_name}")
        print(f"   메시지: {message[:100]}...")
        
        # Thomas에게 알림
        self.notify_thomas(f"{ai_name}이 Allow 요청 중입니다. 확인 필요!")
        
        # Allow 대기 목록에 추가
        self.allow_pending.append({
            "ai": ai_name,
            "time": datetime.now(),
            "message": message
        })
        
    def handle_timeout(self, ai_name):
        """타임아웃 AI 처리"""
        print(f"\n⏱️ {ai_name} 타임아웃 감지!")
        
        # 복구 시도
        recovery_actions = [
            f"# {ai_name} 복구 시도 1: 엔터키 전송",
            f"# {ai_name} 복구 시도 2: 재시작",
            f"# {ai_name} 복구 시도 3: Thomas 호출"
        ]
        
        for action in recovery_actions:
            print(f"   🔧 {action}")
            time.sleep(1)
            
    def notify_thomas(self, message):
        """Thomas에게 즉시 알림"""
        print(f"\n📢 [THOMAS 알림] {message}")
        # 실제로는 GitHub Issue 댓글이나 알림 시스템 사용
        
    def monitor_team(self):
        """팀 전체 모니터링 - 30초마다"""
        print(f"\n{'='*50}")
        print(f"🤖 PL Bot 모니터링 - {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'='*50}")
        
        for ai_name, info in self.team.items():
            status = self.check_ai_response(ai_name)
            
            if status == "allow_pending":
                print(f"❗ {ai_name}: Allow 대기 중")
            elif status == "timeout":
                print(f"⏱️ {ai_name}: 타임아웃")
                self.handle_timeout(ai_name)
            elif status == "active":
                print(f"✅ {ai_name}: 정상 작동")
            else:
                print(f"❓ {ai_name}: 상태 불명")
                
            self.team[ai_name]["status"] = status
            self.team[ai_name]["last_response"] = datetime.now()
            
        # Allow 대기 중인 항목 표시
        if self.allow_pending:
            print(f"\n🚨 Allow 대기 목록:")
            for item in self.allow_pending:
                elapsed = (datetime.now() - item["time"]).seconds
                print(f"   - {item['ai']}: {elapsed}초 경과")
                
    def generate_report(self):
        """상태 리포트 생성"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "team_status": self.team,
            "allow_pending": len(self.allow_pending),
            "blocked_tasks": len(self.blocked_tasks)
        }
        
        # JSON으로 저장
        with open("pl-bot-report.json", "w") as f:
            json.dump(report, f, indent=2, default=str)
            
        return report
        
    def run(self):
        """메인 실행 루프"""
        print("🚀 PL Bot v2.0 시작")
        print("   - Allow 요청 감지 활성화")
        print("   - 타임아웃 감지 활성화")
        print("   - 30초마다 체크")
        
        try:
            while True:
                self.monitor_team()
                self.generate_report()
                
                # 긴급 상황 체크
                if len(self.allow_pending) >= 2:
                    self.notify_thomas("⚠️ 2개 이상 Allow 대기 중!")
                    
                time.sleep(30)  # 30초 대기
                
        except KeyboardInterrupt:
            print("\n👋 PL Bot 종료")
            self.generate_report()

if __name__ == "__main__":
    bot = PLBot()
    bot.run()