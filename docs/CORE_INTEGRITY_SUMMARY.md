# CORE INTEGRITY SUMMARY (Integrity Pack v1)

**Status:** Canonical overview  
**Scope:** MAYAssistant backend, infrastructure, and automation safety

## 1. Purpose

This document gives a high-level map of all safety and integrity systems in MAYAssistant, so that:

- Humans know what protects production.
- AI assistants know where they may act.
- CI/CD knows which rules to enforce.

## 2. Safety Pillars

1. **Gilman Accords**  
   - System-wide safety constitution.  
   - Emphasizes: "Safety first, data integrity, code quality, auditability."

2. **Backend Integrity Guard**  
   - Protects core backend paths from casual edits.  
   - Enforced by:
     - `docs/BACKEND_INTEGRITY_POLICY.md`
     - `.github/backend_protected_paths.yml`
     - `.github/workflows/backend_integrity_guard.yml`

3. **Dependency Freeze Guard**  
   - Ensures all backend dependencies are pinned and reproducible.  
   - Enforced by:
     - `docs/PYTHON_DEPENDENCY_POLICY.md`
     - `backend/requirements.txt`
     - `backend/requirements.lock`
     - `.github/workflows/dependency_freeze_guard.yml`

4. **Self-Update Policy**  
   - AI-assisted changes must go through:
     1. Branch → 2. Staging → 3. Tests/health → 4. Human approval → 5. Rollback-ready.  
   - Defined in:
     - `docs/SELF_UPDATE_POLICY.md`
     - `.github/workflows/self_update_check.yml`
     - `infrastructure/LAST_PROD_DEPLOY.json`

5. **Solin Auto-Fix Policy v2 + Security–UX Harmony**  
   - Solin must:
     - Prefer safety over convenience when in conflict.
     - Consider UX happiness vs outrage before proposing flow changes.
     - Design auto-fixes that are reversible, auditable, and staged.
   - Defined in:
     - `docs/SOLIN_AUTOFIX_POLICY_V2.md`
     - `.cursor/rules/SOLIN_SECURITY_UX_PRINCIPLES.md`

## 3. Protected Areas (High Risk Zones)

The following are "do not touch casually" zones:

- `backend/app/core/**`
- `backend/app/security/**`
- `backend/app/database/**`
- `backend/app/db/migrations/**`
- `backend/app/services/payment*`
- `backend/app/guardian/**`

Any change here MUST:

- Be done in a feature branch.
- Go through a Pull Request.
- Include the label: `approved-core-change`.
- Pass CI + staging verification.

## 4. Automation Boundaries

AI and Copilot MAY:

- Refactor docs, specs, and comments.
- Improve CI/YAML and scripts in `/infrastructure`.
- Add non-critical endpoints and services behind flags.
- Propose changes to tests.

AI and Copilot MAY NOT:

- Auto-edit security, auth, encryption, or payments.
- Auto-change DB schema or migrations.
- Auto-update dependencies without a PR and label.
- Push directly to `main`.

## 5. Rollback & Audit

- `infrastructure/LAST_PROD_DEPLOY.json` tracks last production SHA.  
- CI supports:
  - "Rollback to last_good_sha" workflows.
  - System correction events in logs.
- All self-updates must remain auditable via:
  - Git history
  - CI logs
  - SYSTEM CORRECTION EVENT entries

## 6. How to Extend This Pack

- New guardrails must:
  - Be documented here.
  - Have a dedicated policy file.
  - Have CI enforcement where possible.

Integrity Pack v1 is the baseline; future versions may add:

- Dependency sandbox autopilot
- More granular risk levels per directory
- Automated risk scoring for PRs.

