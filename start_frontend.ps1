# PowerShell script to start Resume-Matcher frontend
# Run this from the Resume-Matcher directory

Write-Host "🚀 Starting Resume-Matcher Frontend..." -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "apps/frontend")) {
    Write-Host "❌ Please run this script from the Resume-Matcher root directory" -ForegroundColor Red
    exit 1
}

# Create .env.local if it doesn't exist
if (-not (Test-Path ".env.local")) {
    Write-Host "⚠️  .env.local file not found. Creating from template..." -ForegroundColor Yellow
    
    $envContent = @"
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8888

# Frontend Port
PORT=3333
"@
    
    $envContent | Out-File -FilePath ".env.local" -Encoding UTF8
    Write-Host "✅ Created .env.local file" -ForegroundColor Green
}

# Navigate to frontend directory
Set-Location "apps/frontend"

# Check if package.json needs port modification
$packageJson = Get-Content "package.json" -Raw | ConvertFrom-Json
if ($packageJson.scripts.dev -notmatch "3333") {
    Write-Host "📝 Updating package.json for port 3333..." -ForegroundColor Cyan
    
    # Backup original
    Copy-Item "package.json" "package.json.backup"
    
    # Update dev script
    $packageJson.scripts.dev = "next dev -p 3333"
    $packageJson | ConvertTo-Json -Depth 10 | Out-File "package.json" -Encoding UTF8
    
    Write-Host "✅ Updated package.json" -ForegroundColor Green
}

# Start the frontend server
Write-Host "🔥 Starting frontend server on port 3333..." -ForegroundColor Green
Write-Host "Frontend will be available at: http://localhost:3333" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow

npm run dev
