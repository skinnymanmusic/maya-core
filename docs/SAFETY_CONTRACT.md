# SAFETY CONTRACT (Humans + AI)

**Status:** Operational agreement  
**Applies to:** Humans, Solin, Claude, Copilot, and any other AI agents

## 1. Shared Responsibilities

- **Humans**:
  - Own final decisions on production changes.
  - Approve PRs that change protected code or dependencies.
  - Decide when to promote from staging to production.
- **AI Agents**:
  - MUST follow all policies:
    - Gilman Accords
    - Backend Integrity Policy
    - Dependency Policy
    - Self-Update Policy
    - Solin Auto-Fix Policy v2
    - Security–UX Harmony Rules
  - MUST pause and ask for approval when:
    - Changing protected areas.
    - Changing dependencies.
    - Changing CI/CD semantics.

## 2. Non-Negotiable Rules

- No AI may:
  - Push directly to `main`.
  - Bypass CI or tests.
  - Modify migrations without explicit request.
  - Touch payment logic or guardian core without label + review.
- No human should:
  - Force-merge failing PRs into `main`.
  - Disable safety workflows without documenting why.

## 3. Approval Labels

- `approved-core-change`  
  Required when:
  - Protected backend paths are modified.

- `approved-dependency-upgrade`  
  Required when:
  - `backend/requirements.txt` or `backend/requirements.lock` changes.

More labels can be added later; these are core for Integrity Pack v1.

## 4. UX vs Security

- When UX comfort conflicts with security/privacy:
  - **Security wins**, but:
    - Provide clear explanation.
    - Offer "expert mode" or opt-out where safe.
- AI proposals must:
  - Avoid dark patterns.
  - Avoid surprising or irreversible flows.

## 5. Violations

If any policy is broken:

- Log a SYSTEM CORRECTION EVENT.
- Document:
  - What happened.
  - Impact.
  - What guardrail will prevent recurrence.

This contract is living; updates must be documented and versioned.

