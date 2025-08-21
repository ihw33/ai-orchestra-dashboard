#!/usr/bin/env python3
"""
AI Orchestra MCP Server
각 CLI가 연결해서 실시간으로 작업을 받을 수 있는 서버
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Dict, List
from pathlib import Path

from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("orchestra-mcp")

class OrchestraServer:
    def __init__(self):
        self.server = Server("ai-orchestra")
        self.tasks = {}  # CLI별 작업 큐
        self.connected_clis = set()
        
        # 툴 등록
        self.setup_tools()
        
    def setup_tools(self):
        """MCP 툴 정의"""
        
        @self.server.list_tools()
        async def list_tools() -> List[types.Tool]:
            return [
                types.Tool(
                    name="register_cli",
                    description="CLI를 오케스트라에 등록",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "cli_name": {"type": "string"},
                            "capabilities": {"type": "array", "items": {"type": "string"}}
                        },
                        "required": ["cli_name"]
                    }
                ),
                types.Tool(
                    name="get_tasks",
                    description="할당된 작업 가져오기",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "cli_name": {"type": "string"}
                        },
                        "required": ["cli_name"]
                    }
                ),
                types.Tool(
                    name="assign_task",
                    description="CLI에 작업 할당",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "cli_name": {"type": "string"},
                            "task": {"type": "object"}
                        },
                        "required": ["cli_name", "task"]
                    }
                ),
                types.Tool(
                    name="report_progress",
                    description="작업 진행 상황 보고",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "cli_name": {"type": "string"},
                            "task_id": {"type": "string"},
                            "status": {"type": "string"},
                            "message": {"type": "string"}
                        },
                        "required": ["cli_name", "task_id", "status"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
            if name == "register_cli":
                cli_name = arguments["cli_name"]
                self.connected_clis.add(cli_name)
                if cli_name not in self.tasks:
                    self.tasks[cli_name] = []
                
                return [types.TextContent(
                    type="text",
                    text=f"✅ {cli_name} 등록 완료! 현재 연결된 CLI: {list(self.connected_clis)}"
                )]
            
            elif name == "get_tasks":
                cli_name = arguments["cli_name"]
                tasks = self.tasks.get(cli_name, [])
                
                if tasks:
                    # 첫 번째 작업 반환하고 큐에서 제거
                    task = tasks.pop(0)
                    return [types.TextContent(
                        type="text",
                        text=json.dumps(task, indent=2)
                    )]
                else:
                    return [types.TextContent(
                        type="text",
                        text="대기 중인 작업이 없습니다."
                    )]
            
            elif name == "assign_task":
                cli_name = arguments["cli_name"]
                task = arguments["task"]
                task["assigned_at"] = datetime.now().isoformat()
                task["status"] = "pending"
                
                if cli_name not in self.tasks:
                    self.tasks[cli_name] = []
                
                self.tasks[cli_name].append(task)
                
                return [types.TextContent(
                    type="text",
                    text=f"✅ {cli_name}에 작업 할당: {task.get('title', 'Untitled')}"
                )]
            
            elif name == "report_progress":
                cli_name = arguments["cli_name"]
                task_id = arguments["task_id"]
                status = arguments["status"]
                message = arguments.get("message", "")
                
                logger.info(f"Progress: {cli_name} - Task {task_id}: {status}")
                
                return [types.TextContent(
                    type="text",
                    text=f"✅ 진행 상황 기록: {cli_name} - {task_id} - {status}"
                )]
            
            else:
                return [types.TextContent(
                    type="text",
                    text=f"Unknown tool: {name}"
                )]
    
    async def run(self):
        """서버 실행"""
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="ai-orchestra",
                    server_version="1.0.0"
                )
            )

if __name__ == "__main__":
    orchestra = OrchestraServer()
    asyncio.run(orchestra.run())