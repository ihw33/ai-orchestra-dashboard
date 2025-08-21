#!/usr/bin/env python3
"""
간단한 오케스트라 테스트
실제로 MCP 없이도 작동 가능한 시뮬레이션
"""

import json
import time
from datetime import datetime

# 가상의 작업 큐
task_queue = {
    "gemini": [],
    "codex": [],
    "cursor": []
}

def assign_task(cli_name, task):
    """PM이 작업 할당"""
    task_queue[cli_name].append({
        "id": task["id"],
        "title": task["title"],
        "assigned_at": datetime.now().isoformat()
    })
    print(f"✅ PM → {cli_name}: {task['title']}")
    
    # 파일로도 저장 (CLI가 확인 가능)
    with open(f"/tmp/{cli_name}_task.json", "w") as f:
        json.dump(task_queue[cli_name], f, indent=2)

def check_tasks(cli_name):
    """CLI가 작업 확인"""
    try:
        with open(f"/tmp/{cli_name}_task.json", "r") as f:
            tasks = json.load(f)
            if tasks:
                print(f"📋 {cli_name}의 작업:")
                for task in tasks:
                    print(f"  - {task['title']}")
                return tasks
    except:
        pass
    print(f"❌ {cli_name}: 작업 없음")
    return []

# 테스트 시나리오
print("=" * 50)
print("🎯 AI Orchestra 테스트 시작")
print("=" * 50)

# PM이 작업 할당
print("\n1️⃣ PM이 작업 할당:")
assign_task("gemini", {"id": "3", "title": "사용자 가이드 작성"})
assign_task("codex", {"id": "2", "title": "API 최적화"})
assign_task("cursor", {"id": "1", "title": "UI 디자인 개선"})

print("\n2️⃣ 각 CLI가 작업 확인:")
time.sleep(1)
check_tasks("gemini")
check_tasks("codex")
check_tasks("cursor")

print("\n✅ 테스트 완료!")