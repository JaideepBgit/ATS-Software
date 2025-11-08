# PowerShell script to start Resume-Matcher backend with LM Studio
# Run this from the Resume-Matcher directory

Write-Host "🚀 Starting Resume-Matcher Backend with LM Studio..." -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "apps/backend")) {
    Write-Host "❌ Please run this script from the Resume-Matcher root directory" -ForegroundColor Red
    exit 1
}

# Navigate to backend directory
Set-Location "apps/backend"

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  .env file not found. Creating from template..." -ForegroundColor Yellow
    
    $envContent = @"
# LM Studio Configuration
LLM_URL=http://127.0.0.1:1234/v1
MODEL_NAME=gemma-3n-e4b
API_KEY=lm-studio

# Backend Port Configuration
PORT=8888

# Frontend URL for CORS
CORS_ORIGIN=http://localhost:3333

# Database Configuration
DATABASE_URL=sqlite:///./resume_matcher.db

# Other Configuration
DEBUG=true
LOG_LEVEL=info
"@
    
    $envContent | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "✅ Created .env file" -ForegroundColor Green
}

# Install additional requirements if needed
if (Test-Path "requirements_lmstudio.txt") {
    Write-Host "📦 Installing LM Studio requirements..." -ForegroundColor Cyan
    pip install -r requirements_lmstudio.txt
}

# Start the backend server
Write-Host "🔥 Starting backend server on port 8888..." -ForegroundColor Green
Write-Host "Backend will be available at: http://localhost:8888" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow

python -m uvicorn app.main:app --reload --port 8888 --host 0.0.0.0
