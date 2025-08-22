#!/usr/bin/env python3
"""
스마트 프롬프트 전송 시스템
엔터 확인 + 재시도 + 상태 추적
"""

import time
import subprocess
from typing import Dict, List, Tuple
from datetime import datetime
from enum import Enum

class DeliveryStatus(Enum):
    SUCCESS = "✅ 성공"
    FAILED = "❌ 실패"
    RETRY = "🔄 재시도 중"
    PENDING = "⏳ 대기 중"
    NO_ENTER = "⚠️ 엔터 미전송"

class SmartPromptSender:
    def __init__(self):
        self.session_status = {}
        self.delivery_queue = []
        self.retry_count = {}
        
    def send_prompt(self, session_id: str, message: str, require_enter: bool = True) -> Dict:
        """
        스마트 프롬프트 전송
        """
        result = {
            "session_id": session_id,
            "message": message[:50] + "..." if len(message) > 50 else message,
            "timestamp": datetime.now().isoformat(),
            "status": DeliveryStatus.PENDING,
            "details": {}
        }
        
        # 1. 세션 확인
        if not self.verify_session_exists(session_id):
            result["status"] = DeliveryStatus.FAILED
            result["details"]["error"] = "세션을 찾을 수 없음"
            return result
        
        # 2. 메시지 전송
        send_success = self.send_to_iterm(session_id, message)
        
        if not send_success:
            result["status"] = DeliveryStatus.FAILED
            result["details"]["error"] = "전송 실패"
            return result
        
        # 3. 엔터 확인 (필요한 경우)
        if require_enter:
            enter_pressed = self.verify_enter_pressed(session_id)
            
            if not enter_pressed:
                # 엔터 재전송
                self.send_enter_key(session_id)
                time.sleep(0.5)
                
                # 다시 확인
                enter_pressed = self.verify_enter_pressed(session_id)
                
                if not enter_pressed:
                    result["status"] = DeliveryStatus.NO_ENTER
                    result["details"]["warning"] = "엔터가 전송되지 않음"
                    
                    # 재시도 큐에 추가
                    self.add_to_retry_queue(session_id, message)
                    return result
        
        # 4. 성공
        result["status"] = DeliveryStatus.SUCCESS
        result["details"]["delivery_time"] = f"{time.time():.2f}s"
        
        # 상태 업데이트
        self.update_session_status(session_id, "active", message)
        
        return result
    
    def verify_session_exists(self, session_id: str) -> bool:
        """세션 존재 확인"""
        script = f'''
        tell application "iTerm2"
            tell current window
                repeat with aTab in tabs
                    repeat with aSession in sessions of aTab
                        if name of aSession is "{session_id}" then
                            return "exists"
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
        
        return result.stdout.strip() == "exists"
    
    def send_to_iterm(self, session_id: str, message: str) -> bool:
        """iTerm2 세션에 메시지 전송"""
        escaped_message = message.replace('"', '\\"').replace('\n', '\\n')
        
        script = f'''
        tell application "iTerm2"
            tell current window
                repeat with aTab in tabs
                    repeat with aSession in sessions of aTab
                        if name of aSession is "{session_id}" then
                            tell aSession to write text "{escaped_message}"
                            return "sent"
                        end if
                    end repeat
                end repeat
            end tell
        end tell
        return "failed"
        '''
        
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True
        )
        
        return result.stdout.strip() == "sent"
    
    def verify_enter_pressed(self, session_id: str) -> bool:
        """엔터가 눌렸는지 확인"""
        script = f'''
        tell application "iTerm2"
            tell current window
                repeat with aTab in tabs
                    repeat with aSession in sessions of aTab
                        if name of aSession is "{session_id}" then
                            tell aSession
                                if is processing then
                                    return "processing"
                                else if is at shell prompt then
                                    return "at_prompt"
                                else
                                    return "busy"
                                end if
                            end tell
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
        
        status = result.stdout.strip()
        # processing이나 busy면 엔터가 눌린 것
        return status in ["processing", "busy"]
    
    def send_enter_key(self, session_id: str):
        """엔터키만 전송"""
        script = f'''
        tell application "iTerm2"
            tell current window
                repeat with aTab in tabs
                    repeat with aSession in sessions of aTab
                        if name of aSession is "{session_id}" then
                            tell aSession to write text ""
                            return "sent"
                        end if
                    end repeat
                end repeat
            end tell
        end tell
        '''
        
        subprocess.run(['osascript', '-e', script])
    
    def add_to_retry_queue(self, session_id: str, message: str):
        """재시도 큐에 추가"""
        self.delivery_queue.append({
            "session_id": session_id,
            "message": message,
            "retry_count": self.retry_count.get(f"{session_id}_{message}", 0) + 1,
            "added_at": datetime.now()
        })
        
        self.retry_count[f"{session_id}_{message}"] = self.retry_count.get(f"{session_id}_{message}", 0) + 1
    
    def process_retry_queue(self, max_retries: int = 3):
        """재시도 큐 처리"""
        while self.delivery_queue:
            item = self.delivery_queue.pop(0)
            
            if item["retry_count"] > max_retries:
                print(f"❌ 최대 재시도 횟수 초과: {item['session_id']}")
                continue
            
            print(f"🔄 재시도 {item['retry_count']}/{max_retries}: {item['session_id']}")
            result = self.send_prompt(item["session_id"], item["message"])
            
            if result["status"] != DeliveryStatus.SUCCESS:
                # 다시 큐에 추가
                self.add_to_retry_queue(item["session_id"], item["message"])
    
    def update_session_status(self, session_id: str, status: str, last_message: str):
        """세션 상태 업데이트"""
        self.session_status[session_id] = {
            "status": status,
            "last_message": last_message,
            "updated_at": datetime.now().isoformat()
        }
    
    def get_all_status(self) -> Dict:
        """모든 세션 상태 조회"""
        return self.session_status

def test_smart_sender():
    """테스트 실행"""
    sender = SmartPromptSender()
    
    print("🚀 스마트 프롬프트 전송 테스트")
    print("=" * 60)
    
    # 테스트 메시지들
    test_messages = [
        ("ORCH_TERMINAL", "ls -la", True),
        ("ENGINE_GEMINI", "Issue #27 진행 상황 확인해줘", False),
        ("IWL_PM", "PR #37 리뷰 계속 진행", False),
    ]
    
    results = []
    for session_id, message, require_enter in test_messages:
        print(f"\n📤 전송: {session_id}")
        print(f"   메시지: {message}")
        
        result = sender.send_prompt(session_id, message, require_enter)
        results.append(result)
        
        print(f"   상태: {result['status'].value}")
        if "error" in result["details"]:
            print(f"   에러: {result['details']['error']}")
        elif "warning" in result["details"]:
            print(f"   경고: {result['details']['warning']}")
        
        time.sleep(1)
    
    # 재시도 큐 처리
    if sender.delivery_queue:
        print("\n" + "=" * 60)
        print("📋 재시도 큐 처리 중...")
        sender.process_retry_queue()
    
    # 최종 상태
    print("\n" + "=" * 60)
    print("📊 세션 상태:")
    for sid, status in sender.get_all_status().items():
        print(f"  {sid}: {status['status']} - {status['last_message'][:30]}...")

if __name__ == "__main__":
    test_smart_sender()