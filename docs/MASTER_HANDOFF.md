# MASTER_HANDOFF.md  
## MayAssistant / Maya Unified Platform — Canonical System Overview (v1.2)
### Authoritative Reference — Read FIRST  
### Last Updated: 2025-01-27  
### Status: POST-CRASH REBUILD (Backend stable, Frontend being restored)

---

# 1. PURPOSE OF THIS DOCUMENT

This file is the **root authority** for the entire MayAssistant platform.

Every AI agent (Claude, Cursor, GPT-based assistants, future agents) MUST:

1. Read this file *before* performing any action.  
2. Treat its content as the **single source of architectural and strategic truth**.  
3. Follow its boundaries when interpreting all other `/docs/*.md` files.  

This document consolidates:

- System status after the v4.0 reset  
- Core architecture (backend + frontend + intelligence)  
- Product strategy (MayAssistant pivot)  
- Required future-proof & accessibility standards  
- Development phases (0 → 3)  
- Safety rules (via Gilman Accords)  
- UX philosophy  
- Auto-build principles  
- Vertical pack strategy  

All other documentation files extend and reinforce this one.

---

# 2. WHY THIS EXISTS (THE CRASH + RESET CONTEXT)

On December 19th, 2024, Maya v4.0 reached its peak state:

- Fully built **Next.js 14+** frontend  
- **Clerk SSO**  
- **10+ pages** (dashboard, agents, automations, developer portal, etc.)  
- **Multi-tenant** workspace model  
- **Themes**, **integrations**, **settings**, **files**, etc.  

Then:

### 🚨 A catastrophic command was executed:
```
git reset --hard origin/main
```

Result:

- **Frontend destroyed (≈100 files lost)**  
- **Backend survived** with 95% functionality  
- **All intelligence modules preserved**  
- **Guardian Framework intact**  
- **Database intact with minor SSO table leftovers**

This documentation suite is part of the **structured recovery**.

---

# 3. CURRENT REAL SYSTEM STATE (v1.2 REWRITE)

## ✔ Backend (Stable • 95% Complete)
- FastAPI (Python)  
- Supabase Postgres  
- AES-256 PII encryption  
- Row Level Security (RLS)  
- 25/25 integration tests passing  
- All 8 intelligence modules operational  
- Guardian Framework (Solin, Vita, Sentra, Aegis, Archivus) intact  
- Microservices:
  - **Nova** → Pricing / QuickBooks  
  - **Eli** → Venue intelligence  

### ⚠ CRITICAL BUG (Phase 0):
**Email search broken due to Fernet random IVs.**  
Fix required:
- Hash migration (`email_hash`) must be executed  
- Then re-run basic tests (expect 9/9 passing)

---

## ❌ Frontend (Needs full rebuild)
After the crash, only the **bookings page** remains.

What must be restored:
- Dashboard  
- Agents panel  
- Automations  
- Developer portal  
- Integrations  
- Payments  
- Messages  
- Files  
- Settings  
- Multi-tenant UI  
- Accessibility engine  
- PRIME/CORE theming  

All rebuilt according to:
- `/docs/FRONTEND_AUTOBUILD_SPEC.md`  
- `/docs/UX_GUIDELINES.md`  
- `/docs/ADAPTIVE_ONBOARDING.md`

---

## ⚙ Deployment (Partially broken)
- Azure Functions pipeline was pointing to the wrong directory → produced 500 errors
- Corrected workflow included in:
  `/docs/DEPLOYMENT_PIPELINE.md`

Backend deploy target: **Azure Functions OR Railway**  
Frontend deploy target: **Vercel**

---

# 4. PRODUCT STRATEGY (MAYASSISTANT PLATFORM)

MayAssistant = one unified AI booking system for ALL appointment-based services.

### Core Concept:
**80% shared platform**  
**20% vertical pack customization**

Vertical packs:

### 🔴 Priority 1 — Beauty Pack  
- huge market (400k–1.5M pros)  
- simple price model  
- SMS-first UX  
- low dev cost, high ROI  

### 🔴 Priority 2 — Events Pack (DJ, AV)  
- 70–85% complete already  
- venue intelligence  
- pricing engine  
- payment links  

Future packs:
- Wellness / Massage  
- Fitness trainers  
- Tutors  
- Pet Groomers  
- Mobile auto detailers  

See: `/docs/PRODUCT_STRATEGY.md`

---

# 5. DEVELOPMENT PHASES (CANONICAL, IN ORDER)

### 🚨 Phase 0 — EMAIL SEARCH FIX (BLOCKER)
- run `email_hash` migration  
- re-run basic tests  
- must reach **9/9 passing** before ANY other work proceeds  

---

### Phase 1 — PAYMENTS (EVENTS → BEAUTY)
- Stripe Payment Links  
- Payment reminders  
- Deposits & balances  
- Reduces Vi’s 25+ hours/month chasing payments

---

### Phase 2 — SMS INTEGRATION (BEAUTY → EVENTS)
- Twilio integration  
- Conversational SMS booking  
- Auto reminders  
- Location-based reminders (optional)  

---

### Phase 3 — FRONTEND RESTORATION (FULL v4.0 REBUILD)
Guided by:
- UX Guidelines  
- Adaptive Onboarding  
- Accessibility / Future-proofing  
- PRIME/CORE themes  

This stage delivers a production-ready SaaS dashboard.

---

# 6. UX & ACCESSIBILITY PHILOSOPHY  
*(Full details in `/docs/UX_GUIDELINES.md`)*

MayAssistant adheres to the **OurBooks Accessibility Model**, enhanced:

- User sets their **complexity level**:
  - Ultra-simple
  - Standard
  - Power User
- Cognitive-friendly design  
- Zero clutter  
- WCAG 2.1 AA  
- Dyslexia mode  
- Color-blind palettes  
- Quiet mode  
- Mobile-first views  

**UI must be “up to the user,” always.**

---

# 7. ADAPTIVE ONBOARDING SYSTEM  
*(Full details in `/docs/ADAPTIVE_ONBOARDING.md`)*

Three modes:

1. **Zero Training**  
2. **Bite-Sized Tips**  
3. **Full Guided Training**  
   - voice → SMS magic moment  
   - real scenarios  
   - short animations  
   - gamified progression  

Matches the MayAssistant philosophy of:
**“Make it optional. Make it magical. Make it smart.”**

---

# 8. AUTO-BUILD PHILOSOPHY  
*(Full specs in FRONTEND_AUTOBUILD + BACKEND_AUTOBUILD)*

Backend:
- test → build → deploy → smoke-test → rollback if needed  
- safe auto-heal allowed  
- no destructive auto-migrations  

Frontend:
- scaffolding → shell → pages → accessibility layer → API integration  
- never overwrite backend docs or architecture  

---

# 9. SAFETY (GILMAN ACCORDS)

The Gilman Accords (= your safety constitution) dictate:

- No dark patterns  
- No manipulative UX  
- No pretending to be human  
- No bypassing consent  
- No unsafe automation  
- Never store raw PII  
- TCPA-compliant SMS  
- PCI-compliant payments  
- Audit everything  

Full accords in: `/docs/GILMAN_ACCORDS.md`

---

# 10. FILES THAT DEFINE THE WHOLE PLATFORM

This file (MASTER_HANDOFF.md) is extended by:

- `GILMAN_ACCORDS.md`  
- `UX_GUIDELINES.md`  
- `ADAPTIVE_ONBOARDING.md`  
- `FRONTEND_AUTOBUILD_SPEC.md`  
- `BACKEND_AUTOBUILD_SPEC.md`  
- `ARCHITECTURE_OVERVIEW.md`  
- `VERTICAL_PACKS.md`  
- `PRODUCT_STRATEGY.md`  
- `DEPLOYMENT_PIPELINE.md`  

No agent should proceed without reading this file first.

---

# 11. FINAL MANDATE

For anyone touching code (human or AI):

### ✔ Follow this doc as law  
### ✔ Follow Gilman Accords as morality  
### ✔ Follow UX_GUIDELINES as experience  
### ✔ Follow AUTOBUILD specs for execution  

Never violate safety.  
Never violate clarity.  
Never violate trust.

This platform exists to **reduce stress**, not create it.

**END OF MASTER_HANDOFF.md**
