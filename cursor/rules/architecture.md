# ARCHITECTURE RULES — MayAssistant v1.2

Cursor MUST adhere to:

- Backend: FastAPI + Supabase Postgres  
- Frontend: Next.js 14 (App Router)  
- Deployment: Azure Functions (backend), Vercel (frontend)  
- Multi-tenant architecture  
- AES-256 encryption  
- Deterministic hashing for email search  
- Microservices: Nova (pricing), Eli (venue intelligence)  
- Guardian Framework components must NOT be altered

Cursor must NEVER:

- Introduce new frameworks  
- Replace FastAPI  
- Replace Next.js  
- Replace the database  
- Remove the intelligence modules  
