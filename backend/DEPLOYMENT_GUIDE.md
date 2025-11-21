# MAYA v3.0 - PRODUCTION DEPLOYMENT GUIDE

## 📋 Pre-Deployment Checklist

### Backend Environment Variables

All these variables must be set in Railway before deployment:

#### Required Variables:
```bash
# Application
APP_NAME=OMEGA Core v3.0
APP_VERSION=3.0.0
DEBUG=false

# Database
DATABASE_URL=postgresql://user:password@host:port/dbname
DATABASE_SSL=true

# Default Tenant
DEFAULT_TENANT_ID=your-tenant-uuid

# JWT Authentication
JWT_SECRET_KEY=your-secret-key-min-32-chars
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Encryption
ENCRYPTION_KEY=your-fernet-key-base64

# Anthropic Claude
ANTHROPIC_API_KEY=sk-ant-api03-...
CLAUDE_MODEL=claude-sonnet-4-20250514
CLAUDE_MAX_TOKENS=4096

# Google APIs
GMAIL_WEBHOOK_URL=https://your-railway-url.up.railway.app/api/gmail/webhook
GMAIL_PUBSUB_TOPIC=projects/PROJECT/topics/TOPIC
GMAIL_PUBSUB_SERVICE_ACCOUNT=service-account@project.iam.gserviceaccount.com

# Stripe
STRIPE_API_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_BUSINESS_NAME=Skinny Man Entertainment
STRIPE_BUSINESS_SUPPORT_EMAIL=maya@skinnymanmusic.com
STRIPE_BUSINESS_RETURN_URL=https://mayassistant.com/booking-confirmed

# Twilio
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_PHONE_NUMBER=+12345678900

# Optional: OpenAI (Hybrid LLM)
OPENAI_API_KEY=sk-... (optional)
OPENAI_MODEL=gpt-4o

# Optional: Google OAuth (SSO)
GOOGLE_OAUTH_CLIENT_ID=... (optional)
GOOGLE_OAUTH_CLIENT_SECRET=... (optional)
GOOGLE_OAUTH_REDIRECT_URI=... (optional)

# Optional: Microsoft OAuth (SSO)
MICROSOFT_OAUTH_CLIENT_ID=... (optional)
MICROSOFT_OAUTH_CLIENT_SECRET=... (optional)
MICROSOFT_OAUTH_REDIRECT_URI=... (optional)
MICROSOFT_OAUTH_TENANT=common
```

### Frontend Environment Variables

Set these in Vercel:

```bash
NEXT_PUBLIC_OMEGA_BACKEND=https://your-railway-url.up.railway.app
NEXT_PUBLIC_APP_URL=https://mayassistant.com
```

---

## 🚂 Railway Deployment (Backend)

### Step 1: Create Railway Project

1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `maya-ai` repository
5. Select `backend/` as the root directory

### Step 2: Configure Build Settings

Railway will auto-detect Python, but verify:
- **Build Command:** (auto-detected)
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Root Directory:** `backend`

### Step 3: Add Environment Variables

1. Go to your Railway project
2. Click "Variables" tab
3. Add all variables from the checklist above
4. Click "Deploy" to restart

### Step 4: Configure Database

1. In Railway, click "New" → "Database" → "PostgreSQL"
2. Railway will create a PostgreSQL database
3. Copy the `DATABASE_URL` from the database service
4. Add it to your environment variables

### Step 5: Configure Workers

Railway supports multiple processes via `Procfile`:

- **web:** Main FastAPI application
- **worker:** Payment reminder worker
- **guardian-daemon:** Guardian monitoring daemon
- **email-retry-worker:** Email retry queue worker

All processes will start automatically.

### Step 6: Verify Deployment

```bash
# Test health endpoint
curl https://your-railway-url.up.railway.app/api/health/

# Expected response:
# {"status": "healthy", "version": "3.0.0", ...}
```

---

## ▲ Vercel Deployment (Frontend)

### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

### Step 2: Login to Vercel

```bash
vercel login
```

### Step 3: Deploy

```bash
cd omega-frontend
vercel --prod
```

Follow the prompts:
- **Project name:** `maya-assistant`
- **Framework:** Next.js (auto-detected)
- **Build command:** `npm run build`
- **Output directory:** `.next`

### Step 4: Configure Environment Variables

1. Go to Vercel dashboard
2. Select your project
3. Go to "Settings" → "Environment Variables"
4. Add:
   - `NEXT_PUBLIC_OMEGA_BACKEND`
   - `NEXT_PUBLIC_APP_URL`

### Step 5: Configure Custom Domain (Optional)

1. Go to "Settings" → "Domains"
2. Add `mayassistant.com`
3. Follow DNS configuration instructions
4. Wait for SSL certificate (automatic)

### Step 6: Verify Deployment

Visit your Vercel URL and test:
- ✅ Homepage loads
- ✅ Login works
- ✅ Bookings page loads
- ✅ API calls succeed

---

## 🧪 Post-Deployment Testing

### Backend Tests

```bash
# Health check
curl https://your-railway-url.up.railway.app/api/health/

# Database check
curl https://your-railway-url.up.railway.app/api/health/db

# Encryption check
curl https://your-railway-url.up.railway.app/api/health/encryption
```

### Frontend Tests

1. ✅ Login/Logout
2. ✅ Bookings page loads
3. ✅ Payment status updates
4. ✅ Mobile responsive
5. ✅ PWA installable

### Integration Tests

1. ✅ Email processing (send test email)
2. ✅ Payment link generation
3. ✅ Stripe webhook (test mode)
4. ✅ SMS sending (test number)
5. ✅ Calendar blocking

---

## 📊 Monitoring

### Railway Monitoring

- **Logs:** Available in Railway dashboard
- **Metrics:** CPU, Memory, Network
- **Alerts:** Configure in Railway settings

### Vercel Monitoring

- **Analytics:** Enable in Vercel dashboard
- **Logs:** Available in Vercel dashboard
- **Performance:** Web Vitals tracking

### Application Monitoring

- **Audit Logs:** Check `audit_log` table
- **Error Tracking:** Check Railway logs
- **Health Endpoint:** Monitor `/api/health/`

---

## 🔒 Security Checklist

- [ ] All environment variables set
- [ ] `DEBUG=false` in production
- [ ] SSL certificates valid
- [ ] CORS configured correctly
- [ ] Rate limiting enabled
- [ ] JWT secrets are strong (32+ chars)
- [ ] Encryption key is secure
- [ ] No secrets in code
- [ ] Database has SSL enabled
- [ ] Webhook signatures verified

---

## 🚨 Rollback Procedure

If deployment fails:

### Railway Rollback

1. Go to Railway dashboard
2. Click "Deployments"
3. Select previous successful deployment
4. Click "Redeploy"

### Vercel Rollback

1. Go to Vercel dashboard
2. Click "Deployments"
3. Select previous successful deployment
4. Click "Promote to Production"

---

## 📝 Post-Launch Tasks

1. [ ] Monitor error rates for 24 hours
2. [ ] Test all critical paths
3. [ ] Verify backups are running
4. [ ] Set up monitoring alerts
5. [ ] Document any issues
6. [ ] Update documentation

---

## 🆘 Troubleshooting

### Backend Issues

**Issue:** Health check fails
- Check environment variables
- Check database connection
- Check Railway logs

**Issue:** Workers not starting
- Check `Procfile` syntax
- Check Railway process logs
- Verify worker dependencies

### Frontend Issues

**Issue:** API calls fail
- Check `NEXT_PUBLIC_OMEGA_BACKEND` is set
- Check CORS configuration
- Check Railway URL is correct

**Issue:** Build fails
- Check Node.js version
- Check dependencies
- Check build logs

---

**Last Updated:** Current Session  
**Version:** 3.0.0

