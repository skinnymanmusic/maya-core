# SET ENVIRONMENT VARIABLES - QUICK GUIDE
**Date:** 2025-01-27  
**Purpose:** Guide for setting Railway environment variables before backend deployment

---

## OPTION 1: Use PowerShell Template Generator (Recommended)

**Script:** `infrastructure/scripts/generate_env_template.ps1`

**What it does:**
- Auto-detects existing values from local `.env` files
- Prompts only for missing values
- Generates secure JWT and ENCRYPTION keys automatically
- Creates a ready-to-paste template file

**Steps:**
1. Open PowerShell in the project root
2. Run:
   ```powershell
   .\infrastructure\scripts\generate_env_template.ps1
   ```
3. Follow prompts to enter:
   - `DATABASE_URL` (from Supabase)
   - `ANTHROPIC_API_KEY` (from Claude console)
4. Script will generate:
   - `JWT_SECRET_KEY` (auto-generated)
   - `ENCRYPTION_KEY` (auto-generated)
   - Template file at `infrastructure/.env.railway.template`
5. Copy the output block and paste into Railway → Variables → Raw Editor

---

## OPTION 2: Use Railway CLI Script

**Script:** `infrastructure/scripts/set_railway_env.ps1`

**What it does:**
- Sets variables directly in Railway via CLI
- Auto-generates JWT_SECRET_KEY and ENCRYPTION_KEY
- Sets placeholders for values you need to update manually

**Steps:**
1. Ensure Railway CLI is installed and authenticated:
   ```powershell
   railway login
   ```
2. Navigate to your Railway project
3. Run:
   ```powershell
   .\infrastructure\scripts\set_railway_env.ps1
   ```
4. **IMPORTANT:** After script runs, manually update:
   - `DATABASE_URL` (replace `UPDATE_ME` with actual Supabase connection string)
   - `ANTHROPIC_API_KEY` (replace `UPDATE_ME` with actual Claude API key)
   - `GMAIL_WEBHOOK_URL` (update after Railway deploy exposes domain)

---

## OPTION 3: Manual Setup in Railway Dashboard

**Steps:**
1. Go to Railway dashboard → Your project → Your service
2. Click "Variables" tab
3. Add each variable manually:

### Required Variables (8):

1. **DATABASE_URL**
   - Get from: Supabase → Settings → Connection String
   - Format: `postgresql://user:password@host:port/database`

2. **DEFAULT_TENANT_ID**
   - Value: `default` (or your actual tenant UUID)

3. **JWT_SECRET_KEY**
   - Generate: `python -c "import secrets; print(secrets.token_hex(32))"`
   - Or use: PowerShell script auto-generation
   - Min length: 32 characters

4. **ENCRYPTION_KEY**
   - Generate: `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`
   - Or use: PowerShell script auto-generation
   - Format: 44-character base64 string

5. **ANTHROPIC_API_KEY**
   - Get from: https://console.anthropic.com/
   - Format: `sk-ant-api03-...`

6. **GMAIL_WEBHOOK_URL**
   - Format: `https://YOUR-RAILWAY-DOMAIN.railway.app/api/gmail/webhook`
   - Can be set after initial deployment

7. **GMAIL_PUBSUB_TOPIC** (Optional)
   - Format: `projects/PROJECT/topics/TOPIC`
   - Can be empty initially

8. **GMAIL_PUBSUB_SERVICE_ACCOUNT** (Optional)
   - Format: `service-account@project.iam.gserviceaccount.com`
   - Can be empty initially

---

## VERIFICATION

After setting variables, verify in Railway:
1. Go to Variables tab
2. Confirm all 8 required variables are present
3. Check that `JWT_SECRET_KEY` and `ENCRYPTION_KEY` are set (not placeholders)

---

## NEXT STEPS

Once environment variables are set:
1. ✅ Proceed to Phase 2B - Production Deployment to Railway
2. ✅ After deployment, verify health endpoints
3. ✅ Update `GMAIL_WEBHOOK_URL` with actual Railway domain

---

**END OF SET ENV VARIABLES GUIDE**

