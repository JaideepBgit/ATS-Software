@echo off
echo ========================================
echo Downloading Piper TTS Model
echo ========================================
echo.
echo This will download the voice model (~63 MB)
echo.
pause

powershell -ExecutionPolicy Bypass -File download_model.ps1

echo.
echo ========================================
echo Done!
echo ========================================
pause
