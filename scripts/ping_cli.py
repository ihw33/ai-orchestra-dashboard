#!/usr/bin/env python3
"""
CLI Ping System
연결된 CLI에 핑 메시지를 보내서 실제 연결 확인
"""

import json
import time
from pathlib import Path
from datetime import datetime

def ping_cli(cli_name: str, message: str = None):
    """특정 CLI에 핑 메시지 전송"""
    
    base_dir = Path.home() / ".ai-orchestra"
    tasks_dir = base_dir / "tasks" / cli_name
    
    # 핑 메시지 생성
    ping_id = f"ping_{int(time.time())}"
    ping_message = message or f"🏓 PING from Dashboard at {datetime.now().strftime('%H:%M:%S')}"
    
    ping_task = {
        "id": ping_id,
        "cli": cli_name,
        "type": "ping",
        "description": ping_message,
        "priority": "high",
        "created_at": datetime.now().isoformat(),
        "status": "pending"
    }
    
    # 핑 파일 생성
    ping_file = tasks_dir / f"{ping_id}.json"
    with open(ping_file, 'w') as f:
        json.dump(ping_task, f, indent=2)
    
    print(f"✅ Ping sent to {cli_name}: {ping_message}")
    return ping_id

def ping_all_connected():
    """모든 연결된 CLI에 핑 전송"""
    base_dir = Path.home() / ".ai-orchestra"
    status_dir = base_dir / "status"
    
    connected_clis = []
    
    # 연결된 CLI 확인
    if status_dir.exists():
        for cli_dir in status_dir.iterdir():
            if cli_dir.is_dir():
                cli_name = cli_dir.name
                status_file = cli_dir / "current.json"
                
                if status_file.exists():
                    try:
                        with open(status_file) as f:
                            status = json.load(f)
                            
                        # 최근 30초 이내 업데이트된 것만
                        updated_at = datetime.fromisoformat(status['updated_at'])
                        time_diff = datetime.now() - updated_at
                        
                        if time_diff.total_seconds() < 30:
                            connected_clis.append(cli_name)
                            ping_cli(cli_name, f"🏓 PING TEST - You are connected! [{datetime.now().strftime('%H:%M:%S')}]")
                    except Exception as e:
                        print(f"Error checking {cli_name}: {e}")
    
    return connected_clis

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # 특정 CLI에 핑
        cli_name = sys.argv[1]
        message = sys.argv[2] if len(sys.argv) > 2 else None
        ping_cli(cli_name, message)
    else:
        # 모든 연결된 CLI에 핑
        connected = ping_all_connected()
        print(f"\n📡 Pinged {len(connected)} connected CLIs: {', '.join(connected)}")