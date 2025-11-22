# MayAssistant Backend Integrity Policy (v1.0)

**Status:** Canonical rules for core backend protection  
**Scope:** backend/app core, security, database, migrations

## Purpose

This policy defines how MayAssistant protects critical backend code from
unsafe or accidental modification — whether by humans, GitHub Copilot,
or any other AI-assisted tool.

It works together with:

- GILMAN_ACCORDS.md  (safety + quality)
- Solin Auto-Fix Policy v2  (auto-repair rules)
- SECURITY_UX_HARMONY_RULES.md  (security vs UX balance)
- SELF_UPDATE_POLICY.md  (staging → production self-update flow)

## Protected Areas

The following paths are considered **core** and must not be modified
automatically without explicit human review and approval:

- backend/app/core/**
- backend/app/security/**
- backend/app/database/**
- backend/app/services/payments**/
- backend/app/services/payment**/
- backend/app/guardian/**
- backend/app/db/migrations/**

Changes to these paths:

- MUST be made in a feature branch (e.g. `core/fix-…`).
- MUST go through Pull Request review.
- MUST be clearly described and justified.
- MUST pass all tests and health checks.
- SHOULD be accompanied by a SYSTEM CORRECTION EVENT entry in logs.

## AI & Copilot Restrictions

AI tools (including GitHub Copilot / ChatGPT / Claude / Cursor):

- MAY propose changes to protected files, but:
  - Only in feature branches.
  - Only with explicit human supervision.
- MAY NOT auto-commit or auto-merge changes to protected paths.
- MAY NOT bypass the backend integrity CI guard.

## CI Enforcement

The CI workflow `backend_integrity_guard.yml`:

- Scans Pull Requests targeting `main`.
- Detects changes to protected paths.
- Fails the check if:
  - Protected files changed AND
  - The PR does NOT contain the label: `approved-core-change`.

## Approval Pattern

To approve a core change:

1. Open a Pull Request to `main`.
2. Ensure all tests and health checks pass.
3. Add the label `approved-core-change`.
4. Optionally update:
   - docs/BACKEND_INTEGRITY_POLICY.md
   - docs/SELF_UPDATE_POLICY.md
   - backend logs with a SYSTEM CORRECTION EVENT.

## Rollback

In case of a bad core change:

- Use the staging + production rollback flow defined in:
  - SELF_UPDATE_POLICY.md
  - LAST_PROD_DEPLOY.json
- Record a SYSTEM CORRECTION EVENT describing:
  - The bad SHA
  - The rollback SHA
  - The impact and resolution

