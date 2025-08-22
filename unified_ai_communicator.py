#!/usr/bin/env python3
"""
통합 AI 통신 시스템 - 완성 버전
이전 작업 검토 결과를 바탕으로 구축
"""
import subprocess
import time
import json
from typing import Dict, Optional, List
from datetime import datetime
from pathlib import Path

class UnifiedAICommunicator:
    """모든 AI와 통신하는 통합 시스템"""
    
    def __init__(self):
        # iTerm2 탭 매핑 (검증된 설정)
        self.tab_mapping = {
            "Gemini": 2,
            "Codex": 3, 
            "Claude": 4,  # Tab 4 Claude
            "Cursor": 5
        }
        
        # 통신 로그
        self.communication_log = []
        self.success_count = 0
        self.failure_count = 0
        
    def send_to_ai(self, ai_name: str, message: str, require_enter: bool = True) -> Dict:
        """
        AI에게 메시지 전송 (검증된 방법)
        """
        result = {
            "ai": ai_name,
            "message": message[:100] + "..." if len(message) > 100 else message,
            "timestamp": datetime.now().isoformat(),
            "success": False,
            "method": None,
            "error": None
        }
        
        # Tab 번호 확인
        tab_number = self.tab_mapping.get(ai_name)
        if not tab_number:
            result["error"] = f"Unknown AI: {ai_name}"
            self._log_communication(result)
            return result
            
        # 메시지 전송 시도
        try:
            # 방법 1: write text (가장 안정적)
            success = self._send_via_write_text(tab_number, message, require_enter)
            
            if not success:
                # 방법 2: keystroke 사용 (백업)
                success = self._send_via_keystroke(tab_number, message, require_enter)
                
            result["success"] = success
            result["method"] = "write_text" if success else "failed"
            
            if success:
                self.success_count += 1
                print(f"✅ {ai_name}: 메시지 전송 성공")
            else:
                self.failure_count += 1
                print(f"❌ {ai_name}: 메시지 전송 실패")
                
        except Exception as e:
            result["error"] = str(e)
            self.failure_count += 1
            print(f"❌ {ai_name}: 에러 발생 - {e}")
            
        self._log_communication(result)
        return result
        
    def _send_via_write_text(self, tab_number: int, message: str, require_enter: bool) -> bool:
        """write text 방식으로 전송 (추천)"""
        # 메시지에 쌍따옴표가 있으면 이스케이프
        escaped_message = message.replace('"', '\\"')
        
        script = f'''
        tell application "iTerm2"
            tell current window
                tell tab {tab_number}
                    select
                    tell current session
                        write text "{escaped_message}"
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
            
            # write text는 자동으로 엔터를 포함
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            return False
        except Exception:
            return False
            
    def _send_via_keystroke(self, tab_number: int, message: str, require_enter: bool) -> bool:
        """keystroke 방식으로 전송 (백업)"""
        script = f'''
        tell application "iTerm2"
            activate
            tell current window
                tell tab {tab_number}
                    select
                end tell
            end tell
        end tell
        
        tell application "System Events"
            keystroke "{message}"
            {"key code 36" if require_enter else "-- no enter"}
        end tell
        '''
        
        try:
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
            
        except:
            return False
            
    def broadcast_message(self, message: str, exclude: List[str] = None) -> Dict:
        """모든 AI에게 동시 메시지 전송"""
        exclude = exclude or []
        results = {}
        
        for ai_name in self.tab_mapping.keys():
            if ai_name not in exclude:
                results[ai_name] = self.send_to_ai(ai_name, message)
                time.sleep(0.5)  # 과부하 방지
                
        return results
        
    def send_task_assignment(self, ai_name: str, task_type: str, description: str, priority: str = "Medium") -> bool:
        """표준화된 작업 할당 메시지"""
        message = f"""
# 🎯 작업 할당
**담당**: {ai_name}
**유형**: {task_type}
**우선순위**: {priority}
**설명**: {description}
**시작 시간**: {datetime.now().strftime('%H:%M:%S')}

작업을 시작하면 '#START'로, 완료하면 '#DONE'으로 응답해주세요.
""".strip()
        
        result = self.send_to_ai(ai_name, message)
        return result["success"]
        
    def check_ai_status(self, ai_name: str) -> bool:
        """AI 상태 확인 (ping)"""
        message = f"# STATUS CHECK - {datetime.now().strftime('%H:%M:%S')}"
        result = self.send_to_ai(ai_name, message, require_enter=False)
        return result["success"]
        
    def _log_communication(self, result: Dict):
        """통신 로그 기록"""
        self.communication_log.append(result)
        
        # 100개 이상이면 오래된 것 삭제
        if len(self.communication_log) > 100:
            self.communication_log = self.communication_log[-100:]
            
    def get_statistics(self) -> Dict:
        """통신 통계"""
        total = self.success_count + self.failure_count
        success_rate = (self.success_count / total * 100) if total > 0 else 0
        
        return {
            "total_communications": total,
            "successful": self.success_count,
            "failed": self.failure_count,
            "success_rate": f"{success_rate:.1f}%",
            "ai_status": {
                ai: self.check_ai_status(ai) for ai in self.tab_mapping.keys()
            }
        }
        
    def save_log(self, filepath: str = "communication_log.json"):
        """로그 저장"""
        log_data = {
            "statistics": self.get_statistics(),
            "recent_communications": self.communication_log[-20:],
            "timestamp": datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(log_data, f, indent=2)
            
        print(f"📝 로그 저장: {filepath}")
        return filepath

# 테스트 함수
def test_communication():
    """통신 테스트"""
    print("\n🧪 AI 통신 시스템 테스트 시작\n")
    
    comm = UnifiedAICommunicator()
    
    # 1. 개별 AI 테스트
    print("1️⃣ 개별 AI 통신 테스트")
    test_results = {}
    
    for ai_name in ["Gemini", "Codex", "Claude", "Cursor"]:
        print(f"\n테스트: {ai_name}")
        result = comm.send_to_ai(
            ai_name, 
            f"echo '✅ {ai_name} 통신 테스트 성공'"
        )
        test_results[ai_name] = result["success"]
        time.sleep(1)
        
    # 2. 작업 할당 테스트
    print("\n2️⃣ 작업 할당 테스트")
    comm.send_task_assignment(
        "Gemini",
        "Frontend Development",
        "Dashboard 컴포넌트 개발",
        "High"
    )
    
    # 3. 브로드캐스트 테스트
    print("\n3️⃣ 브로드캐스트 테스트")
    comm.broadcast_message(
        "# 📢 전체 공지: Round 5 재시작",
        exclude=["Claude"]  # PM은 제외
    )
    
    # 4. 통계 출력
    print("\n4️⃣ 통신 통계")
    stats = comm.get_statistics()
    print(json.dumps(stats, indent=2))
    
    # 5. 로그 저장
    comm.save_log("test_communication_log.json")
    
    print("\n✅ 테스트 완료!")
    print(f"성공: {comm.success_count}, 실패: {comm.failure_count}")
    
    return test_results

if __name__ == "__main__":
    test_communication()