# RUN_ORDER.md  
## Cursor Execution Sequence for Automatic Build (v1.2)

This file tells Cursor EXACTLY how to restore the entire system safely.

---

# 🔥 MASTER RUN ORDER — DO NOT DEVIATE

---

# 0️⃣ PRE-CHECKS (MANDATORY)

Cursor must:

1. Read `/docs/MASTER_HANDOFF.md`
2. Read `/cursor/rules/*.md`
3. Validate repo structure exists
4. Confirm backend + frontend directories exist
5. Confirm no destructive actions

---

# 1️⃣ PHASE 0 — EMAIL HASH FIX (BLOCKER)

Before ANY build actions:

```
@cursor fix Phase 0
```

Cursor must:

- Inspect DB schema for `email_hash`
- Migrate legacy Fernet emails → hashed emails
- Run 9/9 basic email tests
- Abort if tests fail

---

# 2️⃣ PHASE 1 — BACKEND BUILD & STABILIZE

Sequence:

1. Install Python dependencies  
2. Run full backend test suite (25/25)  
3. Confirm 0 errors  
4. Prepare deployment package  
5. Run smoke test instructions  
6. Ask user before deploy

Backend spec lives in:  
`/docs/BACKEND_AUTOBUILD_SPEC.md`

---

# 3️⃣ PHASE 2 — FRONTEND REBUILD

Sequence:

1. Scaffold or re-scaffold `/frontend/`
2. Build global layout (sidebar + topbar)
3. Add accessibility panel
4. Add theme engine
5. Build all pages as stubs
6. Implement components from `ui/`
7. Connect API to backend
8. Add adaptive onboarding modes
9. Run local preview
10. Only then deploy to Vercel (user approval needed)

Frontend spec lives in:  
`/docs/FRONTEND_AUTOBUILD_SPEC.md`

---

# 4️⃣ PHASE 3 — SMS + PAYMENTS

Cursor must follow Phase definitions:

### Payments (Stripe)
- Payment links  
- Reminders  
- Deposits  
- Testing through Sandbox

### SMS (Twilio)
- Conversational flow  
- STOP compliance  
- Reminder engine  
- Test mode only until release  

---

# 5️⃣ PHASE 4 — FINAL STABILIZATION

Steps:

1. Run full lint  
2. Run full test suite (backend + frontend)  
3. Run Lighthouse for UX  
4. Confirm accessibility  
5. Confirm logging + audit  
6. Final deploy (backend → frontend)

---

# 6️⃣ RULES FOR ASK/PAUSE

Cursor must ALWAYS pause and ask before:

- deleting files  
- replacing directories  
- altering backend logic  
- performing API changes  
- applying migrations  
- deploying to production  
- altering database schema  

---

# 7️⃣ OUT OF SCOPE FOR CURSOR

Cursor is NOT allowed to:

- invent features  
- create microservices  
- create jobs not in docs  
- change architecture  
- modify AI behavior  
- touch the Guardian Framework  

---

END OF RUN_ORDER.md
