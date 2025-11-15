@echo off
echo Testing Piper TTS Installation...
echo.

REM Check if piper.exe exists
if not exist "piper\piper\piper.exe" (
    echo [ERROR] Piper executable not found!
    echo Expected location: piper\piper\piper.exe
    echo Please follow MANUAL_SETUP.md to download Piper
    pause
    exit /b 1
)
echo [OK] Piper executable found

REM Check if model exists
if not exist "models\en_US-lessac-medium.onnx" (
    echo [ERROR] Voice model not found!
    echo Expected location: models\en_US-lessac-medium.onnx
    echo Please follow MANUAL_SETUP.md to download the model
    pause
    exit /b 1
)
echo [OK] Voice model found

REM Test TTS generation
echo.
echo Generating test audio...
echo Hello! This is a test of Piper TTS for the ATS system. | piper\piper\piper.exe --model models\en_US-lessac-medium.onnx --output_file test_output.wav

if exist "test_output.wav" (
    echo.
    echo [SUCCESS] Audio file generated: test_output.wav
    echo You can play this file to verify the voice quality.
    echo.
    echo Starting audio playback...
    start test_output.wav
) else (
    echo [ERROR] Failed to generate audio file
    pause
    exit /b 1
)

echo.
echo ========================================
echo Piper TTS is working correctly!
echo ========================================
echo.
echo Next steps:
echo 1. Test Python service: python tts_service.py
echo 2. Start backend: python main.py
echo 3. Use the Listen button in the UI
echo.
pause
