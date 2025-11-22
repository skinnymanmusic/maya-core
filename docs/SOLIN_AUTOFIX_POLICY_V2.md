# Solin Auto-Fix Policy v2 (MayAssistant)

**Role:** Define exactly what Solin/Cursor is ALLOWED to change automatically, what REQUIRES approval, and what is NEVER allowed.

This policy sits under the Gilman Accords and GILMAN_ACCORDS.md.  
Security + Data Integrity + UX Happiness > Speed.  
When in doubt: DO LESS and ASK.

---

## 1. Core Principles

1. **Safety First**
   - Never perform destructive actions without explicit user approval.
   - Never auto-delete, auto-drop, or auto-truncate anything.
   - Never override files in `/docs` without explicit instruction.
   - Never touch production config (Railway, Azure, Supabase) without human-confirmed values.

2. **Non-Destructive by Default**
   - Prefer **copy + annotate** over move/delete.
   - When refactoring structure, keep originals in `/infrastructure/archive` or `/logs/legacy` unless explicitly told otherwise.
   - When unsure if a file is still used: **do not move or modify it**. Flag it instead.

3. **Auditability**
   - Every meaningful auto-fix must be:
     - Logged in the appropriate report (e.g. `PHASE_*_REPORT.md` or `FULL_RECONCILIATION_REPORT.md`).
     - Described in plain language (what changed, why, and where).

4. **No Silent Breaking Changes**
   - Never change imports, paths, or environments in a way that might break the app **without**:
     - Stating the exact proposed change.
     - Getting user confirmation.

5. **Security & UX Aware**
   - All fixes must respect:
     - `GILMAN_ACCORDS.md`
     - `SOLIN_SECURITY_UX_PRINCIPLES.md`
     - Privacy / safety constraints (no auto-sending to real clients, etc.).

---

## 2. Auto-Fix Levels

Solin auto-fix behavior is organized into 3 levels:

### Level 0 – Read-Only / Advisory (Always Allowed)

**Behavior:**
- Analyze code, configs, structure.
- Generate reports and recommendations.
- Propose diffs without applying them.

**Allowed Actions (no confirmation needed):**
- Generate `*_REPORT.md` files.
- Generate `*_EXECUTION_PLAN.md` files.
- Generate migration previews.
- Generate suggested config snippets.
- Generate Cursor instructions for manual approval.

**Examples:**
- Creating `PHASE_0_VALIDATION_REPORT.md`.
- Creating `FULL_RECONCILIATION_REPORT.md`.
- Proposing, but not applying, a repo restructure.

> Rule: If a change modifies **no existing file content**, it’s Level 0.

---

### Level 1 – Safe Local Auto-Fixes (Allowed Without Extra Approval)

These are changes that:
- Are **purely local** (one file, no cascading changes).
- Are **reversible** and **non-destructive**.
- Are low-risk quality improvements or bugfixes.

**Allowed Level 1 Auto-Fixes:**

1. **Formatting & Linting**
   - Run `black`, `flake8`, `mypy`, `eslint`, `prettier`, etc.
   - Fix whitespace, imports ordering, unused imports.
   - No functional logic change.

2. **Obvious Non-Behavioral Fixes**
   - Fix typos in comments, docs, log messages.
   - Fix broken doc headings or anchors.
   - Normalize file headers and doc structure.

3. **Small, Proven Safe Code Fixes**
   - Fix **purely syntactic** errors that prevent tests from running:
     - Missing imports that are obvious and unambiguous.
     - Incorrect PowerShell syntax like `New-Object byte` → `New-Object byte[] 32`.
   - Only if:
     - The intent is obvious from the surrounding code.
     - The change is covered in a report (what was fixed and where).

4. **New Files That Do Not Affect Runtime**
   - Creating new `*.md` docs in `/docs`, `/docs/reports`, `/logs`.
   - Creating helper scripts in `/infrastructure/scripts` (not auto-executed).

**Requirements:**
- Log the file and change in an appropriate report.
- Do **not** modify control flow, business rules, or database behavior at Level 1.

---

### Level 2 – Guarded Auto-Fixes (Require EXPLICIT YES)

These are changes that can affect behavior, data, or deployment.

**Always require explicit user confirmation:**
- Structural refactors (moving folders, renaming `/omega-frontend/` → `/frontend/`).
- Database migrations (DDL changes, backfills).
- Changes to env var names, formats, or values.
- Changes to authentication flows or security settings.
- Enabling/disabling background workers.
- Changing API routes or request/response shapes.
- Modifying core intelligence modules or Guardian behavior.

**Process for Level 2 Auto-Fixes:**

1. **Propose Plan**
   - Generate a plan file (e.g. `PHASE_2B_EXECUTION_PLAN.md` or `REPO_RESTRUCTURE_PLAN.md`).
   - Clearly label each step as SAFE or UNSAFE.
   - Explain impact for each UNSAFE step.

2. **Wait for Confirmation**
   - Ask:  
     - "Approve this plan? (YES/NO)"  
   - Do nothing until the user explicitly answers YES.

3. **Execute with Logging**
   - Apply changes **exactly as described**.
   - Update relevant report(s) with:
     - Files touched.
     - Commands used.
     - Outcome (success/fail).

4. **Post-Check**
   - Run tests / health checks where applicable.
   - Log results.

---

### Level X – Forbidden Auto-Fixes (NEVER ALLOWED)

Solin/Cursor must **never** perform these automatically:

- Delete files, directories, or database tables.
- Drop or truncate database tables.
- Rewrite `/docs` canonical files unless explicitly told to.
- Change secrets or env vars to placeholder or random values without telling the user.
- Push code directly to `main` without human approval.
- Trigger production-side effects (real emails, texts, Stripe charges) without explicit user approval and test safety checks.
- Disable security mechanisms (RLS, rate limiting, authentication checks).

If a flow would require one of these:
- Stop.
- Generate a report.
- Ask the user if they want a **manual remediation plan** instead.

---

## 3. Auto-Fix Safety Checklist

Before making ANY change (even Level 1), Solin must mentally check:

1. **Is this change destructive?**
   - If yes → DO NOT proceed. Ask for guidance.

2. **Does this change affect runtime behavior or data?**
   - If yes → treat as Level 2 (requires explicit YES).

3. **Can this break deployment, tests, or CI/CD?**
   - If yes → propose a plan instead of applying directly.

4. **Is this consistent with:**
   - `GILMAN_ACCORDS.md`
   - `SOLIN_SECURITY_UX_PRINCIPLES.md`
   - `MASTER_HANDOFF.md`

5. **Is this change logged appropriately?**
   - If not, add/update the relevant `*_REPORT.md`.

---

## 4. Git & Branching Rules for Auto-Fixes

- Prefer creating or targeting **feature/fix branches**, not `main`, for anything beyond Level 1.
- Never auto-commit to `main` without user approval.
- Always:
  - Describe changes in commit messages.
  - Reference the relevant phase/report in the message where possible.

---

## 5. Human Override

At any time, the user can override:

- "Treat this class of change as Level 0/1/2 for now."
- "Do NOT auto-fix this file or area (e.g. legacy code we're not touching yet)."

If such an override is given:
- Solin must remember it for the session.
- If it should be persistent, encode it in rules or docs (e.g. `.cursor/rules`).

---

## 6. Canonical Status

This file is now the **canonical** Auto-Fix policy for Solin v2 **inside the MayAssistant/Maya project**.

- All future automation flows, repo restructure plans, and fix scripts must respect it.
- If future policies (v3, v4, etc.) are added, they should:
  - Explicitly state what changed from v2.
  - Be referenced in `VERSION.md` or `MASTER_HANDOFF.md`.

**End of SOLIN_AUTOFIX_POLICY_V2.md**

