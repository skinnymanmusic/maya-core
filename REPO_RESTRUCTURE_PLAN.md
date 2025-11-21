# REPO RESTRUCTURE PLAN
**Generated:** 2025-01-27  
**Status:** PROPOSED - Awaiting Approval  
**Purpose:** Align repository structure with `/docs/README.md` recommendations

---

## 📋 EXECUTIVE SUMMARY

This plan restructures the repository to match the canonical structure defined in `/docs/README.md`:
- `/frontend/` → Next.js app
- `/backend/` → FastAPI + services  
- `/packs/` → Vertical pack configs
- `/docs/` → Documentation
- `/infrastructure/` → CI/CD, Azure Functions, Railway
- `/tests/` → Backend + frontend tests

**Principles:**
- ✅ Copy files, never delete originals
- ✅ Ask for confirmation before removing originals
- ✅ No code modifications
- ✅ No import rewrites
- ✅ Preserve all existing files

---

## 🟢 PHASE 1: FOLDER CREATION (ALL SAFE)

### Step 1.1: Create Missing Root Directories
**Status:** ✅ SAFE  
**Action:** Create empty directories

- [x] `/packs/` - Already created (empty)
- [x] `/infrastructure/` - Already created (empty)
- [ ] `/tests/` - Create at root level (will contain both backend and frontend tests)

**Rationale:** These directories are required per `/docs/README.md` and are currently missing or incomplete.

---

## 🟡 PHASE 2: FRONTEND RENAME (REQUIRES FILE MOVES)

### Step 2.1: Copy Frontend Directory
**Status:** ⚠️ UNSAFE (requires file moves, import updates)  
**Action:** Copy entire `/omega-frontend/` to `/frontend/`

**Files to Copy:**
- All files and subdirectories from `/omega-frontend/` to `/frontend/`

**Impact:**
- Will require updating:
  - `package.json` scripts
  - Vercel configuration
  - GitHub Actions workflows
  - Any absolute path references
  - Import statements in other files

**Confirmation Required:** Yes - This is a major structural change

**Note:** After successful copy and verification, original `/omega-frontend/` can be removed (with approval).

---

## 🟢 PHASE 3: INFRASTRUCTURE ORGANIZATION (SAFE COPIES)

### Step 3.1: Move CI/CD Configuration Files
**Status:** ✅ SAFE (copy only)  
**Action:** Copy infrastructure files to `/infrastructure/`

**Files to Copy:**
- `/.github/workflows/` → `/infrastructure/.github/workflows/` (if exists)
- `/backend/railway.json` → `/infrastructure/railway.json`
- `/backend/nixpacks.toml` → `/infrastructure/nixpacks.toml`
- `/backend/Procfile` → `/infrastructure/Procfile`
- `/backend/vercel.json` → `/infrastructure/vercel-vercel.json` (rename to avoid conflict)
- Root `host.json` → `/infrastructure/azure-functions-host.json`
- Root `local.settings.json` → `/infrastructure/azure-functions-local.settings.json` (if not sensitive)

**Confirmation Required:** Yes - Verify these files are not actively referenced by deployment systems

---

### Step 3.2: Archive Legacy Azure Functions Code
**Status:** ✅ SAFE (copy to archive)  
**Action:** Copy legacy Azure Functions code to `/infrastructure/archive/azure-functions/`

**Directories/Files to Copy:**
- `/api/` → `/infrastructure/archive/azure-functions/api/`
- `/functions/` → `/infrastructure/archive/azure-functions/functions/`
- `/legacy_v3_functions/` → `/infrastructure/archive/azure-functions/legacy_v3/`
- `/deploy_tmp/` → `/infrastructure/archive/azure-functions/deploy_tmp/`
- Root `index.js` → `/infrastructure/archive/azure-functions/index.js`

**Confirmation Required:** Yes - Verify these are truly legacy and not in use

---

## 🟢 PHASE 4: DOCUMENTATION ORGANIZATION (SAFE COPIES)

### Step 4.1: Organize Root-Level Documentation
**Status:** ✅ SAFE (copy only)  
**Action:** Copy markdown files to appropriate locations

**Files to Copy to `/docs/reports/`:**
- `MAYA_V3_IMPLEMENTATION_COMPLETE.md`
- `GITHUB_UPLOAD_REPORT.md`
- `QUICK_STATUS_REPORT.md`
- `SESSION_REPORT.md`
- `DOCUMENTATION_INDEX.md`
- `AZURE_CLI_SETUP.md`
- `README_AZURE_FUNCTIONS.md`
- `README.md` (if different from `/docs/README.md`)

**Files to Copy to `/docs/archive/`:**
- Root-level completion/verification reports that are historical

**Confirmation Required:** Yes - Verify which files are still actively used

---

### Step 4.2: Organize Backend Documentation
**Status:** ✅ SAFE (copy only)  
**Action:** Copy backend markdown files to `/docs/reports/` or `/docs/archive/`

**Files to Copy:**
- `/backend/CLAUDE_PROGRESS_LOG.md` → `/docs/reports/CLAUDE_PROGRESS_LOG.md` (or keep in backend if actively maintained)
- `/backend/PHASE_*_COMPLETE.md` → `/docs/reports/phase-completion/`
- `/backend/*_VERIFICATION.md` → `/docs/reports/verification/`
- `/backend/*_REPORT.md` → `/docs/reports/`
- `/backend/OMEGA_OVERVIEW.md` → `/docs/archive/OMEGA_OVERVIEW.md` (superseded by ARCHITECTURE_OVERVIEW.md)
- `/backend/MASTER_REFERENCE_DOCUMENT.md` → `/docs/archive/` (superseded by MASTER_HANDOFF.md)

**Confirmation Required:** Yes - Some of these may be actively referenced

---

### Step 4.3: Organize Frontend Documentation
**Status:** ✅ SAFE (copy only)  
**Action:** Copy frontend markdown files

**Files to Copy:**
- `/omega-frontend/PHASE_3_WEEK_2_COMPLETE.md` → `/docs/reports/phase-completion/`
- `/omega-frontend/ICONS_NEEDED.md` → `/docs/notes/ICONS_NEEDED.md`

---

## 🟢 PHASE 5: TEST ORGANIZATION (SAFE COPIES)

### Step 5.1: Create Root Tests Directory Structure
**Status:** ✅ SAFE  
**Action:** Create directory structure and copy tests

**Structure to Create:**
```
/tests/
  /backend/
  /frontend/
```

**Files to Copy:**
- `/backend/tests/` → `/tests/backend/` (copy all test files)

**Note:** Frontend tests will be created during Phase 3 frontend rebuild

**Confirmation Required:** Yes - Verify test runners and CI/CD won't break

---

## 🟢 PHASE 6: LEGACY DIRECTORY ARCHIVING (SAFE COPIES)

### Step 6.1: Archive Legacy Frontend Directories
**Status:** ✅ SAFE (copy to archive)  
**Action:** Copy legacy frontend code to `/infrastructure/archive/frontend/`

**Directories to Copy:**
- `/dashboard/` → `/infrastructure/archive/frontend/dashboard/`
- `/dev-portal/` → `/infrastructure/archive/frontend/dev-portal/`

**Confirmation Required:** Yes - Verify these are not in use

---

### Step 6.2: Archive Legacy Shared Code
**Status:** ✅ SAFE (copy to archive)  
**Action:** Copy legacy shared code

**Directories to Copy:**
- `/shared/` → `/infrastructure/archive/shared/`

**Confirmation Required:** Yes - Verify nothing actively imports from `/shared/`

---

### Step 6.3: Archive Microservice Directories
**Status:** ⚠️ UNSAFE (may be actively used)  
**Action:** Copy microservice directories (verify usage first)

**Directories to Copy (if confirmed legacy):**
- `/eli-backend/` → `/infrastructure/archive/microservices/eli-backend/`
- `/nova-backend/` → `/infrastructure/archive/microservices/nova-backend/`

**Confirmation Required:** **CRITICAL** - These may be active microservices referenced by backend

**Note:** Per `MASTER_HANDOFF.md`, Nova and Eli are active microservices. These should likely stay in root or move to `/infrastructure/microservices/` (not archive).

---

## 🟢 PHASE 7: SCRIPT ORGANIZATION (SAFE COPIES)

### Step 7.1: Organize Root-Level Scripts
**Status:** ✅ SAFE (copy only)  
**Action:** Copy setup and utility scripts

**Files to Copy to `/infrastructure/scripts/`:**
- `complete_setup.sh`
- `fix_github_secrets.sh`
- `migrate_to_v4.sh`
- `setup_maya_rbac.sh`
- `setup_patch_runners_unistring.py`
- `set_github_secrets.ps1`

**Confirmation Required:** Yes - Verify these scripts don't have hardcoded paths

---

### Step 7.2: Organize Backend Scripts
**Status:** ✅ SAFE (copy only)  
**Action:** Backend scripts are already in `/backend/scripts/` - verify if any should move

**Current Location:** `/backend/scripts/` ✓ (already organized)

---

## 🟢 PHASE 8: BACKEND FILE ORGANIZATION (SAFE COPIES)

### Step 8.1: Organize Backend Root Files
**Status:** ✅ SAFE (copy only)  
**Action:** Copy backend root files to appropriate locations

**Migration Scripts (keep in backend, already organized):**
- `/backend/apply_*.py` - Keep in backend (actively used)

**Utility Scripts:**
- `/backend/fix_email_search.py` → Keep in backend (actively used)
- `/backend/fix_email_search.bat` → Keep in backend (actively used)

**Configuration Files:**
- `/backend/requirements.txt` - Keep in backend ✓
- `/backend/Procfile` - Copy to `/infrastructure/` (see Step 3.1)
- `/backend/railway.json` - Copy to `/infrastructure/` (see Step 3.1)
- `/backend/nixpacks.toml` - Copy to `/infrastructure/` (see Step 3.1)

**Credentials (verify .gitignore):**
- `/backend/credentials/` - Verify in `.gitignore`, keep in backend if needed for local dev

---

## 🟡 PHASE 9: VERTICAL PACKS STRUCTURE (SAFE - EMPTY DIRECTORIES)

### Step 9.1: Create Pack Directory Structure
**Status:** ✅ SAFE  
**Action:** Create empty pack directories per `VERTICAL_PACKS.md`

**Directories to Create:**
- `/packs/beauty/` (empty, will contain `config.json` later)
- `/packs/events/` (empty, will contain `config.json` later)
- `/packs/wellness/` (empty, future)
- `/packs/fitness/` (empty, future)

**Confirmation Required:** No - These are empty directories

---

## 📊 SUMMARY BY SAFETY LEVEL

### ✅ SAFE Operations (Can proceed immediately):
- Create `/tests/` directory structure
- Create pack directories (`/packs/beauty/`, `/packs/events/`, etc.)
- Copy documentation files to `/docs/reports/` and `/docs/archive/`
- Copy infrastructure config files to `/infrastructure/`
- Copy legacy code to `/infrastructure/archive/`
- Copy scripts to `/infrastructure/scripts/`

### ⚠️ UNSAFE Operations (Require careful planning):
- Rename `/omega-frontend/` → `/frontend/` (requires import updates, config changes)
- Move microservice directories (may be actively referenced)
- Remove original files after copying (requires explicit approval)

---

## 🔍 VERIFICATION CHECKLIST

Before executing any phase:

- [ ] Verify no active references to paths being moved
- [ ] Check `.gitignore` for files that shouldn't be moved
- [ ] Verify CI/CD workflows won't break
- [ ] Check `package.json` scripts for hardcoded paths
- [ ] Verify deployment configurations
- [ ] Check import statements in code
- [ ] Verify test runners and paths

---

## 📝 EXECUTION ORDER

**Recommended Sequence:**
1. **Phase 1** - Create missing directories (SAFE)
2. **Phase 9** - Create pack structure (SAFE)
3. **Phase 3** - Copy infrastructure files (SAFE, verify first)
4. **Phase 4** - Organize documentation (SAFE)
5. **Phase 5** - Organize tests (SAFE, verify test runners)
6. **Phase 6** - Archive legacy code (SAFE, verify not in use)
7. **Phase 7** - Organize scripts (SAFE, verify paths)
8. **Phase 8** - Organize backend files (SAFE)
9. **Phase 2** - Frontend rename (UNSAFE - requires approval and import updates)

---

## ⚠️ CRITICAL WARNINGS

1. **Frontend Rename:** Will break all references to `/omega-frontend/`. Must update:
   - Vercel configuration
   - GitHub Actions workflows
   - Any absolute imports
   - Documentation references

2. **Microservices:** `/eli-backend/` and `/nova-backend/` may be actively used. Verify before moving.

3. **Credentials:** `/backend/credentials/` should remain in backend if needed for local development. Verify `.gitignore`.

4. **Test Runners:** Moving `/backend/tests/` to `/tests/backend/` may break test runners. Verify pytest configuration.

---

## ✅ APPROVAL REQUIRED

**Before executing any phase, confirm:**
- [ ] Which phases to execute
- [ ] Which files/directories are safe to archive
- [ ] Whether frontend rename should proceed
- [ ] Whether microservice directories should be moved or archived
- [ ] Whether original files should be removed after copying

---

**END OF REPO_RESTRUCTURE_PLAN.md**

