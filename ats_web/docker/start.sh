#!/bin/bash
set -e

echo "🚀 Starting ATS Application..."

# Check if host Ollama is accessible
echo "🔍 Checking for Ollama on host machine..."
OLLAMA_HOST="http://host.docker.internal:11434"

for i in {1..10}; do
    if curl -s ${OLLAMA_HOST}/api/tags > /dev/null 2>&1; then
        echo "✅ Found Ollama running on host machine!"
        break
    fi
    if [ $i -eq 10 ]; then
        echo "⚠️  WARNING: Cannot connect to Ollama on host machine"
        echo "   Make sure Ollama is running on your Windows machine"
        echo "   Run: ollama serve"
        echo "   Continuing anyway..."
    else
        echo "   Attempt $i/10..."
        sleep 2
    fi
done

# Start backend
echo "🐍 Starting Python backend..."
cd /app/backend
python main.py &
BACKEND_PID=$!

# Wait for backend to be ready
echo "⏳ Waiting for backend to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:8000/ > /dev/null 2>&1; then
        echo "✅ Backend is ready!"
        break
    fi
    echo "   Attempt $i/30..."
    sleep 2
done

# Start nginx
echo "🌐 Starting Nginx..."
nginx -g 'daemon off;' &
NGINX_PID=$!

echo ""
echo "✅ All services started successfully!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌐 Frontend:  http://localhost"
echo "🔧 Backend:   http://localhost:8000"
echo "🤖 Ollama:    ${OLLAMA_HOST} (on host)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?
