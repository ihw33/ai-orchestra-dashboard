#!/usr/bin/env python3
"""
AI Orchestra Auto-onboarding Wizard
5분 안에 프로젝트 시작!
"""
import os
import json
import subprocess
from datetime import datetime

class SetupWizard:
    def __init__(self):
        self.project_types = {
            "web": {
                "name": "웹 애플리케이션",
                "team": ["Cursor", "Codex", "Gemini"],
                "template": "nextjs"
            },
            "mobile": {
                "name": "모바일 앱",
                "team": ["Codex", "Gemini", "Claude"],
                "template": "react-native"
            },
            "data": {
                "name": "데이터 분석",
                "team": ["Gemini", "Codex", "Claude"],
                "template": "jupyter"
            },
            "ai": {
                "name": "AI/ML 프로젝트",
                "team": ["Codex", "Claude", "Gemini"],
                "template": "python-ml"
            }
        }
        
    def welcome(self):
        """환영 메시지"""
        print("""
╔══════════════════════════════════════╗
║   🎭 AI Orchestra Setup Wizard       ║
║   5분 안에 프로젝트 시작하기!        ║
╚══════════════════════════════════════╝
        """)
        
    def get_project_info(self):
        """프로젝트 정보 수집"""
        print("\n📋 프로젝트 정보를 입력해주세요:\n")
        
        # 프로젝트 이름
        project_name = input("프로젝트 이름: ").strip()
        
        # 프로젝트 타입
        print("\n프로젝트 타입을 선택하세요:")
        for key, value in self.project_types.items():
            print(f"  [{key}] {value['name']}")
        
        project_type = input("\n선택 (web/mobile/data/ai): ").strip()
        
        # 비공개 여부
        is_private = input("\n비공개 레포지토리? (y/n): ").strip().lower() == 'y'
        
        return {
            "name": project_name,
            "type": project_type,
            "private": is_private,
            "created_at": datetime.now().isoformat()
        }
        
    def suggest_team(self, project_type):
        """AI 팀 구성 제안"""
        team_config = self.project_types.get(project_type, self.project_types["web"])
        
        print(f"\n🤖 추천 팀 구성 ({team_config['name']}):")
        for i, ai in enumerate(team_config['team'], 1):
            print(f"  {i}. {ai}")
            
        # 수정 옵션
        modify = input("\n팀 구성을 수정하시겠습니까? (y/n): ").strip().lower()
        
        if modify == 'y':
            print("\nAI 목록: Claude, Gemini, Codex, Cursor")
            custom_team = input("팀 구성 (쉼표로 구분): ").strip().split(',')
            return [ai.strip() for ai in custom_team]
        
        return team_config['team']
        
    def create_github_repo(self, project_info):
        """GitHub 레포지토리 생성"""
        print(f"\n📦 GitHub 레포지토리 생성 중...")
        
        cmd = [
            "gh", "repo", "create", 
            project_info['name'],
            "--public" if not project_info['private'] else "--private",
            "--clone"
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print(f"✅ 레포지토리 생성 완료: {project_info['name']}")
            return True
        except:
            print(f"❌ 레포지토리 생성 실패")
            return False
            
    def setup_iterm_sessions(self, team):
        """iTerm2 세션 자동 설정"""
        print(f"\n🖥️ iTerm2 세션 설정 중...")
        
        # AppleScript로 탭 생성
        for i, ai in enumerate(team, start=1):
            script = f'''
            tell application "iTerm2"
                tell current window
                    create tab with default profile
                    tell current session
                        set name to "ORCH_{ai.upper()}"
                        write text "echo '🤖 {ai} 준비 완료'"
                    end tell
                end tell
            end tell
            '''
            subprocess.run(['osascript', '-e', script])
            
        print(f"✅ {len(team)}개 AI 세션 생성 완료")
        
    def create_initial_files(self, project_info, team):
        """초기 파일 생성"""
        print(f"\n📄 초기 파일 생성 중...")
        
        # CLAUDE.md 생성
        claude_md = f"""# 🎭 {project_info['name']} - AI Orchestra

## 프로젝트 정보
- 타입: {project_info['type']}
- 생성일: {project_info['created_at']}
- PM: Claude

## AI 팀 구성
{chr(10).join([f"- {ai}" for ai in team])}

## 작업 프로세스
1. GitHub Issue 생성
2. 라벨로 AI 지정
3. 자동 작업 시작
4. PR 생성 및 리뷰
"""
        
        with open("CLAUDE.md", "w") as f:
            f.write(claude_md)
            
        # .ai-orchestra/config.json 생성
        os.makedirs(".ai-orchestra", exist_ok=True)
        config = {
            "project": project_info,
            "team": team,
            "sessions": {f"ORCH_{ai.upper()}": {"ai": ai} for ai in team}
        }
        
        with open(".ai-orchestra/config.json", "w") as f:
            json.dump(config, f, indent=2)
            
        print("✅ 초기 파일 생성 완료")
        
    def run(self):
        """메인 실행"""
        self.welcome()
        
        # 1. 프로젝트 정보 수집
        project_info = self.get_project_info()
        
        # 2. 팀 구성
        team = self.suggest_team(project_info['type'])
        
        print(f"\n{'='*40}")
        print(f"📋 최종 구성")
        print(f"{'='*40}")
        print(f"프로젝트: {project_info['name']}")
        print(f"타입: {project_info['type']}")
        print(f"팀: {', '.join(team)}")
        
        confirm = input("\n시작하시겠습니까? (y/n): ").strip().lower()
        
        if confirm != 'y':
            print("취소되었습니다.")
            return
            
        # 3. 자동 설정
        print(f"\n🚀 자동 설정 시작...")
        
        # GitHub 레포 생성
        if self.create_github_repo(project_info):
            os.chdir(project_info['name'])
            
        # 초기 파일 생성
        self.create_initial_files(project_info, team)
        
        # iTerm 세션 설정
        self.setup_iterm_sessions(team)
        
        print(f"\n{'='*40}")
        print(f"✨ 설정 완료!")
        print(f"{'='*40}")
        print(f"프로젝트가 준비되었습니다.")
        print(f"GitHub Issue를 생성하여 작업을 시작하세요!")

if __name__ == "__main__":
    wizard = SetupWizard()
    wizard.run()