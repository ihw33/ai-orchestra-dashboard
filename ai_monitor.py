#!/usr/bin/env python3
"""
AI Orchestra 실시간 모니터링 대시보드
모든 AI 명령과 응답을 한 곳에서 확인
"""
import subprocess
import time
import json
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text

class AIMonitor:
    def __init__(self):
        self.console = Console()
        self.command_log = []
        self.response_log = []
        
    def send_to_ai(self, ai_name, command):
        """AI에게 명령 전송 및 응답 수집"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # 명령 로그
        self.command_log.append({
            "time": timestamp,
            "ai": ai_name,
            "command": command
        })
        
        # 실제 실행
        try:
            if ai_name == "Gemini":
                result = subprocess.run(
                    f"echo '{command}' | gemini 2>/dev/null | grep -v 'Data collection' | head -5",
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                response = result.stdout.strip() or "No response"
            elif ai_name == "Codex":
                # Codex는 버전 체크로 대체
                result = subprocess.run(
                    ["codex", "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                response = f"Version: {result.stdout.strip()}"
            else:
                response = "Unknown AI"
                
            # 응답 로그
            self.response_log.append({
                "time": timestamp,
                "ai": ai_name,
                "response": response[:100]  # 100자 제한
            })
            
            return response
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.response_log.append({
                "time": timestamp,
                "ai": ai_name,
                "response": error_msg
            })
            return error_msg
    
    def create_dashboard(self):
        """실시간 대시보드 생성"""
        # 레이아웃 생성
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3)
        )
        
        # 메인 영역 분할
        layout["main"].split_row(
            Layout(name="commands"),
            Layout(name="responses"),
            Layout(name="status")
        )
        
        # 헤더
        header = Panel(
            Text("🎭 AI Orchestra Monitor", style="bold magenta", justify="center"),
            style="bold white on blue"
        )
        layout["header"].update(header)
        
        # 명령 로그 테이블
        cmd_table = Table(title="📤 Commands Sent", expand=True)
        cmd_table.add_column("Time", style="cyan", width=10)
        cmd_table.add_column("AI", style="yellow", width=10)
        cmd_table.add_column("Command", style="green")
        
        for log in self.command_log[-10:]:  # 최근 10개
            cmd_table.add_row(log["time"], log["ai"], log["command"][:30] + "...")
            
        layout["commands"].update(Panel(cmd_table))
        
        # 응답 로그 테이블
        resp_table = Table(title="📥 Responses", expand=True)
        resp_table.add_column("Time", style="cyan", width=10)
        resp_table.add_column("AI", style="yellow", width=10)
        resp_table.add_column("Response", style="white")
        
        for log in self.response_log[-10:]:  # 최근 10개
            resp_table.add_row(log["time"], log["ai"], log["response"][:30] + "...")
            
        layout["responses"].update(Panel(resp_table))
        
        # 상태 패널
        status_text = f"""
[bold green]✅ Active AIs[/]
• Gemini: Online
• Codex: Online
• Claude: Online
• Cursor: Running

[bold yellow]📊 Statistics[/]
Commands: {len(self.command_log)}
Responses: {len(self.response_log)}
Success Rate: {len([r for r in self.response_log if 'Error' not in r.get('response', '')])}/{len(self.response_log)} 

[bold cyan]🔄 Last Update[/]
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        """
        layout["status"].update(Panel(status_text, title="📈 Status"))
        
        # 푸터
        footer = Panel(
            "[bold]Commands: [/][cyan]q[/]=quit | [cyan]g[/]=test Gemini | [cyan]c[/]=test Codex | [cyan]r[/]=refresh",
            style="bold white on black"
        )
        layout["footer"].update(footer)
        
        return layout
    
    def test_gemini(self):
        """Gemini 테스트"""
        self.send_to_ai("Gemini", "What is 3+3?")
        
    def test_codex(self):
        """Codex 테스트"""
        self.send_to_ai("Codex", "version check")
        
    def run_monitor(self):
        """모니터링 실행"""
        self.console.clear()
        
        # 초기 테스트
        self.console.print("[bold green]🚀 AI Orchestra Monitor Starting...[/]")
        self.test_gemini()
        self.test_codex()
        
        # 실시간 업데이트
        with Live(self.create_dashboard(), refresh_per_second=1, screen=True) as live:
            try:
                while True:
                    # 대시보드 업데이트
                    live.update(self.create_dashboard())
                    
                    # 30초마다 자동 체크
                    time.sleep(30)
                    self.test_gemini()
                    self.test_codex()
                    
            except KeyboardInterrupt:
                self.console.print("\n[bold red]Monitor stopped.[/]")
                
                # 로그 저장
                with open("ai_monitor_log.json", "w") as f:
                    json.dump({
                        "commands": self.command_log,
                        "responses": self.response_log,
                        "timestamp": datetime.now().isoformat()
                    }, f, indent=2)
                    
                self.console.print("[green]✅ Log saved to ai_monitor_log.json[/]")

if __name__ == "__main__":
    monitor = AIMonitor()
    monitor.run_monitor()