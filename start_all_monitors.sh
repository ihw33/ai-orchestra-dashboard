#!/bin/bash

# 🚀 모든 CLI 모니터 시작 스크립트

echo "🎯 Starting CLI Monitors..."

# 각 CLI에 대한 모니터 시작
echo "Starting PM Claude monitor..."
python3 scripts/cli_monitor.py --cli claude &

echo "Starting Gemini monitor..."
python3 scripts/cli_monitor.py --cli gemini &

echo "Starting Codex monitor..."
python3 scripts/cli_monitor.py --cli codex &

sleep 2

echo ""
echo "✅ All monitors started!"
echo ""
echo "Checking status..."
curl -s http://localhost:8000/api/pm/detect-clis | python3 -m json.tool | grep -A5 '"claude"\|"gemini"\|"codex"' | grep -E '"(available|monitor_connected)"'

echo ""
echo "📌 To stop monitors: pkill -f cli_monitor.py"