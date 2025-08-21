#!/usr/bin/env python3
"""
iTerm2 세션 ID 관리 시스템
각 세션에 고유 ID를 부여하고 추적
"""

import json
import subprocess
from datetime import datetime
from typing import Dict, List, Optional

class ITermSessionManager:
    def __init__(self):
        self.session_map = {}
        self.load_session_map()
        
    def load_session_map(self):
        """기존 세션 맵 로드"""
        try:
            with open('iterm_sessions.json', 'r') as f:
                self.session_map = json.load(f)
        except FileNotFoundError:
            self.session_map = self.create_default_map()
            self.save_session_map()
    
    def create_default_map(self) -> Dict:
        """기본 세션 맵 생성"""
        return {
            "tabs": {
                "1": {
                    "name": "🏠 Home",
                    "sessions": {
                        "1-1": {"id": "HOME_MAIN", "cli": "Terminal", "role": "General"},
                        "1-2": {"id": "HOME_MONITOR", "cli": "Monitor", "role": "Monitoring"}
                    }
                },
                "2": {
                    "name": "🤖 AI Engine",
                    "sessions": {
                        "2-1": {"id": "ENGINE_GEMINI", "cli": "Gemini", "role": "Data Processing"},
                        "2-2": {"id": "ENGINE_CODEX", "cli": "Codex", "role": "Backend Dev"},
                        "2-3": {"id": "ENGINE_TERMINAL", "cli": "Terminal", "role": "Testing"}
                    }
                },
                "3": {
                    "name": "📚 IWL Project",
                    "sessions": {
                        "3-1": {"id": "IWL_PM", "cli": "PM Claude", "role": "Project Management"},
                        "3-2": {"id": "IWL_CURSOR", "cli": "Cursor", "role": "Frontend Dev"},
                        "3-3": {"id": "IWL_GEMINI", "cli": "Gemini", "role": "Content"},
                        "3-4": {"id": "IWL_CODEX", "cli": "Codex", "role": "API"}
                    }
                },
                "4": {
                    "name": "🎼 Orchestra Board",
                    "sessions": {
                        "4-1": {"id": "ORCH_CLAUDE", "cli": "Claude", "role": "Backend"},
                        "4-2": {"id": "ORCH_TERMINAL", "cli": "Terminal", "role": "Testing"},
                        "4-3": {"id": "ORCH_GEMINI", "cli": "Gemini", "role": "Data"},
                        "4-4": {"id": "ORCH_CODEX", "cli": "Codex", "role": "Backend"}
                    }
                }
            },
            "updated": datetime.now().isoformat()
        }
    
    def save_session_map(self):
        """세션 맵 저장"""
        with open('iterm_sessions.json', 'w') as f:
            json.dump(self.session_map, f, indent=2)
    
    def get_session_by_id(self, session_id: str) -> Optional[Dict]:
        """ID로 세션 정보 찾기"""
        for tab_num, tab_info in self.session_map["tabs"].items():
            for session_num, session_info in tab_info["sessions"].items():
                if session_info["id"] == session_id:
                    return {
                        "tab": tab_num,
                        "session": session_num,
                        "tab_name": tab_info["name"],
                        **session_info
                    }
        return None
    
    def get_session_by_position(self, tab: str, session: str) -> Optional[Dict]:
        """위치로 세션 정보 찾기"""
        try:
            tab_info = self.session_map["tabs"][tab]
            session_info = tab_info["sessions"][f"{tab}-{session}"]
            return {
                "tab": tab,
                "session": f"{tab}-{session}",
                "tab_name": tab_info["name"],
                **session_info
            }
        except KeyError:
            return None
    
    def list_all_sessions(self):
        """모든 세션 목록 출력"""
        print("\n🗂️ iTerm2 세션 맵")
        print("=" * 60)
        
        for tab_num, tab_info in self.session_map["tabs"].items():
            print(f"\n📑 Tab {tab_num}: {tab_info['name']}")
            print("-" * 40)
            
            for session_num, session_info in tab_info["sessions"].items():
                print(f"  [{session_info['id']:15}] {session_num:5} | {session_info['cli']:10} | {session_info['role']}")
        
        print("\n" + "=" * 60)
        print(f"마지막 업데이트: {self.session_map.get('updated', 'Unknown')}")
    
    def find_cli(self, cli_name: str) -> List[Dict]:
        """특정 CLI 찾기"""
        results = []
        for tab_num, tab_info in self.session_map["tabs"].items():
            for session_num, session_info in tab_info["sessions"].items():
                if cli_name.lower() in session_info["cli"].lower():
                    results.append({
                        "tab": tab_num,
                        "session": session_num,
                        "tab_name": tab_info["name"],
                        **session_info
                    })
        return results
    
    def update_session_status(self, session_id: str, status: str):
        """세션 상태 업데이트"""
        session = self.get_session_by_id(session_id)
        if session:
            tab = session["tab"]
            session_num = session["session"]
            self.session_map["tabs"][tab]["sessions"][session_num]["status"] = status
            self.session_map["updated"] = datetime.now().isoformat()
            self.save_session_map()
            print(f"✅ {session_id} 상태 업데이트: {status}")
        else:
            print(f"❌ 세션 ID를 찾을 수 없음: {session_id}")

def main():
    """테스트 실행"""
    manager = ITermSessionManager()
    
    print("🔧 iTerm2 세션 ID 관리 시스템")
    print("=" * 60)
    
    # 1. 전체 세션 목록
    manager.list_all_sessions()
    
    # 2. ID로 세션 찾기
    print("\n🔍 테스트: ID로 세션 찾기")
    test_id = "ORCH_GEMINI"
    result = manager.get_session_by_id(test_id)
    if result:
        print(f"  {test_id} → Tab {result['tab']}, Session {result['session']} ({result['cli']})")
    
    # 3. CLI 이름으로 찾기
    print("\n🔍 테스트: Gemini CLI 찾기")
    gemini_sessions = manager.find_cli("Gemini")
    for session in gemini_sessions:
        print(f"  {session['id']} → Tab {session['tab']}-{session['session']}")
    
    # 4. 위치로 찾기
    print("\n🔍 테스트: Tab 4, Session 3 찾기")
    result = manager.get_session_by_position("4", "3")
    if result:
        print(f"  위치 4-3 → {result['id']} ({result['cli']})")

if __name__ == "__main__":
    main()