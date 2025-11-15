@echo off
echo ========================================
echo Testing ATS Storage System
echo ========================================
echo.
echo Make sure the backend is running first!
echo Press Ctrl+C to cancel, or
pause

python test_storage_system.py

echo.
echo ========================================
echo Test Complete!
echo ========================================
pause
