# GITHUB COPILOT SAFETY MATRIX

**Scope:** How Copilot is allowed to behave in this repo.

## 1. Zones

- **Green Zone (Low Risk)**
  - `/docs/**`
  - `/frontend/**` (non-auth)
  - `/infrastructure/scripts/**`
  - Test files (`/backend/tests/**`, `/tests/**`)

- **Yellow Zone (Medium Risk)**
  - `/backend/app/routers/**`
  - `/backend/app/services/**` (non-payment)
  - `/frontend/**` auth-related UI

- **Red Zone (High Risk / Protected)**
  - `backend/app/core/**`
  - `backend/app/security/**`
  - `backend/app/database/**`
  - `backend/app/db/migrations/**`
  - `backend/app/services/payment*`
  - `backend/app/guardian/**`
  - `backend/requirements.txt`
  - `backend/requirements.lock`

## 2. Copilot Rules

- Green Zone:
  - Free to suggest code, tests, and docs.

- Yellow Zone:
  - Suggestions allowed, but **human must review carefully**.

- Red Zone:
  - Copilot suggestions should be treated as potential hints ONLY.
  - No blind accept.
  - Changes require:
    - PR
    - Correct label
    - Passing CI and staging.

## 3. Integration with .github/copilot_rules.yml

- This matrix is the human-readable counterpart to:
  - `.github/copilot_rules.yml`
- Any changes to that file should:
  - Be reflected here.
  - Be consistent with:
    - BACKEND_INTEGRITY_POLICY
    - PYTHON_DEPENDENCY_POLICY
    - SELF_UPDATE_POLICY

