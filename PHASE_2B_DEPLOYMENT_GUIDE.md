# PHASE 2B: PRODUCTION DEPLOYMENT TO RAILWAY
**Date:** 2025-01-27  
**Status:** READY FOR DEPLOYMENT

---

## DEPLOYMENT OPTIONS

### Option 1: Deploy via Railway Dashboard (Recommended)

**Steps:**
1. **Connect Repository:**
   - Go to Railway dashboard: https://railway.app
   - Create new project or select existing project
   - Click "New" → "GitHub Repo"
   - Select your `maya-ai` repository
   - Railway will auto-detect the backend

2. **Configure Service:**
   - Railway should detect `backend/` directory
   - If not, set root directory to `backend/`
   - Verify build settings:
     - Builder: Nixpacks (auto-detected)
     - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **Set Environment Variables:**
   - Go to service → Variables tab
   - Paste the variables from `infrastructure/.env.railway.template`
   - Or use the values generated earlier:
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

4. **Deploy:**
   - Railway will automatically deploy on git push
   - Or click "Deploy" button to trigger manual deployment
   - Monitor build logs in Railway dashboard

5. **Get Deployment URL:**
   - After deployment, Railway will provide a domain
   - Example: `https://your-service-name.up.railway.app`
   - Update `GMAIL_WEBHOOK_URL` with this domain

---

### Option 2: Deploy via Railway CLI

**Prerequisites:**
- Railway CLI authenticated: `railway login`
- Project linked: `railway link`

**Steps:**
1. **Authenticate:**
   ```powershell
   railway login
   ```

2. **Link Project:**
   ```powershell
   cd backend
   railway link
   ```

3. **Deploy:**
   ```powershell
   railway up
   ```

4. **Monitor:**
   ```powershell
   railway logs
   ```

---

## POST-DEPLOYMENT HEALTH CHECKS

After deployment completes, verify the following endpoints:

### 1. Health Check
```bash
GET https://your-service.up.railway.app/api/health/
```

**Expected Response:**
```json
{
  "status": "healthy",
  "database": true,
  "encryption": true,
  "timestamp": "2025-01-27T...",
  "version": "3.0.0"
}
```

### 2. Database Health
```bash
GET https://your-service.up.railway.app/api/health/db
```

**Expected Response:**
```json
{
  "status": "ok",
  "message": "Database connection successful"
}
```

### 3. System Status
```bash
GET https://your-service.up.railway.app/api/system/status
```

### 4. Email Test
```bash
GET https://your-service.up.railway.app/api/email/test
```

### 5. Calendar Ping
```bash
GET https://your-service.up.railway.app/api/calendar/ping
```

---

## WORKER PROCESSES

Verify worker processes are running:

1. **Payment Reminder Worker:**
   - Check Railway logs for `payment_reminder_worker`
   - Should see: "Payment Reminder Worker started"

2. **Email Retry Worker:**
   - Check Railway logs for `email_retry_worker`
   - Should see: "Email Retry Worker started"

3. **Guardian Daemon:**
   - Check Railway logs for `guardian_daemon`
   - Should see: "Guardian Daemon started"

**Note:** Workers are defined in `Procfile` and should start automatically.

---

## TROUBLESHOOTING

### Build Fails
- Check Railway build logs
- Verify `requirements.txt` is in `backend/` directory
- Verify Python version in `nixpacks.toml` (python311)

### Application Crashes
- Check Railway logs for error messages
- Verify all environment variables are set
- Verify `DATABASE_URL` is correct and accessible

### Health Check Fails
- Check database connection
- Verify `ENCRYPTION_KEY` is valid (44 chars, base64)
- Check Railway logs for specific errors

### Workers Not Starting
- Verify `Procfile` is in `backend/` directory
- Check Railway service settings for worker processes
- Verify environment variables are accessible to workers

---

## NEXT STEPS

After successful deployment and health checks:
1. ✅ Update `GMAIL_WEBHOOK_URL` with actual Railway domain
2. ✅ Proceed to Phase 2C - Pack Configs Activation
3. ✅ Generate POST_DEPLOY_HEALTHCHECK_REPORT.md

---

**END OF PHASE 2B DEPLOYMENT GUIDE**

