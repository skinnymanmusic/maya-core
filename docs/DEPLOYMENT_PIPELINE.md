# 🚀 DEPLOYMENT PIPELINE

**CI/CD Automation & Deployment Procedures**  
**Version:** 1.0  
**Last Updated:** 2025-01-27

---

## 📋 Overview

This document describes the complete deployment pipeline for the MAYA/OMEGA system, including CI/CD automation, deployment procedures, and rollback strategies.

---

## 🏗️ Pipeline Architecture

### High-Level Flow

```
Code Push
    ↓
GitHub Actions (CI)
    ↓
Build & Test
    ↓
Security Scan
    ↓
Deploy to Staging
    ↓
Smoke Tests
    ↓
Deploy to Production
    ↓
Health Checks
    ↓
Monitor & Alert
```

---

## 🔄 CI/CD Workflows

### Frontend Pipeline

**Trigger:** Push to `main` or `develop` branch

**Stages:**
1. **Lint & Type Check**
   - ESLint
   - TypeScript check
   - Format check

2. **Test**
   - Unit tests
   - Integration tests
   - Coverage report

3. **Build**
   - Next.js production build
   - Bundle analysis
   - Asset optimization

4. **Security Scan**
   - npm audit
   - Snyk scan
   - Dependency check

5. **Deploy**
   - Deploy to Vercel
   - Run smoke tests
   - Verify deployment

**See:** `FRONTEND_AUTOBUILD_SPEC.md` for details

---

### Backend Pipeline

**Trigger:** Push to `main` or `develop` branch

**Stages:**
1. **Lint & Type Check**
   - Ruff (linter)
   - Ruff (formatter)
   - MyPy (type check)

2. **Test**
   - Unit tests
   - Integration tests
   - Database tests
   - Coverage report

3. **Build**
   - Verify imports
   - Check migrations
   - Validate configuration

4. **Security Scan**
   - Safety check
   - Bandit scan
   - Dependency audit

5. **Deploy**
   - Deploy to Railway
   - Run health checks
   - Verify deployment

**See:** `BACKEND_AUTOBUILD_SPEC.md` for details

---

## 🚀 Deployment Environments

### Development

**Purpose:** Local development

**Setup:**
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd omega-frontend
npm install
npm run dev
```

**Database:** Local PostgreSQL or Supabase dev instance

---

### Staging

**Purpose:** Pre-production testing

**Backend:** Railway staging environment
**Frontend:** Vercel preview deployment

**Access:**
- Staging URL: `https://staging.mayassistant.com`
- Test data only
- Mirrors production configuration

**Testing:**
- Full test suite
- Integration tests
- Manual QA
- Performance testing

---

### Production

**Purpose:** Live system

**Backend:** Railway production
**Frontend:** Vercel production

**Access:**
- Production URL: `https://mayassistant.com`
- Real user data
- Production configuration

**Monitoring:**
- Health checks
- Error tracking
- Performance monitoring
- Alerting

---

## 📦 Deployment Procedures

### Backend Deployment (Railway)

**Prerequisites:**
- Environment variables set
- Database migrations ready
- Tests passing

**Steps:**

1. **Pre-Deployment Checklist**
   ```bash
   # Run tests locally
   cd backend
   pytest tests/
   
   # Check migrations
   ls migrations/
   
   # Verify environment variables
   cat .env.example
   ```

2. **Deploy**
   ```bash
   # Push to main triggers auto-deploy
   git push origin main
   
   # Or manual deploy via Railway CLI
   railway up
   ```

3. **Verify**
   ```bash
   # Check health endpoint
   curl https://your-app.up.railway.app/api/health
   
   # Check logs
   railway logs
   ```

4. **Monitor**
   - Watch Railway dashboard
   - Check application logs
   - Monitor error rates
   - Verify health checks

---

### Frontend Deployment (Vercel)

**Prerequisites:**
- Environment variables set
- Build passing
- Tests passing

**Steps:**

1. **Pre-Deployment Checklist**
   ```bash
   # Run tests locally
   cd omega-frontend
   npm test
   
   # Build locally
   npm run build
   
   # Verify environment variables
   cat .env.local.example
   ```

2. **Deploy**
   ```bash
   # Push to main triggers auto-deploy
   git push origin main
   
   # Or manual deploy via Vercel CLI
   vercel --prod
   ```

3. **Verify**
   ```bash
   # Check deployment
   curl https://mayassistant.com
   
   # Check build logs
   vercel logs
   ```

4. **Monitor**
   - Watch Vercel dashboard
   - Check build logs
   - Monitor performance
   - Verify functionality

---

## 🔄 Database Migrations

### Migration Process

1. **Create Migration**
   ```bash
   # Create migration file
   touch backend/migrations/015_new_feature.sql
   ```

2. **Write SQL**
   ```sql
   -- Migration: 015_new_feature.sql
   CREATE TABLE IF NOT EXISTS new_table (
     id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
     tenant_id UUID NOT NULL REFERENCES tenants(id),
     -- columns
   );
   ```

3. **Test Locally**
   ```bash
   # Apply migration locally
   psql $DATABASE_URL -f backend/migrations/015_new_feature.sql
   ```

4. **Deploy**
   ```bash
   # Migration runs automatically on deploy
   # Or run manually:
   python backend/apply_migration.py 015_new_feature.sql
   ```

5. **Verify**
   ```sql
   -- Check migration applied
   SELECT * FROM schema_migrations WHERE version = '015';
   ```

---

## 🔐 Environment Variables

### Backend Variables

**Required:**
- `DATABASE_URL` - PostgreSQL connection
- `JWT_SECRET_KEY` - JWT signing key
- `ENCRYPTION_KEY` - AES-256 encryption key
- `ANTHROPIC_API_KEY` - Claude API key
- `STRIPE_API_KEY` - Stripe secret key
- `TWILIO_ACCOUNT_SID` - Twilio credentials

**See:** `backend/ENVIRONMENT_VARIABLES.md` for complete list

### Frontend Variables

**Required:**
- `NEXT_PUBLIC_API_URL` - Backend API URL

**See:** Vercel environment variables documentation

---

## 🧪 Testing in Pipeline

### Automated Tests

**Backend:**
- Unit tests (pytest)
- Integration tests
- Database tests
- API tests

**Frontend:**
- Unit tests (Jest)
- Component tests (React Testing Library)
- E2E tests (Playwright)

### Manual Testing

**Staging:**
- Full feature testing
- User acceptance testing
- Performance testing
- Security testing

---

## 🔄 Rollback Procedures

### Backend Rollback

**Railway:**
1. Open Railway dashboard
2. Select previous deployment
3. Click "Redeploy"
4. Verify health checks
5. Monitor for issues

**Git:**
```bash
# Revert commit
git revert <commit-hash>
git push origin main
```

### Frontend Rollback

**Vercel:**
1. Open Vercel dashboard
2. Select previous deployment
3. Click "Promote to Production"
4. Verify deployment
5. Monitor for issues

**Git:**
```bash
# Revert commit
git revert <commit-hash>
git push origin main
```

### Database Rollback

**If migration fails:**
```sql
-- Rollback migration
BEGIN;
-- Reverse migration SQL
ROLLBACK;
```

**If data corrupted:**
```bash
# Restore from backup
pg_restore -d $DATABASE_URL backup.dump
```

---

## 📊 Monitoring & Alerts

### Health Checks

**Backend:**
- Endpoint: `/api/health`
- Checks: Database, external APIs
- Frequency: Every 30 seconds

**Frontend:**
- Endpoint: `/api/health` (via backend)
- Checks: Build status, deployment
- Frequency: Every 5 minutes

### Alerts

**Triggers:**
- Health check failures
- High error rates
- Performance degradation
- Deployment failures

**Channels:**
- Email
- Slack (future)
- PagerDuty (future)

---

## 🐛 Troubleshooting

### Common Issues

**Build Failures:**
- Check logs for errors
- Verify dependencies
- Check environment variables
- Review recent changes

**Deployment Failures:**
- Check health checks
- Verify environment variables
- Check database connectivity
- Review application logs

**Performance Issues:**
- Check database queries
- Review API response times
- Check external API calls
- Monitor resource usage

---

## ✅ Deployment Checklist

### Pre-Deployment

- [ ] All tests passing
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] Environment variables set
- [ ] Migrations tested
- [ ] Security scan passed

### Deployment

- [ ] Deploy to staging
- [ ] Run smoke tests
- [ ] Verify functionality
- [ ] Check performance
- [ ] Deploy to production
- [ ] Verify health checks

### Post-Deployment

- [ ] Monitor error rates
- [ ] Check performance metrics
- [ ] Verify user functionality
- [ ] Review logs
- [ ] Update documentation

---

## 📚 Related Documentation

- `FRONTEND_AUTOBUILD_SPEC.md` - Frontend build specification
- `BACKEND_AUTOBUILD_SPEC.md` - Backend build specification
- `backend/DEPLOYMENT_GUIDE.md` - Detailed deployment guide
- `backend/ENVIRONMENT_VARIABLES.md` - Environment variable reference

---

**Version:** 1.0  
**Status:** Active  
**Maintained By:** DevOps Team

