#!/bin/bash

echo "========================================"
echo "  ATS Application - Docker Launcher"
echo "========================================"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "[ERROR] Docker is not running!"
    echo "Please start Docker and try again."
    exit 1
fi

echo "[OK] Docker is running"
echo ""

# Check if docker-compose exists
if ! command -v docker-compose &> /dev/null; then
    echo "[ERROR] docker-compose not found!"
    echo "Please install docker-compose."
    exit 1
fi

echo "[OK] docker-compose found"
echo ""

echo "Starting ATS Application..."
echo "This may take 5-10 minutes on first run (downloading AI model)"
echo ""

docker-compose up -d

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Failed to start application"
    echo "Check the logs with: docker-compose logs"
    exit 1
fi

echo ""
echo "========================================"
echo "  Application Started Successfully!"
echo "========================================"
echo ""
echo "Frontend:  http://localhost"
echo "Backend:   http://localhost:8000"
echo "Ollama:    http://localhost:11434"
echo ""
echo "To view logs:  docker-compose logs -f"
echo "To stop:       docker-compose down"
echo ""

# Try to open browser (works on Mac and some Linux)
if command -v open &> /dev/null; then
    echo "Opening browser..."
    sleep 3
    open http://localhost
elif command -v xdg-open &> /dev/null; then
    echo "Opening browser..."
    sleep 3
    xdg-open http://localhost
fi

echo ""
echo "Press Ctrl+C to exit"
