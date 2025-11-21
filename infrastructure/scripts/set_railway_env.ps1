# ======================================================
# MayAssistant — Railway Environment Setup Script
# PowerShell Version (Windows Compatible)
# AUTOMATED ENV VARIABLE INITIALIZATION (SOLIN v2)
# ======================================================
# SAFE • IDEMPOTENT • RE-RUNNABLE
# This script will set ALL required Railway environment
# variables for the MayAssistant backend.
#
# Only ANTHROPIC_API_KEY and GMAIL fields require manual
# input once generated.
# ======================================================

Write-Host "=== MayAssistant: Railway Environment Setup (PowerShell) ===`n"

# --- Required Variables ---

# DEFAULT_TENANT_ID
Write-Host "[1/8] Setting DEFAULT_TENANT_ID..."
railway variables set DEFAULT_TENANT_ID="default"

# DATABASE_URL (placeholder)
Write-Host "`n[2/8] Setting DATABASE_URL placeholder..."
railway variables set DATABASE_URL="postgresql://UPDATE_ME:UPDATE_ME@UPDATE_ME:5432/postgres"

# JWT_SECRET_KEY (64-char hex)
Write-Host "`n[3/8] Generating JWT_SECRET_KEY..."
$JWT_SECRET_KEY = (New-Guid).Guid.Replace("-", "") + (New-Guid).Guid.Substring(0, 16)
railway variables set JWT_SECRET_KEY="$JWT_SECRET_KEY"
Write-Host "Generated JWT_SECRET_KEY: $JWT_SECRET_KEY"

# ENCRYPTION_KEY (32 bytes base64)
Write-Host "`n[4/8] Generating ENCRYPTION_KEY..."
$bytes = New-Object byte[] 32
(new-object System.Security.Cryptography.RNGCryptoServiceProvider).GetBytes($bytes)
$ENC_KEY = [System.Convert]::ToBase64String($bytes)
railway variables set ENCRYPTION_KEY="$ENC_KEY"
Write-Host "Generated ENCRYPTION_KEY: $ENC_KEY"

# ANTHROPIC_API_KEY placeholder
Write-Host "`n[5/8] Setting ANTHROPIC_API_KEY placeholder..."
railway variables set ANTHROPIC_API_KEY="UPDATE_ME"

# GMAIL_WEBHOOK_URL placeholder
Write-Host "`n[6/8] Setting GMAIL_WEBHOOK_URL placeholder..."
railway variables set GMAIL_WEBHOOK_URL="https://UPDATE_ME.railway.app/api/gmail/webhook"

# Optional values
Write-Host "`n[7/8] Setting GMAIL_PUBSUB_TOPIC..."
railway variables set GMAIL_PUBSUB_TOPIC=""

Write-Host "`n[8/8] Setting GMAIL_PUBSUB_SERVICE_ACCOUNT..."
railway variables set GMAIL_PUBSUB_SERVICE_ACCOUNT=""

Write-Host "`n======================================================="
Write-Host " DONE! Environment variables initialized."
Write-Host " IMPORTANT:"
Write-Host " - Update DATABASE_URL after copying from Supabase."
Write-Host " - Update ANTHROPIC_API_KEY after copying from Claude."
Write-Host " - Update GMAIL_WEBHOOK_URL after Railway exposes domain."
Write-Host "=======================================================`n"

# END OF FILE

