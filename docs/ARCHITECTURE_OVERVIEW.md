# 🏛️ ARCHITECTURE OVERVIEW

**MAYA/OMEGA System Architecture**  
**Version:** 3.5.0  
**Last Updated:** 2025-01-27

---

## 📋 Executive Summary

MAYA (MayAssistant) is an AI-powered email and SMS assistant built on **OMEGA Core v3.0**, a multi-agent AI operations system. This document provides a comprehensive overview of the system architecture, components, and design decisions.

---

## 🎯 System Purpose

MAYA automates client communication for DJ Skinny (Greg) at Skinny Man Entertainment, handling:
- Email processing and response generation
- SMS-based booking flows
- Payment processing and reminders
- Calendar management and conflict detection
- Client relationship management

---

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT LAYER                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Web App    │  │  Mobile PWA  │  │  Email/SMS    │      │
│  │  (Next.js)   │  │  (PWA)       │  │  (External)  │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
└─────────┼──────────────────┼─────────────────┼──────────────┘
          │                  │                 │
          └──────────────────┼─────────────────┘
                             │
          ┌──────────────────▼──────────────────┐
          │         API GATEWAY LAYER            │
          │  ┌────────────────────────────────┐  │
          │  │    FastAPI Application        │  │
          │  │  - Authentication (JWT)       │  │
          │  │  - Rate Limiting             │  │
          │  │  - Request Validation        │  │
          │  └──────────────┬───────────────┘  │
          └─────────────────┼───────────────────┘
                            │
          ┌─────────────────▼───────────────────┐
          │      APPLICATION LAYER              │
          │  ┌────────────────────────────────┐ │
          │  │   Email Processor V3           │ │
          │  │   - Intelligence Modules        │ │
          │  │   - Claude AI Integration      │ │
          │  │   - Response Generation        │ │
          │  └──────────────┬─────────────────┘ │
          │                  │                   │
          │  ┌──────────────▼─────────────────┐ │
          │  │   Booking Service               │ │
          │  │   - State Machine               │ │
          │  │   - Calendar Integration        │ │
          │  │   - Payment Link Generation     │ │
          │  └──────────────┬─────────────────┘ │
          │                  │                   │
          │  ┌──────────────▼─────────────────┐ │
          │  │   Stripe Service               │ │
          │  │   SMS Service                  │ │
          │  │   Calendar Service              │ │
          │  └──────────────┬─────────────────┘ │
          └─────────────────┼───────────────────┘
                            │
          ┌─────────────────▼───────────────────┐
          │        DATA LAYER                     │
          │  ┌────────────────────────────────┐  │
          │  │   PostgreSQL (Supabase)       │  │
          │  │   - Multi-tenant RLS          │  │
          │  │   - AES-256 Encryption        │  │
          │  │   - Audit Logging              │  │
          │  └────────────────────────────────┘  │
          └──────────────────────────────────────┘
                            │
          ┌─────────────────▼───────────────────┐
          │      EXTERNAL SERVICES                │
          │  ┌──────────┐  ┌──────────┐         │
          │  │  Gmail   │  │ Stripe  │          │
          │  │  API     │  │  API    │          │
          │  └──────────┘  └──────────┘         │
          │  ┌──────────┐  ┌──────────┐         │
          │  │ Twilio   │  │ Calendar│          │
          │  │  API     │  │   API   │          │
          │  └──────────┘  └──────────┘         │
          └──────────────────────────────────────┘
```

---

## 🔧 Technology Stack

### Frontend

- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** TailwindCSS
- **State Management:** React Hooks, Zustand (future)
- **Deployment:** Vercel

### Backend

- **Framework:** FastAPI (Python 3.14)
- **Database:** PostgreSQL (Supabase)
- **AI:** Anthropic Claude Sonnet 4
- **Authentication:** JWT (HS256)
- **Encryption:** AES-256 (Fernet)
- **Deployment:** Railway

### External Integrations

- **Gmail API:** OAuth 2.0, Pub/Sub webhooks
- **Google Calendar API:** OAuth 2.0, event sync
- **Stripe API:** Payment processing
- **Twilio API:** SMS messaging

---

## 🧩 Core Components

### 1. Email Processing Pipeline

**Location:** `backend/app/services/email_processor_v3.py`

**Flow:**
1. Gmail webhook receives email
2. Intelligence modules analyze:
   - Acceptance detection
   - Missing information detection
   - Venue intelligence
   - Equipment awareness
   - Context reconstruction
3. Claude AI generates response
4. If acceptance detected → Create Stripe payment link
5. Send draft email (never auto-send)

**Intelligence Modules:**
- `acceptance_detection.py` - Detects booking acceptance
- `missing_info_detection.py` - Identifies missing details
- `venue_intelligence.py` - Venue research and context
- `equipment_awareness.py` - Equipment requirements
- `context_reconstruction.py` - Thread history analysis

### 2. SMS Booking Flow

**Location:** `backend/app/routers/sms.py`, `backend/app/services/booking_service.py`

**State Machine:**
```
initial → service_selected → date_selected → time_selected → payment_pending → confirmed
```

**Features:**
- Calendar availability checking
- Automatic time slot suggestions
- Payment link generation
- Confirmation messages

### 3. Payment Integration

**Location:** `backend/app/services/stripe_service.py`

**Features:**
- Payment link creation
- Webhook processing
- Payment status tracking
- Automated reminders (Day 3, 7, 14)

**Worker:** `backend/app/workers/payment_reminder_worker.py`

### 4. Calendar Management

**Location:** `backend/app/services/calendar_service_v3.py`

**Features:**
- Event creation and blocking
- Conflict detection
- Availability checking
- Multi-calendar support

### 5. Security Framework

**Components:**
- **JWT Authentication** - `backend/app/routers/auth.py`
- **AES-256 Encryption** - `backend/app/encryption.py`
- **Rate Limiting** - SlowAPI middleware
- **Audit Logging** - `backend/app/services/audit_service.py`
- **Row-Level Security** - PostgreSQL RLS policies

---

## 🗄️ Database Architecture

### Multi-Tenancy

**Design:**
- All tables include `tenant_id` column
- Row-Level Security (RLS) policies enforce isolation
- Application code filters by `tenant_id`

**Key Tables:**
- `tenants` - Tenant information
- `users` - User accounts
- `clients` - Client records (encrypted PII)
- `bookings` - Booking records
- `conversations` - SMS conversation state
- `sms_messages` - SMS message history
- `audit_logs` - Security audit trail

### Encryption

**PII Encryption:**
- Client emails encrypted with AES-256
- Encryption key stored in environment variable
- Decryption happens in-memory only

**Search Optimization:**
- `email_hash` column for fast lookups
- SHA-256 hash of normalized email
- Indexed for performance

---

## 🔄 Data Flow

### Email Processing Flow

```
Gmail Webhook
    ↓
Email Processor V3
    ↓
Intelligence Modules
    ↓
Claude AI
    ↓
Response Generation
    ↓
Payment Link (if accepted)
    ↓
Draft Email Creation
    ↓
User Review & Send
```

### SMS Booking Flow

```
Twilio Webhook
    ↓
SMS Router
    ↓
Conversation Service
    ↓
Booking Service
    ↓
Calendar Check
    ↓
Payment Link Generation
    ↓
SMS Response
```

### Payment Flow

```
Stripe Webhook
    ↓
Stripe Router
    ↓
Payment Processing
    ↓
Booking Status Update
    ↓
Database Update
    ↓
Audit Log
```

---

## 🔐 Security Architecture

### Authentication

- **JWT Tokens:** HS256 algorithm
- **Token Expiration:** 30 minutes (access), 7 days (refresh)
- **Password Hashing:** bcrypt

### Authorization

- **Role-Based Access Control (RBAC):** Future implementation
- **Tenant Isolation:** RLS policies
- **API Rate Limiting:** Per-IP, per-endpoint

### Data Protection

- **Encryption at Rest:** AES-256 for PII
- **Encryption in Transit:** TLS 1.3
- **Audit Logging:** All actions logged
- **Input Validation:** Pydantic models

---

## 📊 Scalability

### Horizontal Scaling

- **Stateless API:** Can scale horizontally
- **Database Connection Pooling:** SQLAlchemy pool
- **Caching:** Future Redis implementation

### Performance Optimization

- **Database Indexes:** Optimized queries
- **Async Operations:** FastAPI async/await
- **Connection Pooling:** Database connections
- **Query Optimization:** Efficient SQL queries

---

## 🚀 Deployment Architecture

### Backend (Railway)

- **Platform:** Railway (Nixpacks)
- **Processes:**
  - `web` - FastAPI application
  - `worker` - Payment reminder worker
- **Health Checks:** `/api/health` endpoint

### Frontend (Vercel)

- **Platform:** Vercel
- **Build:** Next.js production build
- **CDN:** Global edge network
- **PWA:** Installable on mobile

---

## 🔄 Integration Points

### Gmail Integration

- **OAuth 2.0:** Gmail API access
- **Pub/Sub:** Webhook notifications
- **Scope:** Read, compose, send (draft only)

### Stripe Integration

- **API:** REST API
- **Webhooks:** Payment status updates
- **Features:** Payment links, webhook verification

### Twilio Integration

- **API:** REST API
- **Webhooks:** Incoming SMS
- **Features:** Send/receive SMS, conversation management

### Calendar Integration

- **OAuth 2.0:** Google Calendar API
- **Features:** Event creation, conflict detection, availability

---

## 📈 Monitoring & Observability

### Logging

- **Application Logs:** Structured JSON logs
- **Audit Logs:** Security and compliance
- **Error Tracking:** Sentry integration (future)

### Metrics

- **API Response Times:** Tracked per endpoint
- **Database Query Performance:** Monitored
- **Error Rates:** Tracked and alerted

### Health Checks

- **Endpoint:** `/api/health`
- **Checks:** Database connectivity, external APIs
- **Status:** 200 OK if healthy

---

## 🔮 Future Architecture

### Planned Enhancements

1. **Redis Caching:** Performance optimization
2. **Message Queue:** Background job processing
3. **Microservices:** Service decomposition (if needed)
4. **GraphQL API:** Alternative to REST
5. **Real-time Updates:** WebSocket support

---

## 📚 Related Documentation

- `MASTER_HANDOFF.md` - Complete handoff guide
- `backend/OMEGA_OVERVIEW.md` - Detailed system overview
- `DEPLOYMENT_PIPELINE.md` - Deployment procedures
- `PRODUCT_STRATEGY.md` - Product roadmap

---

**Version:** 3.5.0  
**Status:** Production  
**Maintained By:** Architecture Team

