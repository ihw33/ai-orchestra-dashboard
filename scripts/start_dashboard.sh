#!/bin/bash

# AI Orchestra Dashboard Startup Script

echo "🎭 Starting AI Orchestra Dashboard..."

# Check if .env file exists
if [ ! -f "../.env" ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp ../.env.example ../.env
    echo "📝 Please edit .env file with your API keys before running again."
    exit 1
fi

# Start backend server
echo "🚀 Starting Backend Server..."
cd ../backend
python -m uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend
echo "🎨 Starting Frontend..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo "✅ Dashboard is running!"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services..."

# Wait for interrupt
trap "echo '🛑 Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait