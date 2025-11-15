# Piper TTS Setup Script for Windows
# This script downloads and sets up Piper TTS

Write-Host "=== Piper TTS Setup ===" -ForegroundColor Cyan
Write-Host ""

# Create directories
$modelsDir = "models"
$piperDir = "piper"

if (-not (Test-Path $modelsDir)) {
    New-Item -ItemType Directory -Path $modelsDir | Out-Null
    Write-Host "Created models directory" -ForegroundColor Green
}

if (-not (Test-Path $piperDir)) {
    New-Item -ItemType Directory -Path $piperDir | Out-Null
    Write-Host "Created piper directory" -ForegroundColor Green
}

Write-Host ""
Write-Host "Downloading Piper TTS..." -ForegroundColor Yellow

# Download Piper for Windows
$piperUrl = "https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_windows_amd64.zip"
$piperZip = "piper_windows_amd64.zip"

try {
    Invoke-WebRequest -Uri $piperUrl -OutFile $piperZip
    Write-Host "Downloaded Piper executable" -ForegroundColor Green
    
    # Extract
    Expand-Archive -Path $piperZip -DestinationPath $piperDir -Force
    Remove-Item $piperZip
    Write-Host "Extracted Piper" -ForegroundColor Green
} catch {
    Write-Host "Failed to download Piper" -ForegroundColor Red
    Write-Host "Please download manually from: https://github.com/rhasspy/piper/releases" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Downloading voice model (en_US-lessac-medium)..." -ForegroundColor Yellow

# Download voice model
$modelUrl = "https://github.com/rhasspy/piper/releases/download/v1.2.0/en_US-lessac-medium.onnx"
$modelJsonUrl = "https://github.com/rhasspy/piper/releases/download/v1.2.0/en_US-lessac-medium.onnx.json"

try {
    $modelPath = Join-Path $modelsDir "en_US-lessac-medium.onnx"
    $modelJsonPath = Join-Path $modelsDir "en_US-lessac-medium.onnx.json"
    
    Invoke-WebRequest -Uri $modelUrl -OutFile $modelPath
    Write-Host "Downloaded model file" -ForegroundColor Green
    
    Invoke-WebRequest -Uri $modelJsonUrl -OutFile $modelJsonPath
    Write-Host "Downloaded model config" -ForegroundColor Green
} catch {
    Write-Host "Failed to download model" -ForegroundColor Red
    Write-Host "Please download manually from: https://github.com/rhasspy/piper/releases" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Testing Piper TTS..." -ForegroundColor Yellow

# Test Piper
$piperExe = Join-Path $piperDir "piper\piper.exe"
if (Test-Path $piperExe) {
    try {
        $testText = "Hello! This is a test of Piper TTS."
        $testOutput = "test_output.wav"
        $modelFile = Join-Path $modelsDir "en_US-lessac-medium.onnx"
        
        $testText | & $piperExe --model $modelFile --output_file $testOutput
        
        if (Test-Path $testOutput) {
            Write-Host "TTS test successful! Audio file created: $testOutput" -ForegroundColor Green
            Write-Host "You can play it to verify the voice quality." -ForegroundColor Cyan
        } else {
            Write-Host "TTS test failed - no audio file created" -ForegroundColor Red
        }
    } catch {
        Write-Host "TTS test failed" -ForegroundColor Red
    }
} else {
    Write-Host "Piper executable not found at: $piperExe" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Setup Complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Update tts_service.py with the correct paths if needed" -ForegroundColor White
Write-Host "2. Run: python tts_service.py (to test)" -ForegroundColor White
Write-Host "3. Start your backend server: python main.py" -ForegroundColor White
Write-Host ""
$piperExePath = Join-Path $piperDir "piper\piper.exe"
$modelLocation = Join-Path $modelsDir "en_US-lessac-medium.onnx"
Write-Host "Piper executable: $piperExePath" -ForegroundColor Cyan
Write-Host "Model location: $modelLocation" -ForegroundColor Cyan
Write-Host ""
