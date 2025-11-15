@echo off
echo ========================================
echo   ATS Application - Docker Launcher
echo ========================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not running!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)

echo [OK] Docker is running
echo.

REM Check if Ollama is running on host
echo Checking for Ollama on host machine...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo.
    echo [WARNING] Ollama is not running on your machine!
    echo.
    echo Please start Ollama first:
    echo   1. Open a new terminal
    echo   2. Run: ollama serve
    echo   3. Make sure your model is pulled: ollama pull qwen2.5:7b
    echo.
    echo Press any key to continue anyway, or Ctrl+C to exit...
    pause >nul
) else (
    echo [OK] Ollama is running on host
)
echo.

REM Check if docker-compose exists
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] docker-compose not found!
    echo Please install Docker Desktop which includes docker-compose.
    pause
    exit /b 1
)

echo [OK] docker-compose found
echo.

echo Starting ATS Application...
echo Using Ollama from your host machine (faster startup!)
echo.

docker-compose up -d

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to start application
    echo Check the logs with: docker-compose logs
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Application Started Successfully!
echo ========================================
echo.
echo Frontend:  http://localhost
echo Backend:   http://localhost:8000
echo Ollama:    http://localhost:11434 (host)
echo.
echo To view logs:  docker-compose logs -f
echo To stop:       docker-compose down
echo.
echo Opening browser in 3 seconds...
timeout /t 3 /nobreak >nul
start http://localhost
echo.
pause
