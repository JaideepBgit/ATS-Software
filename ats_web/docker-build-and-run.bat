@echo off
echo ========================================
echo ATS Application - Docker Build and Run
echo ========================================
echo.
echo This will:
echo 1. Build the Docker image
echo 2. Start the container
echo 3. Job tracking feature included!
echo.
echo Data will be saved to: .\data\jobs_applied\
echo.
pause

echo.
echo [1/2] Building Docker image...
echo.
docker-compose build

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Docker build failed!
    echo Make sure Docker Desktop is running.
    pause
    exit /b 1
)

echo.
echo [2/2] Starting container...
echo.
docker-compose up -d

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Failed to start container!
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS! Application is running!
echo ========================================
echo.
echo Frontend:  http://localhost
echo Backend:   http://localhost:8000
echo.
echo Job Tracker: Click the button in top-right corner!
echo Excel File:  .\data\jobs_applied\job_applicaiton.xlsx
echo.
echo To view logs: docker-compose logs -f
echo To stop:      docker-compose down
echo.
pause
