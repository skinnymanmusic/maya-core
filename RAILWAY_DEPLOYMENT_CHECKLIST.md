# RAILWAY DEPLOYMENT CHECKLIST
**Date:** 2025-01-27  
**Repository:** https://github.com/skinnymanmusic/maya-core  
**Status:** READY FOR DEPLOYMENT

---

## PRE-DEPLOYMENT CHECKLIST

### ✅ Repository Setup
- [x] Code pushed to `maya-core` repository
- [x] All deployment files present (`railway.json`, `nixpacks.toml`, `Procfile`, `requirements.txt`)
- [x] Backend directory structure correct
- [x] Secrets removed from commit history

### ⚠️ Railway Setup (Required)
- [ ] Railway account created/logged in
- [ ] New project created in Railway
- [ ] GitHub repository connected to Railway
- [ ] Service configured (root directory: `backend/`)
- [ ] Environment variables set (8 required)

---

## STEP-BY-STEP DEPLOYMENT INSTRUCTIONS

### Step 1: Create Railway Project

1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Authorize Railway to access your GitHub account
5. Select repository: `skinnymanmusic/maya-core`
6. Railway will auto-detect the project

### Step 2: Configure Service

1. **Set Root Directory:**
   - Go to service settings
   - Set "Root Directory" to `backend`
   - This tells Railway where your `requirements.txt` and `Procfile` are

2. **Verify Build Settings:**
   - Builder: Nixpacks (auto-detected)
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT` (from `railway.json`)

### Step 3: Set Environment Variables

Go to service → Variables tab and add:

```
DATABASE_URL=postgresql://postgres:L_yRCLBEJAp7xuf@db.brmljgxrpksxfazkguej.supabase.co:5432/postgres
DEFAULT_TENANT_ID=will-be-created-on-first-run
JWT_SECRET_KEY=ZQJAG2k7vGcqVgz2GIFRQFOWZdFslk7CMD65gZnaIak=
ENCRYPTION_KEY=MMyg2Z_DeYqvkcWRjFZU-h0a1fsRh9gsL7kZmLgbXDk=
ANTHROPIC_API_KEY=sk-ant-api03-UPDATE_ME_WITH_YOUR_CLAUDE_API_KEY
GMAIL_WEBHOOK_URL=https://UPDATE_ME.railway.app/api/gmail/webhook
GMAIL_PUBSUB_TOPIC=
GMAIL_PUBSUB_SERVICE_ACCOUNT=
```

**Important:** 
- Replace `ANTHROPIC_API_KEY` with your actual Claude API key
- `GMAIL_WEBHOOK_URL` will be updated after deployment (replace `UPDATE_ME` with your Railway domain)

### Step 4: Deploy

1. Railway will automatically start building after you:
   - Connect the repository (auto-deploys on push)
   - Or click "Deploy" button manually

2. Monitor build logs:
   - Click on the deployment
   - Watch for build progress
   - Check for any errors

3. **Expected Build Steps:**
   - Installing Python 3.11
   - Installing PostgreSQL
   - Running `pip install -r requirements.txt`
   - Starting application

### Step 5: Get Deployment URL

1. After successful deployment:
   - Railway will provide a domain (e.g., `maya-core-production.up.railway.app`)
   - Copy this domain

2. **Update GMAIL_WEBHOOK_URL:**
   - Go back to Variables
   - Update `GMAIL_WEBHOOK_URL` to: `https://YOUR-DOMAIN.railway.app/api/gmail/webhook`
   - Railway will automatically redeploy

### Step 6: Verify Worker Processes

Railway should automatically start all processes from `Procfile`:
- `web` - Main FastAPI application
- `worker` - Payment reminder worker
- `guardian-daemon` - Guardian framework daemon
- `email-retry-worker` - Email retry queue worker

**Note:** Railway may require you to configure these as separate services or use a process manager.

---

## POST-DEPLOYMENT HEALTH CHECKS

After deployment, verify these endpoints:

### 1. Health Check
```bash
GET https://your-domain.railway.app/api/health/
```

**Expected:**
```json
{
  "status": "healthy",
  "database": true,
  "encryption": true,
  "timestamp": "...",
  "version": "3.0.0"
}
```

### 2. Database Health
```bash
GET https://your-domain.railway.app/api/health/db
```

### 3. System Status
```bash
GET https://your-domain.railway.app/api/system/status
```

### 4. Email Test
```bash
GET https://your-domain.railway.app/api/email/test
```

### 5. Calendar Ping
```bash
GET https://your-domain.railway.app/api/calendar/ping
```

---

## TROUBLESHOOTING

### Build Fails
- Check Railway build logs
- Verify `backend/requirements.txt` exists
- Verify Python version in `nixpacks.toml`

### Application Crashes
- Check Railway logs
- Verify all environment variables are set
- Verify `DATABASE_URL` is accessible

### Health Check Fails
- Check database connection
- Verify `ENCRYPTION_KEY` format (44 chars, base64)
- Check Railway logs for errors

### Workers Not Starting
- Railway may require separate service configuration
- Check `Procfile` format
- Verify process commands are correct

---

## NEXT STEPS AFTER DEPLOYMENT

1. ✅ Run health checks (see above)
2. ✅ Update `GMAIL_WEBHOOK_URL` with actual domain
3. ✅ Verify all worker processes are running
4. ✅ Generate POST_DEPLOY_HEALTHCHECK_REPORT.md
5. ✅ Proceed to Phase 2C - Pack Configs Activation

---

**END OF RAILWAY DEPLOYMENT CHECKLIST**

