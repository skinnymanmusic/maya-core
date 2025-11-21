# DEPLOYMENT_PIPELINE.md  
## MayAssistant Deployment Pipeline Specification (v1.2)

Last Updated: 2025-01-27

---

# 1. OVERVIEW

Deployment must be:
- safe  
- tested  
- predictable  
- reversible  
- compliant  

This pipeline covers:
- backend (Azure / Railway)  
- frontend (Vercel)  
- tests  
- migrations  
- smoke tests  
- rollback  

---

# 2. BACKEND PIPELINE (AZURE FUNCTIONS OR RAILWAY)

## Step 1 — GitHub Actions Trigger
On push → `main`

## Step 2 — Lint
Python linting  
Type checks

## Step 3 — Run Full Tests
25/25 backend tests  
9/9 basic tests  
If fail → STOP

## Step 4 — Build
Azure:
- zip and deploy via `azure/functions-action@v1`

Railway:
- build image  
- push to registry  

## Step 5 — Deploy

## Step 6 — Smoke Test
- GET `/health`  
- GET `/health/deep`  

If failing → rollback

---

# 3. FRONTEND PIPELINE (VERCEL)

### Step 1 — Lint  
### Step 2 — Build  
### Step 3 — Test (Playwright optional)  
### Step 4 — Deploy  
### Step 5 — Verify on staging  
### Step 6 — Promote to production  

---

# 4. DATABASE MIGRATIONS

Rules:
- MUST be run manually unless trivial  
- MUST be reversible  
- MUST be tested locally  
- MUST have backups  

Email-hash migration = critical and executed once.

---

# 5. ENVIRONMENT VARIABLES

Backend:
- DB URL  
- Stripe keys  
- Twilio keys  
- Gmail/Calendar keys  
- Encryption keys  
- JWT keys  

Frontend:
- NEXT_PUBLIC_API_URL  
- Clerk keys  

---

# 6. MONITORING

Backend:
- health checks every 30–60 seconds  
- logs monitored for anomalies  

Frontend:
- 5-minute checks  

Guardian Framework integrates with alerts.

---

# 7. ROLLBACK

Automatic rollback if:
- tests fail  
- health checks fail  
- anomaly detected  

Rollback = deploy previous known-good build.

---

END OF DEPLOYMENT_PIPELINE.md
