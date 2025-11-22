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

## Step 1.5 — Backend Integrity Guard
Before deployment, `backend_integrity_guard.yml` ensures that any changes to protected backend paths have been explicitly approved via the `approved-core-change` label.

Protected paths include:
- `backend/app/core/**`
- `backend/app/security/**`
- `backend/app/database/**`
- `backend/app/services/payments**`
- `backend/app/guardian/**`
- `backend/app/db/migrations/**`

See: `docs/BACKEND_INTEGRITY_POLICY.md` for complete details.

## Step 1.6 — Dependency Freeze Guard

- Ensures all backend Python dependencies are:
  - Fully pinned in `backend/requirements.txt`.
  - Mirrored exactly in `backend/requirements.lock`.
- Blocks PRs that:
  - Modify dependencies without the `approved-dependency-upgrade` label.
  - Have out-of-sync or missing lockfiles.

See: `docs/PYTHON_DEPENDENCY_POLICY.md` for details.

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

See Integrity Pack v1 (`docs/CORE_INTEGRITY_SUMMARY.md`) for full safety and guardrail map.

---

# 8. STAGING → PRODUCTION PROMOTION & ROLLBACK

## Staging Environment

**Purpose:** Validate AI-assisted changes before production deployment

**Deployment Source:**
- `auto/*` branches (AI-assisted feature/update branches)
- `develop` branch (optional integration branch)

**Railway Service:** `mayassistant-staging`

**Process:**
1. AI commits changes to `auto/*` branch
2. CI pipeline runs tests + type checks
3. If green, CI deploys to `mayassistant-staging`
4. Staging health checks run:
   - `/api/health/` endpoint
   - `/api/health/db` database connection
   - Key functional probes
5. If all checks pass, commit is marked as "ready to promote"

## Production Promotion

**Deployment Source:**
- `main` branch only
- Requires explicit human approval (GitHub environment protection)

**Railway Service:** `mayassistant-prod`

**Process:**
1. Human approves promotion via GitHub (manual approval step)
2. CI deploys the same commit SHA to `mayassistant-prod`
3. CI updates `infrastructure/LAST_PROD_DEPLOY.json` with:
   - `last_good_sha`: The deployed commit SHA
   - `deployed_at`: Timestamp of deployment

## Rollback Mechanism

**Rollback Reference:** `infrastructure/LAST_PROD_DEPLOY.json`

**Contains:**
- `last_good_sha`: Last known-good production deployment
- `deployed_at`: Timestamp of that deployment

**Rollback Process:**
1. CI includes a "Rollback to last good" workflow
2. Redeploys `last_good_sha` to `mayassistant-prod`
3. Logs a SYSTEM CORRECTION EVENT for audit trail

**Emergency Rollback:**
- Can be triggered manually via GitHub Actions
- Always maintains audit trail in logs

---

END OF DEPLOYMENT_PIPELINE.md
