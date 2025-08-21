#!/usr/bin/env python3
"""
iTerm2 세션 상태 관리 및 복구 시스템
"""

import subprocess
import time
import json
from enum import Enum
from typing import Dict, Optional, Tuple

class SessionState(Enum):
    READY = "ready"
    BUSY = "busy"
    PROCESSING = "processing"
    THINKING = "thinking"
    PAUSED = "paused"
    AUTH_REQUIRED = "auth_required"
    ERROR = "error"
    UNKNOWN = "unknown"

class SessionStateManager:
    """세션 상태 관리 및 복구"""
    
    def __init__(self):
        self.recovery_strategies = {
            SessionState.BUSY: self._handle_busy,
            SessionState.PROCESSING: self._handle_processing,
            SessionState.THINKING: self._handle_thinking,
            SessionState.PAUSED: self._handle_paused,
            SessionState.AUTH_REQUIRED: self._handle_auth,
            SessionState.ERROR: self._handle_error,
            SessionState.UNKNOWN: self._handle_unknown
        }
    
    def check_and_prepare_session(self, tab: int, session: int) -> Tuple[bool, str]:
        """세션 상태를 확인하고 메시지 수신 가능하도록 준비"""
        
        # 1. 현재 상태 확인
        state, details = self._check_session_state(tab, session)
        
        # 2. Ready 상태면 바로 OK
        if state == SessionState.READY:
            return True, "Session is ready to receive messages"
        
        # 3. 복구 전략 실행
        if state in self.recovery_strategies:
            success, message = self.recovery_strategies[state](tab, session, details)
            if success:
                # 복구 후 다시 확인
                time.sleep(1)
                new_state, _ = self._check_session_state(tab, session)
                if new_state == SessionState.READY:
                    return True, f"Session recovered: {message}"
            return False, f"Recovery failed: {message}"
        
        return False, f"Unknown state: {state}"
    
    def _handle_busy(self, tab: int, session: int, details: dict) -> Tuple[bool, str]:
        """Busy 상태 처리 - Ctrl+C 전송"""
        print(f"Session is busy. Attempting to interrupt...")
        
        # Ctrl+C 전송
        self._send_control_key(tab, session, "c")
        time.sleep(1)
        
        # 상태 재확인
        state, _ = self._check_session_state(tab, session)
        if state == SessionState.READY:
            return True, "Successfully interrupted busy session"
        
        # 두 번째 시도
        self._send_control_key(tab, session, "c")
        time.sleep(1)
        
        state, _ = self._check_session_state(tab, session)
        return state == SessionState.READY, "Double interrupt attempted"
    
    def _handle_processing(self, tab: int, session: int, details: dict) -> Tuple[bool, str]:
        """Processing 상태 처리 - 잠시 대기"""
        print("Session is processing. Waiting...")
        
        # 최대 30초 대기
        for i in range(30):
            time.sleep(1)
            state, _ = self._check_session_state(tab, session)
            if state == SessionState.READY:
                return True, f"Processing completed after {i+1} seconds"
        
        # 30초 후에도 처리 중이면 interrupt
        return self._handle_busy(tab, session, details)
    
    def _handle_thinking(self, tab: int, session: int, details: dict) -> Tuple[bool, str]:
        """AI Thinking 상태 처리 - 대기"""
        print("AI is thinking. Please wait...")
        
        # 최대 60초 대기 (AI 응답은 시간이 걸릴 수 있음)
        for i in range(60):
            time.sleep(2)
            state, _ = self._check_session_state(tab, session)
            if state == SessionState.READY:
                return True, f"AI finished thinking after {(i+1)*2} seconds"
        
        return False, "AI thinking timeout"
    
    def _handle_paused(self, tab: int, session: int, details: dict) -> Tuple[bool, str]:
        """Paused 상태 처리 - 스페이스나 엔터 전송"""
        print("Session is paused. Sending continuation...")
        
        # 엔터 전송
        self._send_key(tab, session, "return")
        time.sleep(1)
        
        state, _ = self._check_session_state(tab, session)
        if state == SessionState.READY:
            return True, "Resumed from pause"
        
        # 스페이스 시도
        self._send_key(tab, session, "space")
        time.sleep(1)
        
        state, _ = self._check_session_state(tab, session)
        return state == SessionState.READY, "Attempted space/enter to resume"
    
    def _handle_auth(self, tab: int, session: int, details: dict) -> Tuple[bool, str]:
        """인증 필요 상태 처리"""
        print("Authentication required. Cannot proceed automatically.")
        return False, "Manual authentication required"
    
    def _handle_error(self, tab: int, session: int, details: dict) -> Tuple[bool, str]:
        """에러 상태 처리"""
        print("Session in error state. Attempting recovery...")
        
        # clear 명령어 전송
        self._send_text(tab, session, "clear")
        time.sleep(1)
        
        state, _ = self._check_session_state(tab, session)
        return state == SessionState.READY, "Attempted clear command"
    
    def _handle_unknown(self, tab: int, session: int, details: dict) -> Tuple[bool, str]:
        """알 수 없는 상태 처리"""
        print("Unknown session state. Sending test command...")
        
        # 엔터 전송해보기
        self._send_key(tab, session, "return")
        time.sleep(1)
        
        state, _ = self._check_session_state(tab, session)
        if state == SessionState.READY:
            return True, "Session responded to enter key"
        
        # echo 테스트
        self._send_text(tab, session, "echo 'test'")
        time.sleep(1)
        
        state, _ = self._check_session_state(tab, session)
        return state == SessionState.READY, "Attempted echo test"
    
    def _check_session_state(self, tab: int, session: int) -> Tuple[SessionState, dict]:
        """AppleScript를 사용하여 세션 상태 확인"""
        script = f'''
        tell application "iTerm"
            tell current window
                tell tab {tab}
                    tell session {session}
                        set sessionText to contents
                        set lastLine to paragraph -1 of sessionText
                        return lastLine
                    end tell
                end tell
            end tell
        end tell
        '''
        
        try:
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True,
                timeout=5
            )
            last_line = result.stdout.strip()
            
            # 상태 판단
            if ">" in last_line or "$" in last_line or "%" in last_line:
                return SessionState.READY, {"last_line": last_line}
            elif "..." in last_line:
                return SessionState.PROCESSING, {"last_line": last_line}
            elif "Thinking" in last_line:
                return SessionState.THINKING, {"last_line": last_line}
            elif "Press" in last_line and "continue" in last_line:
                return SessionState.PAUSED, {"last_line": last_line}
            elif "Password:" in last_line:
                return SessionState.AUTH_REQUIRED, {"last_line": last_line}
            elif not last_line:
                return SessionState.UNKNOWN, {"last_line": "(empty)"}
            else:
                return SessionState.BUSY, {"last_line": last_line}
                
        except Exception as e:
            return SessionState.ERROR, {"error": str(e)}
    
    def _send_text(self, tab: int, session: int, text: str):
        """텍스트 전송"""
        script = f'''
        tell application "iTerm"
            tell current window
                tell tab {tab}
                    tell session {session}
                        write text "{text}"
                    end tell
                end tell
            end tell
        end tell
        '''
        subprocess.run(['osascript', '-e', script], capture_output=True)
    
    def _send_key(self, tab: int, session: int, key: str):
        """특수 키 전송"""
        script = f'''
        tell application "System Events"
            tell process "iTerm2"
                keystroke {key}
            end tell
        end tell
        '''
        subprocess.run(['osascript', '-e', script], capture_output=True)
    
    def _send_control_key(self, tab: int, session: int, key: str):
        """Control + 키 전송"""
        script = f'''
        tell application "System Events"
            tell process "iTerm2"
                keystroke "{key}" using control down
            end tell
        end tell
        '''
        subprocess.run(['osascript', '-e', script], capture_output=True)


# 사용 예시
if __name__ == "__main__":
    manager = SessionStateManager()
    
    # Tab 1, Session 1 체크 및 준비
    ready, message = manager.check_and_prepare_session(1, 1)
    
    if ready:
        print("✅ Session is ready!")
        # 메시지 전송 로직
    else:
        print(f"❌ Session not ready: {message}")
