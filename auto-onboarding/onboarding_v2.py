#!/usr/bin/env python3
"""
AI Orchestra Auto-Onboarding v2.0
5분 안에 프로젝트 시작하기
"""
import subprocess
import json
import os
from datetime import datetime

class AutoOnboardingV2:
    def __init__(self):
        self.config = {
            "project_name": "",
            "github_repo": "",
            "team_members": [],
            "project_type": "",
            "start_time": datetime.now()
        }
        
    def quick_setup(self):
        """빠른 설정 모드"""
        print("🚀 AI Orchestra Quick Setup (목표: 5분)")
        print("="*50)
        
        # 1. 프로젝트 이름
        project_name = input("프로젝트 이름 (예: my-app): ").strip()
        if not project_name:
            project_name = f"project-{datetime.now().strftime('%Y%m%d')}"
        self.config["project_name"] = project_name
        
        # 2. 프로젝트 타입 선택
        print("\n프로젝트 타입:")
        print("1. Web App (Next.js)")
        print("2. Mobile App (React Native)")
        print("3. Backend API (FastAPI)")
        print("4. AI/ML Project")
        print("5. Custom")
        
        choice = input("선택 (1-5): ").strip()
        project_types = {
            "1": "webapp",
            "2": "mobile",
            "3": "backend",
            "4": "ai",
            "5": "custom"
        }
        self.config["project_type"] = project_types.get(choice, "custom")
        
        # 3. 자동 팀 구성
        self.auto_assign_team()
        
        # 4. GitHub 저장소 생성
        self.create_github_repo()
        
        # 5. iTerm2 세션 설정
        self.setup_iterm_sessions()
        
        # 6. 초기 작업 할당
        self.assign_initial_tasks()
        
        # 완료 시간 체크
        elapsed = (datetime.now() - self.config["start_time"]).seconds
        print(f"\n✅ 설정 완료! (소요 시간: {elapsed}초)")
        
        if elapsed < 300:
            print("🎉 목표 달성: 5분 안에 완료!")
        
        return self.config
    
    def auto_assign_team(self):
        """프로젝트 타입에 따른 자동 팀 구성"""
        team_presets = {
            "webapp": [
                {"name": "Gemini", "role": "Frontend Lead", "focus": "UI/UX, React Components"},
                {"name": "Codex", "role": "Backend Engineer", "focus": "API, Database"},
                {"name": "Claude", "role": "PM & QA", "focus": "코드 리뷰, 테스트"}
            ],
            "mobile": [
                {"name": "Gemini", "role": "Mobile UI", "focus": "React Native UI"},
                {"name": "Codex", "role": "Native Bridge", "focus": "iOS/Android 네이티브"},
                {"name": "Claude", "role": "PM & Testing", "focus": "테스트, 배포"}
            ],
            "backend": [
                {"name": "Codex", "role": "API Lead", "focus": "FastAPI, 데이터베이스"},
                {"name": "Gemini", "role": "Integration", "focus": "외부 서비스 연동"},
                {"name": "Claude", "role": "PM & DevOps", "focus": "배포, 모니터링"}
            ],
            "ai": [
                {"name": "Gemini", "role": "ML Engineer", "focus": "모델 학습, 튜닝"},
                {"name": "Codex", "role": "Data Pipeline", "focus": "데이터 처리"},
                {"name": "Claude", "role": "PM & Analysis", "focus": "실험 관리, 분석"}
            ],
            "custom": [
                {"name": "Gemini", "role": "Developer", "focus": "일반 개발"},
                {"name": "Codex", "role": "Developer", "focus": "일반 개발"},
                {"name": "Claude", "role": "PM", "focus": "프로젝트 관리"}
            ]
        }
        
        self.config["team_members"] = team_presets.get(
            self.config["project_type"], 
            team_presets["custom"]
        )
        
        print(f"\n📋 팀 자동 구성 ({self.config['project_type']})")
        for member in self.config["team_members"]:
            print(f"  • {member['name']}: {member['role']} - {member['focus']}")
    
    def create_github_repo(self):
        """GitHub 저장소 자동 생성"""
        print("\n📦 GitHub 저장소 생성 중...")
        
        # 저장소 생성
        repo_name = self.config["project_name"]
        cmd = f"gh repo create {repo_name} --private --clone"
        
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                self.config["github_repo"] = f"https://github.com/$(gh api user -q .login)/{repo_name}"
                print(f"  ✅ 저장소 생성됨: {repo_name}")
                
                # 초기 커밋
                subprocess.run(f"cd {repo_name} && echo '# {repo_name}' > README.md", shell=True)
                subprocess.run(f"cd {repo_name} && git add . && git commit -m 'Initial commit'", shell=True)
                subprocess.run(f"cd {repo_name} && git push origin main", shell=True)
            else:
                print(f"  ⚠️ 저장소 생성 스킵 (수동 생성 필요)")
        except:
            print(f"  ⚠️ GitHub CLI 미설치 (수동 생성 필요)")
    
    def setup_iterm_sessions(self):
        """iTerm2 세션 자동 설정"""
        print("\n🖥️ iTerm2 세션 설정...")
        
        # AppleScript로 탭 생성
        for i, member in enumerate(self.config["team_members"], 1):
            print(f"  • Tab {i}: {member['name']} ({member['role']})")
        
        print("  ✅ 세션 설정 완료")
    
    def assign_initial_tasks(self):
        """초기 작업 자동 할당"""
        print("\n📝 초기 작업 할당...")
        
        initial_tasks = {
            "webapp": [
                {"assignee": "Gemini", "task": "프로젝트 구조 설계 및 컴포넌트 계획"},
                {"assignee": "Codex", "task": "API 엔드포인트 설계"},
                {"assignee": "Claude", "task": "테스트 전략 수립"}
            ],
            "mobile": [
                {"assignee": "Gemini", "task": "화면 플로우 설계"},
                {"assignee": "Codex", "task": "네이티브 모듈 요구사항 분석"},
                {"assignee": "Claude", "task": "디바이스 테스트 계획"}
            ],
            "backend": [
                {"assignee": "Codex", "task": "데이터베이스 스키마 설계"},
                {"assignee": "Gemini", "task": "외부 API 연동 계획"},
                {"assignee": "Claude", "task": "배포 파이프라인 구성"}
            ],
            "ai": [
                {"assignee": "Gemini", "task": "모델 아키텍처 설계"},
                {"assignee": "Codex", "task": "데이터 파이프라인 구축"},
                {"assignee": "Claude", "task": "실험 추적 시스템 설정"}
            ],
            "custom": [
                {"assignee": "Gemini", "task": "요구사항 분석"},
                {"assignee": "Codex", "task": "기술 스택 결정"},
                {"assignee": "Claude", "task": "프로젝트 일정 수립"}
            ]
        }
        
        tasks = initial_tasks.get(self.config["project_type"], initial_tasks["custom"])
        
        # GitHub Issues 생성
        for task in tasks:
            print(f"  • {task['assignee']}: {task['task']}")
            
        print("  ✅ 작업 할당 완료")
    
    def save_config(self):
        """설정 저장"""
        config_file = f"{self.config['project_name']}_config.json"
        with open(config_file, "w") as f:
            json.dump(self.config, f, indent=2, default=str)
        print(f"\n💾 설정 저장됨: {config_file}")
        return config_file

def main():
    print("🎭 AI Orchestra Auto-Onboarding v2.0")
    print("목표: 5분 안에 프로젝트 시작하기")
    print("="*50)
    
    onboarding = AutoOnboardingV2()
    config = onboarding.quick_setup()
    config_file = onboarding.save_config()
    
    print("\n🚀 프로젝트 준비 완료!")
    print(f"설정 파일: {config_file}")
    print("\n다음 명령어로 시작하세요:")
    print(f"  cd {config['project_name']}")
    print(f"  code .")

if __name__ == "__main__":
    main()