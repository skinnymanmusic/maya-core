# MayAssistant Self-Update Policy (v1.2)

**Status:** Canonical rules for AI-assisted changes  
**Scope:** Backend (FastAPI), infrastructure, docs

## Overview

MayAssistant supports AI-assisted "self-updates", but ONLY under strict safety rules:

- All AI changes must go through:
  1. Branch → 2. Staging deploy → 3. Tests & health checks → 4. Approved promotion → 5. Rollback readiness
- No AI may modify production code directly on `main`.
- No AI may bypass tests or deployment checks.

## Allowed Change Scope

AI may auto-edit:

- `/docs/*.md` (documentation, specs, policies)
- `/docs/*.md` under `reports/` or `archive/` (logs, status reports)
- `/infrastructure/*.yml`, `/infrastructure/*.json`, `/infrastructure/scripts/*` (CI/CD, env helpers)
- Backend "non-core" modules under:
  - `backend/app/routers/` (new endpoints, behind feature flags)
  - `backend/app/services/` (new service functions)
  - `backend/app/api/deps.py` (new dependencies, no breaking changes)

AI may NOT auto-edit without explicit human review:

- `backend/app/core/security.py`
- `backend/app/core/encryption.py`
- `backend/app/core/auth.py`
- `backend/app/db/migrations/` (SQL migrations)
- Payment modules (`backend/app/services/payments*`)
- Guardian framework core modules

## Branching Model

- `main` — Production branch, deployed to production Railway service
- `develop` (optional) — Integration branch
- `auto/*` — AI-assisted feature/update branches (e.g., `auto/self-update-001`)

AI-assisted changes must:

- Be committed on `auto/*` branches
- Go through CI + staging deploy
- Be merged via Pull Request, never force-pushed to main

## Environments

- **Staging** — Railway service `mayassistant-staging`
  - Deploys from `auto/*` branches or `develop`
  - Uses separate env vars / DB (recommended)
- **Production** — Railway service `mayassistant-prod`
  - Deploys only from `main`
  - Receives only approved commits

## Self-Update Flow

1. AI proposes changes → applies them to an `auto/*` branch.
2. CI pipeline runs tests + type checks.
3. If green, CI deploys to `mayassistant-staging`.
4. Staging health checks run:
   - `/health` endpoint
   - Key functional probes (e.g. DB connection)
5. If all checks pass, CI marks the commit as "ready to promote".
6. Human approves promotion (GitHub environment, manual approval step).
7. CI deploys the same commit SHA to `mayassistant-prod`.
8. CI updates `infrastructure/LAST_PROD_DEPLOY.json` with the SHA and timestamp.

## Rollback

- `infrastructure/LAST_PROD_DEPLOY.json` stores:
  - `last_good_sha`
  - `deployed_at`
- CI includes a "Rollback to last good" workflow that:
  - Redeploys `last_good_sha` to `mayassistant-prod`
  - Logs a SYSTEM CORRECTION EVENT

## Guardrails

- No direct pushes to `main` from AIs.
- No deployments to production from untagged or failing commits.
- All self-updates must be auditable:
  - Commits
  - CI logs
  - SYSTEM CORRECTION EVENT entries in logs.

See also:

- `PYTHON_VERSION_POLICY.md`
- `BACKEND_AUTOBUILD_SPEC.md`
- `DEPLOYMENT_PIPELINE.md`

