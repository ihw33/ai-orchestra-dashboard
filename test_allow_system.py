#!/usr/bin/env python3
"""
Allow 요청 시스템 테스트 프로토타입
테스트 목적: Allow 요청 감지 → PM Claude 알림 → 자동 응답
"""

import re
import time
import subprocess
from datetime import datetime
from typing import Tuple, Optional

class AllowRequestTest:
    def __init__(self):
        # 테스트용 간단한 패턴
        self.safe_commands = [
            'npm install', 'npm run', 'git status', 'git diff',
            'ls', 'pwd', 'cat', 'gh issue list'
        ]
        
        self.dangerous_commands = [
            'rm -rf', 'sudo', 'chmod 777', 'export PATH'
        ]
        
        print("🧪 Allow 요청 테스트 시스템 시작")
        print("-" * 50)
    
    def analyze_command(self, command: str) -> Tuple[str, int]:
        """명령어 분석 (테스트용 간단 버전)"""
        cmd_lower = command.lower().strip()
        
        # 안전한 명령 체크
        for safe in self.safe_commands:
            if cmd_lower.startswith(safe):
                return "LOW", 1
        
        # 위험한 명령 체크
        for danger in self.dangerous_commands:
            if danger in cmd_lower:
                return "HIGH", 2
        
        # 나머지는 검토 필요
        return "MEDIUM", 3
    
    def create_test_message(self, cli_name: str, command: str) -> str:
        """테스트용 Allow 요청 메시지 생성"""
        risk_level, suggested = self.analyze_command(command)
        
        message = f"""
[ALLOW_REQUEST]
FROM: {cli_name}
TAB: test-tab
COMMAND: {command}
RISK_LEVEL: {risk_level}
SUGGESTED_ACTION: {suggested}
TIME: {datetime.now().strftime('%H:%M:%S')}
[/ALLOW_REQUEST]
"""
        return message, risk_level, suggested
    
    def simulate_pm_response(self, risk_level: str, suggested: int) -> str:
        """PM Claude 응답 시뮬레이션"""
        if risk_level == "LOW":
            return f"✅ 자동 승인 (1) - 안전한 명령"
        elif risk_level == "HIGH":
            return f"🚫 자동 거부 (2) - 위험한 명령"
        else:
            return f"⚠️ 검토 필요 (3) - 컨텍스트 확인"

def run_test():
    """테스트 실행"""
    tester = AllowRequestTest()
    
    # 테스트 케이스들
    test_cases = [
        ("Gemini", "npm install axios"),
        ("Codex", "git status"),
        ("Claude", "rm -rf node_modules"),
        ("Gemini", "sudo apt-get update"),
        ("Codex", "git push origin main"),
        ("Claude", "python script.py"),
    ]
    
    print("\n📋 테스트 케이스 실행:\n")
    
    for cli_name, command in test_cases:
        print(f"테스트: {cli_name} → {command}")
        message, risk, action = tester.create_test_message(cli_name, command)
        
        # 메시지 출력
        print(f"  위험도: {risk}")
        print(f"  제안: {action}")
        
        # PM 응답 시뮬레이션
        response = tester.simulate_pm_response(risk, action)
        print(f"  PM 응답: {response}")
        print("-" * 50)
        
        time.sleep(0.5)  # 가독성을 위한 딜레이
    
    print("\n✅ 테스트 완료!")
    print("\n다음 단계:")
    print("1. 실제 iTerm2 세션 모니터링 추가")
    print("2. PM Claude 프롬프트에 실제 메시지 전송")
    print("3. 응답 자동 입력 구현")

if __name__ == "__main__":
    run_test()