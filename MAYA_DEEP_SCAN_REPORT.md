# MAYA PROJECT DEEP SCAN REPORT
**Scan Date:** 2025-11-22T22:14:34.975337
**Project Root:** .

---

## 📊 EXECUTIVE SUMMARY

- **Backend Files:** 105
- **Frontend Files:** 10
- **Documentation Files:** 152
- **TODOs Found:** 100
- **Hallucinations Detected:** 50

## 🔧 BACKEND ANALYSIS

### Routers (12)
- ✅ `backend/app/routers/metrics.py` (106 lines)
- ✅ `backend/app/routers/auth.py` (315 lines)
- ✅ `backend/app/routers/calendar.py` (344 lines)
- ✅ `backend/app/routers/agents.py` (135 lines)
- ✅ `backend/app/routers/bookings.py` (148 lines)
- ✅ `backend/app/routers/clients.py` (296 lines)
- ✅ `backend/app/routers/health.py` (56 lines)
- ✅ `backend/app/routers/stripe.py` (125 lines)
- ✅ `backend/app/routers/unsafe_threads.py` (133 lines)
- ✅ `backend/app/routers/sms.py` (268 lines)
- ✅ `backend/app/routers/__init__.py` (33 lines)
- ✅ `backend/app/routers/gmail.py` (135 lines)

### Services (29)
- ✅ `backend/app/services/conversation_service.py` (167 lines)
- ✅ `backend/app/services/stripe_service.py` (253 lines)
- ✅ `backend/app/services/eli_service.py` (94 lines)
- ✅ `backend/app/services/gmail_webhook.py` (378 lines)
- ✅ `backend/app/services/auth_service.py` (306 lines)
- ✅ `backend/app/services/audit_service.py` (148 lines)
- ✅ `backend/app/services/calendar_service_v3.py` (467 lines)
- ✅ `backend/app/services/retry_queue_service.py` (216 lines)
- ✅ `backend/app/services/aegis_anomaly_service.py` (260 lines)
- ✅ `backend/app/services/supabase_service.py` (508 lines)
- ✅ `backend/app/services/idempotency_service.py` (129 lines)
- ✅ `backend/app/services/sso_service.py` (213 lines)
- ✅ `backend/app/services/booking_service.py` (150 lines)
- ✅ `backend/app/services/sms_service.py` (92 lines)
- ✅ `backend/app/services/email_processor_v3.py` (623 lines)
- ... and 14 more

### Guardians (6)
- ✅ `backend/app/guardians/guardian_manager.py` (101 lines)
- ✅ `backend/app/guardians/vita_repair.py` (361 lines)
- ✅ `backend/app/guardians/sentra_safety.py` (361 lines)
- ✅ `backend/app/guardians/solin_mcp.py` (333 lines)
- ✅ `backend/app/guardians/guardian_daemon.py` (339 lines)
- ⚠️ `backend/app/guardians/__init__.py` (24 lines)

### Workers (3)
- ✅ `backend/app/workers/email_retry_worker.py` (216 lines)
- ✅ `backend/app/workers/payment_reminder_worker.py` (247 lines)
- ✅ `backend/app/workers/__init__.py` (12 lines)

### Migrations (13)
- ✅ `migrations/007_add_system_state.sql`
- ✅ `migrations/005_add_unsafe_threads.sql`
- ✅ `migrations/004_performance_indexes.sql`
- ✅ `migrations/006_add_repair_log.sql`
- ✅ `migrations/015_add_clients_email_hash.sql`
- ✅ `migrations/002_add_calendar_events.sql`
- ✅ `migrations/012_add_bookings_table.sql`
- ✅ `migrations/014_add_conversations_table.sql`
- ✅ `migrations/013_add_reminder_columns.sql`
- ✅ `migrations/008_add_v4_sso_tables.sql`
- ✅ `migrations/011_archivus_schema.sql`
- ✅ `migrations/001_add_email_hash.sql`
- ✅ `migrations/003_add_idempotency_tables.sql`

## 🎨 FRONTEND ANALYSIS

### Pages (2)
- ✅ `omega-frontend/src/app/page.tsx` (213 lines)
- ✅ `omega-frontend/src/app/bookings/page.tsx` (147 lines)

### Components (6)
- ✅ `omega-frontend/src/components/error-message.tsx` (56 lines)
- ✅ `omega-frontend/src/components/skeleton.tsx` (31 lines)
- ✅ `omega-frontend/src/components/loading-spinner.tsx` (29 lines)
- ✅ `omega-frontend/src/components/payment-status.tsx` (98 lines)
- ⚠️ `omega-frontend/src/components/layout/Sidebar.tsx` (1 lines)
- ✅ `omega-frontend/src/components/layout/AppLayout.tsx` (21 lines)

## 📚 DOCUMENTATION

### Core Documentation (40)
- `docs/PRODUCT_STRATEGY.md` (256 words)
- `docs/FRONTEND_AUTOBUILD_SPEC.md` (384 words)
- `docs/SAFETY_CONTRACT.md` (267 words)
- `docs/GILMAN_ACCORDS.md` (984 words)
- `docs/VERSION.md` (48 words)
- `docs/BACKEND_AUTOBUILD_SPEC.md` (172 words)
- `docs/WORKFLOW_PROTECTION_MAP.md` (127 words)
- `docs/PYTHON_DEPENDENCY_POLICY.md` (456 words)
- `docs/VERTICAL_PACKS.md` (283 words)
- `docs/README.md` (471 words)
- `docs/COPILOT_SAFETY_MATRIX.md` (164 words)
- `docs/SELF_UPDATE_POLICY.md` (405 words)
- `docs/DEPLOYMENT_PIPELINE.md` (597 words)
- `docs/BACKEND_INTEGRITY_POLICY.md` (336 words)
- `docs/ARCHITECTURE_OVERVIEW.md` (122 words)
- `docs/SELF_UPDATE_RISK_MODEL.md` (182 words)
- `docs/UX_GUIDELINES.md` (982 words)
- `docs/CORE_INTEGRITY_SUMMARY.md` (417 words)
- `docs/MASTER_HANDOFF.md` (1,308 words)
- `docs/SOLIN_AUTOFIX_POLICY_V2.md` (1,068 words)
- `docs/ADAPTIVE_ONBOARDING.md` (529 words)
- `docs/AUTO_FIX_POLICY_REPORT.md` (220 words)
- `repo_integrity_pack/docs/REPO_INTEGRITY_POLICY.md` (3 words)
- `v3_integrity_pack/docs/REPO_INTEGRITY_POLICY.md` (3 words)
- `repo_integrity_pack_v3/docs/REPO_INTEGRITY_POLICY.md` (15 words)
- `repo_integrity_pack_v3/docs/DEPLOYMENT_PIPELINE.md` (10 words)
- `repo_integrity_pack_v3/docs/MASTER_HANDOFF.md` (10 words)
- `backend/docs/REPORT_IMPORT_FIXES.md` (785 words)
- `backend/docs/REPORT_CONFIG_RUNTIME_ALIGNMENT.md` (1,101 words)
- `backend/docs/REPORT_FULL_DEPENDENCY_MAP.md` (345 words)
- `backend/docs/REPORT_IMPORT_ISSUES.md` (267 words)
- `backend/docs/REPORT_DEPENDENCY_AUDIT.md` (421 words)
- `backend/docs/REPORT_BACKEND_HEALTH_CHECK.md` (622 words)
- `backend/docs/REPORT_RUNTIME_ASSUMPTIONS.md` (668 words)
- `docs/archive/OMEGA_OVERVIEW.md` (8,468 words)
- `docs/archive/MASTER_REFERENCE_DOCUMENT.md` (3,492 words)
- `docs/roadmaps/REINTRODUCTION_PLAN.md` (297 words)
- `docs/roadmaps/POSTPONED_FEATURES.md` (281 words)
- `docs/roadmaps/ROADMAP_OVERVIEW.md` (249 words)
- `docs/notes/ICONS_NEEDED.md` (142 words)

### Reports (29)
- `docs/reports/FINAL_CLAUDE_REFINEMENT_FOR_SOLIN.md` (5,657 words)
- `docs/reports/README_AZURE_FUNCTIONS.md` (296 words)
- `docs/reports/FINAL_CLAUDE_REFINEMENT_FOR_SOLIN_v2.md` (7,032 words)
- `docs/reports/ENVIRONMENT_VARIABLES.md` (233 words)
- `docs/reports/QUICK_STATUS_REPORT.md` (164 words)
- `docs/reports/DEPLOYMENT_GUIDE.md` (851 words)
- `docs/reports/DOCUMENTATION_INDEX.md` (396 words)
- `docs/reports/MAYA_V3_IMPLEMENTATION_COMPLETE.md` (648 words)
- `docs/reports/SANITY_CHECK_REPORT.md` (1,204 words)
- `docs/reports/REBUILD_VERIFICATION_REPORT.md` (783 words)
- ... and 19 more

## 🧪 TESTS

### Backend Tests
- **Files:** 10
- **Total Tests:** 24

### Frontend Tests
- **Files:** 0
- **Total Tests:** 0

## ⚠️ ISSUES DETECTED

### Hallucinations (50)
- `MAYA_DEEP_SCAN_HANDOFF.md` references missing file: `backend\tests\fixtures.py`
- `MAYA_DEEP_SCAN_HANDOFF.md` references missing file: `backend\tests\test_acceptance_ab.py`
- `MAYA_DEEP_SCAN_HANDOFF.md` references missing file: `backend\tests\test_aegis_integration.py`
- `MAYA_DEEP_SCAN_HANDOFF.md` references missing file: `backend\tests\test_archivus_service.py`
- `MAYA_DEEP_SCAN_HANDOFF.md` references missing file: `backend\tests\test_calendar.py`
- `MAYA_DEEP_SCAN_HANDOFF.md` references missing file: `backend\tests\test_intelligence.py`
- `MAYA_DEEP_SCAN_HANDOFF.md` references missing file: `backend\tests\test_pipeline.py`
- `MAYA_DEEP_SCAN_HANDOFF.md` references missing file: `backend\tests\test_pricing_integration.py`
- `MAYA_DEEP_SCAN_HANDOFF.md` references missing file: `backend\tests\test_runner.py`
- `MAYA_DEEP_SCAN_HANDOFF.md` references missing file: `backend\tests\test_safety_gate_phase5.py`
- `MAYA_DEEP_SCAN_HANDOFF.md` references missing file: `backend\app\config.py`
- `MAYA_DEEP_SCAN_HANDOFF.md` references missing file: `backend\app\main.py`
- `MAYA_DEEP_SCAN_HANDOFF.md` references missing file: `backend\app\guardians\sentra_safety.py`
- `MAYA_DEEP_SCAN_HANDOFF.md` references missing file: `backend\app\config.py`
- `MAYA_DEEP_SCAN_HANDOFF.md` references missing file: `backend\app\main.py`
- `MAYA_DEEP_SCAN_HANDOFF.md` references missing file: `backend\app\main.py`
- `MAYA_DEEP_SCAN_HANDOFF.md` references missing file: `backend\app\config\stripe_config.py`
- `MAYA_DEEP_SCAN_HANDOFF.md` references missing file: `backend\app\routers\bookings.py`
- `MAYA_DEEP_SCAN_HANDOFF.md` references missing file: `backend\app\routers\stripe.py`
- `MAYA_DEEP_SCAN_HANDOFF.md` references missing file: `backend\app\routers\calendar.py`
- ... and 30 more

### TODOs (100)
- `MAYA_DEEP_SCAN_HANDOFF.md` (72 TODOs)
  - Line 14: - **TODOs Found:** 79
  - Line 15: - **FIXMEs/Bugs Found:** 33
  - Line 279: ## 📝 TODOs
- `deep_scan.py` (28 TODOs)
  - Line 28: "todos": [],
  - Line 44: self.find_todos_fixmes()
  - Line 125: # Find TODOs/FIXMEs

## 🔌 INTEGRATION STATUS

- **Frontend API Calls:** 2
- **Backend Routes:** 26

**Frontend calls these endpoints:**
- `api/bookings`
- `api/health`

**Backend provides these routes:**
- `/{client_id}`
- `/google/callback`
- `/payment-status/{booking_id}`
- `/watch`
- `/me`
- `/{booking_id}`
- `/db`
- `/events`
- `/block`
- `/{agent_id}/pause`

## ⚙️ CONFIGURATION FILES

- `host.json`
- `package-lock.json`
- `package.json`
- `omega-frontend/package-lock.json`
- `omega-frontend/package.json`
- `deploy_tmp/package-lock.json`
- `deploy_tmp/package.json`
- `backend/railway.json`
- `dev-portal/package-lock.json`
- `dev-portal/package.json`
- `api/health/function.json`
- `infrastructure/archive/azure-functions/deploy_tmp/package-lock.json`
- `infrastructure/archive/azure-functions/deploy_tmp/package.json`
- `infrastructure/archive/frontend/dev-portal/package-lock.json`
- `infrastructure/archive/frontend/dev-portal/package.json`
- `.github/copilot_rules.yml`
- `.github/backend_protected_paths.yml`
- `.github/workflows/deploy-backend.yml`
- `.github/workflows/deploy.yml`
- `.github/workflows/self_update_check.yml`
- ... and 17 more
