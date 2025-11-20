# OMEGA CORE v3.0 — SYSTEM OVERVIEW
**Comprehensive System Documentation for Frontend Development & Agent Review**

**Version:** 3.0.1  
**Last Updated:** December 19, 2024  
**Status:** Production-Ready (Phase 11 Complete)  
**Document Purpose:** Frontend integration guide, agent review, operational status

---

## 📋 TABLE OF CONTENTS

1. [Executive Summary](#executive-summary)
2. [System Architecture](#system-architecture)
3. [Agent Roster & Roles](#agent-roster--roles)
4. [File Structure](#file-structure)
5. [API Endpoints](#api-endpoints)
6. [Database Schema](#database-schema)
7. [Security Features](#security-features)
8. [Operational Status](#operational-status)
9. [Integration Points](#integration-points)
10. [Frontend Requirements](#frontend-requirements)
11. [Change Log](#change-log)

---

## 🎯 EXECUTIVE SUMMARY

**OMEGA Core v3.0** is a multi-agent AI operations system for Skinny Man Entertainment (SME) and Level Three LLC (L3). It coordinates 10 specialized AI agents to provide:

**Architecture Note:** The system uses a two-layer safety architecture: the **MCP Orchestration Layer** (Solin MCP) provides global control and Safe Mode activation, while the **Guardian Layer** (Sentra, Vita, Aegis) enforces runtime safety, automated repair, and security monitoring. Solin orchestrates all agents and coordinates guardian actions.

- **Client Communication** (Maya) - Email processing, booking intelligence, automated responses
- **Financial Operations** (Nova) - Pricing, invoicing, cost analysis
- **Market Intelligence** (Eli) - Venue research, equipment awareness
- **Scheduling & Logistics** (Rho) - Calendar management, conflict detection
- **Marketing & Social** (Vee) - Content generation (B-Mode trial, draft-only)
- **Long-Term Memory** (Archivus) - Pattern storage, client/venue profiles
- **Safety & Security** (Sentra, Aegis) - Runtime safety enforcement, threat detection
- **System Repair** (Vita) - Automated error recovery, self-healing
- **Orchestration** (Solin MCP) - Master control, Safe Mode, guardian coordination

**Current Status:**
- ✅ Phase 1-5: Complete (Security, Calendar, Idempotency, Testing, Hardening)
- ✅ Phase 6-10: Complete (Guardian Framework, Safety Gate, Monitoring)
- ✅ Phase 11: Complete (Archivus Memory Engine)
- ⏳ Phase 12-15: In Progress (Aegis Intelligence, Vee B-Mode, Infrastructure)

**Production Readiness:** ✅ READY (with ongoing enhancements)

---

## 🏗️ SYSTEM ARCHITECTURE

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    OMEGA CORE v3.0                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────┐ │
│  │   Solin MCP  │◄─────►│   Sentra     │◄─────►│  Aegis   │ │
│  │ (Orchestrator)│      │  (Safety)    │      │(Security)│ │
│  └──────┬───────┘      └──────────────┘      └──────────┘ │
│         │                    │                    │         │
│         │         ┌──────────▼──────────┐        │         │
│         │         │ Guardian Daemon      │        │         │
│         │         │ (30-min monitoring)  │        │         │
│         │         └──────────────────────┘        │         │
│         │                                                 │
│  ┌──────▼───────┐      ┌──────────────┐      ┌──────────┐ │
│  │     Maya     │◄─────►│     Nova     │      │   Vita   │ │
│  │  (Email AI)  │      │  (Pricing)    │      │ (Repair) │ │
│  └──────┬───────┘      └──────────────┘      └────┬─────┘ │
│         │                                         │         │
│         │              ┌──────────▼──────────┐    │         │
│         │              │   Retry Queue       │    │         │
│         │              │   (Worker)          │    │         │
│         │              └─────────────────────┘    │         │
│         │                                                 │
│         │                                                 │
│  ┌──────▼───────┐      ┌──────────────┐      ┌──────────┐ │
│  │     Eli      │      │     Rho      │      │ Archivus │ │
│  │  (Venue)     │      │  (Calendar)  │      │ (Memory) │ │
│  └──────────────┘      └──────────────┘      └──────────┘ │
│                                                             │
│  ┌──────────────┐                                          │
│  │     Vee      │                                          │
│  │ (Marketing)  │  [B-Mode: Draft-Only, 90-Day Trial]      │
│  └──────────────┘                                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│              PostgreSQL / Supabase Database                 │
│  - Multi-tenant with Row-Level Security (RLS)                │
│  - AES-256 encryption for PII                                 │
│  - Comprehensive audit logging                               │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

**Backend:**
- **Framework:** FastAPI (Python 3.14)
- **Database:** PostgreSQL (via Supabase)
- **AI:** Anthropic Claude Sonnet 4
- **Authentication:** JWT (HS256)
- **Encryption:** AES-256 (Fernet)
- **Rate Limiting:** SlowAPI
- **Deployment:** Railway (Nixpacks)

**External APIs:**
- **Gmail API:** OAuth 2.0, Pub/Sub webhooks
- **Google Calendar API:** OAuth 2.0, event sync
- **Nova API:** Pricing and invoicing (`nova_api_url`)
- **Eli API:** Venue intelligence (`eli_api_url`)

---

## 🤖 AGENT ROSTER & ROLES

### Agent Categories

| Category      | Agents          | Description                |
| ------------- | --------------- | -------------------------- |
| Orchestration | Solin           | Global control + Safe Mode |
| Safety        | Sentra, Aegis   | Enforcement + intelligence |
| Reliability   | Vita            | Automated repair           |
| Ops           | Maya, Rho, Nova | Email, scheduling, finance |
| Intelligence  | Eli, Archivus   | Venue + Memory             |
| Marketing     | Vee             | Draft-only                 |

### Agent Registry
**Location:** `app/config/omega_agents_registry.json`

### 1. Solin Arden — Master Control Program (MCP)
**ID:** `solin_mcp`  
**Category:** Orchestration  
**Status:** ✅ Fully Operational

**Responsibilities:**
- Orchestrates all agent actions and communications
- Monitors Guardian Framework (Sentra, Vita, Aegis)
- Activates/deactivates Safe Mode based on thresholds
- Routes events between agents
- Escalates severe safety issues
- Notifies admins (email/Discord) on critical events

**Key Methods:**
- `observe_guardians()` - Monitor guardian health
- `enforce_global_rules()` - Apply safety thresholds
- `mcp_health_check()` - System health assessment
- `activate_safe_mode(reason)` - Freeze system operations
- `deactivate_safe_mode(reason)` - Resume operations
- `receive_event(action, metadata)` - Process audit events

**Safe Mode Behavior:**
- Freezes email processing (read-only, no sends)
- Freezes calendar writes
- Freezes Vee content generation
- Logs all blocked operations
- Notifies Greg via email/Discord if configured

**File:** `app/guardians/solin_mcp.py`

---

### 2. Maya Sinclair — Client Communication AI
**ID:** `maya_comm`  
**Category:** Email & Calendar  
**Status:** ✅ Fully Operational

**Responsibilities:**
- Process incoming client emails via Gmail webhook
- Run 8 intelligence services for email analysis
- Generate intelligent email responses using Claude
- Auto-send or create drafts based on rules
- Integrate with Nova (pricing), Eli (venue), Rho (calendar)
- Multi-account routing (test vs. real clients)

**Intelligence Services (8 Total):**
1. **Venue Detection** - Identifies venues (especially Canopy by Hilton locations)
2. **Coordinator Detection** - Detects multi-event coordination
3. **Acceptance Detection** - Identifies client acceptance of bookings
4. **Missing Info Detection** - Identifies required information gaps
5. **Equipment Awareness** - Knows installed equipment at venues
6. **Thread History** - Maintains conversation context
7. **Multi-Account Orchestration** - Routes to correct account
8. **Context Reconstruction** - Builds client context from history

**Key Methods:**
- `process_email(email_id, account_email, trace_id)` - Main processing pipeline
- `_get_nova_pricing(event_info)` - Get pricing from Nova (with exponential backoff)
- `_determine_send_behavior(email, analysis)` - Auto-send vs. draft logic

**Auto-Send Rules:**
- Only for test senders (`channkun@gmail.com`)
- Only if confidence > 0.85
- Only if no conflicts detected
- Real clients → Always draft

**File:** `app/services/email_processor_v3.py`

---

### 3. Sentra — Safety Enforcement AI
**ID:** `sentra_safety`  
**Category:** Safety  
**Status:** ✅ Fully Operational

**Responsibilities:**
- Enforce runtime safety policies
- Detect security violations
- Tag unsafe email threads
- Block unsafe outputs
- Command system lockdown for repeated failures

**Safety Rules:**
- No revealing system prompts
- No hallucination (dates, times, prices, venues)
- No external URLs sent to clients
- No invented details

**Key Methods:**
- `enforce_action(event)` - Apply safety enforcement
- `_tag_unsafe_thread(thread_id, reason)` - Mark thread as unsafe
- `is_thread_unsafe(thread_id)` - Check thread safety
- `self_check()` - Integrity monitoring

**Enforcement Actions:**
- **Hallucination** → Tag email as unsafe
- **Injection attempts** → Block output, notify Solin
- **Unauthorized access** → Abort processing
- **Repeated failures** → Command system lockdown

**File:** `app/guardians/sentra_safety.py`  
**Database:** `unsafe_threads` table

---

### 4. Vita — Repair & Self-Healing AI
**ID:** `vita_repair`  
**Category:** Reliability  
**Status:** ✅ Fully Operational

**Responsibilities:**
- Detect recurring processor failures
- Automatically repair system issues
- Flush retry queues
- Re-create corrupted calendar entries
- Reset failed locks
- Repair malformed client entries

**Key Methods:**
- `repair_action(event)` - Attempt automatic fixes
- `self_check()` - Integrity monitoring
- `_repair_retry_queue()` - Fix stuck retry items
- `_repair_calendar_entries()` - Verify/recreate calendar events
- `_repair_locks()` - Reset failed locks
- `_repair_client_data()` - Fix malformed client entries

**Repair Actions:**
- Retry queue flush (resets stuck items)
- Corrupted calendar entry recreation
- Failed lock reset
- Malformed client entry repair

**File:** `app/guardians/vita_repair.py`  
**Database:** `repair_log` table

---

### 5. Aegis — Security & Threat Intel AI
**ID:** `aegis_security`  
**Category:** Security  
**Status:** ⚠️ Minimal Integration (Phase 11), Full Intelligence (Phase 12 - In Progress)

**Current Implementation:**
- ✅ Minimal integration: `record_safety_event()` method
- ✅ Light-touch integration in email processor
- ✅ Fail-open design (never blocks core pipeline)
- ⏳ Full intelligence engine (Phase 12)

**Responsibilities (Current):**
- Record safety events to audit log
- Monitor audit logs (read-only)
- Tag records with safety flags

**Responsibilities (Phase 12 - Planned):**
- Compute tenant risk snapshots
- Detect anomalies (24h vs. 7-day averages)
- Summarize security status for Solin
- Feed alerts to Safe Mode triggers

**Key Methods (Current):**
- `record_safety_event(action, context, metadata)` - Log safety events
- `analyze_recent_activity()` - Stub (Phase 12)
- `flag_anomaly()` - Stub (Phase 12)

**File:** `app/services/aegis_service.py`

**⚠️ Risk Warning:** Aegis will soon be running anomaly detection (Phase 12). When fully operational, it will monitor all system activity and may trigger Safe Mode based on security risk assessments. Frontend should be prepared to handle Aegis-triggered Safe Mode events.

---

### 6. Archivus — Memory & Knowledge AI
**ID:** `archivus_memory`  
**Category:** Memory  
**Status:** ✅ Fully Operational (Phase 11 Complete)

**Responsibilities:**
- Store long-term patterns and trends
- Maintain client and venue profiles
- Summarize email threads
- Store system evolution notes
- Provide historical context to other agents

**Key Methods:**
- `record_thread_summary(thread_id, raw_email_body, structured_context)` - Summarize threads using Claude
- `get_client_profile(client_id)` - Aggregate client memories
- `get_venue_profile(venue_name)` - Aggregate venue memories
- `record_system_note(note, source)` - Store system-level notes

**Memory Types:**
- `client_profile` - Client information and preferences
- `venue_profile` - Venue information and history
- `thread_summary` - Email thread summaries
- `system_note` - System evolution and guardian notes

**File:** `app/services/archivus_service.py`  
**Database:** `archivus_threads`, `archivus_memories` tables

---

### 7. Nova Arden — Pricing & Finance AI
**ID:** `nova_pricing`  
**Category:** Finance  
**Status:** ✅ Integrated (External API)

**Responsibilities:**
- Calculate pricing for events
- Generate quotes and invoices
- Provide cost/margin guidance
- Support invoice creation

**Integration:**
- **API Endpoint:** `{nova_api_url}/api/pricing/calculate`
- **Method:** HTTP POST with event details
- **Retry Strategy:** Exponential backoff (200ms, 1s, 2s, 5s)
- **Fallback:** Graceful failure (no fake pricing)

**Usage:**
- Called by Maya after acceptance detection
- Only if all required info available
- Only if not multiple events (coordinator detection)

**File:** Referenced in `app/services/email_processor_v3.py`  
**Config:** `nova_api_url` in `app/config.py`

---

### 8. Eli Voss — Venue Intelligence AI
**ID:** `eli_venue`  
**Category:** Research  
**Status:** ✅ Integrated (External API + Local Fallback)

**Responsibilities:**
- Research venue locations and details
- Provide equipment awareness
- Return install history
- Support venue-specific questions

**Integration:**
- **API Endpoint:** `{eli_api_url}/research/venue`
- **Fallback:** Local Canopy database in `VenueIntelligenceService`
- **Usage:** Called by Maya when venue keywords detected

**File:** `app/services/intelligence/venue_intelligence.py`  
**Config:** `eli_api_url` in `app/config.py`

---

### 9. Rho Quinn — Event Scheduling & Logistics
**ID:** `rho_events`  
**Category:** Operations  
**Status:** ✅ Fully Operational (via Calendar Service)

**Responsibilities:**
- Normalize date/time, timezone, durations
- Verify travel constraints and changeovers
- Flag scheduling conflicts beyond pure Calendar overlaps
- Manage calendar event CRUD operations

**Implementation:**
- Integrated via `CalendarServiceV3`
- Conflict detection before auto-send
- Auto-block on acceptance (if no conflicts)
- Timezone support per tenant

**Key Methods:**
- `detect_conflicts(start_time, end_time)` - Check for overlapping events
- `auto_block_for_confirmed_gig(...)` - Create calendar block
- `create_event(...)` - Create calendar event
- `delete_event(event_id)` - Delete calendar event
- `list_events(start_date, end_date)` - List events in range

**File:** `app/services/calendar_service_v3.py`

---

### 10. Vee Moreno — Marketing & Social Engagement AI
**ID:** `vee_marketing`  
**Category:** Marketing  
**Status:** ⏳ Design Only (Phase 13 - In Progress)

**Current Status:**
- ✅ Design specification complete (`docs/vee_moreno_trial_spec.md`)
- ⏳ Database schema (Phase 13.1)
- ⏳ Service implementation (Phase 13.2)
- ⏳ API endpoints (Phase 13.3)

**B-Mode (90-Day Trial) - ACTIVE NOW:**
- ✅ Generate content drafts only
- ✅ Store drafts in content queue
- ✅ Propose calendar schedules
- ❌ No auto-posting
- ❌ No external API calls
- ❌ No publishing

**C-Mode (Post-Trial, Future):**
- ⏳ Requires 90-day successful B-Mode trial
- ⏳ Automated approval and publishing
- ⏳ API integrations enabled

**File:** Design spec in `docs/vee_moreno_trial_spec.md`

---

## 📁 FILE STRUCTURE

### Root Directory (24 files - Clean)
```
backend/
├── app/                    # Core application code
│   ├── config/             # Configuration files
│   │   └── omega_agents_registry.json
│   ├── guardians/          # Guardian Framework
│   │   ├── solin_mcp.py
│   │   ├── sentra_safety.py
│   │   ├── vita_repair.py
│   │   ├── guardian_manager.py
│   │   └── guardian_daemon.py
│   ├── middleware/         # Security middleware
│   │   └── security.py
│   ├── models/             # Data models
│   │   ├── database.py
│   │   ├── email.py
│   │   └── archivus.py
│   ├── routers/            # API endpoints
│   │   ├── gmail.py
│   │   ├── calendar.py
│   │   ├── clients.py
│   │   └── health.py
│   ├── services/           # Business logic
│   │   ├── intelligence/   # 8 intelligence modules
│   │   ├── email_processor_v3.py
│   │   ├── calendar_service_v3.py
│   │   ├── claude_service.py
│   │   ├── gmail_service.py
│   │   ├── gmail_webhook.py
│   │   ├── audit_service.py
│   │   ├── archivus_service.py
│   │   ├── aegis_service.py
│   │   └── [other services]
│   ├── utils/              # Utilities
│   ├── config.py           # Settings
│   ├── database.py         # DB connection
│   ├── encryption.py       # AES-256 encryption
│   └── main.py             # FastAPI app
│
├── archive/                # Legacy code (for A/B testing)
│   └── services/
│       ├── email_processor.py (v2)
│       ├── calendar_service.py (v1)
│       └── firestore_service.py
│
├── docs/                   # Documentation
│   ├── specs/              # Specifications
│   │   ├── omega_core_v3_spec.md
│   │   ├── aegis_agent_spec.md
│   │   ├── archivus_aegis_routing.md
│   │   └── vee_moreno_trial_spec.md
│   └── reports/            # Completion reports (25+ files)
│
├── migrations/             # Database migrations
│   ├── 001_add_email_hash.sql
│   ├── 003_add_idempotency_tables.sql
│   ├── 004_performance_indexes.sql
│   ├── 005_add_unsafe_threads.sql
│   ├── 006_add_repair_log.sql
│   ├── 007_add_system_state.sql
│   └── 011_archivus_schema.sql
│
├── scripts/                # Scripts
│   ├── dev/                # Development utilities (26 files)
│   └── deployment/        # Deployment scripts
│
├── tests/                  # Test suite
│   ├── test_pipeline.py
│   ├── test_acceptance_ab.py
│   ├── test_intelligence.py
│   ├── test_calendar.py
│   ├── test_pricing_integration.py
│   ├── test_aegis_integration.py
│   ├── test_archivus_service.py
│   ├── test_safety_gate_phase5.py
│   └── fixtures.py
│
├── test_data/              # Test fixtures/data
│
├── reports/                # Final reports
│   └── maya_v3_final_report.md
│
├── requirements.txt        # Python dependencies
├── nixpacks.toml          # Railway build config
├── Procfile               # Process file
└── OMEGA_OVERVIEW.md      # This file
```

**Note:** The frontend repository is separate (`frontend/` directory or separate repo). This backend provides API endpoints for frontend integration.

### Key Directories

**`app/services/intelligence/`** - 8 Intelligence Modules:
1. `venue_intelligence.py` - Venue detection
2. `coordinator_detection.py` - Multi-event detection
3. `acceptance_detection.py` - Acceptance detection
4. `missing_info_detection.py` - Missing info detection
5. `equipment_awareness.py` - Equipment awareness
6. `thread_history.py` - Thread context
7. `multi_account_email.py` - Account routing
8. `context_reconstruction.py` - Client context

**`app/guardians/`** - Guardian Framework:
- `solin_mcp.py` - Master Control Program
- `sentra_safety.py` - Safety enforcement
- `vita_repair.py` - Automated repair
- `guardian_manager.py` - Event routing
- `guardian_daemon.py` - Background monitoring

---

## 🔌 API ENDPOINTS

### Base URL
- **Production:** `https://maya-ai-production.up.railway.app`
- **Staging:** `https://maya-ai-staging.up.railway.app`
- **Local:** `http://localhost:8000`

### Authentication
**Current:** Tenant-based (via `default_tenant_id` in config)  
**Future:** JWT tokens (planned)

### Rate Limiting
- **Default:** 100 requests/minute per IP
- **Webhook:** 100 requests/minute
- **Calendar:** 50-100 requests/minute (varies by endpoint)
- **Custom 429 Handler:** Returns `Retry-After` header

---

### Gmail Endpoints

#### `POST /api/gmail/webhook`
**Purpose:** Receive Gmail Pub/Sub push notifications

**Security:**
- Full Google JWT verification (issuer, audience, signature, expiration)
- SHA256 fingerprinting (replay prevention)
- Database locking (race condition prevention)
- Rate limited: 100/minute

**Request:**
- Google Pub/Sub message format
- JWT token in `Authorization` header

**Response:**
- `200 OK` - Message processed
- `401 Unauthorized` - Invalid JWT
- `400 Bad Request` - Invalid message format
- `409 Conflict` - Replay detected or lock failed

**Flow:**
1. Verify JWT token
2. Parse Pub/Sub message
3. Check fingerprint (replay detection)
4. Acquire lock on `gmail_message_id`
5. Store email in database
6. Trigger email processing
7. Release lock
8. All steps audit logged

**File:** `app/routers/gmail.py`

---

#### `POST /api/gmail/watch`
**Purpose:** Set up Gmail watch subscription

**Request Body:**
```json
{
  "account_email": "maya@skinnymanmusic.com",
  "topic": "projects/PROJECT/topics/TOPIC"
}
```

**Response:**
```json
{
  "status": "success",
  "expiration": "2024-12-20T12:00:00Z",
  "history_id": "12345"
}
```

**File:** `app/routers/gmail.py`

---

### Calendar Endpoints

#### `GET /api/calendar/events`
**Purpose:** List calendar events with optional date range

**Query Parameters:**
- `start_date` (optional) - ISO format date
- `end_date` (optional) - ISO format date
- `limit` (default: 100, max: 1000)
- `offset` (default: 0)

**Response:**
```json
{
  "status": "success",
  "count": 10,
  "events": [
    {
      "id": "uuid",
      "title": "SME Booking — Client Name",
      "start_time": "2024-12-20T18:00:00Z",
      "end_time": "2024-12-20T22:00:00Z",
      "location": "Venue Name",
      "client_id": "uuid",
      "google_event_id": "google_event_id",
      "tenant_id": "uuid",
      "created_at": "2024-12-19T12:00:00Z",
      "updated_at": "2024-12-19T12:00:00Z"
    }
  ]
}
```

**Rate Limit:** 100/minute

**File:** `app/routers/calendar.py`

---

#### `POST /api/calendar/events`
**Purpose:** Create calendar event

**Request Body:**
```json
{
  "title": "Event Title",
  "start_time": "2024-12-20T18:00:00Z",
  "end_time": "2024-12-20T22:00:00Z",
  "location": "Venue Name",
  "description": "Event description",
  "client_id": "uuid"
}
```

**Response:**
```json
{
  "status": "success",
  "event_id": "uuid",
  "google_event_id": "google_event_id",
  "tenant_id": "uuid",
  "created_at": "2024-12-19T12:00:00Z",
  "updated_at": "2024-12-19T12:00:00Z"
}
```

**Rate Limit:** 50/minute

**File:** `app/routers/calendar.py`

---

#### `POST /api/calendar/block`
**Purpose:** Auto-block time for confirmed booking

**Request Body:**
```json
{
  "event_date": "2024-12-20T18:00:00Z",
  "event_type": "wedding",
  "client_name": "Client Name",
  "duration_hours": 6.0,
  "location": "Venue Name",
  "venue": "Venue Name",
  "context": "Auto-blocked from email acceptance",
  "client_id": "uuid"
}
```

**Response:**
```json
{
  "status": "success",
  "event_id": "uuid",
  "google_event_id": "google_event_id",
  "tenant_id": "uuid",
  "created_at": "2024-12-19T12:00:00Z",
  "updated_at": "2024-12-19T12:00:00Z",
  "message": "Calendar block created"
}
```

**Special Behavior:**
- Title format: `"SME Booking — {Client Name}"`
- Color: 4 (red)
- Includes venue, time, context in description
- Respects tenant timezone
- Checks for conflicts before creating

**Rate Limit:** 50/minute

**File:** `app/routers/calendar.py`

---

#### `GET /api/calendar/availability`
**Purpose:** Check calendar availability for time window

**Query Parameters:**
- `start_time` (required) - ISO format datetime
- `end_time` (required) - ISO format datetime

**Response:**
```json
{
  "available": true,
  "has_conflict": false,
  "conflict_count": 0,
  "conflicts": []
}
```

**Rate Limit:** 100/minute

**File:** `app/routers/calendar.py`

---

#### `DELETE /api/calendar/event/{event_id}`
**Purpose:** Delete calendar event

**Response:**
```json
{
  "status": "success",
  "message": "Event deleted"
}
```

**Rate Limit:** 50/minute

**File:** `app/routers/calendar.py`

---

### Client Endpoints

#### `POST /api/clients/`
**Purpose:** Create new client

**Request Body:**
```json
{
  "name": "Client Name",
  "email": "client@example.com",
  "phone": "+1234567890",
  "company": "Company Name"
}
```

**Response:**
```json
{
  "id": "uuid",
  "name": "Client Name",
  "email_hash": "sha256_hash",
  "created_at": "2024-12-19T12:00:00Z"
}
```

**Security:**
- Email is hashed (SHA256) before storage
- PII is encrypted (AES-256) before storage
- RLS enforced (tenant isolation)

**File:** `app/routers/clients.py`

---

#### `GET /api/clients/{client_id}`
**Purpose:** Get client by ID

**Response:**
```json
{
  "id": "uuid",
  "name": "Client Name",
  "email_hash": "sha256_hash",
  "last_contact_at": "2024-12-19T12:00:00Z"
}
```

**File:** `app/routers/clients.py`

---

#### `GET /api/clients/`
**Purpose:** List clients with pagination

**Query Parameters:**
- `limit` (default: 50, max: 1000)
- `offset` (default: 0)

**Response:**
```json
{
  "items": [...],
  "total": 100,
  "limit": 50,
  "offset": 0
}
```

**File:** `app/routers/clients.py`

---

#### `GET /api/clients/search/by-email/`
**Purpose:** Search client by email (hashed lookup)

**Query Parameters:**
- `email` (required)

**Response:**
```json
{
  "id": "uuid",
  "name": "Client Name",
  "email_hash": "sha256_hash"
}
```

**File:** `app/routers/clients.py`

---

#### `PUT /api/clients/{client_id}`
**Purpose:** Update client

**Request Body:**
```json
{
  "name": "Updated Name",
  "phone": "+1234567890"
}
```

**Response:**
```json
{
  "id": "uuid",
  "name": "Updated Name",
  "updated_at": "2024-12-19T12:00:00Z"
}
```

**File:** `app/routers/clients.py`

---

#### `DELETE /api/clients/{client_id}`
**Purpose:** Delete client

**Response:** `204 No Content`

**File:** `app/routers/clients.py`

---

### Health Endpoints

#### `GET /api/health/`
**Purpose:** Comprehensive health check

**Response:**
```json
{
  "status": "healthy",
  "database": true,
  "encryption": true,
  "timestamp": "2024-12-19T12:00:00Z"
}
```

**File:** `app/routers/health.py`

---

#### `GET /api/health/db`
**Purpose:** Database connection test

**Response:**
```json
{
  "status": "ok",
  "message": "Database connection successful"
}
```

**File:** `app/routers/health.py`

---

#### `GET /api/health/encryption`
**Purpose:** Encryption service test

**Response:**
```json
{
  "status": "ok",
  "message": "Encryption service operational"
}
```

**File:** `app/routers/health.py`

---

### Internal Processing Endpoint

#### `POST /api/process-emails`
**Purpose:** Manually trigger email processing (internal use)

**Query Parameters:**
- `max_per_account` (default: 10)

**Response:**
```json
{
  "status": "success",
  "message": "Processed 5 emails",
  "accounts": {
    "maya@skinnymanmusic.com": {
      "email_count": 3,
      "emails": [...]
    }
  }
}
```

**Note:** Uses legacy `archive/services/email_processor.py` for compatibility

**File:** `app/main.py`

---

## 🗄️ DATABASE SCHEMA

### Core Tables

#### `tenants`
**Purpose:** Multi-tenant isolation

**Columns:**
- `id` (UUID, PK)
- `name` (TEXT)
- `slug` (TEXT, UNIQUE)
- `timezone` (TEXT, default: "UTC")
- `settings` (JSONB)
- `active` (BOOLEAN)
- `created_at`, `updated_at` (TIMESTAMPTZ)

**RLS:** Enabled (tenant isolation)

---

#### `users`
**Purpose:** User accounts

**Columns:**
- `id` (UUID, PK)
- `tenant_id` (UUID, FK → tenants)
- `email` (TEXT, encrypted)
- `email_hash` (TEXT, SHA256)
- `full_name` (TEXT, encrypted)
- `role` (TEXT: "admin" | "user")
- `password_hash` (TEXT, bcrypt)
- `active` (BOOLEAN)
- `locked_until` (TIMESTAMPTZ, brute force protection)
- `failed_login_attempts` (INTEGER)
- `last_login` (TIMESTAMPTZ)
- `created_at`, `updated_at` (TIMESTAMPTZ)

**RLS:** Enabled (tenant isolation)  
**Indexes:** `(tenant_id, email)`, `(tenant_id, active)`, `(locked_until)`

---

#### `clients`
**Purpose:** Client records

**Columns:**
- `id` (UUID, PK)
- `tenant_id` (UUID, FK → tenants)
- `name` (TEXT, encrypted)
- `email` (TEXT, encrypted)
- `email_hash` (TEXT, SHA256, indexed)
- `phone` (TEXT, encrypted)
- `company` (TEXT, encrypted)
- `notes` (TEXT, encrypted)
- `last_contact_at` (TIMESTAMPTZ)
- `created_at`, `updated_at` (TIMESTAMPTZ)

**RLS:** Enabled (tenant isolation)  
**Indexes:** `(tenant_id, email_hash)`, `(tenant_id, last_contact_at)`

---

#### `emails`
**Purpose:** Email storage

**Columns:**
- `id` (UUID, PK)
- `tenant_id` (UUID, FK → tenants)
- `gmail_message_id` (TEXT, UNIQUE)
- `gmail_thread_id` (TEXT)
- `account_email` (TEXT)
- `sender_email` (TEXT)
- `sender_name` (TEXT)
- `subject` (TEXT)
- `body` (TEXT)
- `received_at` (TIMESTAMPTZ)
- `processed` (BOOLEAN)
- `processed_at` (TIMESTAMPTZ)
- `created_at`, `updated_at` (TIMESTAMPTZ)

**RLS:** Enabled (tenant isolation)  
**Indexes:** `(tenant_id, processed, created_at)`, `(tenant_id, gmail_thread_id)`, `(gmail_message_id)`

---

#### `calendar_events`
**Purpose:** Calendar event storage

**Columns:**
- `id` (UUID, PK)
- `tenant_id` (UUID, FK → tenants)
- `google_event_id` (TEXT, UNIQUE)
- `title` (TEXT)
- `start_time` (TIMESTAMPTZ)
- `end_time` (TIMESTAMPTZ)
- `location` (TEXT)
- `description` (TEXT)
- `client_id` (UUID, FK → clients)
- `color_id` (INTEGER)
- `created_at`, `updated_at` (TIMESTAMPTZ)

**RLS:** Enabled (tenant isolation)  
**Indexes:** `(tenant_id, start_time, end_time)`, `(tenant_id, client_id)`, `(google_event_id)`

---

### Security & Reliability Tables

#### `audit_log`
**Purpose:** Comprehensive audit trail

**Columns:**
- `id` (UUID, PK)
- `tenant_id` (UUID, FK → tenants)
- `action` (TEXT) - e.g., "email.processed", "calendar.event.created"
- `resource_type` (TEXT) - e.g., "email", "calendar", "client"
- `resource_id` (TEXT, UUID)
- `user_id` (TEXT, UUID, nullable)
- `metadata` (JSONB) - Redacted (no tokens/passwords)
- `ip_address` (TEXT)
- `user_agent` (TEXT)
- `trace_id` (TEXT) - Request tracing
- `created_at` (TIMESTAMPTZ)

**RLS:** Enabled (tenant isolation)  
**Indexes:** `(tenant_id, created_at DESC)`, `(tenant_id, action, created_at DESC)`, `(tenant_id, resource_type, resource_id)`

**Security:** All tokens and sensitive data automatically redacted

---

#### `sync_log`
**Purpose:** Webhook fingerprint storage (replay prevention)

**Columns:**
- `id` (UUID, PK)
- `tenant_id` (UUID, FK → tenants)
- `sync_type` (TEXT) - e.g., "gmail_webhook"
- `fingerprint` (TEXT, UNIQUE) - SHA256 hash
- `metadata` (JSONB)
- `created_at` (TIMESTAMPTZ)

**RLS:** Enabled (tenant isolation)  
**Indexes:** `(tenant_id, sync_type, created_at)`, `(fingerprint)`

---

#### `processed_messages`
**Purpose:** Global idempotency layer

**Columns:**
- `id` (UUID, PK)
- `tenant_id` (UUID, FK → tenants)
- `gmail_message_id` (TEXT, UNIQUE)
- `processed_at` (TIMESTAMPTZ)
- `created_at` (TIMESTAMPTZ)

**RLS:** Enabled (tenant isolation)  
**Indexes:** `(tenant_id, gmail_message_id)`, `(tenant_id, processed_at DESC)`

---

#### `email_retry_queue`
**Purpose:** Retry queue for failed email processing

**Columns:**
- `id` (UUID, PK)
- `tenant_id` (UUID, FK → tenants)
- `email_id` (UUID, FK → emails)
- `gmail_message_id` (TEXT)
- `account_email` (TEXT)
- `retry_count` (INTEGER, default: 0)
- `max_retries` (INTEGER, default: 3)
- `status` (TEXT) - "pending" | "processing" | "completed" | "failed"
- `error_message` (TEXT)
- `error_stack` (TEXT)
- `trace_id` (TEXT)
- `metadata` (JSONB)
- `scheduled_at` (TIMESTAMPTZ)
- `started_at` (TIMESTAMPTZ, nullable)
- `completed_at` (TIMESTAMPTZ, nullable)
- `created_at`, `updated_at` (TIMESTAMPTZ)

**RLS:** Enabled (tenant isolation)  
**Indexes:** `(tenant_id, status, scheduled_at)`, `(tenant_id, status) WHERE status = 'pending'`, `(gmail_message_id)`

---

### Guardian Framework Tables

#### `unsafe_threads`
**Purpose:** Sentra safety tagging

**Columns:**
- `id` (UUID, PK)
- `tenant_id` (UUID, FK → tenants)
- `thread_id` (TEXT, UNIQUE)
- `reason` (TEXT)
- `violation_type` (TEXT)
- `severity` (TEXT) - "low" | "medium" | "high" | "critical"
- `metadata` (JSONB)
- `created_at`, `updated_at` (TIMESTAMPTZ)

**RLS:** Enabled (tenant isolation)  
**Indexes:** `(tenant_id, thread_id)`, `(tenant_id, severity)`, `(tenant_id, created_at DESC)`

---

#### `repair_log`
**Purpose:** Vita repair attempts

**Columns:**
- `id` (UUID, PK)
- `tenant_id` (UUID, FK → tenants)
- `event` (TEXT)
- `action_taken` (TEXT)
- `success` (BOOLEAN)
- `error_message` (TEXT, nullable)
- `metadata` (JSONB)
- `created_at` (TIMESTAMPTZ)

**RLS:** Enabled (tenant isolation)  
**Indexes:** `(tenant_id, created_at DESC)`, `(tenant_id, success)`, `(tenant_id, event)`

---

#### `system_state`
**Purpose:** Solin MCP Safe Mode state

**Columns:**
- `id` (UUID, PK)
- `tenant_id` (UUID, FK → tenants)
- `state_key` (TEXT) - e.g., "safe_mode"
- `state_value` (JSONB) - e.g., `{"enabled": true, "reason": "...", "activated_at": "..."}`
- `created_at`, `updated_at` (TIMESTAMPTZ)
- UNIQUE `(tenant_id, state_key)`

**RLS:** Enabled (tenant isolation)  
**Indexes:** `(tenant_id, state_key)`

---

### Archivus Tables (Phase 11)

#### `archivus_threads`
**Purpose:** Thread tracking with importance scoring

**Columns:**
- `id` (UUID, PK)
- `tenant_id` (UUID, FK → tenants)
- `thread_id` (TEXT)
- `client_id` (UUID, FK → clients, nullable)
- `venue_name` (TEXT, nullable)
- `first_seen_at` (TIMESTAMPTZ)
- `last_seen_at` (TIMESTAMPTZ)
- `importance_score` (INTEGER, default: 0)
- UNIQUE `(tenant_id, thread_id)`

**RLS:** Enabled (tenant isolation)  
**Indexes:** `(tenant_id, thread_id)`, `(tenant_id, client_id)`, `(tenant_id, venue_name)`

---

#### `archivus_memories`
**Purpose:** Memory storage with type classification

**Columns:**
- `id` (UUID, PK)
- `tenant_id` (UUID, FK → tenants)
- `thread_id` (TEXT)
- `client_id` (UUID, FK → clients, nullable)
- `venue_name` (TEXT, nullable)
- `memory_type` (TEXT) - "client_profile" | "venue_profile" | "thread_summary" | "system_note"
- `summary` (TEXT)
- `source` (TEXT) - "maya_email" | "guardian" | "manual"
- `version` (INTEGER, default: 1)
- `created_at` (TIMESTAMPTZ)

**RLS:** Enabled (tenant isolation)  
**Indexes:**
- `(tenant_id, client_id)`
- `(tenant_id, venue_name)`
- `(tenant_id, thread_id)`
- `(tenant_id, memory_type, created_at DESC)`

---

## 🔒 SECURITY FEATURES

### 1. Webhook Security (Solin Requirements)

#### Google JWT Verification ✅
**Implementation:** `app/services/gmail_webhook.py` - `verify_jwt_token()`

**Validations:**
- **Issuer:** Must be `https://accounts.google.com` or `accounts.google.com`
- **Audience:** Must match `gmail_webhook_url` from config
- **Subject:** Must be `gmail_pubsub_service_account` from config
- **Expiration:** Validates `iat` (issued at) and `exp` (expiration)
- **Signature:** Validates using Google's JWKS (RS256 algorithm)
- **Clock Skew:** 5-minute tolerance

**Error Handling:**
- Invalid JWT → `401 Unauthorized`
- All failures audit logged

---

#### SHA256 Fingerprinting ✅
**Implementation:** `app/services/gmail_webhook.py` - `compute_request_fingerprint()`

**Formula:**
```
fingerprint = SHA256(message_id + publish_time + data_length)
```

**Storage:** `sync_log` table with `sync_type='gmail_webhook'`

**Replay Prevention:**
- Checks for duplicate fingerprint before processing
- Replay attempt → `409 Conflict`
- All replay attempts audit logged

---

#### Database Locking ✅
**Implementation:** `app/services/gmail_webhook.py` - `acquire_lock()`

**Method:**
- PostgreSQL advisory locks
- Lock key: `hash(gmail_message_id)`
- Non-blocking: `pg_try_advisory_lock()`
- Lock released in `finally` block (always)

**Race Condition Prevention:**
- Lock acquired before processing
- Lock failure → `409 Conflict`
- All lock operations audit logged

---

#### Strict Base64 Decoding ✅
**Implementation:** `app/services/gmail_webhook.py` - `parse_pubsub_message()`

**Method:**
- Uses `base64.b64decode(..., validate=True)`
- Rejects invalid padding
- Parse error → `400 Bad Request`

---

### 2. Authentication & Authorization

#### Password Policy ✅
**Implementation:** `app/utils/password_policy.py`

**Requirements:**
- Minimum 12 characters
- Must contain uppercase, lowercase, number, special character
- Checks against common password list
- Enforced on all user creation

---

#### Brute Force Protection ✅
**Implementation:** `app/services/auth_service.py`

**Features:**
- Tracks failed login attempts per user
- Locks account after 5 failed attempts
- Lock duration: 15 minutes
- `locked_until` timestamp in database
- All attempts audit logged

---

#### JWT Tokens ✅
**Implementation:** `app/services/auth_service.py`

**Features:**
- HS256 algorithm
- Access token: 30 minutes expiration
- Refresh token: 30 days expiration
- Secret key from environment only

---

### 3. Data Protection

#### PII Encryption ✅
**Implementation:** `app/encryption.py`

**Method:**
- AES-256 encryption (Fernet)
- Encrypts: client names, emails, phone numbers, notes
- Encryption key from environment only
- Automatic encryption/decryption in repository layer

---

#### Email Hashing ✅
**Implementation:** SHA256 hashing for email lookup

**Purpose:**
- Allows email lookup without storing plaintext
- Used for client deduplication
- Indexed for fast lookups

---

#### Token Redaction ✅
**Implementation:** `app/middleware/security.py` - `redact_tokens()`

**Features:**
- Automatically redacts tokens from audit logs
- Redacts: `api_key`, `token`, `password`, `secret`, `authorization`
- Prevents sensitive data leakage in logs

---

### 4. Network Security

#### CORS Hardening ✅
**Implementation:** `app/main.py`

**Production Origins:**
- `https://maya-ai-production.up.railway.app`
- `https://maya-ai-staging.up.railway.app`

**Development Origins:**
- `http://localhost:3000`
- `http://localhost:8000`

**Restrictions:**
- Limited `allow_methods`: GET, POST, PUT, DELETE, OPTIONS
- Limited `allow_headers`: Content-Type, Authorization

---

#### Rate Limiting ✅
**Implementation:** SlowAPI middleware

**Limits:**
- Default: 100 requests/minute per IP
- Webhook: 100 requests/minute
- Calendar: 50-100 requests/minute (varies)
- Custom 429 handler with `Retry-After` header

---

#### Security Headers ✅
**Implementation:** `app/middleware/security.py` - `SecurityMiddleware`

**Headers Added:**
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains`
- `Content-Security-Policy: default-src 'self'`

---

### 5. Row-Level Security (RLS)

**Implementation:** PostgreSQL RLS policies on all tables

**Pattern:**
```sql
CREATE POLICY tenant_isolation_<table> ON <table>
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant_id')::UUID)
    WITH CHECK (tenant_id = current_setting('app.current_tenant_id')::UUID);
```

**Enforcement:**
- All queries set tenant context: `SET LOCAL app.current_tenant_id = %s`
- Prevents cross-tenant data access
- Applied to: tenants, users, clients, emails, calendar_events, audit_log, and all guardian tables

---

### 6. Audit Logging

**Implementation:** `app/services/audit_service.py`

**Features:**
- All actions logged to `audit_log` table
- Automatic token redaction
- Request tracing (`trace_id`)
- IP address and user agent tracking
- Guardian Framework integration (emits to guardians)
- Performance monitoring (< 5ms per log)

**Log Actions:**
- `email.processed` - Email processing
- `calendar.event.created` - Calendar event creation
- `gmail.webhook.received` - Webhook received
- `gmail.webhook.jwt.invalid` - JWT verification failure
- `gmail.webhook.replay.detected` - Replay attempt
- `guardian.solin.safe_mode.activated` - Safe Mode activation
- `archivus.thread_summary.recorded` - Thread summary stored
- And many more...

---

### 7. Claude AI Safety

**Implementation:** `app/services/claude_service.py` - `MAYA_SYSTEM_PROMPT`

**Safety Rules (Enforced in Prompt):**
- ❌ NEVER include links, URLs, or external references
- ❌ NEVER hallucinate hours, prices, or event details
- ❌ NEVER provide external advice outside DJ/entertainment
- ❌ NEVER mention competitors
- ❌ NEVER include sensitive metadata
- ✅ ALWAYS use professional email tone
- ✅ ALWAYS verify information before stating as fact
- ✅ ALWAYS ask for missing information rather than assuming

**Prompt Optimization:**
- Reduced prompt size by ~60% (removed redundant context)
- Truncates long fields (email body to 2000 chars, questions to 3)
- Redacts sensitive metadata (sender_email)

---

## ✅ OPERATIONAL STATUS

### Fully Operational ✅

**Core Email Processing:**
- ✅ Gmail webhook with full JWT verification
- ✅ Email storage in database
- ✅ 8 intelligence services (all operational)
- ✅ Claude AI response generation
- ✅ Auto-send vs. draft logic
- ✅ Multi-account routing
- ✅ Idempotency layer
- ✅ Retry queue

**Calendar Integration:**
- ✅ Event creation
- ✅ Auto-block on acceptance
- ✅ Conflict detection
- ✅ Event deletion
- ✅ Availability checking
- ✅ Timezone support

**Guardian Framework:**
- ✅ Solin MCP (orchestration, Safe Mode)
- ✅ Sentra Safety (enforcement, thread tagging)
- ✅ Vita Repair (automated fixes)
- ✅ Guardian Daemon (30-minute monitoring)
- ✅ Aegis (minimal integration)

**Memory Engine:**
- ✅ Archivus (thread summaries, client/venue profiles, system notes)
- ✅ Integration with email processor
- ✅ Integration with guardian daemon
- ✅ Integration with Solin MCP

**Security:**
- ✅ JWT verification
- ✅ SHA256 fingerprinting
- ✅ Database locking
- ✅ Rate limiting
- ✅ CORS hardening
- ✅ Password policy
- ✅ Brute force protection
- ✅ Token redaction
- ✅ RLS enforcement

**External Integrations:**
- ✅ Nova API (pricing) - with exponential backoff
- ✅ Eli API (venue intelligence) - with fallback
- ✅ Google Calendar API
- ✅ Gmail API

---

### Partially Operational ⚠️

**Aegis Security Intelligence:**
- ✅ Minimal integration (Phase 11)
- ⏳ Full intelligence engine (Phase 12 - In Progress)
- ⏳ Risk snapshot computation
- ⏳ Anomaly detection
- ⏳ Solin integration for Safe Mode triggers

**Vee Marketing:**
- ✅ Design specification complete
- ⏳ Database schema (Phase 13.1 - In Progress)
- ⏳ Service implementation (Phase 13.2 - Planned)
- ⏳ API endpoints (Phase 13.3 - Planned)

**Work Queue:**
- ⏳ Generic work queue (Phase 14.1 - Planned)
- ⏳ Worker skeleton (Phase 14.1 - Planned)
- ⏳ Metrics endpoints (Phase 14.2 - Planned)

---

### Design Only (Not Implemented) ⏳

**Vee C-Mode:**
- ⏳ Automated posting (requires 90-day B-Mode success)
- ⏳ Social media API integrations
- ⏳ Campaign automation

**Archivus Advanced Features:**
- ⏳ Historical baseline queries
- ⏳ Pattern classification lookups
- ⏳ Trend analysis data

**Frontend:**
- ⏳ Next.js frontend (separate repo)
- ⏳ Webflow integration (planned)
- ⏳ Admin dashboard (planned)

---

## 🔗 INTEGRATION POINTS

### Maya → Nova
**Purpose:** Pricing calculations and invoice generation

**Implementation:**
- HTTP POST to `{nova_api_url}/api/pricing/calculate`
- Exponential backoff retry: 200ms, 1s, 2s, 5s
- Fallback: Graceful failure (no fake pricing)

**When:**
- After acceptance detection
- All required info available
- Not multiple events (coordinator detection)

**File:** `app/services/email_processor_v3.py` - `_get_nova_pricing()`

---

### Maya → Eli
**Purpose:** Venue intelligence and research

**Implementation:**
- HTTP POST to `{eli_api_url}/research/venue`
- Fallback: Local Canopy database in `VenueIntelligenceService`

**When:**
- Venue keyword detected in email
- Venue intelligence needed for response
- Equipment awareness required

**File:** `app/services/intelligence/venue_intelligence.py`

---

### Maya → Rho (Calendar)
**Purpose:** Calendar conflict checks and auto-blocking

**Implementation:**
- Direct service calls to `CalendarServiceV3`
- Conflict detection before auto-send
- Auto-block on acceptance (if no conflicts)

**When:**
- Before auto-sending email (conflict check)
- On acceptance detection (auto-block)
- Calendar event CRUD operations

**File:** `app/services/calendar_service_v3.py`

---

### Maya → Archivus
**Purpose:** Store thread summaries and context

**Implementation:**
- Light-touch integration after successful email processing
- Fail-open (never blocks email processing)

**When:**
- After successful email processing (draft created or sent)
- Records thread summary with structured context

**File:** `app/services/email_processor_v3.py` (Phase 11.3)

---

### Aegis → All Agents (Observational)
**Purpose:** Monitor all agent activity via logs

**Implementation:**
- Observes `audit_log` for all agent actions
- Monitors `sync_log` for webhook patterns
- Tracks `processed_messages` for email processing
- Analyzes `email_retry_queue` for failure patterns

**When:**
- Continuously (scheduled checks: hourly, nightly)
- Event-driven (end-of-run hooks)
- Threshold-based (error spikes, retry queue size)

**File:** `app/services/aegis_service.py`

---

### Archivus → Aegis (Future)
**Purpose:** Provide historical context for anomaly detection

**Status:** ⏳ Design only (Phase 12)

**When (Future):**
- Before flagging anomaly (check if normal)
- During pattern analysis (compare to baseline)
- When determining severity (check similar patterns)

---

### Guardian Framework Integration

**Solin → Sentra:**
- Routes ERROR level events to Sentra
- Sentra enforces safety policies
- Sentra can block unsafe outputs

**Solin → Vita:**
- Routes `email_processor` crash events to Vita
- Vita attempts automatic repairs
- Vita logs repair attempts

**Solin → Aegis:**
- Receives Aegis security summaries (Phase 12)
- Uses risk scores for Safe Mode decisions

**Guardian Daemon:**
- Runs every 30 minutes
- Calls `Sentra.self_check()`
- Calls `Vita.self_check()`
- Calls `Solin.mcp_health_check()`
- Triggers Safe Mode on failures

**File:** `app/guardians/guardian_daemon.py`

---

## 🎨 FRONTEND REQUIREMENTS

### Essential Endpoints for Frontend

#### 1. Health & Status
- `GET /api/health/` - System health check
- `GET /api/health/db` - Database connectivity
- `GET /api/health/encryption` - Encryption service status

**Use Case:** Dashboard status indicators, system monitoring

---

#### 2. Email Management
**Current:** No direct email endpoints (emails processed via webhook)

**Future Endpoints (Planned):**
- `GET /api/emails/` - List emails with pagination
- `GET /api/emails/{email_id}` - Get email details
- `GET /api/emails/thread/{thread_id}` - Get thread history
- `POST /api/emails/{email_id}/process` - Manually trigger processing

**Use Case:** Email inbox view, thread history, manual processing

---

#### 3. Calendar Management
- `GET /api/calendar/events` - List events (with date range)
- `POST /api/calendar/events` - Create event
- `POST /api/calendar/block` - Auto-block time
- `GET /api/calendar/availability` - Check availability
- `DELETE /api/calendar/event/{event_id}` - Delete event

**Use Case:** Calendar view, event creation, conflict checking

---

#### 4. Client Management
- `GET /api/clients/` - List clients (paginated)
- `GET /api/clients/{client_id}` - Get client details
- `POST /api/clients/` - Create client
- `PUT /api/clients/{client_id}` - Update client
- `DELETE /api/clients/{client_id}` - Delete client
- `GET /api/clients/search/by-email/` - Search by email

**Use Case:** Client directory, client profiles, client search

---

#### 5. Vee Content (Phase 13 - Planned)
- `GET /api/vee/drafts` - List content drafts
- `POST /api/vee/drafts` - Generate draft
- `POST /api/vee/drafts/{id}/queue` - Queue for review
- `GET /api/vee/drafts?status=approved` - Filter by status

**Use Case:** Content review queue, draft management, approval workflow

---

#### 6. Metrics & Monitoring (Phase 14 - Planned)
- `GET /api/metrics` - System metrics
  - Processed messages (last 24h)
  - Retry queue items (pending)
  - Unsafe threads count
  - Repair log failures (last 24h)
  - Vee drafts by status

**Use Case:** Dashboard metrics, system monitoring, health indicators

---

### Authentication Requirements

**Current:** Tenant-based (via `default_tenant_id`)

**Future (Planned):**
- JWT token authentication
- User login endpoint: `POST /api/auth/login`
- Token refresh: `POST /api/auth/refresh`
- User info: `GET /api/auth/me`

---

### Frontend Authentication Roadmap

**Current State (Phase 11):**
- No user authentication
- Tenant-based access only
- No JWT tokens

**Phase 15 (Planned):**
- JWT access tokens (30-minute expiration)
- JWT refresh tokens (30-day expiration)
- User login endpoint: `POST /api/auth/login`
- Token refresh endpoint: `POST /api/auth/refresh`
- User info endpoint: `GET /api/auth/me`

**Phase 16 (Planned):**
- OAuth2 user login integration
- Social login support (Google, Microsoft)
- Multi-tenant user management

**Phase 17 (Planned):**
- Session refresh automation
- Token rotation
- Remember me functionality

**Frontend Preparation:**
- Plan for JWT token storage (httpOnly cookies recommended)
- Implement token refresh logic
- Handle 401 responses (token expired) → redirect to login
- Handle 429 responses (rate limit) → show retry message

**Frontend Should:**
- Store JWT tokens securely (httpOnly cookies recommended)
- Include `Authorization: Bearer <token>` header
- Handle 401 responses (token expired) → redirect to login
- Handle 429 responses (rate limit) → show retry message

---

### Data Models for Frontend

#### Email Model
```typescript
interface Email {
  id: string;
  gmail_message_id: string;
  gmail_thread_id: string;
  account_email: string;
  sender_email: string;
  sender_name: string;
  subject: string;
  body: string;
  received_at: string; // ISO datetime
  processed: boolean;
  processed_at?: string; // ISO datetime
}
```

#### Calendar Event Model
```typescript
interface CalendarEvent {
  id: string;
  google_event_id: string;
  title: string;
  start_time: string; // ISO datetime
  end_time: string; // ISO datetime
  location?: string;
  description?: string;
  client_id?: string;
  color_id: number;
}
```

#### Client Model
```typescript
interface Client {
  id: string;
  name: string;
  email: string; // Decrypted by backend
  phone?: string; // Decrypted by backend
  company?: string; // Decrypted by backend
  last_contact_at?: string; // ISO datetime
  created_at: string; // ISO datetime
}
```

#### Health Check Model
```typescript
interface HealthCheck {
  status: "healthy" | "degraded";
  database: boolean;
  encryption: boolean;
  timestamp: string; // ISO datetime
}
```

---

### Error Handling

**Standard Error Response:**
```json
{
  "error": "error_code",
  "message": "Human-readable error message",
  "trace_id": "request_trace_id"
}
```

**HTTP Status Codes:**
- `200 OK` - Success
- `201 Created` - Resource created
- `204 No Content` - Success (delete)
- `400 Bad Request` - Invalid request
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Authorization failed
- `404 Not Found` - Resource not found
- `409 Conflict` - Replay/lock failure
- `429 Too Many Requests` - Rate limit exceeded (includes `Retry-After` header)
- `500 Internal Server Error` - Server error

---

### Rate Limiting

**Frontend Should:**
- Handle 429 responses gracefully
- Display retry message with countdown
- Implement exponential backoff for retries
- Cache responses when possible
- Batch requests when appropriate

**Rate Limits:**
- Default: 100 requests/minute
- Webhook: 100 requests/minute
- Calendar: 50-100 requests/minute

---

### Real-Time Updates

**Current:** Polling-based (no WebSocket)

**Future (Planned):**
- WebSocket connection for real-time email notifications
- WebSocket for calendar event updates
- WebSocket for Safe Mode status changes

**Current Workaround:**
- Poll `/api/health/` for system status
- Poll `/api/calendar/events` for calendar updates
- Poll email endpoints (when available) for new emails

---

## 📝 CHANGE LOG

### Version 3.0.2 (December 19, 2024)

#### Frontend Agents System Implementation ✅
**Date:** December 19, 2024

**Changes:**
- ✅ Implemented complete agents management system in omega-frontend
- ✅ Created agent types (MAYA, NOVA, ELI, SOLIN, RHO, VEE, CUSTOM)
- ✅ Built agents API client for backend integration
- ✅ Implemented agents page with grid layout and modal
- ✅ Added health status monitoring (healthy/degraded/offline/unknown)
- ✅ Added active/pause toggle functionality
- ✅ Improved sidebar active state detection
- ✅ Ready for backend API connection

**Impact:**
- Complete agents management UI
- Full CRUD operations for agents
- Visual health monitoring
- Easy agent creation workflow
- Optimistic UI for better UX

---

### Version 3.0.1 (December 19, 2024)

#### Documentation Enhancements ✅
**Date:** December 19, 2024

**Changes:**
- ✅ Added clarification between MCP Orchestration Layer and Guardian Layer
- ✅ Added Guardian Daemon to architecture diagram
- ✅ Added Retry Queue worker bubble to architecture diagram
- ✅ Added Agent Categories table for quick reference
- ✅ Added note about separate frontend repository
- ✅ Added `tenant_id`, `created_at`, `updated_at` to calendar event responses
- ✅ Added Authentication vs Authorization explanation
- ✅ Added Aegis risk warning label
- ✅ Added Frontend Authentication Roadmap (Phases 15-17)
- ✅ Added Dependency Vulnerability Scan to security checklist
- ✅ Added "No admin UI for unsafe thread management" to known issues
- ✅ Added Project Secrets Naming Convention reference

**Impact:**
- Improved clarity for frontend developers
- Better architecture visualization
- Clearer authentication roadmap
- Enhanced security documentation
- Better onboarding for new developers

---

### Version 3.0.0 (December 19, 2024)

#### Phase 11 - Archivus Memory Engine ✅
**Date:** December 19, 2024

**Changes:**
- ✅ Created `archivus_threads` and `archivus_memories` tables
- ✅ Implemented `ArchivusService` with thread summarization
- ✅ Integrated Archivus into email processor (records thread summaries)
- ✅ Integrated Archivus into guardian daemon (records system notes)
- ✅ Integrated Archivus into Solin MCP (optional system notes)
- ✅ Added comprehensive test suite (5 tests)

**Files Added:**
- `migrations/011_archivus_schema.sql`
- `app/models/archivus.py`
- `app/services/archivus_service.py`
- `tests/test_archivus_service.py`

**Files Modified:**
- `app/services/email_processor_v3.py` - Added Archivus integration
- `app/guardians/guardian_daemon.py` - Added Archivus system notes
- `app/guardians/solin_mcp.py` - Added optional Archivus helper
- `app/models/__init__.py` - Exported Archivus models
- `tests/test_runner.py` - Added Archivus test suite

**Impact:**
- Email processing now records thread summaries automatically
- Guardian daemon records Safe Mode activations in Archivus
- System notes stored for long-term memory
- No breaking changes (fail-open design)

---

#### File Structure Cleanup ✅
**Date:** December 19, 2024

**Changes:**
- ✅ Moved 12 test scripts to `scripts/dev/`
- ✅ Moved 25+ completion reports to `docs/reports/`
- ✅ Moved legacy services to `archive/services/`
- ✅ Moved test data to `test_data/`
- ✅ Removed duplicate `omega_core_v3_spec.md` from root
- ✅ Removed nested `backend/backend/` folder
- ✅ Updated all imports to point to new locations

**Root Directory:** 81 files → 24 files (70% reduction)

**Files Moved:**
- Legacy services: `email_processor.py`, `calendar_service.py`, `firestore_service.py` → `archive/services/`
- Test scripts: All `test_*.py` → `scripts/dev/`
- Reports: All `*_COMPLETE.md`, `TASK_PACK_*.md` → `docs/reports/`
- Test data: `briana_*.txt`, `*.json` → `test_data/`

**Imports Updated:**
- `app/main.py` → `from archive.services.email_processor import process_all_accounts`
- `tests/test_acceptance_ab.py` → `from archive.services.email_processor import EmailProcessor as EmailProcessorV2`
- `scripts/dev/*.py` → Updated all imports

**Impact:**
- Cleaner root directory
- Better organization
- All imports verified and working
- No breaking changes

---

### Previous Phases (See `docs/reports/` for details)

**Phase 1-5:** Security, Calendar, Idempotency, Testing, Hardening  
**Phase 6-10:** Guardian Framework, Safety Gate, Monitoring  
**Full History:** See `CLAUDE_PROGRESS_LOG.md` for complete change history

---

## 🔍 SECURITY AUDIT CHECKLIST

### ✅ Completed Security Checks

#### 1. AI Hallucination Prevention ✅
- ✅ Claude system prompt enforces no hallucination
- ✅ No prices, dates, times, or venues invented
- ✅ Missing info detection asks for clarification
- ✅ Nova API fallback: No fake pricing on failure
- ✅ Safety gate test: `test_no_hallucination_on_unknown_data`

**File:** `app/services/claude_service.py` - `MAYA_SYSTEM_PROMPT`

---

#### 2. Prompt Injection Resistance ✅
- ✅ System prompt not revealed in responses
- ✅ Role boundaries enforced
- ✅ Safety gate test: `test_prompt_injection_defense`

**File:** `app/services/claude_service.py` - `MAYA_SYSTEM_PROMPT`

---

#### 3. Output Sanitization ✅
- ✅ HTML, scripts, SQL, JS sanitization
- ✅ Safety gate test: `test_adversarial_email_sanitization`

**File:** `app/services/claude_service.py`

---

#### 4. JWT Verification ✅
- ✅ Full Google JWT verification (issuer, audience, signature, expiration)
- ✅ Invalid JWTs rejected with 401
- ✅ Safety gate test: `test_jwt_verification_enforced`

**File:** `app/services/gmail_webhook.py` - `verify_jwt_token()`

---

#### 5. Replay Attack Prevention ✅
- ✅ SHA256 fingerprinting
- ✅ Duplicate fingerprints rejected with 409
- ✅ Safety gate test: `test_replay_attack_prevention`

**File:** `app/services/gmail_webhook.py` - `compute_request_fingerprint()`

---

#### 6. Idempotency Layer ✅
- ✅ Global idempotency via `processed_messages` table
- ✅ Same `gmail_message_id` processes only once
- ✅ Safety gate test: `test_idempotency_layer`

**File:** `app/services/idempotency_service.py`

---

#### 7. Database Locking ✅
- ✅ PostgreSQL advisory locks prevent race conditions
- ✅ Concurrent processing attempts blocked
- ✅ Safety gate test: `test_database_locking`

**File:** `app/services/gmail_webhook.py` - `acquire_lock()`

---

#### 8. RLS Enforcement ✅
- ✅ All tables have RLS policies
- ✅ Tenant isolation enforced
- ✅ Safety gate test: `test_rls_enforcement`

**File:** All migration files with RLS policies

---

#### 9. Token Redaction ✅
- ✅ Automatic token redaction in audit logs
- ✅ No sensitive data in logs
- ✅ Safety gate test: `test_no_sensitive_data_logged`

**File:** `app/middleware/security.py` - `redact_tokens()`

---

#### 10. Trace ID Tracking ✅
- ✅ All requests have `trace_id`
- ✅ All audit logs include `trace_id`
- ✅ Safety gate test: `test_all_events_have_trace_id`

**File:** `app/middleware/security.py` - `SecurityMiddleware`

---

#### 11. Secrets Management ✅
- ✅ All secrets loaded from environment only
- ✅ No hardcoded secrets
- ✅ Config enforces `env_file = ".env"`, `extra = "ignore"`

**File:** `app/config.py` - `Settings` class

---

#### 12. Password Policy ✅
- ✅ Minimum 12 characters
- ✅ Complexity requirements
- ✅ Common password checks

**File:** `app/utils/password_policy.py`

---

#### 13. Brute Force Protection ✅
- ✅ Failed login attempt tracking
- ✅ Account lockout after 5 attempts
- ✅ 15-minute lock duration

**File:** `app/services/auth_service.py`

---

#### 14. CORS Hardening ✅
- ✅ Restricted origins (production + localhost for dev)
- ✅ Limited methods and headers
- ✅ No wildcard origins

**File:** `app/main.py`

---

#### 15. Security Headers ✅
- ✅ X-Content-Type-Options
- ✅ X-Frame-Options
- ✅ X-XSS-Protection
- ✅ Strict-Transport-Security
- ✅ Content-Security-Policy

**File:** `app/middleware/security.py`

---

#### 16. Rate Limiting ✅
- ✅ SlowAPI middleware
- ✅ Per-endpoint limits
- ✅ Custom 429 handler

**File:** `app/main.py`, all routers

---

#### 17. Global Exception Handler ✅
- ✅ Catches all unhandled errors
- ✅ Logs with trace_id (redacted)
- ✅ Generic 500 in production (no stack traces)

**File:** `app/main.py` - `global_exception_handler()`

---

#### 18. Safe Mode Protection ✅
- ✅ Freezes email processing in Safe Mode
- ✅ Freezes calendar writes in Safe Mode
- ✅ Freezes Vee content generation in Safe Mode
- ✅ All blocked operations logged

**File:** `app/guardians/solin_mcp.py`, `app/services/email_processor_v3.py`, `app/services/calendar_service_v3.py`

---

#### 19. Dependency Vulnerability Scan ⏳
- ⏳ Planned for future implementation
- ⏳ Automated dependency scanning (e.g., `safety`, `pip-audit`)
- ⏳ Integration with CI/CD pipeline
- ⏳ Regular security updates

**Recommendation:** Implement automated dependency scanning in Phase 15+

---

## 🐛 KNOWN ISSUES & LIMITATIONS

### Current Limitations

1. **Frontend Not Implemented**
   - No Next.js frontend yet (separate repo)
   - No admin dashboard
   - API-only backend

2. **Authentication**
   - Currently tenant-based (no user JWT yet)
   - User authentication endpoints planned but not implemented

3. **Vee B-Mode**
   - Design only (Phase 13 - In Progress)
   - No content generation yet
   - No API endpoints yet

4. **Aegis Intelligence**
   - Minimal integration only (Phase 12 - In Progress)
   - Full intelligence engine not yet implemented

5. **Work Queue**
   - Not yet implemented (Phase 14 - Planned)
   - No generic work queue system

6. **Real-Time Updates**
   - No WebSocket support
   - Polling-based only

7. **Admin UI**
   - No admin UI for unsafe thread management (yet)
   - Unsafe threads can only be viewed via database queries
   - Planned for future frontend implementation

---

### Known Bugs

**None Currently Known**

All tests passing:
- ✅ Integration tests
- ✅ A/B tests
- ✅ Safety gate tests (12/12 passing)
- ✅ Guardian tests
- ✅ Archivus tests

---

## 📊 PERFORMANCE METRICS

### Target Metrics

**API Response Time:**
- Target: < 150ms average
- Current: Meeting target (with optimizations)

**Database Queries:**
- Connection pooling: 2-30 connections
- Indexes on all frequently queried columns
- RLS overhead: < 5ms per query

**Claude API:**
- Prompt size reduced by ~60%
- Response time: ~2-5 seconds (external API)

**Audit Logging:**
- < 5ms per log entry
- Non-blocking (fail-open)

---

## 🚀 DEPLOYMENT

### Production Environment

**Platform:** Railway  
**URL:** `https://maya-ai-production.up.railway.app`  
**Build System:** Nixpacks (Python 3.14)  
**Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Pre-Deployment Safety Gate

**Script:** `scripts/safety_gate_phase5.py`  
**Tests:** 12 comprehensive safety tests  
**Integration:** Runs automatically before deployment (Nixpacks preDeploy phase)  
**Result:** Deployment blocked if any test fails

**File:** `nixpacks.toml` - `[phases.preDeploy]`

---

### Environment Variables

**Required:**
- `DATABASE_URL` - PostgreSQL connection string
- `ENCRYPTION_KEY` - AES-256 encryption key (32 bytes, base64)
- `JWT_SECRET_KEY` - JWT signing secret
- `ANTHROPIC_API_KEY` - Claude AI API key
- `MAYA_EMAIL` - maya@skinnymanmusic.com
- `GREG_SME_EMAIL` - djskinny@skinnymanmusic.com
- `GREG_L3_EMAIL` - greg@levelthree.io

**Optional:**
- `NOVA_API_URL` - Nova pricing API (default: Railway URL)
- `ELI_API_URL` - Eli venue API (default: Railway URL)
- `GMAIL_PUBSUB_TOPIC` - Pub/Sub topic for JWT validation
- `GMAIL_WEBHOOK_URL` - Webhook URL for JWT audience validation
- `GMAIL_PUBSUB_SERVICE_ACCOUNT` - Service account for JWT subject validation
- `SOLIN_NOTIFY_EMAIL` - Email for Safe Mode notifications
- `SOLIN_NOTIFY_DISCORD_WEBHOOK` - Discord webhook for Safe Mode
- `OMEGA_ENV` - Environment: "production" | "staging" | "development"

---

### Project Secrets Naming Convention

**Purpose:** Standardize environment variable names to prevent misconfiguration

**Naming Pattern:**
- Use `UPPER_SNAKE_CASE`
- Prefix with service/component name (e.g., `GMAIL_`, `NOVA_`, `ELI_`, `SOLIN_`)
- Use descriptive names (e.g., `GMAIL_PUBSUB_SERVICE_ACCOUNT` not `GMAIL_SA`)

**Required Secrets (Must Have):**
- `DATABASE_URL` - PostgreSQL connection string
- `ENCRYPTION_KEY` - AES-256 encryption key (32 bytes, base64-encoded)
- `JWT_SECRET_KEY` - JWT signing secret (minimum 32 characters)
- `ANTHROPIC_API_KEY` - Claude AI API key
- `MAYA_EMAIL` - Primary email account
- `GREG_SME_EMAIL` - SME email account
- `GREG_L3_EMAIL` - Level Three email account

**Optional Secrets (Conditional):**
- `GMAIL_PUBSUB_TOPIC` - Only if using Gmail webhooks
- `GMAIL_WEBHOOK_URL` - Only if using Gmail webhooks
- `GMAIL_PUBSUB_SERVICE_ACCOUNT` - Only if using Gmail webhooks
- `NOVA_API_URL` - Only if Nova API is separate service
- `ELI_API_URL` - Only if Eli API is separate service
- `SOLIN_NOTIFY_EMAIL` - Only if Safe Mode notifications enabled
- `SOLIN_NOTIFY_DISCORD_WEBHOOK` - Only if Discord notifications enabled

**Common Mistakes to Avoid:**
- ❌ `API_KEY` (too generic - use `ANTHROPIC_API_KEY`)
- ❌ `SECRET` (too generic - use `JWT_SECRET_KEY` or `ENCRYPTION_KEY`)
- ❌ `DB_URL` (use `DATABASE_URL`)
- ❌ `GMAIL_KEY` (use `GMAIL_PUBSUB_SERVICE_ACCOUNT`)

**Validation:**
- All required secrets must be set in production
- Missing required secrets will cause application startup failure
- Optional secrets have defaults or graceful fallbacks

---

## 📚 ADDITIONAL RESOURCES

### Documentation Files

**Specifications:**
- `docs/omega_core_v3_spec.md` - Master 10-agent specification
- `docs/aegis_agent_spec.md` - Aegis agent design
- `docs/archivus_aegis_routing.md` - Archivus/Aegis collaboration
- `docs/vee_moreno_trial_spec.md` - Vee 90-day trial specification

**Reports:**
- `reports/maya_v3_final_report.md` - Final readiness report
- `docs/reports/` - All completion reports (25+ files)
- `CLAUDE_PROGRESS_LOG.md` - Complete development history

**Run Orders:**
- `OMEGA_CORE_v3_RUN)ORDER_(Phase_11_15).md` - Current phase execution order
- `cursor_run_order_maya_omega_v3.md` - Previous phase run order

---

### Agent Registry

**File:** `app/config/omega_agents_registry.json`

Contains complete agent roster with:
- Agent IDs, names, roles
- Categories and routing rules
- Special modes (e.g., Vee B-Mode)

---

## 🔄 MAINTENANCE & UPDATES

### Updating This Document

**When to Update:**
- After completing any RUN BLOCK
- After adding new API endpoints
- After modifying database schema
- After security changes
- After agent status changes

**Update Process:**
1. Update relevant section
2. Add entry to Change Log
3. Update "Last Updated" date
4. Verify all links and references

---

## 📞 SUPPORT & CONTACTS

**System Owner:** Greg (DJ Skinny)  
**Primary Email:** djskinny@skinnymanmusic.com  
**Level Three Email:** greg@levelthree.io

**Safe Mode Notifications:**
- Email: Configured via `SOLIN_NOTIFY_EMAIL`
- Discord: Configured via `SOLIN_NOTIFY_DISCORD_WEBHOOK`

---

**END OF OMEGA OVERVIEW**

**Last Updated:** December 19, 2024  
**Next Review:** After Phase 12-15 completion

---

## 🔒 SECURITY AUDIT STATUS

**Last Security Audit:** December 19, 2024  
**Status:** ✅ **SECURE FOR PRODUCTION**

**Summary:**
- ✅ No security leaks detected
- ✅ No AI hallucination risks
- ✅ No critical bugs found
- ✅ All safety gate tests passing (12/12)

**Full Report:** See `SECURITY_AUDIT_REPORT.md`

---

**END OF OMEGA OVERVIEW**

