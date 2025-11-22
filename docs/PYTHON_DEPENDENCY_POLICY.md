# Python Dependency Policy (MayAssistant v1.2)

**Status:** Canonical policy for backend Python dependencies  
**Scope:** `backend/` (FastAPI app, services, workers)

## 1. Goals

- Prevent surprise breakage from upstream packages (PyPI changes, yanked versions, Python minor releases).
- Ensure every deployment is reproducible.
- Make dependency upgrades **intentional**, **reviewed**, and **tested in staging**.
- Keep a clear rollback path to the last known good dependency set.

## 2. Canonical Files

The backend dependency truth lives in:

- `backend/requirements.txt` — human-edited, pinned versions (`package==x.y.z`).
- `backend/requirements.lock` — machine-generated lockfile that MUST match `requirements.txt`.

Rules:

- Every line in `backend/requirements.txt` MUST be fully pinned (`==`).
- `backend/requirements.lock` MUST contain the same set of pinned dependencies.
- CI will fail if:
  - Any unpinned dependency exists (`>=`, `>`, `<`, `~=` etc.).
  - `requirements.lock` is missing.
  - `requirements.lock` is out of sync with `requirements.txt`.

## 3. Change Process

Dependency changes MUST follow this flow:

1. Create a feature branch:
   - `auto/dependency-upgrade-YYYYMMDD-001` (or similar).
2. Update `backend/requirements.txt` intentionally.
3. Regenerate the lockfile:
   - e.g., using `pip-compile` or `pip freeze` as defined in future tooling.
4. Commit BOTH files:
   - `backend/requirements.txt`
   - `backend/requirements.lock`
5. Open a Pull Request into `main`.
6. Add label: `approved-dependency-upgrade`.
7. CI will:
   - Verify pinning + lock sync.
   - Run backend tests.
   - Deploy to staging (via self-update policy).
8. If staging health checks pass:
   - Approve & merge PR into `main`.
   - CI will deploy to production and update `infrastructure/LAST_PROD_DEPLOY.json`.

## 4. CI Enforcement

Enforced by:

- `.github/workflows/dependency_freeze_guard.yml`  
- Triggers on:
  - PRs that touch:
    - `backend/requirements.txt`
    - `backend/requirements.lock`
  - Pushes to `main` that touch the same files.

Checks:

- All requirements are fully pinned (`==` present, no range specifiers).
- `backend/requirements.lock` exists.
- The set of non-comment, non-empty lines in both files match.
- For Pull Requests:
  - The label `approved-dependency-upgrade` MUST be present if these files changed.

If any check fails → CI fails and blocks merge.

## 5. Self-Update & Sandbox Behavior

Dependency self-updates MUST:

- Run in branches (`auto/*`), never directly on `main`.
- Use staging deployments first (see `SELF_UPDATE_POLICY.md`).
- Be tested via:
  - Backend test suite.
  - Health checks on staging.
- Only be promoted to production after:
  - Manual approval.
  - CI confirmation.
  - Update of `LAST_PROD_DEPLOY.json`.

Future improvement (v2.1+):

- Automated "sandbox" dependency upgrade workflow:
  - Spawns `auto/dependency-upgrade-*` branch.
  - Proposes updated dependencies.
  - Runs tests + staging.
  - Opens a PR with a summary for human approval.

## 6. Rollback

- Production deployments are tracked in:
  - `infrastructure/LAST_PROD_DEPLOY.json`
- Rollback steps:
  - Redeploy the `last_good_sha` recorded in that file.
  - Ensure the matching `requirements.lock` is used.
  - Log a SYSTEM CORRECTION EVENT in the appropriate log.

## 7. Related Docs

- `docs/SELF_UPDATE_POLICY.md`
- `docs/BACKEND_INTEGRITY_POLICY.md`
- `docs/DEPLOYMENT_PIPELINE.md`
- `docs/MASTER_HANDOFF.md`

