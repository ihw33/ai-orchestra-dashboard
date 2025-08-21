#!/bin/bash

# AI Orchestra Dashboard Backend Startup Script
# This script sets up and runs the FastAPI backend server

echo "🚀 AI Orchestra Dashboard Backend Startup"
echo "========================================="

# Navigate to backend directory
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found! Please configure it first."
    echo "Copy .env.example to .env and add your API keys:"
    echo "  - GITHUB_TOKEN"
    echo "  - ANTHROPIC_API_KEY" 
    echo "  - OPENAI_API_KEY"
    exit 1
fi

# Check for required environment variables
source .env
if [ -z "$GITHUB_TOKEN" ] || [ "$GITHUB_TOKEN" = "your_github_token_here" ]; then
    echo "⚠️  GITHUB_TOKEN not configured in .env file!"
    echo "Please add your GitHub Personal Access Token to the .env file"
    echo "Get one at: https://github.com/settings/tokens"
    exit 1
fi

# Start the server
echo "🌟 Starting FastAPI server on http://localhost:8000"
echo "📖 API Documentation: http://localhost:8000/docs"
echo "========================================="
echo ""

# Run uvicorn with auto-reload for development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > backend_stdout.log 2> backend_stderr.log