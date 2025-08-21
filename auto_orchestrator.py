#!/usr/bin/env python3
"""
진짜 자동화 오케스트레이터
GitHub 이슈 모니터링 → 자동 할당 → 결과 수집
"""

import subprocess
import time
import json
from datetime import datetime

def check_new_issues():
    """새 이슈 확인"""
    cmd = "gh issue list -R ihw33/ai-orchestra-test --state open --json number,title,assignees"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        return json.loads(result.stdout)
    return []

def assign_issue_to_cli(issue_num, issue_title):
    """이슈 제목 보고 자동 할당"""
    cli_map = {
        "프론트": "vscode",
        "백엔드": "codex", 
        "API": "codex",
        "콘텐츠": "gemini",
        "가이드": "gemini",
        "설계": "cursor"
    }
    
    # 제목에서 키워드 찾아 자동 매칭
    for keyword, cli in cli_map.items():
        if keyword in issue_title:
            return cli
    return "pm-claude"  # 기본값

def create_task_for_cli(cli_name, issue_num, issue_title):
    """CLI에게 작업 생성"""
    task_dir = f"/Users/m4_macbook/.ai-orchestra/tasks/{cli_name}"
    subprocess.run(f"mkdir -p {task_dir}", shell=True)
    
    task_file = f"{task_dir}/issue_{issue_num}.json"
    task_data = {
        "issue_number": issue_num,
        "title": issue_title,
        "assigned_at": datetime.now().isoformat(),
        "status": "pending",
        "cli": cli_name
    }
    
    with open(task_file, 'w') as f:
        json.dump(task_data, f, indent=2)
    
    print(f"✅ Issue #{issue_num} → {cli_name}")
    
    # GitHub 이슈에 코멘트 추가
    comment = f"🤖 자동 할당: {cli_name.upper()}가 이 작업을 담당합니다."
    subprocess.run(
        f'gh issue comment {issue_num} -R ihw33/ai-orchestra-test -b "{comment}"',
        shell=True
    )

def main():
    print("🎯 AI Orchestra 자동 오케스트레이터 시작")
    print("10초마다 새 이슈 확인 및 자동 할당")
    print("종료: Ctrl+C")
    print("-" * 50)
    
    processed_issues = set()
    
    while True:
        issues = check_new_issues()
        
        for issue in issues:
            issue_num = issue['number']
            issue_title = issue['title']
            
            # 이미 처리한 이슈는 스킵
            if issue_num in processed_issues:
                continue
                
            # 이미 할당된 이슈는 스킵
            if issue.get('assignees'):
                processed_issues.add(issue_num)
                continue
            
            # 자동 할당
            cli = assign_issue_to_cli(issue_num, issue_title)
            create_task_for_cli(cli, issue_num, issue_title)
            processed_issues.add(issue_num)
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Issue #{issue_num} → {cli}")
        
        time.sleep(10)  # 10초 대기

if __name__ == "__main__":
    main()