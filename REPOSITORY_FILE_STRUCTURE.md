# MayAssistant Repository - Complete File Structure

**Repository:** maya-ai (maya-core on GitHub)  
**Last Updated:** 2025-01-27  
**Purpose:** Complete file and directory structure for ChatGPT/Claude handoff

---

## ROOT DIRECTORY STRUCTURE

```
maya-ai/
├── .cursor/                          # Cursor IDE rules and configuration
├── .github/                          # GitHub Actions workflows and configs
├── api/                              # Legacy Azure Functions API (archived)
├── backend/                          # FastAPI backend application
├── cursor/                           # Cursor-specific rules and docs
├── dashboard/                        # Legacy dashboard frontend (archived)
├── deploy_tmp/                       # Temporary deployment files
├── dev-portal/                       # Legacy dev portal (archived)
├── diagnostics/                     # Diagnostic files
├── docs/                             # Canonical documentation suite (v1.2)
├── eli-backend/                      # Eli microservice backend
├── functions/                        # Legacy Azure Functions
├── infrastructure/                  # CI/CD, deployment configs, scripts
├── legacy_v3_functions/              # Legacy v3 functions (archived)
├── nova-backend/                     # Nova microservice backend
├── omega-frontend/                   # Frontend application (Next.js)
├── packs/                            # Vertical pack configurations
├── shared/                           # Legacy shared code (archived)
├── tests/                            # Test files (backend + frontend)
└── [root-level config files]         # Various config and documentation files
```

---

## 📁 DETAILED DIRECTORY BREAKDOWN

### `.cursor/` - Cursor IDE Rules
```
.cursor/
└── rules/
    └── SOLIN_SECURITY_UX_PRINCIPLES.md    # Security and UX principles for Solin
```

### `.github/` - GitHub Configuration
```
.github/
├── backend_protected_paths.yml            # Protected backend paths config
├── copilot_rules.yml                      # GitHub Copilot safety rules
└── workflows/
    ├── backend_integrity_guard.yml       # Backend integrity CI guard
    ├── dependency_freeze_guard.yml       # Dependency pinning CI guard
    ├── deploy-backend.yml                 # Backend deployment workflow
    ├── deploy.yml                         # General deployment workflow
    └── self_update_check.yml             # Self-update staging check workflow
```

### `backend/` - FastAPI Backend Application
```
backend/
├── .python-version                       # Python version: 3.11.9
├── Procfile                              # Railway process definitions
├── nixpacks.toml                         # Nixpacks build configuration
├── railway.json                          # Railway deployment config
├── requirements.txt                     # Python dependencies (pinned)
├── requirements.lock                     # Dependency lockfile
├── vercel.json                           # Vercel deployment config
│
├── app/                                  # Main application code
│   ├── main.py                           # FastAPI application entry point
│   ├── config.py                         # Application configuration
│   ├── database.py                       # Database connection management
│   ├── encryption.py                     # PII encryption utilities
│   │
│   ├── config/                           # Configuration modules
│   │   ├── omega_agents_registry.json   # Agent registry
│   │   ├── stripe_config.py             # Stripe configuration
│   │   └── twilio_config.py             # Twilio configuration
│   │
│   ├── guardians/                        # Guardian Framework
│   │   ├── __init__.py
│   │   ├── guardian_daemon.py           # Guardian daemon process
│   │   ├── guardian_manager.py           # Guardian coordination
│   │   ├── sentra_safety.py             # Safety enforcement
│   │   ├── solin_mcp.py                  # Master Control Program
│   │   └── vita_repair.py                # Automated repair
│   │
│   ├── middleware/                       # FastAPI middleware
│   │   ├── __init__.py
│   │   ├── security.py                   # Security middleware
│   │   └── tenant_context.py            # Tenant context middleware
│   │
│   ├── models/                           # Database models
│   │   ├── __init__.py
│   │   ├── archivus.py                   # Archivus model
│   │   ├── calendar.py                   # Calendar model
│   │   ├── client.py                     # Client model
│   │   ├── email.py                      # Email model
│   │   └── user.py                       # User model
│   │
│   ├── routers/                          # API route handlers
│   │   ├── __init__.py
│   │   ├── agents.py                     # Agent management endpoints
│   │   ├── auth.py                       # Authentication endpoints
│   │   ├── bookings.py                   # Booking management endpoints
│   │   ├── calendar.py                   # Calendar integration endpoints
│   │   ├── clients.py                    # Client management endpoints
│   │   ├── gmail.py                      # Gmail webhook and API
│   │   ├── health.py                     # Health check endpoints
│   │   ├── metrics.py                    # Metrics endpoints
│   │   ├── sms.py                        # SMS integration endpoints
│   │   ├── stripe.py                     # Payment processing endpoints
│   │   └── unsafe_threads.py             # Unsafe thread handling
│   │
│   ├── services/                         # Business logic services
│   │   ├── __init__.py
│   │   ├── aegis_anomaly_service.py      # Anomaly detection
│   │   ├── archivus_service.py           # Conversation archival
│   │   ├── audit_service.py              # Audit logging
│   │   ├── auth_service.py                # Authentication service
│   │   ├── booking_service.py            # Booking management
│   │   ├── calendar_service_v3.py        # Calendar integration v3
│   │   ├── claude_service.py             # Claude AI integration
│   │   ├── conversation_service.py       # Conversation management
│   │   ├── eli_service.py                # Eli microservice integration
│   │   ├── email_processor_v3.py         # Email processing pipeline v3
│   │   ├── gmail_service.py              # Gmail API integration
│   │   ├── gmail_webhook.py              # Gmail webhook handling
│   │   ├── idempotency_service.py        # Idempotency tracking
│   │   ├── retry_queue_service.py        # Retry queue management
│   │   ├── sms_service.py                # SMS integration
│   │   ├── sso_service.py                # SSO integration
│   │   ├── stripe_service.py             # Payment processing
│   │   ├── supabase_service.py           # Database operations
│   │   ├── tenant_resolution_service.py  # Tenant resolution
│   │   │
│   │   └── intelligence/                 # Intelligence modules (8 modules)
│   │       ├── __init__.py
│   │       ├── acceptance_detection.py   # Acceptance detection
│   │       ├── context_reconstruction.py # Context reconstruction
│   │       ├── coordinator_detection.py # Coordinator detection
│   │       ├── equipment_awareness.py    # Equipment awareness
│   │       ├── missing_info_detection.py # Missing info detection
│   │       ├── multi_account_email.py    # Multi-account email handling
│   │       ├── thread_history.py         # Thread history management
│   │       └── venue_intelligence.py     # Venue intelligence
│   │
│   └── workers/                          # Background workers
│       ├── __init__.py
│       ├── payment_reminder_worker.py    # Payment reminder worker
│       └── email_retry_worker.py         # Email retry queue worker
│
├── migrations/                           # Database migrations
│   ├── 001_add_email_hash.sql
│   ├── 002_add_calendar_events.sql
│   ├── 003_add_idempotency_tables.sql
│   ├── 004_performance_indexes.sql
│   ├── 005_add_unsafe_threads.sql
│   ├── 006_add_repair_log.sql
│   ├── 007_add_system_state.sql
│   ├── 008_add_v4_sso_tables.sql
│   ├── 011_archivus_schema.sql
│   ├── 012_add_bookings_table.sql
│   ├── 013_add_reminder_columns.sql
│   ├── 014_add_conversations_table.sql
│   └── 015_add_clients_email_hash.sql
│
├── scripts/                              # Utility scripts
│   ├── safety_gate_phase5.py
│   ├── startup_schema_check.py
│   └── v4_backfill_agent_profiles.py
│
├── tests/                                # Backend tests
│   ├── __init__.py
│   ├── fixtures.py
│   ├── test_acceptance_ab.py
│   ├── test_aegis_integration.py
│   ├── test_archivus_service.py
│   ├── test_calendar.py
│   ├── test_intelligence.py
│   ├── test_pipeline.py
│   ├── test_pricing_integration.py
│   ├── test_runner.py
│   ├── test_safety_gate_phase5.py
│   └── test_stripe_integration.py
│
├── credentials/                          # Service account credentials
│   ├── firestore-key.json
│   └── gmail-credentials.json
│
├── fix_email_search.py                   # Email search fix script
├── fix_email_search.bat                  # Email search fix (Windows)
└── [various .md report files]            # Progress and status reports
```

### `docs/` - Canonical Documentation Suite (v1.2)
```
docs/
├── README.md                             # Documentation index
├── VERSION.md                            # Version: 2.0 (docs are v1.2)
│
├── Core Documentation (v1.2):
│   ├── MASTER_HANDOFF.md                 # Master reference (read first)
│   ├── GILMAN_ACCORDS.md                 # Ethical and safety rules
│   ├── ARCHITECTURE_OVERVIEW.md          # System architecture
│   ├── UX_GUIDELINES.md                  # UX design standards
│   ├── ADAPTIVE_ONBOARDING.md            # Onboarding system
│   ├── PRODUCT_STRATEGY.md               # Product roadmap
│   ├── VERTICAL_PACKS.md                 # Vertical pack framework
│   │
│   ├── Autobuild Specs:
│   │   ├── BACKEND_AUTOBUILD_SPEC.md     # Backend build spec
│   │   └── FRONTEND_AUTOBUILD_SPEC.md    # Frontend build spec
│   │
│   └── Deployment:
│       └── DEPLOYMENT_PIPELINE.md         # CI/CD pipeline spec
│
├── Integrity Pack v1:
│   ├── CORE_INTEGRITY_SUMMARY.md          # Safety systems overview
│   ├── SAFETY_CONTRACT.md                # Human-AI agreement
│   ├── AUTO_FIX_POLICY_REPORT.md         # Solin auto-fix levels
│   ├── COPILOT_SAFETY_MATRIX.md          # Copilot zone rules
│   ├── WORKFLOW_PROTECTION_MAP.md        # CI workflow mapping
│   ├── SELF_UPDATE_RISK_MODEL.md         # Risk assessment model
│   ├── BACKEND_INTEGRITY_POLICY.md       # Backend protection
│   ├── PYTHON_DEPENDENCY_POLICY.md       # Dependency management
│   ├── SELF_UPDATE_POLICY.md             # Self-update flow
│   └── SOLIN_AUTOFIX_POLICY_V2.md        # Solin auto-fix policy
│
├── reports/                              # Status and progress reports
│   ├── DOCUMENTATION_INDEX.md
│   ├── GITHUB_UPLOAD_REPORT.md
│   ├── QUICK_STATUS_REPORT.md
│   ├── SESSION_REPORT.md
│   ├── FINAL_VERIFICATION_REPORT.md
│   ├── REBUILD_STATUS_REPORT.md
│   ├── REBUILD_VERIFICATION_REPORT.md
│   ├── INCIDENT_RECOVERY_REPORT.md
│   ├── SANITY_CHECK_REPORT.md
│   ├── MAYA_V3_IMPLEMENTATION_COMPLETE.md
│   ├── CLAUDE_HANDOFF_FOR_SOLIN.md
│   ├── FINAL_CLAUDE_REFINEMENT_FOR_SOLIN.md
│   ├── FINAL_CLAUDE_REFINEMENT_FOR_SOLIN_v2.md
│   ├── AZURE_CLI_SETUP.md
│   ├── README_AZURE_FUNCTIONS.md
│   ├── DEPLOYMENT_GUIDE.md
│   ├── ENVIRONMENT_VARIABLES.md
│   ├── QUICK_SEARCH_GUIDE.md
│   │
│   ├── phase-completion/                 # Phase completion reports
│   │   ├── PHASE_1_WEEK_1_COMPLETE.md
│   │   ├── PHASE_1_WEEK_2_COMPLETE.md
│   │   ├── PHASE_1_WEEK_3_COMPLETE.md
│   │   ├── PHASE_2_WEEK_1_COMPLETE.md
│   │   ├── PHASE_2_WEEK_2_COMPLETE.md
│   │   ├── PHASE_3_COMPLETE.md
│   │   ├── PHASE_3_WEEK_1_COMPLETE.md
│   │   ├── PHASE_3_WEEK_2_COMPLETE.md
│   │   └── PHASE_4_COMPLETE.md
│   │
│   └── verification/                     # Verification reports
│       ├── HONEST_VERIFICATION.md
│       └── PHASE_0_VERIFICATION.md
│
├── roadmaps/                             # Product roadmaps
│   ├── ROADMAP_OVERVIEW.md               # Overall roadmap structure
│   ├── POSTPONED_FEATURES.md             # Features postponed from v1.2
│   └── REINTRODUCTION_PLAN.md            # Plan for reintroducing features
│
├── archive/                               # Superseded documentation
│   ├── MASTER_REFERENCE_DOCUMENT.md
│   └── OMEGA_OVERVIEW.md
│
└── notes/                                 # Miscellaneous notes
    └── ICONS_NEEDED.md
```

### `infrastructure/` - CI/CD and Deployment
```
infrastructure/
├── LAST_PROD_DEPLOY.json                 # Production deployment tracking
├── Procfile                               # Process definitions
├── nixpacks.toml                         # Nixpacks config
├── railway.json                           # Railway config
├── vercel-backend.json                    # Vercel backend config
├── azure-functions-host.json             # Azure Functions host config
├── azure-functions-local.settings.json   # Azure Functions local settings
│
├── scripts/                               # Deployment and setup scripts
│   ├── complete_setup.sh                 # Complete setup script
│   ├── fix_github_secrets.sh             # GitHub secrets fix
│   ├── generate_env_template.ps1         # Environment template generator (PowerShell)
│   ├── migrate_to_v4.sh                  # Migration script
│   ├── set_github_secrets.ps1            # Set GitHub secrets (PowerShell)
│   ├── set_railway_env.ps1               # Railway env setup (PowerShell)
│   ├── set_railway_env.sh                # Railway env setup (Bash)
│   ├── setup_maya_rbac.sh                # RBAC setup
│   └── setup_patch_runners_unistring.py  # Patch runner setup
│
└── archive/                               # Archived legacy code
    ├── azure-functions/                   # Legacy Azure Functions
    ├── frontend/                          # Legacy frontend code
    └── shared/                            # Legacy shared code
```

### `packs/` - Vertical Pack Configurations
```
packs/
├── beauty/                               # Beauty pack (Priority 1)
├── events/                               # Events pack (Priority 2)
├── fitness/                              # Fitness pack (future)
└── wellness/                             # Wellness pack (future)
```

### `tests/` - Test Files
```
tests/
├── backend/
│   └── tests/                            # Backend test files
│       ├── __init__.py
│       ├── fixtures.py
│       ├── test_acceptance_ab.py
│       ├── test_aegis_integration.py
│       ├── test_archivus_service.py
│       ├── test_calendar.py
│       ├── test_intelligence.py
│       ├── test_pipeline.py
│       ├── test_pricing_integration.py
│       ├── test_runner.py
│       ├── test_safety_gate_phase5.py
│       └── test_stripe_integration.py
└── frontend/                             # Frontend tests (empty)
```

### `cursor/` - Cursor Rules
```
cursor/
├── RUN_ORDER.md                           # Cursor execution order
└── rules/                                 # Cursor behavior rules
    ├── base.md                            # Base rules
    ├── safety.md                          # Safety rules
    ├── architecture.md                    # Architecture constraints
    ├── execution.md                       # Execution standards
    └── VERSION_SELECTOR.md                # Version detection rules
```

---

## 📄 ROOT-LEVEL FILES

### Configuration Files
- `.gitignore` - Git ignore rules
- `.env` - Environment variables (local, not committed)
- `package.json` - Node.js dependencies (legacy)
- `package-lock.json` - Node.js lockfile
- `host.json` - Azure Functions host config
- `local.settings.json` - Azure Functions local settings

### Documentation Files (Root Level)
- `README.md` - Project README
- `CLAUDE_DESKTOP_ANALYSIS_REPORT.md` - Claude analysis
- `SOLIN_HANDOFF_2025-11-21.md` - Solin handoff document
- `FEATURE_IMPLEMENTATION_ANALYSIS.md` - Feature analysis
- `FULL_RECONCILIATION_REPORT.md` - Reconciliation report
- `MAYA_DEEP_SCAN_HANDOFF.md` - Deep scan handoff
- `DOCUMENTATION_INDEX.md` - Documentation index
- `GITHUB_UPLOAD_REPORT.md` - GitHub upload report
- `QUICK_STATUS_REPORT.md` - Quick status
- `SESSION_REPORT.md` - Session report
- `REPO_RESTRUCTURE_PLAN.md` - Restructure plan

### Phase Reports (Root Level)
- `PHASE_0_COMPLETE_REPORT.md`
- `PHASE_0_EXECUTION_PLAN.md`
- `PHASE_0_EXECUTION_RESULTS.md`
- `PHASE_0_SQL_PREVIEW.md`
- `PHASE_0_VALIDATION_REPORT.md`
- `PHASE_0-2_COMPLETE_SUMMARY.md`
- `PHASE_0B_TEST_PLAN.md`
- `PHASE_1_TEST_VALIDATION_REPORT.md`
- `PHASE_2_DEPLOYMENT_READINESS_REPORT.md`
- `PHASE_2B_DEPLOYMENT_GUIDE.md`
- `PHASE_2B_DEPLOYMENT_READY.md`
- `RAILWAY_DEPLOYMENT_CHECKLIST.md`
- `SET_ENV_VARIABLES_GUIDE.md`
- `BACKEND_ENVIRONMENT_VARIABLES_REQUIRED.md`

### Scripts (Root Level)
- `complete_setup.sh` - Setup script
- `fix_github_secrets.sh` - GitHub secrets fix
- `migrate_to_v4.sh` - Migration script
- `set_github_secrets.ps1` - PowerShell secrets script
- `setup_maya_rbac.sh` - RBAC setup
- `setup_patch_runners_unistring.py` - Patch runner setup
- `scan_frontend.py` - Frontend scanner
- `deep_scan.py` - Deep scan script
- `DEEP_SCAN_FOR_CLAUDE_DESKTOP.py` - Claude desktop scan

### Legacy/Archived Directories
- `api/` - Legacy Azure Functions API
- `dashboard/` - Legacy dashboard frontend
- `dev-portal/` - Legacy dev portal
- `deploy_tmp/` - Temporary deployment files
- `functions/` - Legacy Azure Functions
- `legacy_v3_functions/` - Legacy v3 functions
- `shared/` - Legacy shared code
- `eli-backend/` - Eli microservice (separate)
- `nova-backend/` - Nova microservice (separate)
- `omega-frontend/` - Frontend application (Next.js)

---

## 🔑 KEY FILES SUMMARY

### Backend Core
- `backend/app/main.py` - FastAPI entry point
- `backend/app/config.py` - Configuration
- `backend/app/database.py` - Database connection
- `backend/app/encryption.py` - PII encryption
- `backend/requirements.txt` - Python dependencies (pinned)
- `backend/requirements.lock` - Dependency lockfile
- `backend/Procfile` - Railway process definitions
- `backend/railway.json` - Railway deployment config
- `backend/nixpacks.toml` - Build configuration

### Documentation (Canonical v1.2)
- `docs/MASTER_HANDOFF.md` - **READ FIRST** - Master reference
- `docs/GILMAN_ACCORDS.md` - Safety and ethics rules
- `docs/CORE_INTEGRITY_SUMMARY.md` - Integrity Pack overview
- `docs/SAFETY_CONTRACT.md` - Human-AI agreement
- `docs/BACKEND_INTEGRITY_POLICY.md` - Backend protection rules
- `docs/PYTHON_DEPENDENCY_POLICY.md` - Dependency management
- `docs/SELF_UPDATE_POLICY.md` - Self-update flow

### CI/CD and Safety
- `.github/workflows/backend_integrity_guard.yml` - Backend protection
- `.github/workflows/dependency_freeze_guard.yml` - Dependency protection
- `.github/workflows/self_update_check.yml` - Self-update checks
- `.github/backend_protected_paths.yml` - Protected paths config
- `.github/copilot_rules.yml` - Copilot safety rules

### Infrastructure
- `infrastructure/LAST_PROD_DEPLOY.json` - Production tracking
- `infrastructure/scripts/` - Deployment scripts
- `infrastructure/.env.railway.template` - Railway env template

---

## 📊 STATISTICS

### Backend
- **Routers:** 11 API route handlers
- **Services:** 29 service modules
- **Intelligence Modules:** 8 modules
- **Workers:** 2 background workers
- **Guardian Modules:** 5 modules
- **Migrations:** 13 SQL migration files
- **Tests:** 12 test files

### Documentation
- **Core Docs:** 10 v1.2 specification files
- **Integrity Pack:** 10 safety and integrity documents
- **Reports:** 20+ status and progress reports
- **Roadmaps:** 3 roadmap planning documents

### CI/CD
- **Workflows:** 5 GitHub Actions workflows
- **Config Files:** 3 protection/config YAML files
- **Scripts:** 9 deployment and setup scripts

---

## 🎯 QUICK REFERENCE

**Start Here:**
1. `docs/MASTER_HANDOFF.md` - System overview
2. `docs/CORE_INTEGRITY_SUMMARY.md` - Safety systems map
3. `docs/README.md` - Documentation index

**Backend Entry Point:**
- `backend/app/main.py`

**Deployment Configs:**
- `backend/railway.json` - Railway deployment
- `backend/nixpacks.toml` - Build configuration
- `backend/Procfile` - Process definitions

**Safety & Integrity:**
- `docs/SAFETY_CONTRACT.md` - Human-AI agreement
- `.github/copilot_rules.yml` - Copilot rules
- `.cursor/rules/` - Cursor behavior rules

---

**END OF FILE STRUCTURE DOCUMENT**

