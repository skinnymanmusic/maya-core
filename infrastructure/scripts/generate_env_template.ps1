# ======================================================
# MayAssistant — Railway Env Template Generator
# PowerShell Version (Windows Compatible)
# Mode: Smart Auto-Detect (Option B)
# ======================================================
# This script:
#  - Checks for existing env values in local .env* files
#  - Prompts only for missing values
#  - Generates secure JWT + ENCRYPTION keys if missing
#  - Writes a ready-to-paste .env template for Railway
#  - Prints the block to console for copy/paste
# ======================================================

Write-Host "=== MayAssistant: Railway Env Template Generator ===`n"

# ---------- Helper: Try to load existing values from local .env files ----------

$existingEnv = @{}

function Load-EnvFromFile($path) {
    if (Test-Path $path) {
        Write-Host "Loading existing values from $path"
        Get-Content $path | ForEach-Object {
            if ($_ -match '^\s*#') { return }
            if ($_ -match '^\s*$') { return }
            $parts = $_ -split '=', 2
            if ($parts.Count -eq 2) {
                $key = $parts[0].Trim()
                $val = $parts[1].Trim()
                if (-not [string]::IsNullOrWhiteSpace($key) -and -not $existingEnv.ContainsKey($key)) {
                    $existingEnv[$key] = $val
                }
            }
        }
    }
}

# Look for common env files
Load-EnvFromFile ".env"
Load-EnvFromFile "backend/.env"
Load-EnvFromFile ".env.local"
Load-EnvFromFile ".env.railway"
Load-EnvFromFile ".env.maya"

function Get-OrPrompt([string]$key, [string]$prompt, [bool]$isSecret = $false) {
    if ($existingEnv.ContainsKey($key) -and -not [string]::IsNullOrWhiteSpace($existingEnv[$key])) {
        Write-Host "$key found in local env files. Reusing existing value."
        return $existingEnv[$key]
    }

    Write-Host ""
    Write-Host $prompt

    if ($isSecret) {
        $secure = Read-Host -AsSecureString
        $bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
        $plain = [Runtime.InteropServices.Marshal]::PtrToStringAuto($bstr)
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
        return $plain
    } else {
        $val = Read-Host
        return $val
    }
}

# ---------- Collect values (auto-detect + prompt) ----------

# DATABASE_URL
$DATABASE_URL = Get-OrPrompt `
    -key "DATABASE_URL" `
    -prompt "Enter your Supabase DATABASE_URL (from Supabase → Settings → Connection String):"

# DEFAULT_TENANT_ID
if ($existingEnv.ContainsKey("DEFAULT_TENANT_ID")) {
    $DEFAULT_TENANT_ID = $existingEnv["DEFAULT_TENANT_ID"]
    Write-Host "`nDEFAULT_TENANT_ID found. Using: $DEFAULT_TENANT_ID"
} else {
    $DEFAULT_TENANT_ID = "default"
    Write-Host "`nDEFAULT_TENANT_ID not found. Using default value: default"
}

# JWT_SECRET_KEY
if ($existingEnv.ContainsKey("JWT_SECRET_KEY")) {
    $JWT_SECRET_KEY = $existingEnv["JWT_SECRET_KEY"]
    Write-Host "`nJWT_SECRET_KEY found. Reusing existing value."
} else {
    Write-Host "`nGenerating JWT_SECRET_KEY (64-char hex)..."
    $JWT_SECRET_KEY = (New-Guid).Guid.Replace("-", "") + (New-Guid).Guid.Substring(0, 16)
}

# ENCRYPTION_KEY
if ($existingEnv.ContainsKey("ENCRYPTION_KEY")) {
    $ENCRYPTION_KEY = $existingEnv["ENCRYPTION_KEY"]
    Write-Host "`nENCRYPTION_KEY found. Reusing existing value."
} else {
    Write-Host "`nGenerating ENCRYPTION_KEY (32-byte base64)..."
    $bytes = New-Object byte[] 32
    (New-Object System.Security.Cryptography.RNGCryptoServiceProvider).GetBytes($bytes)
    $ENCRYPTION_KEY = [System.Convert]::ToBase64String($bytes)
}

# ANTHROPIC_API_KEY
$ANTHROPIC_API_KEY = Get-OrPrompt `
    -key "ANTHROPIC_API_KEY" `
    -prompt "Enter your ANTHROPIC_API_KEY (Claude API Key):" `
    -isSecret $true

# GMAIL_WEBHOOK_URL (optional – can be updated after Railway deploy)
if ($existingEnv.ContainsKey("GMAIL_WEBHOOK_URL")) {
    $GMAIL_WEBHOOK_URL = $existingEnv["GMAIL_WEBHOOK_URL"]
    Write-Host "`nGMAIL_WEBHOOK_URL found. Reusing existing value."
} else {
    Write-Host "`nGMAIL_WEBHOOK_URL can be set after Railway exposes your domain."
    $GMAIL_WEBHOOK_URL = "https://UPDATE_ME.railway.app/api/gmail/webhook"
}

# Optional Gmail Pub/Sub values
if ($existingEnv.ContainsKey("GMAIL_PUBSUB_TOPIC")) {
    $GMAIL_PUBSUB_TOPIC = $existingEnv["GMAIL_PUBSUB_TOPIC"]
} else {
    $GMAIL_PUBSUB_TOPIC = ""
}
if ($existingEnv.ContainsKey("GMAIL_PUBSUB_SERVICE_ACCOUNT")) {
    $GMAIL_PUBSUB_SERVICE_ACCOUNT = $existingEnv["GMAIL_PUBSUB_SERVICE_ACCOUNT"]
} else {
    $GMAIL_PUBSUB_SERVICE_ACCOUNT = ""
}

# ---------- Build template content ----------

$lines = @()
$lines += "DATABASE_URL=$DATABASE_URL"
$lines += "DEFAULT_TENANT_ID=$DEFAULT_TENANT_ID"
$lines += "JWT_SECRET_KEY=$JWT_SECRET_KEY"
$lines += "ENCRYPTION_KEY=$ENCRYPTION_KEY"
$lines += "ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY"
$lines += "GMAIL_WEBHOOK_URL=$GMAIL_WEBHOOK_URL"
$lines += "GMAIL_PUBSUB_TOPIC=$GMAIL_PUBSUB_TOPIC"
$lines += "GMAIL_PUBSUB_SERVICE_ACCOUNT=$GMAIL_PUBSUB_SERVICE_ACCOUNT"

$templatePath = "infrastructure/.env.railway.template"
$templateDir = Split-Path $templatePath -Parent
if (-not (Test-Path $templateDir)) {
    New-Item -ItemType Directory -Path $templateDir | Out-Null
}

$lines | Set-Content -Path $templatePath -Encoding UTF8

Write-Host "`n======================================================="
Write-Host " TEMPLATE GENERATED: $templatePath"
Write-Host "=======================================================`n"
Write-Host "Copy the following block into Railway → Variables → Raw Editor:`n"

$lines | ForEach-Object { Write-Host $_ }

Write-Host "`nDone. After pasting and saving in Railway, you can proceed with backend deployment."

# END OF FILE

