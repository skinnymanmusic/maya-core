# BACKEND_AUTOBUILD_SPEC.md  
## Automated Backend Build, Test & Deploy Instructions (v1.2)

Last Updated: 2025-01-27

---

# 1. PURPOSE
This file defines exactly how the backend should:
- build  
- test  
- deploy  
- smoke-test  
- auto-heal (safe modes only)  

Backend stack:
- FastAPI  
- PostgreSQL (Supabase)  
- AES-256 encrypted fields  
- Microservices: Nova, Eli  
- Guardian Framework  

---

# 2. PHASE 0 — EMAIL HASH MIGRATION (BLOCKER)

Before ANY build:

1. Check if `email_hash` column exists.  
2. If empty → run migration script.  
3. Re-run basic tests.  
4. Must reach **9/9**.  
5. Abort if not passing.

This step ensures deterministic search.

---

# 3. TEST REQUIREMENTS (Mandatory)

Backend must pass:

### ✔ 25/25 integration tests  
### ✔ 9/9 basic tests  
### ✔ Lint checks  
### ✔ Type checks  

Failing any test = STOP BUILD.

---

# 4. BUILD SEQUENCE

### Step 1 — Install dependencies
```
pip install -r requirements.txt
```

### Step 2 — Run tests
```
pytest
```

### Step 3 — Package backend
If Railway:
- build Docker imag
