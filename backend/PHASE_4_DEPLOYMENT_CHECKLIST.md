# PHASE 4: PRODUCTION DEPLOYMENT - CHECKLIST

## ✅ Pre-Deployment

### Backend Preparation
- [ ] All tests passing (`pytest tests/ -v`)
- [ ] Environment variables documented (`.env.example`)
- [ ] Database migrations applied
- [ ] `DEBUG=false` in production config
- [ ] All secrets removed from code
- [ ] `Procfile` configured correctly
- [ ] `requirements.txt` up to date
- [ ] Railway project created
- [ ] Database service added in Railway

### Frontend Preparation
- [ ] Production build succeeds (`npm run build`)
- [ ] Environment variables documented (`.env.production.example`)
- [ ] PWA icons created (or placeholders noted)
- [ ] All API endpoints tested locally
- [ ] Mobile responsive verified
- [ ] Vercel project created

---

## 🚂 Railway Deployment (Backend)

### Step 1: Environment Variables
- [ ] `DATABASE_URL` set (from Railway PostgreSQL)
- [ ] `JWT_SECRET_KEY` set (32+ characters)
- [ ] `ENCRYPTION_KEY` set (Fernet key)
- [ ] `ANTHROPIC_API_KEY` set
- [ ] `STRIPE_API_KEY` set (production key)
- [ ] `STRIPE_WEBHOOK_SECRET` set
- [ ] `TWILIO_ACCOUNT_SID` set
- [ ] `TWILIO_AUTH_TOKEN` set
- [ ] `GMAIL_WEBHOOK_URL` set (Railway URL)
- [ ] `GMAIL_PUBSUB_TOPIC` set
- [ ] `GMAIL_PUBSUB_SERVICE_ACCOUNT` set
- [ ] `DEFAULT_TENANT_ID` set
- [ ] `DEBUG=false` set

### Step 2: Deployment
- [ ] Code pushed to GitHub
- [ ] Railway connected to GitHub repo
- [ ] Railway auto-deployed
- [ ] All processes started (web, worker, guardian-daemon, email-retry-worker)

### Step 3: Verification
- [ ] Health endpoint responds: `/api/health/`
- [ ] Database health check: `/api/health/db`
- [ ] Encryption health check: `/api/health/encryption`
- [ ] Railway logs show no errors
- [ ] All workers running

---

## ▲ Vercel Deployment (Frontend)

### Step 1: Environment Variables
- [ ] `NEXT_PUBLIC_OMEGA_BACKEND` set (Railway URL)
- [ ] `NEXT_PUBLIC_APP_URL` set (Vercel URL)

### Step 2: Deployment
- [ ] Code pushed to GitHub
- [ ] Vercel connected to GitHub repo
- [ ] Vercel auto-deployed
- [ ] Build succeeded

### Step 3: Verification
- [ ] Homepage loads
- [ ] Login page works
- [ ] Bookings page loads
- [ ] API calls succeed
- [ ] Mobile responsive
- [ ] PWA manifest loads

---

## 🧪 Post-Deployment Testing

### Backend Tests
- [ ] Health endpoint: `GET /api/health/`
- [ ] Database health: `GET /api/health/db`
- [ ] Encryption health: `GET /api/health/encryption`
- [ ] Auth endpoint: `POST /api/auth/login`
- [ ] Bookings endpoint: `GET /api/bookings/`
- [ ] Stripe webhook: `POST /api/stripe/webhook` (test)
- [ ] SMS webhook: `POST /api/sms/receive` (test)

### Frontend Tests
- [ ] Login flow works
- [ ] Bookings page displays data
- [ ] Payment status updates
- [ ] Error handling works
- [ ] Loading states work
- [ ] Mobile layout correct
- [ ] PWA installable

### Integration Tests
- [ ] Email processing (send test email)
- [ ] Payment link generation
- [ ] Stripe webhook processing
- [ ] SMS sending (test number)
- [ ] SMS receiving (test webhook)
- [ ] Calendar blocking
- [ ] Payment reminders

---

## 🔒 Security Verification

- [ ] All environment variables set (no defaults in production)
- [ ] `DEBUG=false` in production
- [ ] SSL certificates valid (HTTPS)
- [ ] CORS configured correctly
- [ ] Rate limiting enabled
- [ ] JWT secrets are strong (32+ chars)
- [ ] Encryption key is secure
- [ ] No secrets in code/logs
- [ ] Database has SSL enabled
- [ ] Webhook signatures verified
- [ ] API endpoints require authentication

---

## 📊 Monitoring Setup

### Railway Monitoring
- [ ] Logs accessible
- [ ] Metrics visible (CPU, Memory)
- [ ] Alerts configured (optional)

### Vercel Monitoring
- [ ] Analytics enabled (optional)
- [ ] Logs accessible
- [ ] Performance tracking (optional)

### Application Monitoring
- [ ] Audit logs working
- [ ] Error tracking working
- [ ] Health endpoint monitored

---

## 🚨 Rollback Plan

If deployment fails:

### Railway Rollback
- [ ] Know how to access Railway dashboard
- [ ] Know how to redeploy previous version
- [ ] Have previous deployment ID noted

### Vercel Rollback
- [ ] Know how to access Vercel dashboard
- [ ] Know how to promote previous deployment
- [ ] Have previous deployment ID noted

---

## 📝 Post-Launch

### Immediate (First 24 Hours)
- [ ] Monitor error rates
- [ ] Monitor performance
- [ ] Test all critical paths
- [ ] Verify backups running
- [ ] Check logs for issues

### Short-term (First Week)
- [ ] Collect user feedback
- [ ] Fix critical bugs
- [ ] Optimize performance
- [ ] Update documentation
- [ ] Set up monitoring alerts

### Long-term (First Month)
- [ ] Analyze usage patterns
- [ ] Optimize costs
- [ ] Plan improvements
- [ ] Gather testimonials
- [ ] Plan next features

---

## ✅ Final Sign-Off

- [ ] All checklist items completed
- [ ] All tests passing
- [ ] All security checks passed
- [ ] Monitoring configured
- [ ] Documentation updated
- [ ] Team notified
- [ ] **READY FOR LAUNCH! 🚀**

---

**Last Updated:** Current Session  
**Version:** 3.0.0

