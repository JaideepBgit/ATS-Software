# Download Piper TTS Model
# Downloads the en_US-lessac-medium voice model for Piper TTS

$MODEL_URL = "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx"
$CONFIG_URL = "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json"

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "Piper TTS Model Downloader" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan

# Create models directory
$modelsDir = "models"
if (-not (Test-Path $modelsDir)) {
    New-Item -ItemType Directory -Path $modelsDir | Out-Null
}
Write-Host "`n✓ Models directory: $((Get-Item $modelsDir).FullName)" -ForegroundColor Green

# Download model file
$modelPath = Join-Path $modelsDir "en_US-lessac-medium.onnx"
Write-Host "`n1. Downloading model file (~63 MB)..." -ForegroundColor Yellow

if (Test-Path $modelPath) {
    $size = (Get-Item $modelPath).Length
    if ($size -gt 1000000) {
        Write-Host "   Model already exists ($($size.ToString('N0')) bytes)" -ForegroundColor Green
        $response = Read-Host "   Download again? (y/n)"
        if ($response -ne 'y') {
            Write-Host "   Skipping model download" -ForegroundColor Yellow
        } else {
            Write-Host "   Downloading..." -ForegroundColor Yellow
            Invoke-WebRequest -Uri $MODEL_URL -OutFile $modelPath -UseBasicParsing
        }
    } else {
        Write-Host "   Existing file is corrupted ($size bytes), re-downloading..." -ForegroundColor Red
        Invoke-WebRequest -Uri $MODEL_URL -OutFile $modelPath -UseBasicParsing
    }
} else {
    Write-Host "   Downloading..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri $MODEL_URL -OutFile $modelPath -UseBasicParsing
}

# Verify model
if (Test-Path $modelPath) {
    $size = (Get-Item $modelPath).Length
    Write-Host "   ✓ Model downloaded: $($size.ToString('N0')) bytes" -ForegroundColor Green
    if ($size -lt 1000000) {
        Write-Host "   ⚠ Warning: File seems too small (expected ~63 MB)" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ✗ Model file not found after download" -ForegroundColor Red
    exit 1
}

# Download config file
$configPath = Join-Path $modelsDir "en_US-lessac-medium.onnx.json"
Write-Host "`n2. Downloading config file..." -ForegroundColor Yellow

if (Test-Path $configPath) {
    Write-Host "   Config already exists" -ForegroundColor Green
    $response = Read-Host "   Download again? (y/n)"
    if ($response -ne 'y') {
        Write-Host "   Skipping config download" -ForegroundColor Yellow
    } else {
        Write-Host "   Downloading..." -ForegroundColor Yellow
        Invoke-WebRequest -Uri $CONFIG_URL -OutFile $configPath -UseBasicParsing
    }
} else {
    Write-Host "   Downloading..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri $CONFIG_URL -OutFile $configPath -UseBasicParsing
}

# Verify config
if (Test-Path $configPath) {
    $size = (Get-Item $configPath).Length
    Write-Host "   ✓ Config downloaded: $($size.ToString('N0')) bytes" -ForegroundColor Green
} else {
    Write-Host "   ✗ Config file not found after download" -ForegroundColor Red
    exit 1
}

Write-Host "`n=====================================================================" -ForegroundColor Cyan
Write-Host "✓ DOWNLOAD COMPLETE!" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Cyan

$modelSize = (Get-Item $modelPath).Length
$configSize = (Get-Item $configPath).Length
$totalSize = $modelSize + $configSize

Write-Host "`nModel: $((Get-Item $modelPath).FullName)" -ForegroundColor White
Write-Host "Config: $((Get-Item $configPath).FullName)" -ForegroundColor White
Write-Host "`nTotal size: $($totalSize.ToString('N0')) bytes" -ForegroundColor White
Write-Host "`nYou can now run: python test_tts.py" -ForegroundColor Yellow
