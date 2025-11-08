@echo off
echo ========================================
echo Installing ATS Requirements
echo ========================================
echo.
echo Installing Python packages...
echo.
pip install -r requirements_advanced.txt
echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Start LM Studio
echo 2. Load model: google/gemma-3n-e4b
echo 3. Click "Start Server"
echo 4. Run: TEST_SETUP.bat
echo.
pause
