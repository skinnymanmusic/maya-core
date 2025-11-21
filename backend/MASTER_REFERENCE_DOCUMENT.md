# MASTER REFERENCE DOCUMENT
**Purpose:** Complete system documentation for AI assistants to search, understand, and fix issues  
**Last Updated:** After git reset recovery  
**Status:** System rebuilt, needs runtime testing

---

## 📋 TABLE OF CONTENTS

1. [What Broke & Why](#what-broke--why)
2. [Current System State](#current-system-state)
3. [File Inventory](#file-inventory)
4. [Integration Points](#integration-points)
5. [Known Issues & Limitations](#known-issues--limitations)
6. [Troubleshooting Guide](#troubleshooting-guide)
7. [Search Index](#search-index)

---

## 🔴 WHAT BROKE & WHY

### The Incident
**Date:** After git reset --hard origin/main  
**Cause:** Git reset operation that discarded all uncommitted changes  
**Impact:** ~100+ files lost, entire system needed rebuild

### What Was Lost
1. **All rebuilt files** - Everything that was created/modified after the last commit
2. **Progress documentation** - Phase completion reports, implementation logs
3. **Test data** - Sample processing results, fixtures
4. **Development scripts** - Utility scripts in `scripts/dev/`
5. **Documentation** - Spec documents, architecture diagrams

### Why It Happened
- User attempted to push to GitHub
- GitHub detected secrets in old commits (push protection)
- User tried to resolve by resetting to origin/main
- `git reset --hard origin/main` discarded all local changes
- No backup of uncommitted work

### Recovery Strategy
- Rebuilt from documentation (`OMEGA_OVERVIEW.md`, `CLAUDE_PROGRESS_LOG.md`)
- Used existing specs and implementation notes
- Recreated all critical files systematically
- Fixed issues as they were discovered

---

## ✅ CURRENT SYSTEM STATE

### Architecture Overview
**System Name:** OMEGA Core v3.0 / v4.0 (Hybrid)  
**Framework:** FastAPI (Python 3.14)  
**Database:** PostgreSQL (Supabase)  
**Frontend:** Next.js 14 (omega-frontend)  
**Deployment:** Azure Functions (maya-core-func)

### Core Components Status

#### ✅ Backend Services (24/24)
- `audit_service.py` - Comprehensive audit logging
- `auth_service.py` - JWT authentication (JUST REBUILT)
- `gmail_webhook.py` - Gmail Pub/Sub webhook handler
- `gmail_service.py` - Gmail API integration
- `claude_service.py` - Anthropic Claude AI integration
- `email_processor_v3.py` - Main email processing pipeline
- `calendar_service_v3.py` - Google Calendar integration
- `idempotency_service.py` - Idempotency layer
- `retry_queue_service.py` - Retry queue management
- `supabase_service.py` - Database operations
- `archivus_service.py` - Long-term memory engine
- `aegis_anomaly_service.py` - Security intelligence
- `eli_service.py` - Venue intelligence integration
- `sso_service.py` - Google/Microsoft OAuth
- `tenant_resolution_service.py` - Multi-tenant SSO resolution
- **Intelligence Modules (8):**
  - `venue_intelligence.py`
  - `coordinator_detection.py`
  - `acceptance_detection.py`
  - `missing_info_detection.py`
  - `equipment_awareness.py`
  - `thread_history.py`
  - `multi_account_email.py`
  - `context_reconstruction.py`

#### ✅ API Routers (9/9)
- `health.py` - Health check endpoints
- `auth.py` - Authentication endpoints (JWT + SSO)
- `gmail.py` - Gmail webhook & watch endpoints
- `calendar.py` - Calendar CRUD endpoints
- `clients.py` - Client management endpoints
- `agents.py` - Agent management endpoints
- `metrics.py` - System metrics (admin-only)
- `unsafe_threads.py` - Unsafe threads admin API
- `main.py` - Main FastAPI app (includes all routers)

#### ✅ Guardian Framework (6/6)
- `solin_mcp.py` - Master Control Program
- `sentra_safety.py` - Safety enforcement AI
- `vita_repair.py` - Automated repair AI
- `guardian_manager.py` - Guardian event routing
- `guardian_daemon.py` - Background monitoring daemon
- `__init__.py` - Package exports

#### ✅ Data Models (6/6)
- `email.py` - Email data models
- `client.py` - Client data models
- `calendar.py` - Calendar event models
- `user.py` - User/auth models
- `archivus.py` - Archivus memory models
- `__init__.py` - Model exports

#### ✅ Workers (2/2)
- `email_retry_worker.py` - Retry queue worker
- `__init__.py` - Package exports

#### ✅ Database Migrations (9/9)
- `001_add_email_hash.sql` - Email hash column
- `002_add_calendar_events.sql` - Calendar events table
- `003_add_idempotency_tables.sql` - Idempotency tables
- `004_performance_indexes.sql` - Performance indexes
- `005_add_unsafe_threads.sql` - Unsafe threads table
- `006_add_repair_log.sql` - Repair log table
- `007_add_system_state.sql` - System state table
- `008_add_v4_sso_tables.sql` - v4.0 SSO tables
- `011_archivus_schema.sql` - Archivus memory tables

#### ✅ Test Suite (11/11)
- `test_pipeline.py` - Pipeline integration tests
- `test_acceptance_ab.py` - Acceptance A/B tests
- `test_intelligence.py` - Intelligence service tests
- `test_calendar.py` - Calendar service tests
- `test_pricing_integration.py` - Nova pricing tests
- `test_aegis_integration.py` - Aegis integration tests
- `test_archivus_service.py` - Archivus service tests
- `test_safety_gate_phase5.py` - Safety gate tests
- `test_runner.py` - Master test runner
- `fixtures.py` - Test fixtures
- `__init__.py` - Test package

#### ✅ Scripts (3/3)
- `safety_gate_phase5.py` - Pre-deployment safety gate
- `startup_schema_check.py` - Schema drift detection
- `v4_backfill_agent_profiles.py` - Agent profile backfill

---

## 📁 FILE INVENTORY

### Backend Structure
```
backend/
├── app/
│   ├── config.py                    # Configuration (Settings class)
│   ├── database.py                   # Database connections (sync + async)
│   ├── encryption.py                 # AES-256 encryption service
│   ├── main.py                       # FastAPI app entry point
│   ├── config/
│   │   └── omega_agents_registry.json
│   ├── guardians/                    # Guardian Framework (6 files)
│   ├── middleware/                   # Security & tenant context
│   ├── models/                       # Pydantic models (6 files)
│   ├── routers/                      # API routers (9 files)
│   ├── services/                     # Core services (24 files)
│   │   └── intelligence/             # Intelligence modules (8 files)
│   ├── utils/                        # Utilities (password policy)
│   └── workers/                       # Background workers (2 files)
├── migrations/                       # SQL migrations (9 files)
├── scripts/                          # Utility scripts (3 files)
├── tests/                            # Test suite (11 files)
├── requirements.txt                  # Python dependencies
├── Procfile                          # Process file
├── nixpacks.toml                     # Build configuration
└── Documentation files (this file, etc.)
```

### Key Files by Function

#### Authentication
- `app/services/auth_service.py` - JWT auth, password hashing, brute force protection
- `app/routers/auth.py` - Auth endpoints (login, refresh, me, SSO)
- `app/utils/password_policy.py` - Password validation & hashing
- `app/models/user.py` - User data models

#### Email Processing
- `app/services/email_processor_v3.py` - Main email processing pipeline
- `app/services/gmail_service.py` - Gmail API integration
- `app/services/gmail_webhook.py` - Webhook verification & processing
- `app/services/claude_service.py` - Claude AI integration
- `app/services/intelligence/*` - 8 intelligence modules

#### Calendar
- `app/services/calendar_service_v3.py` - Calendar operations
- `app/routers/calendar.py` - Calendar API endpoints
- `migrations/002_add_calendar_events.sql` - Calendar schema

#### Database
- `app/database.py` - Connection management (sync + async)
- `app/services/supabase_service.py` - Database operations
- `migrations/*.sql` - All database schemas

#### Security
- `app/services/gmail_webhook.py` - JWT verification, replay prevention
- `app/services/idempotency_service.py` - Idempotency layer
- `app/middleware/security.py` - Security headers, token redaction
- `app/encryption.py` - PII encryption

#### Guardian Framework
- `app/guardians/solin_mcp.py` - Master Control Program
- `app/guardians/sentra_safety.py` - Safety enforcement
- `app/guardians/vita_repair.py` - Automated repair
- `app/guardians/guardian_manager.py` - Event routing
- `app/guardians/guardian_daemon.py` - Background monitoring

---

## 🔗 INTEGRATION POINTS

### Critical Integration Flows

#### 1. Gmail Webhook → Email Processing
**Flow:**
1. Gmail Pub/Sub sends webhook to `/api/gmail/webhook`
2. `gmail_webhook.py` verifies JWT, checks replay, acquires lock
3. `gmail_service.py` stores email in database
4. `email_processor_v3.py` processes email through intelligence pipeline
5. `claude_service.py` generates response
6. `gmail_service.py` creates draft or sends email
7. `archivus_service.py` records thread summary

**Key Files:**
- `app/routers/gmail.py` - Webhook endpoint
- `app/services/gmail_webhook.py` - Security & verification
- `app/services/gmail_service.py` - Gmail API
- `app/services/email_processor_v3.py` - Processing pipeline

#### 2. Authentication Flow
**Flow:**
1. User logs in via `/api/auth/login`
2. `auth_service.py` authenticates user, creates JWT tokens
3. Frontend stores tokens in localStorage
4. Subsequent requests include JWT in Authorization header
5. `get_current_user()` validates token, returns user
6. Admin endpoints use `get_current_admin_user()`

**Key Files:**
- `app/routers/auth.py` - Auth endpoints
- `app/services/auth_service.py` - Auth logic
- `app/middleware/tenant_context.py` - Token extraction
- `app/utils/password_policy.py` - Password hashing

#### 3. Guardian Framework Flow
**Flow:**
1. `audit_service.py` logs event to database
2. `audit_service.py` emits event to `guardian_manager`
3. `guardian_manager.py` routes event based on rules:
   - ERROR level → Sentra
   - email_processor + crash → Vita
   - All events → Solin
4. Guardians process events, may trigger Safe Mode

**Key Files:**
- `app/services/audit_service.py` - Audit logging
- `app/guardians/guardian_manager.py` - Event routing
- `app/guardians/solin_mcp.py` - Master control
- `app/guardians/sentra_safety.py` - Safety enforcement
- `app/guardians/vita_repair.py` - Automated repair

#### 4. Calendar Auto-Block Flow
**Flow:**
1. Email processor detects acceptance
2. `email_processor_v3.py` calls `calendar_service_v3.py`
3. `calendar_service_v3.py` checks for conflicts
4. If no conflict, creates calendar event
5. If conflict, adds warning to draft, prevents auto-send

**Key Files:**
- `app/services/email_processor_v3.py` - Acceptance detection
- `app/services/calendar_service_v3.py` - Calendar operations
- `app/routers/calendar.py` - Calendar API

#### 5. SSO Flow (v4.0)
**Flow:**
1. User clicks "Sign in with Google/Microsoft"
2. Frontend calls `/api/auth/google/start` or `/api/auth/microsoft/start`
3. `sso_service.py` generates OAuth URL
4. User authenticates with provider
5. Provider redirects to `/api/auth/google/callback` or `/api/auth/microsoft/callback`
6. `sso_service.py` exchanges code for tokens
7. `tenant_resolution_service.py` resolves/create user & tenant
8. Session created, tokens returned

**Key Files:**
- `app/routers/auth.py` - SSO endpoints
- `app/services/sso_service.py` - OAuth handling
- `app/services/tenant_resolution_service.py` - Tenant resolution

---

## ⚠️ KNOWN ISSUES & LIMITATIONS

### Issues Fixed During Rebuild

#### 1. Missing `auth_service.py` ✅ FIXED
**Issue:** Routers importing from non-existent file  
**Fix:** Created complete auth service with JWT, password hashing, brute force protection  
**File:** `app/services/auth_service.py`

#### 2. Missing Password Hashing ✅ FIXED
**Issue:** `auth_service.py` needed password hashing  
**Fix:** Added `PasswordPolicyService` class with bcrypt  
**File:** `app/utils/password_policy.py`

#### 3. Missing Async Database Support ✅ FIXED
**Issue:** `metrics.py` and `unsafe_threads.py` need async sessions  
**Fix:** Added `get_async_session()` to `database.py`, added `asyncpg` to requirements  
**Files:** `app/database.py`, `requirements.txt`

#### 4. Calendar Service Config ✅ FIXED
**Issue:** `settings.maya_email` might not exist  
**Fix:** Added fallback: `getattr(settings, 'maya_email', 'maya@skinnymanmusic.com')`  
**File:** `app/services/calendar_service_v3.py`

#### 5. Archivus Service Method Signature ✅ FIXED
**Issue:** Wrong Claude method signature  
**Fix:** Updated to use `generate_response(email_body, context, trace_id)`  
**File:** `app/services/archivus_service.py`

#### 6. Audit Service Guardian Manager ✅ FIXED
**Issue:** Global cache instead of per-tenant, wrong event format  
**Fix:** Per-tenant cache, correct event dict format  
**File:** `app/services/audit_service.py`

### Current Limitations

#### 1. Environment Configuration Required
- **Issue:** System needs `.env` file with all required variables
- **Required Variables:**
  - `database_url` - PostgreSQL connection string
  - `jwt_secret_key` - JWT signing key
  - `encryption_key` - Fernet key for AES-256
  - `anthropic_api_key` - Claude API key
  - `gmail_webhook_url` - Gmail webhook URL
  - `gmail_pubsub_topic` - Pub/Sub topic
  - `gmail_pubsub_service_account` - Service account email
  - `default_tenant_id` - Default tenant UUID
  - Optional: `maya_email`, OAuth client IDs/secrets, OpenAI key

#### 2. Database Migrations Not Applied
- **Issue:** SQL migration files exist but haven't been run
- **Solution:** Run all migrations in order (001-011)
- **Files:** `migrations/*.sql`

#### 3. OAuth Credentials Not Configured
- **Issue:** Google/Microsoft OAuth apps need to be created
- **Solution:** Create OAuth apps, add client IDs/secrets to `.env`
- **Documentation:** See `OMEGA_OVERVIEW.md` for OAuth setup

#### 4. Runtime Testing Not Done
- **Issue:** Code hasn't been tested with actual environment
- **Solution:** Configure environment, run tests, fix runtime issues
- **Tests:** `tests/test_*.py`

#### 5. Some Placeholder Implementations
- **Issue:** Some methods are stubs or placeholders
- **Examples:**
  - `agents.py` router uses mock data
  - Some test implementations are placeholders
  - Refresh token flow not fully implemented

---

## 🔧 TROUBLESHOOTING GUIDE

### Common Issues & Solutions

#### Issue: Import Errors
**Symptoms:** `ModuleNotFoundError`, `ImportError`  
**Causes:**
- Missing file
- Wrong import path
- Circular import
- Missing dependency in requirements.txt

**Solutions:**
1. Check file exists: `glob_file_search` for file
2. Verify import path matches file location
3. Check for circular imports (guardian_manager, audit_service)
4. Verify dependency in `requirements.txt`

**Search Terms:** `import`, `from app`, `ModuleNotFoundError`

#### Issue: Database Connection Errors
**Symptoms:** `psycopg2.OperationalError`, connection refused  
**Causes:**
- Missing `database_url` in `.env`
- Database not running
- Wrong connection string format
- SSL/authentication issues

**Solutions:**
1. Check `.env` file has `database_url`
2. Verify database is running
3. Test connection string format
4. Check SSL settings match database config

**Search Terms:** `database_url`, `get_cursor`, `psycopg2`, `connection`

#### Issue: Authentication Failures
**Symptoms:** `401 Unauthorized`, `Invalid token`  
**Causes:**
- Missing `jwt_secret_key` in `.env`
- Token expired
- Wrong token format
- User not found in database

**Solutions:**
1. Check `.env` has `jwt_secret_key`
2. Verify token hasn't expired
3. Check token format (Bearer token)
4. Verify user exists in `users` table

**Search Terms:** `jwt_secret_key`, `get_current_user`, `authenticate_user`, `TokenPair`

#### Issue: Guardian Framework Not Working
**Symptoms:** No guardian events, Safe Mode not triggering  
**Causes:**
- Guardian manager not receiving events
- Circular import preventing initialization
- Guardian daemon not running
- Database tables missing

**Solutions:**
1. Check `audit_service.py` emits to guardian manager
2. Verify no circular imports (lazy loading used)
3. Check guardian daemon is running
4. Verify guardian tables exist (unsafe_threads, repair_log, system_state)

**Search Terms:** `guardian_manager`, `receive_event`, `get_guardian_manager`, `guardian_daemon`

#### Issue: Email Processing Not Working
**Symptoms:** Emails not processed, no drafts created  
**Causes:**
- Gmail webhook not receiving messages
- JWT verification failing
- Email processor crashing
- Missing intelligence services

**Solutions:**
1. Check Gmail watch subscription is active
2. Verify JWT verification in `gmail_webhook.py`
3. Check email processor logs for errors
4. Verify all 8 intelligence modules are imported

**Search Terms:** `email_processor_v3`, `gmail_webhook`, `process_email`, `intelligence`

#### Issue: Calendar Events Not Creating
**Symptoms:** Auto-block not working, events not created  
**Causes:**
- Calendar service not initialized
- Google Calendar API credentials missing
- Conflict detection preventing creation
- Safe Mode enabled

**Solutions:**
1. Check `calendar_service_v3.py` initialization
2. Verify Google credentials file exists
3. Check conflict detection logic
4. Verify Safe Mode status in `system_state` table

**Search Terms:** `calendar_service_v3`, `auto_block`, `create_event`, `check_availability`

#### Issue: SSO Not Working
**Symptoms:** OAuth redirect fails, callback errors  
**Causes:**
- OAuth client IDs/secrets not configured
- Redirect URI mismatch
- Tenant resolution failing
- Session creation failing

**Solutions:**
1. Check `.env` has OAuth client IDs/secrets
2. Verify redirect URI matches OAuth app config
3. Check `tenant_resolution_service.py` logic
4. Verify `sessions` table exists

**Search Terms:** `sso_service`, `tenant_resolution_service`, `google_oauth`, `microsoft_oauth`

---

## 🔍 SEARCH INDEX

### By Function Name

#### Authentication
- `authenticate_user()` - `app/services/auth_service.py`
- `create_token_pair()` - `app/services/auth_service.py`
- `get_current_user()` - `app/services/auth_service.py`
- `get_current_admin_user()` - `app/services/auth_service.py`
- `get_sso_service()` - `app/services/sso_service.py`
- `get_tenant_resolution_service()` - `app/services/tenant_resolution_service.py`

#### Database
- `get_cursor()` - `app/database.py`
- `get_async_session()` - `app/database.py`
- `get_db()` - `app/database.py`
- `init_db_pool()` - `app/database.py`

#### Email Processing
- `process_email()` - `app/services/email_processor_v3.py`
- `store_email_in_db()` - `app/services/gmail_service.py`
- `verify_jwt_token()` - `app/services/gmail_webhook.py`
- `process_webhook_message()` - `app/services/gmail_webhook.py`

#### Calendar
- `create_event()` - `app/services/calendar_service_v3.py`
- `auto_block_for_confirmed_gig()` - `app/services/calendar_service_v3.py`
- `check_availability()` - `app/services/calendar_service_v3.py`
- `delete_event()` - `app/services/calendar_service_v3.py`

#### Guardian Framework
- `get_guardian_manager()` - `app/guardians/guardian_manager.py`
- `get_solin_mcp()` - `app/guardians/solin_mcp.py`
- `get_sentra_safety()` - `app/guardians/sentra_safety.py`
- `get_vita_repair()` - `app/guardians/vita_repair.py`
- `receive_event()` - Multiple guardians (different signatures)

#### Audit & Logging
- `get_audit_service()` - `app/services/audit_service.py`
- `log_event()` - `app/services/audit_service.py`
- `log_safety_event()` - `app/services/audit_service.py`

#### Encryption
- `encrypt()` - `app/encryption.py`
- `decrypt()` - `app/encryption.py`
- `get_encryption_service()` - `app/encryption.py`

### By Table Name

#### Core Tables
- `users` - User accounts (encrypted PII)
- `tenants` - Multi-tenant isolation
- `emails` - Email messages
- `clients` - Client records (encrypted PII)
- `calendar_events` - Calendar events
- `audit_log` - Audit trail

#### Guardian Tables
- `unsafe_threads` - Sentra safety tags
- `repair_log` - Vita repair attempts
- `system_state` - Solin Safe Mode state

#### v4.0 SSO Tables
- `users_v4` - SSO users (multi-tenant)
- `accounts` - OAuth provider accounts
- `sessions` - User sessions
- `tenant_users` - Tenant membership
- `tenant_agent_profiles` - Agent configurations

#### Memory Tables
- `archivus_threads` - Thread summaries
- `archivus_memories` - Long-term memories

#### Queue Tables
- `email_retry_queue` - Failed email retries
- `processed_messages` - Idempotency tracking
- `sync_log` - Replay prevention

### By Endpoint

#### Health
- `GET /api/health/` - Comprehensive health check
- `GET /api/health/db` - Database health
- `GET /api/health/encryption` - Encryption health

#### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh token (placeholder)
- `GET /api/auth/me` - Get current user
- `GET /api/auth/google/start` - Start Google SSO
- `GET /api/auth/google/callback` - Google SSO callback
- `GET /api/auth/microsoft/start` - Start Microsoft SSO
- `GET /api/auth/microsoft/callback` - Microsoft SSO callback

#### Gmail
- `POST /api/gmail/webhook` - Gmail Pub/Sub webhook
- `POST /api/gmail/watch` - Set up Gmail watch

#### Calendar
- `GET /api/calendar/events` - List events
- `POST /api/calendar/events` - Create event
- `POST /api/calendar/block` - Auto-block for booking
- `GET /api/calendar/availability` - Check availability
- `DELETE /api/calendar/event/{id}` - Delete event

#### Clients
- `POST /api/clients/` - Create client
- `GET /api/clients/{id}` - Get client
- `GET /api/clients/` - List clients
- `GET /api/clients/search/by-email/` - Search by email
- `PUT /api/clients/{id}` - Update client
- `DELETE /api/clients/{id}` - Delete client

#### Agents
- `GET /api/agents/` - List agents
- `GET /api/agents/{id}` - Get agent
- `POST /api/agents/` - Create agent
- `PUT /api/agents/{id}` - Update agent
- `DELETE /api/agents/{id}` - Delete agent

#### Admin
- `GET /api/metrics/` - System metrics (admin-only)
- `GET /api/unsafe-threads/` - List unsafe threads (admin-only)
- `DELETE /api/unsafe-threads/{id}` - Clear unsafe thread (admin-only)

### By Error Type

#### Import Errors
- **Search:** `from app`, `import`, `ModuleNotFoundError`
- **Files to Check:** All service files, router files
- **Common Causes:** Missing file, wrong path, circular import

#### Database Errors
- **Search:** `get_cursor`, `database_url`, `psycopg2`, `SQL`
- **Files to Check:** `database.py`, `supabase_service.py`, all services
- **Common Causes:** Missing env var, wrong connection string, table missing

#### Authentication Errors
- **Search:** `jwt_secret_key`, `get_current_user`, `401`, `Unauthorized`
- **Files to Check:** `auth_service.py`, `auth.py` router
- **Common Causes:** Missing secret key, expired token, user not found

#### Guardian Errors
- **Search:** `guardian_manager`, `receive_event`, `get_guardian_manager`
- **Files to Check:** `audit_service.py`, all guardian files
- **Common Causes:** Circular import, missing tenant_id, wrong event format

#### Email Processing Errors
- **Search:** `email_processor_v3`, `process_email`, `gmail_webhook`
- **Files to Check:** `email_processor_v3.py`, `gmail_webhook.py`, intelligence modules
- **Common Causes:** Missing intelligence service, Claude API error, Gmail API error

---

## 📝 KEY CONFIGURATION FILES

### Environment Variables (.env)
**Location:** `backend/.env` (not in repo, must be created)  
**Required Variables:**
```bash
# Database
database_url=postgresql://user:pass@host:port/dbname
default_tenant_id=uuid-here

# JWT
jwt_secret_key=your-secret-key-here

# Encryption
encryption_key=your-fernet-key-here

# Anthropic Claude
anthropic_api_key=your-api-key-here

# Gmail Pub/Sub
gmail_webhook_url=https://your-domain.com/api/gmail/webhook
gmail_pubsub_topic=projects/PROJECT/topics/TOPIC
gmail_pubsub_service_account=service-account@project.iam.gserviceaccount.com

# Optional
maya_email=maya@skinnymanmusic.com
google_oauth_client_id=...
google_oauth_client_secret=...
microsoft_oauth_client_id=...
microsoft_oauth_client_secret=...
openai_api_key=...
```

### Configuration File
**Location:** `backend/app/config.py`  
**Key Class:** `Settings` (Pydantic BaseSettings)  
**Key Function:** `get_settings()` - Returns cached Settings instance

### Requirements
**Location:** `backend/requirements.txt`  
**Key Dependencies:**
- `fastapi`, `uvicorn` - Web framework
- `psycopg2-binary`, `asyncpg`, `sqlalchemy` - Database
- `PyJWT`, `bcrypt`, `passlib[bcrypt]` - Authentication
- `cryptography` - Encryption
- `anthropic`, `openai` - AI services
- `google-api-python-client` - Google APIs

---

## 🎯 QUICK REFERENCE

### How to Find a Function
1. Search by function name in this document
2. Use `grep` to find all usages
3. Check the file listed in search index
4. Read function definition and all call sites

### How to Fix an Import Error
1. Verify file exists: `glob_file_search` for filename
2. Check import path matches file location
3. Verify file has correct exports (`__all__` or public functions)
4. Check for circular imports (use lazy loading if needed)

### How to Fix a Database Error
1. Check table exists in migrations
2. Verify query syntax matches PostgreSQL
3. Check RLS policies if tenant isolation issues
4. Verify `tenant_id` is passed correctly

### How to Fix an Authentication Error
1. Check `.env` has `jwt_secret_key`
2. Verify token format (Bearer token)
3. Check token expiration
4. Verify user exists in `users` table

### How to Fix a Guardian Error
1. Check `audit_service.py` emits events correctly
2. Verify `guardian_manager.py` receives events
3. Check guardian factory functions exist
4. Verify no circular imports (lazy loading)

---

## 📚 RELATED DOCUMENTATION

### Primary Documentation
- `OMEGA_OVERVIEW.md` - Complete system overview (2524 lines)
- `CLAUDE_PROGRESS_LOG.md` - Implementation history (3874 lines)
- `SECURITY_AUDIT_REPORT.md` - Security audit results
- `SANITY_CHECK_REPORT.md` - Latest verification results
- `HONEST_VERIFICATION.md` - Limitations and honest assessment

### Status Reports
- `REBUILD_STATUS_REPORT.md` - Rebuild completion status
- `REBUILD_PROGRESS.md` - Rebuild progress log
- `MISSING_FILES_DIFFERENTIAL.md` - Files that were lost
- `FINAL_VERIFICATION_REPORT.md` - Final verification results

### Implementation Specs
- `OMEGA_4.0_CURSOR_INSTRUCTIONS.md` - v4.0 implementation guide
- Various phase completion reports (if they exist)

---

## 🔄 RECOVERY CHECKLIST

If system breaks again:

1. **Check Git Status**
   - `git status` - See what changed
   - `git log` - Check commit history
   - `git diff` - See what was modified

2. **Verify Critical Files**
   - Check `app/services/auth_service.py` exists
   - Check `app/database.py` has async support
   - Check all routers exist and are registered
   - Check all migrations exist

3. **Check Integration Points**
   - Verify `audit_service.py` → `guardian_manager` integration
   - Verify `email_processor_v3.py` → intelligence modules
   - Verify `calendar_service_v3.py` → `supabase_service.py`
   - Verify all routers → `auth_service.py`

4. **Test Imports**
   - Try importing each service
   - Check for circular imports
   - Verify all dependencies in requirements.txt

5. **Check Configuration**
   - Verify `.env` file exists
   - Check all required env vars are set
   - Verify config.py loads correctly

6. **Run Tests**
   - Run `pytest tests/`
   - Check for import errors
   - Check for missing files

---

## 🎓 FOR AI ASSISTANTS

### How to Use This Document

1. **Search by Function Name** - Use search index to find where functions are defined
2. **Search by Error Message** - Use troubleshooting guide to find solutions
3. **Search by File Name** - Use file inventory to understand file structure
4. **Search by Integration** - Use integration points to understand data flow

### When Fixing Issues

1. **Read the Error** - Understand what failed
2. **Find the Function** - Use search index to locate code
3. **Check Integration** - Verify integration points are correct
4. **Check Dependencies** - Verify all imports and dependencies
5. **Test the Fix** - Verify fix doesn't break other things

### Common Patterns

- **Lazy Loading** - Used to avoid circular imports (guardian_manager, audit_service)
- **Fail-Open** - Guardian failures don't block main pipeline
- **Per-Tenant Caching** - Services cached per tenant_id
- **Audit Everything** - All operations logged via audit_service
- **RLS Everywhere** - All database queries use tenant_id for isolation

---

**END OF MASTER REFERENCE DOCUMENT**

This document should be your first stop when searching for information about the system. Use Ctrl+F or search tools to find specific functions, files, or error messages.

