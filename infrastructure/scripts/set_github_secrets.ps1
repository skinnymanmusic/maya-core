# GitHub Secrets Setup Script
# This script sets the required secrets for Azure OIDC authentication

$ErrorActionPreference = "Stop"

# Configuration
$REPO_OWNER = "skinnymanmusic"
$REPO_NAME = "maya-core"
$AZURE_CLIENT_ID = "484cbfab-19ef-4bd9-9af0-b3c9ba770ae1"
$AZURE_TENANT_ID = "7f41cfaa-7c09-424e-b7dd-aec5d8d400d9"
$AZURE_SUBSCRIPTION_ID = "8195bf9f-e930-4f0d-8236-9526882d6f32"

Write-Host "Setting GitHub Secrets for $REPO_OWNER/$REPO_NAME..." -ForegroundColor Green
Write-Host ""

# Try using gh CLI
$ghPath = "C:\Program Files\GitHub CLI\gh.exe"
if (Test-Path $ghPath) {
    Write-Host "Using GitHub CLI to set secrets..." -ForegroundColor Cyan

    try {
        & $ghPath secret set AZURE_CLIENT_ID --body $AZURE_CLIENT_ID --repo "$REPO_OWNER/$REPO_NAME"
        Write-Host "  [OK] AZURE_CLIENT_ID set" -ForegroundColor Green

        & $ghPath secret set AZURE_TENANT_ID --body $AZURE_TENANT_ID --repo "$REPO_OWNER/$REPO_NAME"
        Write-Host "  [OK] AZURE_TENANT_ID set" -ForegroundColor Green

        & $ghPath secret set AZURE_SUBSCRIPTION_ID --body $AZURE_SUBSCRIPTION_ID --repo "$REPO_OWNER/$REPO_NAME"
        Write-Host "  [OK] AZURE_SUBSCRIPTION_ID set" -ForegroundColor Green

        Write-Host ""
        Write-Host "All secrets set successfully!" -ForegroundColor Green
        exit 0
    }
    catch {
        Write-Host "  [WARN] gh CLI failed. You may need to run: gh auth login" -ForegroundColor Yellow
        Write-Host ""
    }
}

Write-Host "Please set these secrets manually:" -ForegroundColor Yellow
Write-Host ""
Write-Host "Go to: https://github.com/$REPO_OWNER/$REPO_NAME/settings/secrets/actions" -ForegroundColor Cyan
Write-Host ""
Write-Host "Secret Name: AZURE_CLIENT_ID" -ForegroundColor White
Write-Host "Value: $AZURE_CLIENT_ID" -ForegroundColor Gray
Write-Host ""
Write-Host "Secret Name: AZURE_TENANT_ID" -ForegroundColor White
Write-Host "Value: $AZURE_TENANT_ID" -ForegroundColor Gray
Write-Host ""
Write-Host "Secret Name: AZURE_SUBSCRIPTION_ID" -ForegroundColor White
Write-Host "Value: $AZURE_SUBSCRIPTION_ID" -ForegroundColor Gray
Write-Host ""
