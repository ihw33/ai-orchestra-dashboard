#!/usr/bin/env python3
import time
import os
import sys
import re
import subprocess
from pathlib import Path

LOG_DIR = Path("logs")
RULES_FILE = Path("routes.txt")
POLL = 0.5  # 0.5초마다 체크

def load_rules():
    """routes.txt에서 라우팅 규칙 로드"""
    rules = []
    if not RULES_FILE.exists():
        return rules
    
    for line in RULES_FILE.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        
        # 형식: source -> target  regex(optional)
        parts = re.split(r"\s*->\s*", s, maxsplit=1)
        if len(parts) < 2:
            continue
            
        left, right = parts
        
        # regex가 있는 경우 (공백 2개로 구분)
        if "  " in right:
            dst, regex = right.split("  ", 1)
            regex = regex.strip()
        else:
            dst, regex = right.strip(), None
            
        rules.append((
            left.strip(), 
            dst.strip(), 
            re.compile(regex) if regex else None
        ))
    
    return rules

def tail_file(path: Path):
    """파일을 tail -f처럼 감시"""
    path.touch(exist_ok=True)
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        # 파일 끝으로 이동
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                time.sleep(POLL)
                continue
            yield line.rstrip("\n")

def send_to_tmux(target, text):
    """tmux send-keys로 메시지 전송"""
    cmd = f'tmux send-keys -t {target} "{text}" Enter'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode == 0

def main():
    print("[relay] AI Orchestra CLI Bridge 시작...")
    print("[relay] routes.txt 파일에 라우팅 규칙을 작성하세요")
    print("-" * 50)
    
    LOG_DIR.mkdir(exist_ok=True)
    
    # 각 로그 파일에 대한 tail 생성기
    tails = {}
    
    while True:
        # 새로운 로그 파일 감지
        for log in LOG_DIR.glob("*.out"):
            name = log.stem
            if name not in tails:
                tails[name] = tail_file(log)
                print(f"[relay] 감시 시작: {log} (source: '{name}')")
        
        # 규칙 다시 로드 (동적 업데이트)
        rules = load_rules()
        
        # 각 소스에서 새 라인 체크
        for src, gen in list(tails.items()):
            try:
                line = next(gen)
            except StopIteration:
                continue
            
            # 규칙 매칭
            for (r_src, dst, rgx) in rules:
                if r_src != src:
                    continue
                
                text = line
                
                # regex가 있으면 매칭 체크
                if rgx:
                    m = rgx.search(text)
                    if not m:
                        continue
                    # 첫 번째 캡처 그룹 사용
                    if m.groups():
                        text = m.group(1).strip()
                
                # tmux 타겟 결정 (간단히 세션 이름 사용)
                target = f"{dst}-cli"
                
                if send_to_tmux(target, text):
                    print(f"[relay] {src} -> {dst}: {text[:50]}...")
                else:
                    print(f"[relay] 전송 실패: {dst}")
        
        time.sleep(POLL)

if __name__ == "__main__":
    main()