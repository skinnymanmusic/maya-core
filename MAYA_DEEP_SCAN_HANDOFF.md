# MAYA PROJECT DEEP SCAN HANDOFF
**Generated:** 2025-11-22T22:14:42.717721
**Scanner:** Claude Code
**For Analysis By:** Claude Desktop (Sonnet 4.5)

================================================================================

## 📊 EXECUTIVE SUMMARY

- **Total Files Scanned:** 431
- **Code Files:** 206
- **Documentation Files:** 187
- **Configuration Files:** 2
- **TODOs Found:** 72
- **FIXMEs/Bugs Found:** 33
- **Potential Hallucinations:** 176
- **Drift Issues:** 1
- **Test Files:** 25

## 🚨 POTENTIAL HALLUCINATIONS

Features documented but not found in implementation:

🔴 **API_ENDPOINT**: GET /api/health/` documented but not found in code
🔴 **API_ENDPOINT**: GET /api/metrics documented but not found in code
🔴 **API_ENDPOINT**: POST /api/emails/{email_id}/process` documented but not found in code
🔴 **API_ENDPOINT**: POST /api/agents/{id}/pause documented but not found in code
🔴 **API_ENDPOINT**: POST /api/vee/drafts/{id}/queue` documented but not found in code
🔴 **API_ENDPOINT**: GET /api/auth/google/start` documented but not found in code
🔴 **API_ENDPOINT**: POST /api/calendar/sync` documented but not found in code
🔴 **API_ENDPOINT**: GET /api/auth/google/callback` documented but not found in code
🔴 **API_ENDPOINT**: GET /db` documented but not found in code
🔴 **API_ENDPOINT**: POST /api/workflows/{id}/execute documented but not found in code
🔴 **API_ENDPOINT**: PUT /api/clients/{id}` documented but not found in code
🔴 **API_ENDPOINT**: DELETE /api/scheduler/tasks/{id} documented but not found in code
🔴 **API_ENDPOINT**: GET /api/system/status` documented but not found in code
🔴 **API_ENDPOINT**: POST /events` documented but not found in code
🔴 **API_ENDPOINT**: POST /api/proactive/schedule documented but not found in code
🔴 **API_ENDPOINT**: GET /api/hands-off/automations documented but not found in code
🔴 **API_ENDPOINT**: POST /block` documented but not found in code
🔴 **API_ENDPOINT**: GET /api/proactive/scheduled documented but not found in code
🔴 **API_ENDPOINT**: POST /google/start` documented but not found in code
🔴 **API_ENDPOINT**: GET /api/health/db documented but not found in code
🔴 **API_ENDPOINT**: GET /api/emails/{id} documented but not found in code
🔴 **API_ENDPOINT**: GET /api/agents documented but not found in code
🔴 **API_ENDPOINT**: GET /api/unsafe-threads documented but not found in code
🔴 **API_ENDPOINT**: GET /api/agents` documented but not found in code
🔴 **API_ENDPOINT**: POST /api/auth/refresh documented but not found in code
🔴 **API_ENDPOINT**: POST /api/scheduler/tasks documented but not found in code
🔴 **API_ENDPOINT**: GET /api/emails/` documented but not found in code
🔴 **API_ENDPOINT**: GET /api/clients documented but not found in code
🔴 **API_ENDPOINT**: GET /api/auth/microsoft/callback` documented but not found in code
🔴 **API_ENDPOINT**: POST /api/automations documented but not found in code
🔴 **API_ENDPOINT**: GET /events` documented but not found in code
🔴 **API_ENDPOINT**: GET /api/system/status documented but not found in code
🔴 **API_ENDPOINT**: DELETE /api/bookings/{id} documented but not found in code
🔴 **API_ENDPOINT**: GET /api/health documented but not found in code
🔴 **API_ENDPOINT**: GET /api/vee/drafts?status=approved` documented but not found in code
🔴 **API_ENDPOINT**: POST /api/accessibility/preferences documented but not found in code
🔴 **API_ENDPOINT**: DELETE /api/clients/{id} documented but not found in code
🔴 **API_ENDPOINT**: GET /api/packs/{id} documented but not found in code
🔴 **API_ENDPOINT**: DELETE /api/calendar/event/{event_id}` documented but not found in code
🔴 **API_ENDPOINT**: POST /api/calculate-price` documented but not found in code
🔴 **API_ENDPOINT**: PUT /api/scheduler/tasks/{id} documented but not found in code
🔴 **API_ENDPOINT**: GET /api/metrics` documented but not found in code
🔴 **API_ENDPOINT**: GET /api/clients/{id} documented but not found in code
🔴 **API_ENDPOINT**: POST /api/calendar/events documented but not found in code
🔴 **API_ENDPOINT**: GET /api/workflows/{id}/history documented but not found in code
🔴 **API_ENDPOINT**: GET /api/bookings/{booking_id}` documented but not found in code
🔴 **API_ENDPOINT**: POST /api/notifications/mark-read documented but not found in code
🔴 **API_ENDPOINT**: GET /api/automations documented but not found in code
🔴 **API_ENDPOINT**: DELETE /api/files/{id} documented but not found in code
🔴 **API_ENDPOINT**: GET /api/hands-off/status documented but not found in code
🔴 **API_ENDPOINT**: GET /api/vee/drafts` documented but not found in code
🔴 **API_ENDPOINT**: GET /api/packs documented but not found in code
🔴 **API_ENDPOINT**: POST /api/proactive/send-now documented but not found in code
🔴 **API_ENDPOINT**: DELETE /api/workflows/{id} documented but not found in code
🔴 **API_ENDPOINT**: POST /login` documented but not found in code
🔴 **API_ENDPOINT**: GET /api/files/{id} documented but not found in code
🔴 **API_ENDPOINT**: GET /api/health/db` documented but not found in code
🔴 **API_ENDPOINT**: POST /api/onboarding/complete-step documented but not found in code
🔴 **API_ENDPOINT**: GET /api/workflows/{id} documented but not found in code
🔴 **API_ENDPOINT**: POST /api/integrations/{provider}/connect documented but not found in code
🔴 **API_ENDPOINT**: POST /api/gmail/webhook documented but not found in code
🔴 **API_ENDPOINT**: POST /api/hands-off/disable documented but not found in code
🔴 **API_ENDPOINT**: GET /api/emails/thread/{id} documented but not found in code
🔴 **API_ENDPOINT**: POST /api/gmail/webhook` documented but not found in code
🔴 **API_ENDPOINT**: GET /api/health/encryption documented but not found in code
🔴 **API_ENDPOINT**: GET /api/clients/search/by-email documented but not found in code
🔴 **API_ENDPOINT**: POST /google/callback` documented but not found in code
🔴 **API_ENDPOINT**: POST /api/clients` documented but not found in code
🔴 **API_ENDPOINT**: POST /api/auth/login documented but not found in code
🔴 **API_ENDPOINT**: GET /api/unsafe-threads/` documented but not found in code
🔴 **API_ENDPOINT**: DELETE /api/agents/{id}` documented but not found in code
🔴 **API_ENDPOINT**: POST /api/calendar/auto-block` documented but not found in code
🔴 **API_ENDPOINT**: GET /google/start` documented but not found in code
🔴 **API_ENDPOINT**: DELETE /api/auto-approval/rules/{id} documented but not found in code
🔴 **API_ENDPOINT**: GET /api/bookings/{id} documented but not found in code
🔴 **API_ENDPOINT**: GET /api/emails documented but not found in code
🔴 **API_ENDPOINT**: POST /api/process-emails` documented but not found in code
🔴 **API_ENDPOINT**: POST /api/workflows documented but not found in code
🔴 **API_ENDPOINT**: POST /api/clients/` documented but not found in code
🔴 **API_ENDPOINT**: GET /api/auth/google/start documented but not found in code
🔴 **API_ENDPOINT**: POST /api/onboarding/skip-step documented but not found in code
🔴 **API_ENDPOINT**: GET /api/agents/{id}` documented but not found in code
🔴 **API_ENDPOINT**: POST /api/sms/receive` documented but not found in code
🔴 **API_ENDPOINT**: GET /api/packs/active documented but not found in code
🔴 **API_ENDPOINT**: GET /encryption` documented but not found in code
🔴 **API_ENDPOINT**: GET /api/scheduler/tasks documented but not found in code
🔴 **API_ENDPOINT**: GET /api/stripe/payment-status/{booking_id} documented but not found in code
🔴 **API_ENDPOINT**: POST /api/files/upload documented but not found in code
🔴 **API_ENDPOINT**: GET /google/callback` documented but not found in code
🔴 **API_ENDPOINT**: GET /api/notifications documented but not found in code
🔴 **API_ENDPOINT**: POST /api/bookings documented but not found in code
🔴 **API_ENDPOINT**: POST /` documented but not found in code
🔴 **API_ENDPOINT**: GET /api/pricing-history` documented but not found in code
🔴 **API_ENDPOINT**: POST /api/auto-approval/rules documented but not found in code
🔴 **API_ENDPOINT**: POST /api/messages documented but not found in code
🔴 **API_ENDPOINT**: POST /api/agents/` documented but not found in code
🔴 **API_ENDPOINT**: GET /api/accessibility/preferences documented but not found in code
🔴 **API_ENDPOINT**: POST /api/gmail/watch` documented but not found in code
🔴 **API_ENDPOINT**: DELETE /api/clients/{id}` documented but not found in code
🔴 **API_ENDPOINT**: GET /api/calendar/free-busy` documented but not found in code
🔴 **API_ENDPOINT**: POST /api/stripe/webhook documented but not found in code
🔴 **API_ENDPOINT**: DELETE /api/automations/{id} documented but not found in code
🔴 **API_ENDPOINT**: POST /api/create-invoice` documented but not found in code
🔴 **API_ENDPOINT**: POST /api/calendar/block documented but not found in code
🔴 **API_ENDPOINT**: GET /api/clients/` documented but not found in code
🔴 **API_ENDPOINT**: POST /api/notifications/preferences documented but not found in code
🔴 **API_ENDPOINT**: POST /api/calendar/block` documented but not found in code
🔴 **API_ENDPOINT**: GET /api/calendar/availability documented but not found in code
🔴 **API_ENDPOINT**: GET /api/calendar/events documented but not found in code
🔴 **API_ENDPOINT**: GET /api/bookings/` documented but not found in code
🔴 **API_ENDPOINT**: PUT /api/agents/{id}` documented but not found in code
🔴 **API_ENDPOINT**: PUT /api/clients/{id} documented but not found in code
🔴 **API_ENDPOINT**: GET /api/auth/me documented but not found in code
🔴 **API_ENDPOINT**: POST /api/market-analysis` documented but not found in code
🔴 **API_ENDPOINT**: PATCH /api/bookings/{id} documented but not found in code
🔴 **API_ENDPOINT**: POST /api/calendar/events` documented but not found in code
🔴 **API_ENDPOINT**: GET /` documented but not found in code
🔴 **API_ENDPOINT**: PUT /api/auto-approval/rules/{id} documented but not found in code
🔴 **API_ENDPOINT**: GET /api/calendar/availability` documented but not found in code
🔴 **API_ENDPOINT**: GET /api/bookings documented but not found in code
🔴 **API_ENDPOINT**: GET /api/emails/{email_id}` documented but not found in code
🔴 **API_ENDPOINT**: GET /api/messages documented but not found in code
🔴 **API_ENDPOINT**: GET /api/agents/` documented but not found in code
🔴 **API_ENDPOINT**: PATCH /api/agents/{id}` documented but not found in code
🔴 **API_ENDPOINT**: GET /api/auth/microsoft/start` documented but not found in code
🔴 **API_ENDPOINT**: DELETE /event/{event_id}` documented but not found in code
🔴 **API_ENDPOINT**: POST /api/onboarding/mode documented but not found in code
🔴 **API_ENDPOINT**: DELETE /api/clients/{client_id}` documented but not found in code
🔴 **API_ENDPOINT**: GET /api/emails/thread/{thread_id}` documented but not found in code
🔴 **API_ENDPOINT**: GET /api/auth/google/callback documented but not found in code
🔴 **API_ENDPOINT**: POST /api/agents documented but not found in code
🔴 **API_ENDPOINT**: POST /api/sms/receive documented but not found in code
🔴 **API_ENDPOINT**: GET /api/clients/search/by-email/` documented but not found in code
🔴 **API_ENDPOINT**: POST /api/scheduler/tasks/{id}/execute documented but not found in code
🔴 **API_ENDPOINT**: GET /api/metrics/` documented but not found in code
🔴 **API_ENDPOINT**: POST /api/agents` documented but not found in code
🔴 **API_ENDPOINT**: GET /api/clients/{client_id}` documented but not found in code
🔴 **API_ENDPOINT**: GET /availability` documented but not found in code
🔴 **API_ENDPOINT**: DELETE /api/calendar/event/{id}` documented but not found in code
🔴 **API_ENDPOINT**: PUT /api/workflows/{id} documented but not found in code
🔴 **API_ENDPOINT**: GET /api/integrations documented but not found in code
🔴 **API_ENDPOINT**: POST /api/clients documented but not found in code
🔴 **API_ENDPOINT**: GET /api/calendar/events` documented but not found in code
🔴 **API_ENDPOINT**: PUT /api/automations/{id} documented but not found in code
🔴 **API_ENDPOINT**: DELETE /api/calendar/event/{id} documented but not found in code
🔴 **API_ENDPOINT**: GET /api/venue-details/{venue_id}` documented but not found in code
🔴 **API_ENDPOINT**: GET /api/onboarding/state documented but not found in code
🔴 **API_ENDPOINT**: GET /api/health/encryption` documented but not found in code
🔴 **API_ENDPOINT**: GET /api/clients` documented but not found in code
🔴 **API_ENDPOINT**: POST /api/sms/send documented but not found in code
🔴 **API_ENDPOINT**: GET /api/health` documented but not found in code
🔴 **API_ENDPOINT**: DELETE /api/unsafe-threads/{id}` documented but not found in code
🔴 **API_ENDPOINT**: GET /api/sms/conversations documented but not found in code
🔴 **API_ENDPOINT**: POST /api/auth/refresh` documented but not found in code
🔴 **API_ENDPOINT**: POST /api/emails/{id}/process documented but not found in code
🔴 **API_ENDPOINT**: GET /api/workflows documented but not found in code
🔴 **API_ENDPOINT**: DELETE /api/unsafe-threads/{thread_id}` documented but not found in code
🔴 **API_ENDPOINT**: GET /api/clients/{id}` documented but not found in code
🔴 **API_ENDPOINT**: POST /api/auth/login` documented but not found in code
🔴 **API_ENDPOINT**: DELETE /api/notifications/{id} documented but not found in code
🔴 **API_ENDPOINT**: PUT /api/clients/{client_id}` documented but not found in code
🔴 **API_ENDPOINT**: POST /api/stripe/webhook` documented but not found in code
🔴 **API_ENDPOINT**: GET /api/onboarding/content documented but not found in code
🔴 **API_ENDPOINT**: POST /api/vee/drafts` documented but not found in code
🔴 **API_ENDPOINT**: POST /api/research-venue` documented but not found in code
🔴 **API_ENDPOINT**: POST /api/hands-off/enable documented but not found in code
🔴 **API_ENDPOINT**: GET /api/files documented but not found in code
🔴 **API_ENDPOINT**: GET /api/auto-approval/rules documented but not found in code
🔴 **API_ENDPOINT**: GET /api/agents/{id} documented but not found in code
🔴 **API_ENDPOINT**: POST /api/packs/{id}/activate documented but not found in code
🔴 **API_ENDPOINT**: GET /api/auth/me` documented but not found in code
🔴 **API_ENDPOINT**: DELETE /api/proactive/{id} documented but not found in code
🟡 **DATABASE_TABLE**: Table "014_add_conversations" mentioned in docs but not found in schema
🟡 **DATABASE_TABLE**: Table "huffman" mentioned in docs but not found in schema
🟡 **DATABASE_TABLE**: Table "database" mentioned in docs but not found in schema
🟡 **DATABASE_TABLE**: Table "012_add_bookings" mentioned in docs but not found in schema

## 🔄 CONFIGURATION DRIFT

🟡 **CONFIG_DUPLICATION**: Multiple nixpacks.toml files found: backend/nixpacks.toml, infrastructure/nixpacks.toml

## 🔌 API ENDPOINTS

**Documented:** 562 endpoints
**Implemented:** 41 endpoints

### Implemented Endpoints:
- `GET /` (backend/app/main.py)
- `GET /` (backend/app/routers/metrics.py)
- `GET /` (backend/app/routers/agents.py)
- `GET /` (backend/app/routers/bookings.py)
- `POST /` (backend/app/routers/clients.py)
- `GET /` (backend/app/routers/clients.py)
- `GET /` (backend/app/routers/health.py)
- `GET /` (backend/app/routers/unsafe_threads.py)
- `GET /availability` (backend/app/routers/calendar.py)
- `POST /block` (backend/app/routers/calendar.py)
- `GET /db` (backend/app/routers/health.py)
- `GET /encryption` (backend/app/routers/health.py)
- `DELETE /event/{event_id}` (backend/app/routers/calendar.py)
- `GET /events` (backend/app/routers/calendar.py)
- `POST /events` (backend/app/routers/calendar.py)
- `GET /google/callback` (backend/app/routers/auth.py)
- `POST /google/callback` (backend/app/routers/auth.py)
- `GET /google/start` (backend/app/routers/auth.py)
- `POST /google/start` (backend/app/routers/auth.py)
- `POST /login` (backend/app/routers/auth.py)
- ... and 21 more

## 💾 DATABASE

**Schema Tables/Models:** 16
**Code Files with DB Access:** 41

### Tables/Models:
- `IF` - backend/migrations/007_add_system_state.sql
- `IF` - backend/migrations/005_add_unsafe_threads.sql
- `IF` - backend/migrations/006_add_repair_log.sql
- `IF` - backend/migrations/002_add_calendar_events.sql
- `IF` - backend/migrations/012_add_bookings_table.sql
- `IF` - backend/migrations/014_add_conversations_table.sql
- `IF` - backend/migrations/014_add_conversations_table.sql
- `IF` - backend/migrations/008_add_v4_sso_tables.sql
- `IF` - backend/migrations/008_add_v4_sso_tables.sql
- `IF` - backend/migrations/008_add_v4_sso_tables.sql
- `IF` - backend/migrations/008_add_v4_sso_tables.sql
- `IF` - backend/migrations/008_add_v4_sso_tables.sql
- `IF` - backend/migrations/011_archivus_schema.sql
- `IF` - backend/migrations/011_archivus_schema.sql
- `IF` - backend/migrations/003_add_idempotency_tables.sql
- ... and 1 more

## 🧪 TESTS

**Total Test Functions:** 49
**Test Files:** 25

- `scripts/maintenance/self_test.py`: 1 tests
- `backend/tests/test_calendar.py`: 3 tests
- `backend/tests/test_stripe_integration.py`: 2 tests
- `backend/tests/test_intelligence.py`: 3 tests
- `backend/tests/test_runner.py`: 1 tests
- `backend/tests/test_aegis_integration.py`: 2 tests
- `backend/tests/test_pricing_integration.py`: 2 tests
- `backend/tests/test_acceptance_ab.py`: 3 tests
- `backend/tests/test_safety_gate_phase5.py`: 1 tests
- `backend/tests/test_archivus_service.py`: 3 tests
- ... and 15 more test files

## 🔗 EXTERNAL INTEGRATIONS

### GMAIL
Found in 34 files:
- `DEEP_SCAN_FOR_CLAUDE_DESKTOP.py`
- `api/gmail/webhook/index.js`
- `deploy_tmp/api/gmail/webhook/index.js`
- `backend/check_health.py`
- `backend/migrations/004_performance_indexes.sql`

### CALENDAR
Found in 32 files:
- `DEEP_SCAN_FOR_CLAUDE_DESKTOP.py`
- `CHECK_BACKEND_ENDPOINTS.py`
- `api/calendar/events/index.js`
- `api/calendar/block/index.js`
- `omega-frontend/src/app/page.tsx`

### STRIPE
Found in 16 files:
- `DEEP_SCAN_FOR_CLAUDE_DESKTOP.py`
- `CHECK_BACKEND_ENDPOINTS.py`
- `omega-frontend/src/components/payment-status.tsx`
- `backend/check_health.py`
- `backend/migrations/012_add_bookings_table.sql`

### SUPABASE
Found in 8 files:
- `DEEP_SCAN_FOR_CLAUDE_DESKTOP.py`
- `scripts/maintenance/restructure_repo.py`
- `backend/app/routers/clients.py`
- `backend/app/services/calendar_service_v3.py`
- `backend/app/services/supabase_service.py`

### OPENAI
Found in 2 files:
- `DEEP_SCAN_FOR_CLAUDE_DESKTOP.py`
- `backend/app/config/settings.py`

### TWILIO
Found in 4 files:
- `DEEP_SCAN_FOR_CLAUDE_DESKTOP.py`
- `backend/app/routers/sms.py`
- `backend/app/services/sms_service.py`
- `backend/app/config/twilio_config.py`

### FIREBASE
Found in 1 files:
- `DEEP_SCAN_FOR_CLAUDE_DESKTOP.py`

## 📝 TODOs

Total: 72

**deep_scan.py** (28 TODOs):
  - Line 28: `"todos": [],`
  - Line 44: `self.find_todos_fixmes()`
  - Line 125: `# Find TODOs/FIXMEs`
  - ... and 25 more

**scan_frontend.py** (4 TODOs):
  - Line 16: `"stub_files": [],  # Files with only types/TODOs`
  - Line 57: `# Check if it's a stub (mostly TODOs, types, or very short)`
  - Line 58: `if 'TODO' in content and len(content) < 500:`
  - ... and 1 more

**DEEP_SCAN_FOR_CLAUDE_DESKTOP.py** (23 TODOs):
  - Line 16: `9. TODOs, FIXMEs, and incomplete features`
  - Line 37: `'todos': [],`
  - Line 74: `print(f"✓ Found {len(self.results['todos'])} TODOs")`
  - ... and 20 more

**backend/app/guardians/solin_mcp.py** (1 TODOs):
  - Line 223: `# TODO: Send notifications (email/Discord)`

**backend/app/guardians/guardian_daemon.py** (1 TODOs):
  - Line 269: `# TODO: Make daemon async or create sync Aegis wrapper`

**backend/app/routers/auth.py** (1 TODOs):
  - Line 77: `TODO: In a full implementation, decode and validate refresh token, then re-issue`

**backend/app/routers/agents.py** (4 TODOs):
  - Line 43: `# TODO: Implement actual agent listing from database or registry`
  - Line 83: `# TODO: Implement actual agent lookup`
  - Line 111: `# TODO: Implement actual agent pause logic`
  - ... and 1 more

**backend/app/routers/stripe.py** (2 TODOs):
  - Line 57: `# TODO: Handle failed payments`
  - Line 68: `# TODO: Handle refunds`

**backend/app/routers/gmail.py** (1 TODOs):
  - Line 95: `# TODO: Queue email processing job`

**backend/app/middleware/tenant_context.py** (3 TODOs):
  - Line 17: `# TODO: Extract from JWT token in Authorization header`
  - Line 22: `request.state.user_id = None  # TODO: Extract from JWT`
  - Line 23: `request.state.user_role = None  # TODO: Extract from JWT`

**backend/app/services/stripe_service.py** (2 TODOs):
  - Line 223: `# TODO: Send confirmation email via Maya`
  - Line 224: `# TODO: Sync to QuickBooks via Nova`

**backend/app/services/eli_service.py** (1 TODOs):
  - Line 56: `# TODO: Make this async or use sync httpx client`

**backend/app/workers/email_retry_worker.py** (1 TODOs):
  - Line 63: `# TODO: Make this properly async`


## 🐛 FIXMEs & BUGS

Total: 33

- **deep_scan.py:44**
  `self.find_todos_fixmes()`

- **deep_scan.py:125**
  `# Find TODOs/FIXMEs`

- **deep_scan.py:126**
  `todos = [line.strip() for line in lines if 'TODO' in line.upper() or 'FIXME' in line.upper()]`

- **deep_scan.py:420**
  `def find_todos_fixmes(self):`

- **deep_scan.py:421**
  `"""Find all TODOs and FIXMEs across project"""`

- **deep_scan.py:422**
  `print("📝 Finding TODOs and FIXMEs...")`

- **deep_scan.py:436**
  `if 'TODO' in line.upper() or 'FIXME' in line.upper():`

- **DEEP_SCAN_FOR_CLAUDE_DESKTOP.py:16**
  `9. TODOs, FIXMEs, and incomplete features`

- **DEEP_SCAN_FOR_CLAUDE_DESKTOP.py:38**
  `'fixmes': [],`

- **DEEP_SCAN_FOR_CLAUDE_DESKTOP.py:75**
  `print(f"✓ Found {len(self.results['fixmes'])} FIXMEs")`

- **DEEP_SCAN_FOR_CLAUDE_DESKTOP.py:165**
  `"""Analyze all code files for TODOs, FIXMEs, and patterns"""`

- **DEEP_SCAN_FOR_CLAUDE_DESKTOP.py:183**
  `# Find FIXMEs`

- **DEEP_SCAN_FOR_CLAUDE_DESKTOP.py:184**
  `if 'FIXME' in line.upper() or 'BUG' in line.upper():`

- **DEEP_SCAN_FOR_CLAUDE_DESKTOP.py:185**
  `self.results['fixmes'].append({`

- **DEEP_SCAN_FOR_CLAUDE_DESKTOP.py:506**
  `report.append(f"- **FIXMEs/Bugs Found:** {len(self.results['fixmes'])}")`

- **DEEP_SCAN_FOR_CLAUDE_DESKTOP.py:611**
  `# FIXMEs`

- **DEEP_SCAN_FOR_CLAUDE_DESKTOP.py:612**
  `if self.results['fixmes']:`

- **DEEP_SCAN_FOR_CLAUDE_DESKTOP.py:613**
  `report.append("## 🐛 FIXMEs & BUGS")`

- **DEEP_SCAN_FOR_CLAUDE_DESKTOP.py:615**
  `report.append(f"Total: {len(self.results['fixmes'])}")`

- **DEEP_SCAN_FOR_CLAUDE_DESKTOP.py:618**
  `for fixme in self.results['fixmes'][:20]:`

... and 13 more

## 📦 DEPENDENCIES

**Python Packages:** 35
**JavaScript Packages:** 78

## ⚙️ CONFIGURATION

**Config Files:** 2

- `backend/nixpacks.toml` (0 variables)
- `infrastructure/nixpacks.toml` (0 variables)

## 📁 PROJECT STRUCTURE

### Key Directories:
- `./` (55 files)
- `backend/` (45 files)
- `docs/` (22 files)
- `backend/app/services/` (20 files)
- `docs/reports/` (18 files)
- `backend/migrations/` (13 files)
- `backend/app/routers/` (12 files)
- `backend/tests/` (12 files)
- `tests/backend/tests/` (12 files)
- `restructure/` (10 files)
- `backend/app/services/intelligence/` (9 files)
- `docs/reports/phase-completion/` (9 files)
- `infrastructure/scripts/` (9 files)
- `scripts/maintenance/` (8 files)
- `backend/docs/` (7 files)
- `backend/app/guardians/` (6 files)
- `backend/app/models/` (6 files)
- `infrastructure/archive/shared/` (6 files)
- `shared/` (6 files)
- `omega-frontend/` (5 files)

## ⭐ CRITICAL FILES

- `backend/app/main.py` (3211 bytes)
- `DOCUMENTATION_INDEX.md` (3503 bytes)
- `index.js` (240 bytes)
- `api/calendar/events/index.js` (1115 bytes)
- `backend/app/config.py` (289 bytes)
- `backend/app/config/twilio_config.py` (579 bytes)
- `backend/app/config/settings.py` (2184 bytes)
- `backend/app/config/settings.py` (2184 bytes)

## 📈 STATISTICS

- **Total Project Size:** 19,051,997 bytes (18.17 MB)
- **Average File Size:** 44,204 bytes
- **Largest Files:**
  - `file_structure.txt`: 12,791,941 bytes
  - `diagnostics/project_tree.txt`: 2,166,030 bytes
  - `directory_structure.txt`: 1,112,377 bytes
  - `dev-portal/package-lock.json`: 297,098 bytes
  - `infrastructure/archive/frontend/dev-portal/package-lock.json`: 297,098 bytes

## 🕐 RECENT ACTIVITY

Most recently modified files:
- `MAYA_DEEP_SCAN_REPORT.md` - 2025-11-22T22:14:35.279485
- `backend/.pytest_cache/CACHEDIR.TAG` - 2025-11-22T22:14:17.085514
- `backend/.pytest_cache/v/cache/stepwise` - 2025-11-22T22:14:17.085514
- `backend/.pytest_cache/v/cache/lastfailed` - 2025-11-22T22:14:17.085514
- `backend/.pytest_cache/v/cache/nodeids` - 2025-11-22T22:14:17.085514
- `backend/.pytest_cache/.gitignore` - 2025-11-22T22:14:17.084514
- `backend/.pytest_cache/README.md` - 2025-11-22T22:14:17.084514
- `backend/.env` - 2025-11-22T22:13:45.287572
- `backend/app/config.py` - 2025-11-22T22:13:22.708617
- `backend/app/config/__init__.py` - 2025-11-22T22:13:14.343632

## 💡 RECOMMENDATIONS FOR CLAUDE DESKTOP

Based on this scan, please analyze:

1. **Hallucination Review**: Are the documented features actually implemented?
2. **Drift Analysis**: Do configurations match across environments?
3. **Progress Assessment**: What percentage of planned features are complete?
4. **Bug Priority**: Which FIXMEs should be addressed first?
5. **Technical Debt**: Are there patterns of incomplete implementations?
6. **Integration Health**: Are all external services properly integrated?
7. **Test Coverage**: Is testing adequate for the complexity level?
8. **Documentation Gap**: What's documented vs. what exists in code?
