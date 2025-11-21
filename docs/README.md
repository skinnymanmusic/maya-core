# Welcome to the MayAssistant Documentation Suite (v1.2)

This `/docs` folder contains the **canonical, authoritative, AI-safe** documentation for the MayAssistant platform.

Every document in this directory works together to define:

- Architecture  
- Safety rules  
- UX guidelines  
- Adaptive onboarding  
- Product strategy  
- Vertical packs  
- Deployment pipeline  
- Auto-build specs (frontend + backend)  
- AI agent behavior  
- Engineering standards  

**All AI agents (Cursor, Claude, ChatGPT) MUST read `MASTER_HANDOFF.md` first.**

---

# 📚 Documentation Index

| File | Purpose |
|------|---------|
| **MASTER_HANDOFF.md** | The master reference. Architecture, phases, strategy, system truth. |
| **GILMAN_ACCORDS.md** | Ethical, legal, safety, UX, and compliance rules. Read second. |
| **UX_GUIDELINES.md** | Complete visual + interaction design standards. |
| **ADAPTIVE_ONBOARDING.md** | Optional, fluid, magical onboarding system. |
| **FRONTEND_AUTOBUILD_SPEC.md** | How to rebuild the entire frontend safely. |
| **BACKEND_AUTOBUILD_SPEC.md** | How to build, test, deploy, and auto-heal backend. |
| **ARCHITECTURE_OVERVIEW.md** | High-level engineering diagram + flow logic. |
| **VERTICAL_PACKS.md** | Horizontal → vertical expansion model. Config-driven. |
| **PRODUCT_STRATEGY.md** | Market strategy, pricing, and multi-vertical rollout. |
| **DEPLOYMENT_PIPELINE.md** | CI/CD, smoke tests, rollback, and environment rules. |

---

# 🧠 AI Agent Rules (Summary)

Before modifying ANYTHING:

1. **Read MASTER_HANDOFF.md**
2. Follow **GILMAN_ACCORDS.md**
3. Use AUTOBUILD specs for execution
4. NEVER rewrite docs unless asked
5. NEVER hallucinate architecture or files

---

# 🚦 Development Phases (Short)

### Phase 0 — Email Hash Migration  
Mandatory. Tests must reach **9/9 passing**.

### Phase 1 — Payment integration  
Stripe links, reminders, deposits.

### Phase 2 — SMS integration  
Twilio conversational flows.

### Phase 3 — Frontend rebuild  
Next.js 14 + full dashboard.

---

# 🔗 Repo Navigation

- `/frontend/` → Next.js app  
- `/backend/` → FastAPI + services  
- `/packs/` → Vertical pack configs  
- `/docs/` → YOU ARE HERE  
- `/infrastructure/` → CI/CD, Azure Functions, Railway  
- `/tests/` → Backend + frontend tests  

---

If you’re an AI assistant:  
**Ask before performing destructive actions.**

If you’re a human:  
**Copy/paste freely. No command interpretation happens here.**

END OF README.md
