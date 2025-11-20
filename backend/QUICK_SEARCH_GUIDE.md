# QUICK SEARCH GUIDE
**Purpose:** Fast lookup for AI assistants to find functions, files, and fixes  
**Use:** Ctrl+F to search for function names, error messages, or file paths

---

## 🔍 SEARCH BY FUNCTION NAME

### Authentication
- `authenticate_user()` → `app/services/auth_service.py:46`
- `create_token_pair()` → `app/services/auth_service.py:118`
- `get_current_user()` → `app/services/auth_service.py:178`
- `get_current_admin_user()` → `app/services/auth_service.py:228`
- `get_sso_service()` → `app/services/sso_service.py`
- `get_tenant_resolution_service()` → `app/services/tenant_resolution_service.py`

### Database
- `get_cursor()` → `app/database.py:40`
- `get_async_session()` → `app/database.py:95`
- `get_db()` → `app/database.py:68`
- `init_db_pool()` → `app/database.py:18`

### Email Processing
- `process_email()` → `app/services/email_processor_v3.py`
- `store_email_in_db()` → `app/services/gmail_service.py:65`
- `verify_jwt_token()` → `app/services/gmail_webhook.py:30`
- `process_webhook_message()` → `app/services/gmail_webhook.py:150`

### Calendar
- `create_event()` → `app/services/calendar_service_v3.py:100`
- `auto_block_for_confirmed_gig()` → `app/services/calendar_service_v3.py:200`
- `check_availability()` → `app/services/calendar_service_v3.py:300`
- `delete_event()` → `app/services/calendar_service_v3.py:400`

### Guardian Framework
- `get_guardian_manager()` → `app/guardians/guardian_manager.py:95`
- `get_solin_mcp()` → `app/guardians/solin_mcp.py:327`
- `get_sentra_safety()` → `app/guardians/sentra_safety.py:355`
- `get_vita_repair()` → `app/guardians/vita_repair.py:355`
- `receive_event()` → Multiple files (different signatures - see below)

### Audit & Logging
- `get_audit_service()` → `app/services/audit_service.py:143`
- `log_event()` → `app/services/audit_service.py:37`
- `log_safety_event()` → `app/services/audit_service.py:116`

### Encryption
- `encrypt()` → `app/encryption.py:23`
- `decrypt()` → `app/encryption.py:39`
- `get_encryption_service()` → `app/encryption.py:54`

---

## 🔍 SEARCH BY ERROR MESSAGE

### "ModuleNotFoundError: No module named 'app.services.auth_service'"
**Fix:** File exists at `app/services/auth_service.py` - Check import path

### "AttributeError: 'Settings' object has no attribute 'maya_email'"
**Fix:** Use `getattr(settings, 'maya_email', 'maya@skinnymanmusic.com')` - Already fixed in `calendar_service_v3.py`

### "TypeError: receive_event() missing required positional argument"
**Fix:** Check event format:
- `guardian_manager.receive_event(log_entry: Dict)` - Pass dict
- `solin.receive_event(action, metadata, route_to_sentra, route_to_vita)` - Pass separate args
- `sentra.receive_event(action, metadata)` - Pass separate args
- `vita.receive_event(action, metadata)` - Pass separate args

### "psycopg2.OperationalError: could not connect to server"
**Fix:** Check `database_url` in `.env` file

### "ValidationError: Field required [type=missing, input_value={...}]"
**Fix:** Check `.env` file has all required variables (see `MASTER_REFERENCE_DOCUMENT.md`)

### "401 Unauthorized" or "Invalid token"
**Fix:** Check `jwt_secret_key` in `.env`, verify token format (Bearer token)

### "Circular import" errors
**Fix:** Use lazy loading (see `audit_service.py` and `guardian_manager.py`)

---

## 🔍 SEARCH BY FILE PATH

### Core Services
- `app/services/auth_service.py` - JWT authentication (JUST REBUILT)
- `app/services/audit_service.py` - Audit logging
- `app/services/email_processor_v3.py` - Email processing pipeline
- `app/services/calendar_service_v3.py` - Calendar operations
- `app/services/gmail_service.py` - Gmail API
- `app/services/gmail_webhook.py` - Webhook verification
- `app/services/claude_service.py` - Claude AI
- `app/services/supabase_service.py` - Database operations
- `app/services/sso_service.py` - OAuth SSO
- `app/services/tenant_resolution_service.py` - Tenant resolution

### Routers
- `app/routers/auth.py` - Authentication endpoints
- `app/routers/gmail.py` - Gmail webhook endpoints
- `app/routers/calendar.py` - Calendar endpoints
- `app/routers/clients.py` - Client management
- `app/routers/agents.py` - Agent management
- `app/routers/metrics.py` - System metrics (admin)
- `app/routers/unsafe_threads.py` - Unsafe threads (admin)
- `app/routers/health.py` - Health checks
- `app/main.py` - Main FastAPI app

### Guardian Framework
- `app/guardians/solin_mcp.py` - Master Control Program
- `app/guardians/sentra_safety.py` - Safety enforcement
- `app/guardians/vita_repair.py` - Automated repair
- `app/guardians/guardian_manager.py` - Event routing
- `app/guardians/guardian_daemon.py` - Background monitoring

### Database
- `app/database.py` - Connection management
- `migrations/001_add_email_hash.sql` - Email hash
- `migrations/002_add_calendar_events.sql` - Calendar schema
- `migrations/003_add_idempotency_tables.sql` - Idempotency
- `migrations/008_add_v4_sso_tables.sql` - SSO tables
- `migrations/011_archivus_schema.sql` - Archivus memory

---

## 🔍 SEARCH BY INTEGRATION POINT

### Gmail Webhook Flow
1. `app/routers/gmail.py` → `POST /api/gmail/webhook`
2. `app/services/gmail_webhook.py` → `verify_jwt_token()`, `process_webhook_message()`
3. `app/services/gmail_service.py` → `store_email_in_db()`
4. `app/services/email_processor_v3.py` → `process_email()`
5. `app/services/claude_service.py` → `generate_response()`
6. `app/services/archivus_service.py` → `record_thread_summary()`

### Authentication Flow
1. `app/routers/auth.py` → `POST /api/auth/login`
2. `app/services/auth_service.py` → `authenticate_user()`, `create_token_pair()`
3. Frontend stores tokens
4. `app/services/auth_service.py` → `get_current_user()` validates tokens
5. `app/middleware/tenant_context.py` → Extracts tenant_id from token

### Guardian Event Flow
1. `app/services/audit_service.py` → `log_event()` writes to DB
2. `app/services/audit_service.py` → Emits to `guardian_manager`
3. `app/guardians/guardian_manager.py` → Routes based on rules
4. `app/guardians/solin_mcp.py` → Master control
5. `app/guardians/sentra_safety.py` → Safety enforcement
6. `app/guardians/vita_repair.py` → Automated repair

### Calendar Auto-Block Flow
1. `app/services/email_processor_v3.py` → Detects acceptance
2. `app/services/calendar_service_v3.py` → `check_availability()`
3. `app/services/calendar_service_v3.py` → `auto_block_for_confirmed_gig()`
4. `app/services/supabase_service.py` → `create_calendar_event()`
5. `app/services/calendar_service_v3.py` → Creates Google Calendar event

---

## 🔍 SEARCH BY ISSUE TYPE

### Import Issues
**Search:** `from app`, `import`, `ModuleNotFoundError`  
**Common Files:** All service files, router files  
**Common Fixes:**
- Verify file exists
- Check import path
- Check for circular imports (use lazy loading)

### Database Issues
**Search:** `get_cursor`, `database_url`, `psycopg2`, `SQL`  
**Common Files:** `database.py`, `supabase_service.py`  
**Common Fixes:**
- Check `.env` has `database_url`
- Verify table exists in migrations
- Check RLS policies
- Verify `tenant_id` passed correctly

### Authentication Issues
**Search:** `jwt_secret_key`, `get_current_user`, `401`  
**Common Files:** `auth_service.py`, `auth.py`  
**Common Fixes:**
- Check `.env` has `jwt_secret_key`
- Verify token format (Bearer)
- Check token expiration
- Verify user exists

### Guardian Issues
**Search:** `guardian_manager`, `receive_event`, `get_guardian_manager`  
**Common Files:** `audit_service.py`, all guardian files  
**Common Fixes:**
- Check per-tenant cache (not global)
- Verify event format (dict for guardian_manager)
- Check lazy loading for circular imports
- Verify factory functions exist

### Email Processing Issues
**Search:** `email_processor_v3`, `process_email`, `gmail_webhook`  
**Common Files:** `email_processor_v3.py`, `gmail_webhook.py`  
**Common Fixes:**
- Check all 8 intelligence modules imported
- Verify Claude API key
- Check Gmail API credentials
- Verify webhook JWT verification

---

## 🔍 SEARCH BY CONFIGURATION

### Required Environment Variables
- `database_url` - PostgreSQL connection
- `jwt_secret_key` - JWT signing
- `encryption_key` - Fernet key
- `anthropic_api_key` - Claude API
- `gmail_webhook_url` - Webhook URL
- `gmail_pubsub_topic` - Pub/Sub topic
- `gmail_pubsub_service_account` - Service account
- `default_tenant_id` - Default tenant UUID

### Optional Environment Variables
- `maya_email` - Default Gmail account (fallback: maya@skinnymanmusic.com)
- `google_oauth_client_id` - Google OAuth
- `google_oauth_client_secret` - Google OAuth
- `microsoft_oauth_client_id` - Microsoft OAuth
- `microsoft_oauth_client_secret` - Microsoft OAuth
- `openai_api_key` - OpenAI API (for hybrid LLM)

### Configuration File
- `app/config.py` - Settings class, `get_settings()` function
- Uses `pydantic_settings` for env var loading
- `.env` file required (not in repo)

---

## 🔍 SEARCH BY DATABASE TABLE

### Core Tables
- `users` - User accounts (encrypted PII)
- `tenants` - Multi-tenant isolation
- `emails` - Email messages
- `clients` - Client records (encrypted PII)
- `calendar_events` - Calendar events
- `audit_log` - Audit trail

### Guardian Tables
- `unsafe_threads` - Sentra safety tags
- `repair_log` - Vita repair attempts
- `system_state` - Solin Safe Mode

### v4.0 SSO Tables
- `users_v4` - SSO users
- `accounts` - OAuth accounts
- `sessions` - User sessions
- `tenant_users` - Tenant membership
- `tenant_agent_profiles` - Agent configs

### Memory Tables
- `archivus_threads` - Thread summaries
- `archivus_memories` - Long-term memories

### Queue Tables
- `email_retry_queue` - Failed retries
- `processed_messages` - Idempotency
- `sync_log` - Replay prevention

---

## 🔍 SEARCH BY API ENDPOINT

### Health
- `GET /api/health/` → `app/routers/health.py`
- `GET /api/health/db` → `app/routers/health.py`
- `GET /api/health/encryption` → `app/routers/health.py`

### Auth
- `POST /api/auth/login` → `app/routers/auth.py:40`
- `GET /api/auth/me` → `app/routers/auth.py:92`
- `GET /api/auth/google/start` → `app/routers/auth.py:110`
- `GET /api/auth/google/callback` → `app/routers/auth.py:125`
- `GET /api/auth/microsoft/start` → `app/routers/auth.py:190`
- `GET /api/auth/microsoft/callback` → `app/routers/auth.py:205`

### Gmail
- `POST /api/gmail/webhook` → `app/routers/gmail.py`
- `POST /api/gmail/watch` → `app/routers/gmail.py`

### Calendar
- `GET /api/calendar/events` → `app/routers/calendar.py`
- `POST /api/calendar/events` → `app/routers/calendar.py`
- `POST /api/calendar/block` → `app/routers/calendar.py`
- `GET /api/calendar/availability` → `app/routers/calendar.py`
- `DELETE /api/calendar/event/{id}` → `app/routers/calendar.py`

### Clients
- `POST /api/clients/` → `app/routers/clients.py`
- `GET /api/clients/{id}` → `app/routers/clients.py`
- `GET /api/clients/` → `app/routers/clients.py`
- `GET /api/clients/search/by-email/` → `app/routers/clients.py`
- `PUT /api/clients/{id}` → `app/routers/clients.py`
- `DELETE /api/clients/{id}` → `app/routers/clients.py`

### Admin
- `GET /api/metrics/` → `app/routers/metrics.py` (admin-only)
- `GET /api/unsafe-threads/` → `app/routers/unsafe_threads.py` (admin-only)
- `DELETE /api/unsafe-threads/{id}` → `app/routers/unsafe_threads.py` (admin-only)

---

## 🔍 SEARCH BY FIX APPLIED

### Fix 1: Missing auth_service.py
**File Created:** `app/services/auth_service.py`  
**What It Does:** JWT authentication, password hashing, brute force protection  
**Key Functions:** `authenticate_user()`, `create_token_pair()`, `get_current_user()`, `get_current_admin_user()`

### Fix 2: Missing Password Hashing
**File Modified:** `app/utils/password_policy.py`  
**What Was Added:** `PasswordPolicyService` class with bcrypt  
**Key Functions:** `verify_password()`, `get_password_hash()`

### Fix 3: Missing Async Database Support
**File Modified:** `app/database.py`  
**What Was Added:** `get_async_session()` function  
**Dependency Added:** `asyncpg==0.29.0` to `requirements.txt`

### Fix 4: Calendar Service Config
**File Modified:** `app/services/calendar_service_v3.py`  
**What Was Fixed:** Added fallback for `settings.maya_email`  
**Fix:** `getattr(settings, 'maya_email', 'maya@skinnymanmusic.com')`

### Fix 5: Archivus Method Signature
**File Modified:** `app/services/archivus_service.py`  
**What Was Fixed:** Updated Claude method call  
**Fix:** Changed to `generate_response(email_body, context, trace_id)`

### Fix 6: Audit Service Guardian Manager
**File Modified:** `app/services/audit_service.py`  
**What Was Fixed:** Per-tenant cache, correct event format  
**Fix:** Changed from global cache to per-tenant dict, fixed event dict format

---

## 📚 RELATED DOCUMENTATION

### Master Documents
- `MASTER_REFERENCE_DOCUMENT.md` - Complete system reference (START HERE)
- `INCIDENT_RECOVERY_REPORT.md` - What broke and how it was fixed
- `QUICK_SEARCH_GUIDE.md` - This document

### Verification Reports
- `SANITY_CHECK_REPORT.md` - Latest verification
- `FINAL_VERIFICATION_REPORT.md` - Final verification
- `HONEST_VERIFICATION.md` - Limitations

### System Documentation
- `OMEGA_OVERVIEW.md` - Complete system overview (2524 lines)
- `CLAUDE_PROGRESS_LOG.md` - Implementation history (3874 lines)
- `SECURITY_AUDIT_REPORT.md` - Security audit

---

## 🎯 QUICK FIXES

### "auth_service not found"
→ Check `app/services/auth_service.py` exists (JUST REBUILT)

### "get_async_session not found"
→ Check `app/database.py` has `get_async_session()` function (JUST ADDED)

### "maya_email attribute error"
→ Check `calendar_service_v3.py` uses `getattr()` with fallback (JUST FIXED)

### "receive_event wrong format"
→ Check event is dict for `guardian_manager`, separate args for `solin/sentra/vita` (JUST FIXED)

### "guardian_manager not receiving events"
→ Check `audit_service.py` uses per-tenant cache and correct event format (JUST FIXED)

---

**END OF QUICK SEARCH GUIDE**

Use this for fast lookups. For detailed information, see `MASTER_REFERENCE_DOCUMENT.md`.

