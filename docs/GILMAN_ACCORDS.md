# GILMAN_ACCORDS.md  
## MayAssistant Safety, Ethics, Compliance & UX Standards (v1.2)
### This document governs ALL engineering, UX, AI behavior, automation, and deployment.
### Last Updated: 2025-01-27

---

# 1. PURPOSE OF THESE ACCORDS

The Gilman Accords define the **ethical boundaries**, **legal requirements**, and **experience standards** for building and maintaining the MayAssistant platform.

These rules apply to:

- Backend and frontend developers  
- AI agents (Claude, Cursor, GPT-based assistants)  
- Microservices (Maya, Solin, Nova, Eli, Vita, Sentra, Aegis, Archivus)  
- Any future AI or automation pipeline  

These Accords MUST be followed at every stage of design, engineering, and deployment.

Breaking the Accords = breaking the platform’s integrity.

---

# 2. CORE ETHICAL PRINCIPLES  
### (These cannot be bent or bypassed. They define your brand.)

### ✔ Honesty  
- Maya/MayAssistant NEVER pretends to be human.  
- Do not obscure intent in UI or messaging.  
- Do not use manipulative copy or pressure tactics.

### ✔ Transparency  
- If an AI is taking action, the user must know.  
- Every automation must be visible + controllable.

### ✔ Respect for Cognitive Load  
- Never overwhelm a user.  
- No unnecessary screens or required steps.  
- No surprise actions.

### ✔ Zero Dark Patterns  
Absolutely forbidden:
- guilt-trip modals  
- fake countdown timers  
- deceptive CTAs  
- forced upsells  
- trick cancellations  

### ✔ Compassionate UX  
Every flow should reduce stress — not add to it.

---

# 3. LEGAL COMPLIANCE  
### (Non-negotiable. We avoid liability at all costs.)

## SMS — TCPA Compliance
- Explicit opt-in required  
- Identity MUST be present in every message  
- “STOP” must instantly unsubscribe  
- No marketing without prior consent  
- No silent background messages  

## Email — CAN-SPAM Baseline
- Business identity in footer  
- Unsubscribe link required for non-transactional emails  
- No misleading subject lines  

## Payments — PCI Compliance
- Card info handled ONLY by Stripe  
- No card data stored in DB logs or memory  
- Stripe keys stored in environment variables ONLY  

## Privacy — Data Protection Laws
- Encrypt PII at rest (AES-256 via Supabase)  
- Never log raw PII (email, phone, address)  
- Deterministic hashing for search (`email_hash`)  

## Record Keeping
- Audit logs must track:
  - automations  
  - payment actions  
  - SMS sends  
  - email sends  
  - timeline events  

---

# 4. DATA & SECURITY RULES  

### ✔ Encryption  
All sensitive fields:
- email  
- phone  
- notes  
- client identifiers  

must be encrypted at rest.

### ✔ Deterministic Hashing  
All search queries use:
- SHA-256 `email_hash`  
- Never use encrypted email for search  

### ✔ No Raw Logs  
Logs must NEVER contain:
- raw emails  
- raw phone numbers  
- full names  
- payment details  

### ✔ Environment Variables Only  
- No secrets in code  
- No inline tokens  
- No credentials committed, ever  

### ✔ Rate Limiting  
MayAssistant must self-protect:
- per-IP  
- per-user  
- per-workspace  
- per-token  
to avoid spam or accidental loops.

---

# 5. ACCESSIBILITY ACCORDS  
### (Shared DNA with OurBooks’ accessibility philosophy)

MayAssistant MUST:

- Support large text modes  
- Provide a dyslexia-friendly font  
- Provide color-blind palettes  
- Provide “quiet mode” (reduced animation + notifications)  
- Provide predictable navigation  
- Support keyboard navigation  
- Meet or exceed WCAG 2.1 AA  

Accessibility isn’t optional — it’s a competitive advantage.

---

# 6. AI BEHAVIOR RULES  
### (All agents MUST obey these.)

### ✔ Safe Mode  
Trigger when:
- unexpected user intent  
- ambiguous instructions  
- partial data  
- anomalies in emails/SMS  
- failed migrations  
- deployment inconsistencies  

In Safe Mode:
- No destructive actions  
- No irreversible actions  
- No payments  
- No external sends unless explicitly approved  

### ✔ No Hallucinations  
AI must NOT:
- invent data  
- invent pricing  
- invent schedules  
- invent venue details  

### ✔ Escalation  
If uncertain:
- ask the user  
- or ask another agent  
- or switch to Safe Mode  

### ✔ No Auto-Execution Without Context  
AI may:
- generate code  
- propose actions  
- prepare steps  

AI may NOT:
- run destructive commands  
- deploy to production  
- alter database schema  
Without explicit instruction.

---

# 7. USER EXPERIENCE ACCORDS  
### (The UX must feel ethical, modern, lightweight, and empowering.)

- Respect user time  
- Minimize cognitive load  
- Provide clear and simple flows  
- Avoid unnecessary modals  
- Navigation must be consistent  
- Onboarding must feel optional, not forced  
- Everything is reversible  
- Users should NEVER feel “locked in”  

---

# 8. DEPLOYMENT ACCORDS

### ✔ Tests must pass  
- Backend tests (25/25)  
- Basic email search tests (9/9)  

### ✔ No silent deployments  
User must approve production deploys.

### ✔ Auto-heal restrictions  
Allowed:
- soft restarts  
- transient retry  
- restoring previous deployment  

Not allowed:
- auto-running migrations  
- modifying DB schemas  
- altering user data  

---

# 9. AGENT GOVERNANCE  
### (How Claude, Cursor, Solin, etc. work together.)

- MASTER_HANDOFF.md is law  
- Gilman Accords is morality  
- Cursor must follow execution specs only  
- Claude handles reasoning + architecture  
- Solin oversees hierarchy & safety  
- Maya is the end-user personality  
- Nova & Eli remain microservices  

All agents must align outputs — no contradictions.

---

# 10. NON-NEGOTIABLES (HARD RULES)

### ❌ NO auto-sending to real clients  
### ❌ NO bypassing Safe Mode  
### ❌ NO hallucinated data  
### ❌ NO storing raw PII  
### ❌ NO destructive schema changes without human approval  
### ❌ NO dark patterns or manipulative UX  
### ❌ NO ignoring accessibility  

### ✔ ALWAYS validate input  
### ✔ ALWAYS audit log  
### ✔ ALWAYS escalate when unsure  
### ✔ ALWAYS ask before irreversible actions  

---

# 11. FINAL STATEMENT

These Accords exist to protect:

- the user  
- the business  
- the system  
- the brand  
- the AI  
- the future you’re building  

MayAssistant succeeds by being:
- safer  
- cleaner  
- faster  
- more ethical  
- more accessible  
than every competitor.

**END OF GILMAN_ACCORDS.md**
