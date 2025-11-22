$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Maya v3.0 - Auto Deploy to Railway" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Set-Location "C:\Users\delin\maya-ai"

Write-Host "[1/5] Checking git status..." -ForegroundColor Yellow
git status
Write-Host ""

Write-Host "[2/5] Adding requirements.txt..." -ForegroundColor Yellow
git add backend\requirements.txt
Write-Host "✓ File staged" -ForegroundColor Green
Write-Host ""

Write-Host "[3/5] Committing changes..." -ForegroundColor Yellow
git commit -m "Fix: Add missing tenacity dependency for email retry logic"
Write-Host "✓ Committed" -ForegroundColor Green
Write-Host ""

Write-Host "[4/5] Pushing to GitHub..." -ForegroundColor Yellow
git push
Write-Host "✓ Pushed to GitHub" -ForegroundColor Green
Write-Host ""

Write-Host "[5/5] Opening Railway dashboard..." -ForegroundColor Yellow
Start-Process "https://railway.app"
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ✅ DEPLOYMENT TRIGGERED!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Railway is now deploying your fix..." -ForegroundColor White
Write-Host "Check the browser window that just opened!" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to close..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
