#!/usr/bin/env python3
"""
안전한 메시지 전송 시스템
세션 상태를 확인하고 필요시 복구 후 메시지 전송
"""

import subprocess
import time
import sys

class SafeMessageSender:
    def __init__(self):
        self.max_retries = 3
        self.retry_delay = 2
    
    def send_message_safely(self, tab, session, message, agent_name="AI"):
        """세션 상태를 확인하고 안전하게 메시지 전송"""
        
        print(f"🎯 Attempting to send message to {agent_name} (Tab {tab}, Session {session})")
        
        # 1. 먼저 세션 존재 확인
        if not self._session_exists(tab, session):
            print(f"❌ Session {session} in Tab {tab} does not exist!")
            return False
        
        # 2. 상태 확인 및 복구 시도
        for attempt in range(self.max_retries):
            print(f"\n📍 Attempt {attempt + 1}/{self.max_retries}")
            
            # 현재 상태 확인
            state = self._get_session_state(tab, session)
            print(f"   Current state: {state['status']} - {state['reason']}")
            
            if state['status'] == 'ready':
                # 메시지 전송
                print(f"✅ Session ready! Sending message...")
                self._send_text(tab, session, message)
                time.sleep(0.5)
                self._send_enter(tab, session)
                print(f"✅ Message sent successfully!")
                return True
            
            # 상태별 복구 시도
            if state['status'] == 'busy':
                print("   🔄 Session busy, sending Ctrl+C...")
                self._send_ctrl_c(tab, session)
                time.sleep(self.retry_delay)
                
            elif state['status'] == 'processing':
                print("   ⏳ Waiting for processing to complete...")
                time.sleep(5)
                
            elif state['status'] == 'thinking':
                print("   🤔 AI is thinking, waiting...")
                time.sleep(10)
                
            elif state['status'] == 'paused':
                print("   ▶️ Session paused, sending Enter...")
                self._send_enter(tab, session)
                time.sleep(self.retry_delay)
                
            elif state['status'] == 'unknown':
                print("   ❓ Unknown state, trying Enter...")
                self._send_enter(tab, session)
                time.sleep(self.retry_delay)
                
                # 여전히 unknown이면 clear 시도
                if attempt == 1:
                    print("   🧹 Trying clear command...")
                    self._send_text(tab, session, "clear")
                    time.sleep(self.retry_delay)
        
        print(f"❌ Failed to send message after {self.max_retries} attempts")
        return False
    
    def _session_exists(self, tab, session):
        """세션이 존재하는지 확인"""
        script = f'''
        tell application "iTerm"
            tell current window
                try
                    tell tab {tab}
                        tell session {session}
                            return "exists"
                        end tell
                    end tell
                on error
                    return "not exists"
                end try
            end tell
        end tell
        '''
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        return result.stdout.strip() == "exists"
    
    def _get_session_state(self, tab, session):
        """세션 상태 분석"""
        script = f'''
        tell application "iTerm"
            tell current window
                tell tab {tab}
                    tell session {session}
                        set sessionText to contents
                        set lineList to paragraphs of sessionText
                        set lineCount to count of lineList
                        
                        if lineCount > 0 then
                            set lastLine to item lineCount of lineList
                        else
                            set lastLine to ""
                        end if
                        
                        -- 최근 10줄도 가져오기 (thinking 감지용)
                        set recentText to ""
                        if lineCount > 10 then
                            repeat with i from (lineCount - 9) to lineCount
                                set recentText to recentText & item i of lineList & " "
                            end repeat
                        else
                            set recentText to sessionText
                        end if
                        
                        return lastLine & "|||" & recentText
                    end tell
                end tell
            end tell
        end tell
        '''
        
        try:
            result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=5)
            output = result.stdout.strip()
            parts = output.split("|||")
            last_line = parts[0] if parts else ""
            recent_text = parts[1] if len(parts) > 1 else ""
            
            # 상태 판단
            if ">" in last_line or "$" in last_line or "%" in last_line:
                return {"status": "ready", "reason": "Prompt detected", "last_line": last_line}
            elif "Thinking" in recent_text or "thinking" in recent_text:
                return {"status": "thinking", "reason": "AI is thinking", "last_line": last_line}
            elif "..." in last_line:
                return {"status": "processing", "reason": "Continuation prompt", "last_line": last_line}
            elif "Press" in last_line and "continue" in last_line:
                return {"status": "paused", "reason": "Waiting for input", "last_line": last_line}
            elif not last_line.strip():
                return {"status": "unknown", "reason": "Empty line", "last_line": "(empty)"}
            else:
                return {"status": "busy", "reason": "No prompt detected", "last_line": last_line}
                
        except Exception as e:
            return {"status": "error", "reason": str(e), "last_line": ""}
    
    def _send_text(self, tab, session, text):
        """텍스트 전송"""
        # 특수 문자 이스케이프
        escaped_text = text.replace('"', '\\"').replace("'", "\\'")
        script = f'''
        tell application "iTerm"
            tell current window
                tell tab {tab}
                    tell session {session}
                        write text "{escaped_text}"
                    end tell
                end tell
            end tell
        end tell
        '''
        subprocess.run(['osascript', '-e', script], capture_output=True)
    
    def _send_enter(self, tab, session):
        """엔터키 전송"""
        script = '''
        tell application "System Events"
            tell process "iTerm2"
                keystroke return
            end tell
        end tell
        '''
        subprocess.run(['osascript', '-e', script], capture_output=True)
    
    def _send_ctrl_c(self, tab, session):
        """Ctrl+C 전송"""
        script = '''
        tell application "System Events"
            tell process "iTerm2"
                keystroke "c" using control down
            end tell
        end tell
        '''
        subprocess.run(['osascript', '-e', script], capture_output=True)


# CLI 사용
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python safe_send.py <tab> <session> <message> [agent_name]")
        sys.exit(1)
    
    tab = int(sys.argv[1])
    session = int(sys.argv[2])
    message = sys.argv[3]
    agent_name = sys.argv[4] if len(sys.argv) > 4 else "AI"
    
    sender = SafeMessageSender()
    success = sender.send_message_safely(tab, session, message, agent_name)
    
    sys.exit(0 if success else 1)
