@echo off
echo ========================================
echo Piper TTS Download Helper
echo ========================================
echo.

REM Create directories
if not exist "models" mkdir models
if not exist "piper" mkdir piper

echo Downloading Piper executable (10MB)...
curl -L -o piper_windows_amd64.zip https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_windows_amd64.zip

if exist "piper_windows_amd64.zip" (
    echo [OK] Downloaded Piper
    echo Extracting...
    tar -xf piper_windows_amd64.zip -C piper
    del piper_windows_amd64.zip
    echo [OK] Extracted Piper
) else (
    echo [ERROR] Failed to download Piper
    echo Please download manually from: https://github.com/rhasspy/piper/releases
)

echo.
echo Downloading voice model (25MB)...
curl -L -o models\en_US-lessac-medium.onnx https://github.com/rhasspy/piper/releases/download/v1.2.0/en_US-lessac-medium.onnx

if exist "models\en_US-lessac-medium.onnx" (
    echo [OK] Downloaded model file
) else (
    echo [ERROR] Failed to download model
)

echo.
echo Downloading model config...
curl -L -o models\en_US-lessac-medium.onnx.json https://github.com/rhasspy/piper/releases/download/v1.2.0/en_US-lessac-medium.onnx.json

if exist "models\en_US-lessac-medium.onnx.json" (
    echo [OK] Downloaded model config
) else (
    echo [ERROR] Failed to download model config
)

echo.
echo ========================================
echo Download Complete!
echo ========================================
echo.
echo Testing installation...
call test_piper.bat
