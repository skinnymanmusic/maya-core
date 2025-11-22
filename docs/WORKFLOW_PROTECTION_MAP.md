# WORKFLOW PROTECTION MAP

**Purpose:** Show which CI workflows protect what.

## 1. Workflows

- `backend_integrity_guard.yml`
  - Protects: core backend paths.
  - Blocks PRs without `approved-core-change` label.

- `dependency_freeze_guard.yml`
  - Protects: backend dependencies.
  - Blocks PRs without `approved-dependency-upgrade` label or with out-of-sync lockfiles.

- `self_update_check.yml`
  - Protects: self-update flows.
  - Ensures:
    - Tests pass before staging deploy.
    - Health checks pass on staging.

(Future workflows can be added here.)

## 2. How to Use This Map

- When something fails in CI:
  - Check this doc to see which safety guard triggered.
- When adding new guardrails:
  - Add a short entry here.

## 3. Relationship to MASTER_HANDOFF

- MASTER_HANDOFF.md gives the entire system overview.
- This file focuses specifically on:
  - "Which workflow protects which risk."

