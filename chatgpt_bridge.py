#!/usr/bin/env python3
"""
터미널 Claude가 ChatGPT와 대화하는 브릿지
OpenAI API를 직접 호출
"""

import os
import sys
import json
from openai import OpenAI

# API 키 설정 (환경변수 또는 직접 입력)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")

def ask_chatgpt(prompt):
    """ChatGPT에게 질문하고 응답 받기"""
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error: {e}"

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 chatgpt_bridge.py 'your question'")
        sys.exit(1)
    
    prompt = " ".join(sys.argv[1:])
    print(f"📤 Asking ChatGPT: {prompt}")
    print("-" * 50)
    
    response = ask_chatgpt(prompt)
    
    print("📥 ChatGPT Response:")
    print(response)
    
    # JSON으로도 저장 (다른 프로그램이 읽을 수 있게)
    with open("/tmp/chatgpt_response.json", "w") as f:
        json.dump({
            "prompt": prompt,
            "response": response
        }, f, indent=2)

if __name__ == "__main__":
    main()