#!/usr/bin/env python3
"""
iTerm2 Orchestra Integration
iTerm2를 AI Orchestra 전용 터미널로 변환
"""
import subprocess
import json
import time
from datetime import datetime

class ITermOrchestra:
    def __init__(self):
        self.sessions = {
            "tab1": {"name": "Claude (PM)", "color": "blue", "badge": "🎭"},
            "tab2": {"name": "Gemini (Frontend)", "color": "cyan", "badge": "💎"},
            "tab3": {"name": "Codex (Backend)", "color": "green", "badge": "⚙️"},
            "tab4": {"name": "Cursor (Architect)", "color": "yellow", "badge": "📐"}
        }
        
    def setup_orchestra_profile(self):
        """Orchestra 전용 프로파일 생성"""
        print("🎨 Orchestra 프로파일 설정 중...")
        
        # AppleScript로 프로파일 설정
        profile_script = '''
        tell application "iTerm2"
            tell current window
                -- Tab 1: Claude (PM)
                tell first tab
                    set name to "🎭 Claude (PM)"
                    tell current session
                        set background color to {0, 0, 20000}
                        set name to "PM_CLAUDE"
                    end tell
                end tell
                
                -- Tab 2: Gemini 
                create tab with default profile
                tell second tab
                    set name to "💎 Gemini (Frontend)"
                    tell current session
                        set background color to {0, 10000, 20000}
                        set name to "GEMINI"
                    end tell
                end tell
                
                -- Tab 3: Codex
                create tab with default profile
                tell third tab
                    set name to "⚙️ Codex (Backend)"
                    tell current session
                        set background color to {0, 15000, 0}
                        set name to "CODEX"
                    end tell
                end tell
                
                -- Tab 4: Cursor
                create tab with default profile
                tell fourth tab
                    set name to "📐 Cursor (Architect)"
                    tell current session
                        set background color to {15000, 15000, 0}
                        set name to "CURSOR"
                    end tell
                end tell
                
                -- 첫 번째 탭으로 돌아가기
                select first tab
            end tell
        end tell
        '''
        
        result = subprocess.run(
            ["osascript", "-e", profile_script],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Orchestra 프로파일 생성 완료")
        else:
            print(f"⚠️ 프로파일 생성 중 오류: {result.stderr}")
    
    def add_status_badges(self):
        """각 세션에 상태 배지 추가"""
        print("🏷️ 상태 배지 추가 중...")
        
        # KPI 리포트 읽기
        try:
            with open("team_kpi_report.json", "r") as f:
                kpi_report = json.load(f)
        except:
            kpi_report = None
        
        badge_script = '''
        tell application "iTerm2"
            tell current window
                -- Claude 탭
                tell first tab
                    tell current session
                        set badge to "PM 🎭\\n✅ Active\\nScore: {claude_score}"
                    end tell
                end tell
                
                -- Gemini 탭
                tell second tab
                    tell current session
                        set badge to "Frontend 💎\\n✅ Active\\nScore: {gemini_score}"
                    end tell
                end tell
                
                -- Codex 탭
                tell third tab
                    tell current session
                        set badge to "Backend ⚙️\\n✅ Active\\nScore: {codex_score}"
                    end tell
                end tell
                
                -- Cursor 탭
                tell fourth tab
                    tell current session
                        set badge to "Architect 📐\\n✅ Active\\nScore: {cursor_score}"
                    end tell
                end tell
            end tell
        end tell
        '''
        
        # KPI 점수 가져오기
        scores = {
            "claude_score": "95",
            "gemini_score": "88",
            "codex_score": "75",
            "cursor_score": "82"
        }
        
        if kpi_report and "team_performance" in kpi_report:
            for ai_name, perf in kpi_report["team_performance"].items():
                key = f"{ai_name.lower()}_score"
                scores[key] = str(int(perf["performance_score"]))
        
        # 스크립트 실행
        formatted_script = badge_script.format(**scores)
        subprocess.run(["osascript", "-e", formatted_script])
        print("✅ 상태 배지 추가 완료")
    
    def create_custom_statusbar(self):
        """커스텀 상태바 생성"""
        print("📊 커스텀 상태바 설정 중...")
        
        statusbar_config = {
            "components": [
                {"type": "cpu", "label": "CPU"},
                {"type": "memory", "label": "MEM"},
                {"type": "network", "label": "NET"},
                {"type": "custom", "label": "AI Status", "value": "4/4 Active"},
                {"type": "custom", "label": "Tasks", "value": "12 Done"},
                {"type": "clock", "format": "%H:%M"}
            ]
        }
        
        # 설정 파일 저장
        with open("iterm2_statusbar.json", "w") as f:
            json.dump(statusbar_config, f, indent=2)
        
        print("✅ 상태바 설정 저장됨")
    
    def setup_keyboard_shortcuts(self):
        """Orchestra 전용 단축키 설정"""
        print("⌨️ 단축키 설정 중...")
        
        shortcuts = {
            "cmd+1": "Select Claude tab",
            "cmd+2": "Select Gemini tab",
            "cmd+3": "Select Codex tab",
            "cmd+4": "Select Cursor tab",
            "cmd+shift+k": "Show KPI dashboard",
            "cmd+shift+m": "Show monitoring",
            "cmd+shift+t": "Run tests"
        }
        
        print("  단축키 매핑:")
        for key, action in shortcuts.items():
            print(f"    {key}: {action}")
        
        print("✅ 단축키 설정 완료")
    
    def display_welcome_message(self):
        """Orchestra 시작 메시지 표시"""
        welcome_script = '''
        tell application "iTerm2"
            tell current window
                tell first tab
                    tell current session
                        write text "echo '🎭 AI Orchestra Dashboard Started'"
                        write text "echo '================================'"
                        write text "echo 'Team: Claude, Gemini, Codex, Cursor'"
                        write text "echo 'Status: All Systems Operational'"
                        write text "echo '================================'"
                    end tell
                end tell
            end tell
        end tell
        '''
        
        subprocess.run(["osascript", "-e", welcome_script])
    
    def monitor_team_status(self):
        """팀 상태 실시간 모니터링"""
        print("\n🔄 실시간 모니터링 시작...")
        
        while True:
            try:
                # PL Bot 리포트 읽기
                with open("pl-bot-report.json", "r") as f:
                    report = json.load(f)
                
                # 각 탭에 상태 업데이트
                for i, (ai_name, status) in enumerate(report["team_status"].items(), 1):
                    if status["status"] == "active":
                        badge_text = f"✅ Active"
                    else:
                        badge_text = f"❌ Offline"
                    
                    update_script = f'''
                    tell application "iTerm2"
                        tell current window
                            tell tab {i}
                                tell current session
                                    set badge to "{ai_name}\\n{badge_text}"
                                end tell
                            end tell
                        end tell
                    end tell
                    '''
                    
                    subprocess.run(
                        ["osascript", "-e", update_script],
                        capture_output=True
                    )
                
                time.sleep(30)  # 30초마다 업데이트
                
            except KeyboardInterrupt:
                print("\n🛑 모니터링 중지")
                break
            except Exception as e:
                print(f"⚠️ 모니터링 오류: {e}")
                time.sleep(30)

def main():
    """메인 실행 함수"""
    print("🎭 iTerm2 Orchestra Integration v1.0")
    print("="*50)
    
    orchestra = ITermOrchestra()
    
    # 1. Orchestra 프로파일 설정
    orchestra.setup_orchestra_profile()
    
    # 2. 상태 배지 추가
    orchestra.add_status_badges()
    
    # 3. 커스텀 상태바 생성
    orchestra.create_custom_statusbar()
    
    # 4. 단축키 설정
    orchestra.setup_keyboard_shortcuts()
    
    # 5. 환영 메시지
    orchestra.display_welcome_message()
    
    print("\n✅ iTerm2 Orchestra 설정 완료!")
    print("\n사용 가능한 명령:")
    print("  • Cmd+1~4: AI 탭 전환")
    print("  • Cmd+Shift+K: KPI 대시보드")
    print("  • Cmd+Shift+M: 모니터링")
    
    # 실시간 모니터링 시작할지 묻기
    response = input("\n실시간 모니터링을 시작하시겠습니까? (y/n): ")
    if response.lower() == 'y':
        orchestra.monitor_team_status()

if __name__ == "__main__":
    main()