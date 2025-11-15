@echo off
echo ========================================
echo Restarting ATS Backend Server
echo ========================================
echo.
echo This will stop any running backend and start a fresh instance.
echo.
echo Press Ctrl+C to stop the server when needed.
echo.
pause

cd backend
python main.py
