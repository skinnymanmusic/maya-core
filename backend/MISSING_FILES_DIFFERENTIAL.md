# MISSING FILES DIFFERENTIAL LIST
**Generated:** After git reset --hard origin/main  
**Purpose:** Track all files that existed before reset but are now missing  
**Status:** Files need to be rebuilt

---

## ✅ FILES THAT EXIST (Rebuilt)

### Core Configuration
- ✅ `backend/requirements.txt`
- ✅ `backend/app/config.py`
- ✅ `backend/app/main.py`
- ✅ `backend/app/database.py`

### Middleware
- ✅ `backend/app/middleware/__init__.py`
- ✅ `backend/app/middleware/security.py`
- ✅ `backend/app/middleware/tenant_context.py`

### Routers
- ✅ `backend/app/routers/__init__.py`
- ✅ `backend/app/routers/health.py`

### Documentation
- ✅ `backend/CLAUDE_PROGRESS_LOG.md`
- ✅ `backend/OMEGA_OVERVIEW.md`

---

## ❌ MISSING FILES (Need to be Rebuilt)

### 🔴 CRITICAL - Core Services (HIGH PRIORITY)

#### Email Processing
- ❌ `backend/app/services/email_processor_v3.py` - Main email processing pipeline
- ❌ `backend/app/services/gmail_service.py` - Gmail API integration
- ❌ `backend/app/services/gmail_webhook.py` - Webhook verification & processing
- ❌ `backend/app/services/claude_service.py` - Claude AI integration

#### Calendar
- ❌ `backend/app/services/calendar_service_v3.py` - Calendar operations & auto-blocking

#### Audit & Security
- ❌ `backend/app/services/audit_service.py` - Comprehensive audit logging
- ❌ `backend/app/services/idempotency_service.py` - Idempotency layer
- ❌ `backend/app/services/retry_queue_service.py` - Retry queue management
- ❌ `backend/app/services/supabase_service.py` - Supabase/PostgreSQL operations

#### Intelligence Services
- ❌ `backend/app/services/archivus_service.py` - Long-term memory engine
- ❌ `backend/app/services/aegis_service.py` - Security & threat intelligence
- ❌ `backend/app/services/eli_service.py` - Venue intelligence integration

#### Encryption & Utilities
- ❌ `backend/app/encryption.py` - AES-256 encryption service
- ❌ `backend/app/utils/password_policy.py` - Password validation
- ❌ `backend/app/utils/__init__.py`

---

### 🔴 CRITICAL - Intelligence Modules (8 Total)

**Location:** `backend/app/services/intelligence/`

- ❌ `backend/app/services/intelligence/__init__.py` - Module exports
- ❌ `backend/app/services/intelligence/venue_intelligence.py` - Venue detection
- ❌ `backend/app/services/intelligence/coordinator_detection.py` - Multi-event detection
- ❌ `backend/app/services/intelligence/acceptance_detection.py` - Acceptance detection
- ❌ `backend/app/services/intelligence/missing_info_detection.py` - Missing info detection
- ❌ `backend/app/services/intelligence/equipment_awareness.py` - Equipment awareness
- ❌ `backend/app/services/intelligence/thread_history.py` - Thread context
- ❌ `backend/app/services/intelligence/multi_account_email.py` - Account routing
- ❌ `backend/app/services/intelligence/context_reconstruction.py` - Client context

---

### 🔴 CRITICAL - API Routers

- ❌ `backend/app/routers/gmail.py` - Gmail webhook & watch endpoints
- ❌ `backend/app/routers/calendar.py` - Calendar CRUD endpoints
- ❌ `backend/app/routers/clients.py` - Client management endpoints
- ❌ `backend/app/routers/auth.py` - Authentication endpoints (JWT)
- ❌ `backend/app/routers/agents.py` - Agent management endpoints
- ❌ `backend/app/routers/metrics.py` - System metrics endpoints
- ❌ `backend/app/routers/unsafe_threads.py` - Unsafe threads admin API

---

### 🔴 CRITICAL - Guardian Framework

**Location:** `backend/app/guardians/`

- ❌ `backend/app/guardians/__init__.py` - Package exports
- ❌ `backend/app/guardians/solin_mcp.py` - Master Control Program
- ❌ `backend/app/guardians/sentra_safety.py` - Safety enforcement AI
- ❌ `backend/app/guardians/vita_repair.py` - Automated repair AI
- ❌ `backend/app/guardians/guardian_manager.py` - Guardian event routing
- ❌ `backend/app/guardians/guardian_daemon.py` - Background monitoring daemon

---

### 🔴 CRITICAL - Data Models

**Location:** `backend/app/models/`

- ❌ `backend/app/models/__init__.py` - Model exports
- ❌ `backend/app/models/email.py` - Email data models
- ❌ `backend/app/models/archivus.py` - Archivus memory models
- ❌ `backend/app/models/client.py` - Client data models
- ❌ `backend/app/models/calendar.py` - Calendar event models
- ❌ `backend/app/models/user.py` - User/auth models

---

### 🟡 IMPORTANT - Database Migrations

**Location:** `backend/migrations/` (DIRECTORY MISSING)

- ❌ `backend/migrations/001_add_email_hash.sql`
- ❌ `backend/migrations/002_add_calendar_events.sql`
- ❌ `backend/migrations/003_add_idempotency_tables.sql`
- ❌ `backend/migrations/004_performance_indexes.sql`
- ❌ `backend/migrations/005_add_unsafe_threads.sql`
- ❌ `backend/migrations/006_add_repair_log.sql`
- ❌ `backend/migrations/007_add_system_state.sql`
- ❌ `backend/migrations/011_archivus_schema.sql`

---

### 🟡 IMPORTANT - Workers

**Location:** `backend/app/workers/`

- ❌ `backend/app/workers/__init__.py`
- ❌ `backend/app/workers/email_retry_worker.py` - Retry queue worker
- ❌ `backend/app/workers/retry_worker.py` - Legacy retry worker

---

### 🟡 IMPORTANT - Dependencies & Configuration

**Location:** `backend/app/dependencies/`

- ❌ `backend/app/dependencies/__init__.py`
- ❌ `backend/app/dependencies/roles.py` - Role-based access control

**Location:** `backend/`

- ❌ `backend/nixpacks.toml` - Railway build configuration
- ❌ `backend/Procfile` - Process file for Railway
- ❌ `backend/.env.example` - Environment variable template

---

### 🟡 IMPORTANT - Test Suite

**Location:** `backend/tests/`

- ❌ `backend/tests/__init__.py`
- ❌ `backend/tests/fixtures.py` - Test fixtures
- ❌ `backend/tests/test_pipeline.py` - Pipeline integration tests
- ❌ `backend/tests/test_acceptance_ab.py` - Acceptance A/B tests
- ❌ `backend/tests/test_intelligence.py` - Intelligence service tests
- ❌ `backend/tests/test_calendar.py` - Calendar service tests
- ❌ `backend/tests/test_pricing_integration.py` - Nova pricing tests
- ❌ `backend/tests/test_aegis_integration.py` - Aegis integration tests
- ❌ `backend/tests/test_archivus_service.py` - Archivus service tests
- ❌ `backend/tests/test_safety_gate_phase5.py` - Safety gate tests
- ❌ `backend/tests/test_runner.py` - Master test runner

---

### 🟡 IMPORTANT - Scripts

**Location:** `backend/scripts/`

- ❌ `backend/scripts/safety_gate_phase5.py` - Pre-deployment safety gate
- ❌ `backend/scripts/startup_schema_check.py` - Schema drift detection
- ❌ `backend/scripts/v4_backfill_agent_profiles.py` - Agent profile backfill

**Location:** `backend/scripts/dev/` (DIRECTORY MISSING)

- ❌ Multiple development utility scripts (26+ files)

**Location:** `backend/scripts/deployment/` (DIRECTORY MISSING)

- ❌ Deployment scripts

---

### 🟢 OPTIONAL - Archive & Legacy

**Location:** `backend/archive/services/` (DIRECTORY MISSING)

- ❌ `backend/archive/services/email_processor.py` - v2 email processor (for A/B testing)
- ❌ `backend/archive/services/calendar_service.py` - v1 calendar service
- ❌ `backend/archive/services/firestore_service.py` - Legacy Firestore service

---

### 🟢 OPTIONAL - Documentation

**Location:** `backend/docs/` (DIRECTORY MISSING)

- ❌ `backend/docs/omega_core_v3_spec.md` - Master specification
- ❌ `backend/docs/aegis_agent_spec.md` - Aegis agent spec
- ❌ `backend/docs/archivus_aegis_routing.md` - Routing specification
- ❌ `backend/docs/vee_moreno_trial_spec.md` - Vee trial specification

**Location:** `backend/docs/reports/` (DIRECTORY MISSING)

- ❌ 25+ completion report files

**Location:** `backend/reports/` (DIRECTORY MISSING)

- ❌ `backend/reports/maya_v3_final_report.md` - Final readiness report

---

### 🟢 OPTIONAL - Test Data

**Location:** `backend/test_data/` (DIRECTORY EXISTS BUT EMPTY)

- ❌ `backend/test_data/briana_processing_result.json` - Test fixture data

---

## 📊 SUMMARY STATISTICS

### By Category

| Category | Missing Files | Priority |
|----------|---------------|----------|
| Core Services | 13 | 🔴 CRITICAL |
| Intelligence Modules | 9 | 🔴 CRITICAL |
| API Routers | 7 | 🔴 CRITICAL |
| Guardian Framework | 6 | 🔴 CRITICAL |
| Data Models | 6 | 🔴 CRITICAL |
| Database Migrations | 8 | 🟡 IMPORTANT |
| Workers | 3 | 🟡 IMPORTANT |
| Test Suite | 11 | 🟡 IMPORTANT |
| Scripts | 3+ (26+ in dev/) | 🟡 IMPORTANT |
| Archive/Legacy | 3 | 🟢 OPTIONAL |
| Documentation | 4+ (25+ in reports/) | 🟢 OPTIONAL |
| **TOTAL** | **~100+ files** | |

### By Priority

- 🔴 **CRITICAL:** ~41 files (must rebuild for system to function)
- 🟡 **IMPORTANT:** ~31 files (needed for full functionality)
- 🟢 **OPTIONAL:** ~30+ files (nice to have, can rebuild later)

---

## 🎯 REBUILD PRIORITY ORDER

### Phase 1: Core Infrastructure (CRITICAL)
1. Core services (audit, gmail, email processor, calendar, claude)
2. Database models
3. Encryption service
4. API routers (gmail, calendar, clients, auth)

### Phase 2: Intelligence & Processing (CRITICAL)
5. All 8 intelligence modules
6. Email processor v3 integration
7. Retry queue service
8. Idempotency service

### Phase 3: Guardian Framework (CRITICAL)
9. All 5 guardian files
10. Guardian manager integration

### Phase 4: Database & Migrations (IMPORTANT)
11. All migration files
12. Database schema verification

### Phase 5: Testing & Scripts (IMPORTANT)
13. Test suite
14. Safety gate script
15. Deployment scripts

### Phase 6: Documentation & Archive (OPTIONAL)
16. Documentation files
17. Archive/legacy services

---

## 📝 NOTES

- **Current Status:** Only ~10 files rebuilt out of ~100+ needed
- **Rebuild Progress:** ~10% complete
- **Estimated Files Remaining:** ~90+ files
- **Critical Path:** Core services → Intelligence → Routers → Guardian Framework

---

**Last Updated:** After initial rebuild assessment  
**Next Action:** Continue systematic rebuild starting with Phase 1

