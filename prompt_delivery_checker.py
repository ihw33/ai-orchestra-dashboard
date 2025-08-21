#!/usr/bin/env python3
"""
프롬프트 전송 확인 시스템
메시지가 제대로 전달되고 실행되었는지 확인
"""

import time
import subprocess
import hashlib
from typing import Tuple, Optional
from datetime import datetime

class PromptDeliveryChecker:
    def __init__(self):
        self.last_prompts = {}  # 세션별 마지막 프롬프트 저장
        self.delivery_log = []
        
    def send_prompt_with_check(self, session_id: str, message: str) -> Tuple[bool, str]:
        """
        프롬프트 전송 후 전달 확인
        """
        # 1. 메시지 해시 생성 (중복 확인용)
        msg_hash = hashlib.md5(message.encode()).hexdigest()[:8]
        
        # 2. 세션 상태 확인 (전송 전)
        before_state = self.get_session_state(session_id)
        
        # 3. 프롬프트 전송
        success = self.send_to_session(session_id, message)
        
        if not success:
            return False, "❌ 세션을 찾을 수 없음"
        
        # 4. 잠시 대기 (처리 시간)
        time.sleep(0.5)
        
        # 5. 세션 상태 확인 (전송 후)
        after_state = self.get_session_state(session_id)
        
        # 6. 전달 확인
        delivery_status = self.verify_delivery(
            session_id, before_state, after_state, message
        )
        
        # 7. 로그 기록
        self.log_delivery(session_id, message, msg_hash, delivery_status)
        
        return delivery_status
    
    def get_session_state(self, session_id: str) -> dict:
        """세션 상태 가져오기"""
        script = f'''
        tell application "iTerm2"
            tell current window
                repeat with aTab in tabs
                    repeat with aSession in sessions of aTab
                        if name of aSession is "{session_id}" then
                            set sessionState to {{}}
                            set sessionState to sessionState & "prompt_ready:" & (is at shell prompt of aSession)
                            set sessionState to sessionState & ",processing:" & (is processing of aSession)
                            set sessionState to sessionState & ",session_id:" & (unique id of aSession)
                            return sessionState as string
                        end if
                    end repeat
                end repeat
            end tell
        end tell
        return "not_found"
        '''
        
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True
        )
        
        state_str = result.stdout.strip()
        if state_str == "not_found":
            return {"found": False}
        
        # 상태 파싱
        state = {"found": True}
        for item in state_str.split(","):
            if ":" in item:
                key, value = item.split(":", 1)
                state[key] = value.lower() == "true" if value in ["true", "false"] else value
        
        return state
    
    def send_to_session(self, session_id: str, message: str) -> bool:
        """세션에 메시지 전송"""
        # 메시지에서 따옴표 이스케이프
        escaped_message = message.replace('"', '\\"').replace('\n', '\\n')
        
        script = f'''
        tell application "iTerm2"
            tell current window
                repeat with aTab in tabs
                    repeat with aSession in sessions of aTab
                        if name of aSession is "{session_id}" then
                            tell aSession
                                write text "{escaped_message}"
                            end tell
                            return "sent"
                        end if
                    end repeat
                end repeat
            end tell
        end tell
        return "not_found"
        '''
        
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True
        )
        
        return result.stdout.strip() == "sent"
    
    def verify_delivery(self, session_id: str, before: dict, after: dict, message: str) -> Tuple[bool, str]:
        """전달 확인"""
        if not after.get("found"):
            return False, "세션을 찾을 수 없음"
        
        # 상태 변화 체크
        checks = {
            "세션_찾음": after.get("found", False),
            "프롬프트_전송됨": before.get("prompt_ready", False) != after.get("prompt_ready", True),
            "처리_시작됨": after.get("processing", False),
            "메시지_길이_적절": len(message) < 10000
        }
        
        # 전달 성공 판단
        if checks["세션_찾음"] and (checks["프롬프트_전송됨"] or checks["처리_시작됨"]):
            return True, "✅ 전달 성공"
        elif checks["세션_찾음"] and checks["메시지_길이_적절"]:
            return True, "⚠️ 전달됨 (확인 필요)"
        else:
            return False, "❌ 전달 실패"
    
    def log_delivery(self, session_id: str, message: str, msg_hash: str, status: Tuple[bool, str]):
        """전달 로그 기록"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "message_preview": message[:50] + "..." if len(message) > 50 else message,
            "hash": msg_hash,
            "success": status[0],
            "status": status[1]
        }
        
        self.delivery_log.append(log_entry)
        
        # 콘솔 출력
        print(f"\n📤 프롬프트 전송: {session_id}")
        print(f"  메시지: {log_entry['message_preview']}")
        print(f"  상태: {status[1]}")
        print(f"  시간: {log_entry['timestamp']}")
    
    def check_recent_deliveries(self) -> list:
        """최근 전달 내역 확인"""
        return self.delivery_log[-10:] if self.delivery_log else []
    
    def retry_failed_delivery(self, session_id: str, message: str, max_retries: int = 3) -> bool:
        """실패한 전송 재시도"""
        for attempt in range(max_retries):
            print(f"\n🔄 재시도 {attempt + 1}/{max_retries}...")
            success, status = self.send_prompt_with_check(session_id, message)
            
            if success:
                print(f"✅ 재시도 성공!")
                return True
            
            time.sleep(1)  # 재시도 간격
        
        print(f"❌ {max_retries}회 재시도 실패")
        return False

def test_delivery_system():
    """테스트 실행"""
    checker = PromptDeliveryChecker()
    
    print("🧪 프롬프트 전달 확인 시스템 테스트")
    print("=" * 60)
    
    # 테스트 케이스
    test_cases = [
        ("ORCH_GEMINI", "테스트 메시지입니다"),
        ("ENGINE_CODEX", "npm install 실행해줘"),
        ("IWL_PM", "Issue #27 상태 확인"),
        ("INVALID_SESSION", "잘못된 세션 테스트")
    ]
    
    for session_id, message in test_cases:
        print(f"\n테스트: {session_id}")
        success, status = checker.send_prompt_with_check(session_id, message)
        
        if not success and session_id != "INVALID_SESSION":
            # 실패 시 재시도
            checker.retry_failed_delivery(session_id, message, max_retries=2)
    
    # 전달 내역 확인
    print("\n" + "=" * 60)
    print("📊 전달 내역:")
    for entry in checker.check_recent_deliveries():
        print(f"  [{entry['hash']}] {entry['session_id']}: {entry['status']}")

if __name__ == "__main__":
    test_delivery_system()