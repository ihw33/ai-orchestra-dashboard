#!/usr/bin/env python3
"""
AI Orchestra 실행 로그 시스템
질문-답변 쌍을 번호를 매겨서 기록
"""
import subprocess
import json
from datetime import datetime
import time

class AIExecutionLogger:
    def __init__(self):
        self.log_entries = []
        self.log_number = 1
        
    def execute_and_log(self, ai_name, question):
        """AI에게 질문하고 응답을 로그에 기록"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 질문 전송 및 응답 받기
        response = None
        status = "FAILED"
        
        try:
            if ai_name == "Gemini":
                # Gemini 실행
                result = subprocess.run(
                    f"echo '{question}' | gemini 2>/dev/null | grep -v 'Data collection' | grep -v 'Loaded' | head -1",
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                response = result.stdout.strip()
                if response and response != "":
                    status = "SUCCESS"
                    
            elif ai_name == "Codex":
                # Codex exec 모드로 실행
                result = subprocess.run(
                    f"echo '{question}' | codex exec 2>&1 | grep -A 2 '\\] codex' | tail -1",
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=15
                )
                response = result.stdout.strip()
                if response and response != "":
                    status = "SUCCESS"
                    
            elif ai_name == "Claude":
                # Claude 버전 체크
                result = subprocess.run(
                    ["claude", "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                response = result.stdout.strip()
                if response:
                    status = "SUCCESS"
                    
        except subprocess.TimeoutExpired:
            response = "TIMEOUT"
            status = "TIMEOUT"
        except Exception as e:
            response = f"ERROR: {str(e)}"
            status = "ERROR"
            
        # 로그 엔트리 생성
        log_entry = {
            "번호": self.log_number,
            "시간": timestamp,
            "AI": ai_name,
            "질문": question,
            "응답": response if response else "NO RESPONSE",
            "상태": status
        }
        
        self.log_entries.append(log_entry)
        self.log_number += 1
        
        return log_entry
    
    def print_log(self):
        """현재까지의 로그를 출력"""
        print("\n" + "="*80)
        print("🎭 AI Orchestra 실행 로그")
        print("="*80)
        
        for entry in self.log_entries:
            print(f"\n[로그 #{entry['번호']}] {entry['시간']}")
            print(f"  AI: {entry['AI']}")
            print(f"  질문: {entry['질문']}")
            print(f"  응답: {entry['응답'][:100]}")  # 100자 제한
            print(f"  상태: {'✅' if entry['상태'] == 'SUCCESS' else '❌'} {entry['상태']}")
            
        # 요약
        print("\n" + "-"*80)
        print("📊 실행 요약:")
        total = len(self.log_entries)
        success = len([e for e in self.log_entries if e['상태'] == 'SUCCESS'])
        print(f"  총 실행: {total}")
        print(f"  성공: {success}")
        print(f"  실패: {total - success}")
        print(f"  성공률: {(success/total*100):.1f}%" if total > 0 else "N/A")
        
        # 질문-답변 쌍 체크
        print("\n🔍 질문-답변 쌍 분석:")
        for entry in self.log_entries:
            if entry['상태'] == 'SUCCESS' and entry['응답'] != "NO RESPONSE":
                print(f"  ✅ #{entry['번호']}: 질문과 응답이 쌍을 이룸")
            else:
                print(f"  ❌ #{entry['번호']}: 질문만 있고 응답 없음 (실행 실패)")
                
    def save_log(self, filename="ai_execution_log.json"):
        """로그를 JSON 파일로 저장"""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "logs": self.log_entries,
                "summary": {
                    "total": len(self.log_entries),
                    "success": len([e for e in self.log_entries if e['상태'] == 'SUCCESS']),
                    "failed": len([e for e in self.log_entries if e['상태'] != 'SUCCESS'])
                }
            }, f, ensure_ascii=False, indent=2)
        print(f"\n💾 로그 저장됨: {filename}")

def main():
    """메인 실행 함수"""
    logger = AIExecutionLogger()
    
    print("🚀 AI Orchestra 실행 로그 시작...")
    print("각 AI에게 질문을 보내고 응답을 기록합니다.\n")
    
    # 테스트 케이스들
    test_cases = [
        ("Gemini", "2+2는 무엇입니까?"),
        ("Gemini", "오늘 날씨는 어떻습니까?"),
        ("Codex", "What is 3+3?"),
        ("Codex", "What is 5-2?"),
        ("Claude", "version check"),
        ("Gemini", "1+1은?"),
    ]
    
    # 각 테스트 실행
    for ai_name, question in test_cases:
        print(f"\n실행 중: {ai_name} - {question}")
        entry = logger.execute_and_log(ai_name, question)
        print(f"  결과: {entry['상태']}")
        time.sleep(1)  # 잠시 대기
    
    # 최종 로그 출력
    logger.print_log()
    
    # 로그 저장
    logger.save_log()

if __name__ == "__main__":
    main()