@echo off
echo ========================================
echo Testing Job Tracking in Docker
echo ========================================
echo.

echo [1/5] Checking if container is running...
docker ps | findstr ats-application
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Container not running!
    echo Run: docker-compose up -d
    pause
    exit /b 1
)
echo OK: Container is running
echo.

echo [2/5] Testing backend API...
curl -s http://localhost:8000/ > nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Backend not responding!
    pause
    exit /b 1
)
echo OK: Backend is responding
echo.

echo [3/5] Testing job tracking API...
curl -s http://localhost:8000/api/job-applications > nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Job tracking API not responding!
    pause
    exit /b 1
)
echo OK: Job tracking API is working
echo.

echo [4/5] Checking data directory...
if exist "data\jobs_applied" (
    echo OK: Data directory exists
) else (
    echo WARNING: Data directory not found
    echo It will be created when you log your first application
)
echo.

echo [5/5] Checking Excel file...
if exist "data\jobs_applied\job_applicaiton.xlsx" (
    echo OK: Excel file exists
    dir "data\jobs_applied\job_applicaiton.xlsx"
) else (
    echo INFO: Excel file not created yet
    echo It will be created when you log your first application
)
echo.

echo ========================================
echo Test Results
echo ========================================
echo.
echo Container:  RUNNING
echo Backend:    WORKING
echo Job API:    WORKING
echo Data Dir:   READY
echo.
echo Next Steps:
echo 1. Open: http://localhost
echo 2. Click "Job Tracker" button
echo 3. Log a test application
echo 4. Check: data\jobs_applied\job_applicaiton.xlsx
echo.
pause
