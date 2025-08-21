#!/usr/bin/env python3
"""
Simple PL Bot - AI 팀 모니터링
"""
import subprocess
import time
import json
from datetime import datetime

class SimplePLBot:
    def __init__(self):
        self.sessions = {
            "ORCH_CLAUDE": {"tab": 4, "session": 1, "status": "working", "task": "#53"},
            "ORCH_GEMINI": {"tab": 4, "session": 3, "status": "starting", "task": "#46"},
            "ORCH_CODEX": {"tab": 4, "session": 4, "status": "working", "task": "#45"}
        }
        
    def check_github_comments(self, issue_number):
        """GitHub Issue 댓글 확인"""
        cmd = f"gh issue view {issue_number} -R ihw33/ai-orchestra-dashboard --json comments --jq '.comments[-1].body'"
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.stdout.strip()
        except:
            return None
    
    def send_auto_enter(self, tab, session):
        """자동 엔터키 전송"""
        script = f'''
        tell application "iTerm2"
            tell current window
                tell tab {tab}
                    tell session {session}
                        tell application "System Events"
                            key code 36
                        end tell
                    end tell
                end tell
            end tell
        end tell
        '''
        subprocess.run(['osascript', '-e', script])
    
    def monitor_once(self):
        """1회 모니터링"""
        print(f"\n🤖 PL Bot 모니터링 - {datetime.now().strftime('%H:%M:%S')}")
        print("-" * 50)
        
        for name, info in self.sessions.items():
            # GitHub 댓글 체크
            last_comment = self.check_github_comments(info['task'])
            
            print(f"{name}:")
            print(f"  📋 Task: {info['task']}")
            print(f"  🔄 Status: {info['status']}")
            if last_comment:
                print(f"  💬 Last: {last_comment[:50]}...")
            print()
    
    def run(self, interval=60):
        """지속 모니터링"""
        print("🚀 PL Bot 시작 - AI 팀 모니터링")
        while True:
            self.monitor_once()
            time.sleep(interval)

if __name__ == "__main__":
    bot = SimplePLBot()
    bot.run(interval=60)  # 1분마다 체크