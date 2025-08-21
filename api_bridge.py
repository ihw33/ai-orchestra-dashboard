#!/usr/bin/env python3
"""
진짜 API 레벨 통합 브릿지
각 AI 서비스의 API를 직접 호출
"""

import os
import json
from typing import Dict, Any
import openai
import anthropic
from google import generativeai as genai

class AIOrchestra:
    def __init__(self):
        # API 키 설정
        self.claude = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        openai.api_key = os.getenv("OPENAI_API_KEY")
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        
    def ask_chatgpt(self, prompt: str) -> str:
        """ChatGPT에게 직접 질문"""
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    
    def ask_gemini(self, prompt: str) -> str:
        """Gemini에게 직접 질문"""
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    
    def ask_claude(self, prompt: str) -> str:
        """Claude에게 직접 질문"""
        message = self.claude.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    
    def orchestrate(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """작업을 적절한 AI에게 분배"""
        results = {}
        
        if "frontend" in task:
            results["frontend"] = self.ask_chatgpt(task["frontend"])
            
        if "backend" in task:
            results["backend"] = self.ask_claude(task["backend"])
            
        if "content" in task:
            results["content"] = self.ask_gemini(task["content"])
            
        return results

# 사용 예시
if __name__ == "__main__":
    orchestra = AIOrchestra()
    
    # PM이 작업 분배
    tasks = {
        "frontend": "React 컴포넌트 설계 제안",
        "backend": "API 엔드포인트 구조 설계",
        "content": "사용자 가이드 초안 작성"
    }
    
    results = orchestra.orchestrate(tasks)
    print(json.dumps(results, indent=2, ensure_ascii=False))