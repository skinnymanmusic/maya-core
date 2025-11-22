# AUTO-FIX POLICY REPORT (Solin v2)

**Purpose:** Summarize how Solin is allowed to auto-fix things.

## 1. Auto-Fix Levels

- **Level 0: Suggest Only**
  - Solin proposes changes but does not apply them.

- **Level 1: Safe Docs & Config**
  - Solin may directly edit:
    - `/docs/**/*.md`
    - `/infrastructure/scripts/**`
    - CI YAML (non-destructive edits)

- **Level 2: Non-Core Code**
  - Solin may:
    - Add new endpoints, services, or UI components behind flags.
    - Refactor low-risk code.
  - Must stay away from:
    - Core security, migrations, payments, guardian.

## 2. Required Behavior

For any auto-fix above trivial documentation changes, Solin must:

- Run a "what could go wrong?" scan:
  - Dependencies?
  - Auth flows?
  - Data integrity?
- Prefer:
  - Additive changes (not destructive).
  - Feature flags / toggles for new behavior.
- Leave:
  - Clear comments and references to related policy files.

## 3. Sandbox First for Risky Changes

- Any medium or high-risk change must:
  - Be done in a branch (`auto/*`).
  - Target staging first (not production).
  - Be accompanied by a simple check-list in PR description.

## 4. Future Enhancements

The following belong to a future "Auto-Fix v3" upgrade:

- Automated dependency sandbox testing.
- Automated PR risk scoring.
- Automated rollback suggestion generation.

These are intentionally **not** fully wired yet; backend stability and deployment come first.

