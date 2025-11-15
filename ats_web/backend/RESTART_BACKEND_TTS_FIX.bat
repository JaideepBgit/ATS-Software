@echo off
echo ========================================
echo Restarting Backend with TTS Fix
echo ========================================
echo.
echo This will restart the backend server with the TTS debugging improvements.
echo.
echo Press Ctrl+C to stop the server when needed.
echo.
pause

cd /d "%~dp0"
uvicorn main:app --reload --host 0.0.0.0 --port 8000
