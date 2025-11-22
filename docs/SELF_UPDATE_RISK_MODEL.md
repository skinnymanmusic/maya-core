# SELF-UPDATE RISK MODEL (v1.2)

**Purpose:** Define how we think about risk for self-updates.

## 1. Risk Levels

- **Low Risk**
  - Doc changes
  - CI config tweaks
  - Scripts in infrastructure

- **Medium Risk**
  - New endpoints
  - New services
  - Non-core business logic

- **High Risk**
  - Auth, encryption, security
  - Migrations and DB schema
  - Payments, guardian, or tenant isolation

## 2. Mitigation per Risk Level

- Low:
  - Direct commits to feature branches OK.
  - Light review.

- Medium:
  - Always use `auto/*` branches.
  - Require PR + tests + staging deploy.

- High:
  - Require:
    - `approved-core-change` label.
    - Senior human review.
    - Staging soak time.
    - Rollback tested and documented.

## 3. Future: Dependency Sandbox

Planned "Dependency Autopilot v2" behavior:

- Create sandbox branches for dependency updates.
- Build + test against staging-like environment.
- Only open PRs when all checks pass.
- If sandbox fails:
  - Do NOT suggest update.
  - Produce a short report instead.

This model is documented now, but the actual CI workflow will be added later, after backend production is stable.

