@echo off
echo ========================================
echo Clearing ATS Analysis Results
echo ========================================
echo.

cd backend
python clear_results.py

echo.
echo Press any key to exit...
pause >nul
