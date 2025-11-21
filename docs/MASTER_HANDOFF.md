# 🎯 MASTER HANDOFF DOCUMENTATION

**Project:** MAYA v3.5 / OMEGA Core v3.0  
**Date:** 2025-01-27  
**Status:** Production Ready  
**Version:** 3.5.0

---

## 📋 Executive Summary

This document provides a complete handoff guide for developers, AI assistants, and team members taking over the MAYA/OMEGA project. It covers system architecture, critical components, deployment procedures, and operational knowledge.

---

## 🏗️ System Overview

### What is MAYA/OMEGA?

**MAYA** (MayAssistant) is an AI-powered email and SMS assistant for DJ Skinny (Greg) at Skinny Man Entertainment. It's built on **OMEGA Core v3.0**, a multi-agent AI operations system that coordinates 10 specialized agents.

### Core Capabilities

- ✅ **Email Processing** - Automated email analysis, response generation, booking detection
- ✅ **SMS Booking Flow** - Complete state machine for SMS-based bookings
- ✅ **Payment Integration** - Stripe payment links with automated reminders
- ✅ **Calendar Management** - Auto-blocking, conflict detection, availability checks
- ✅ **Client Management** - Encrypted PII, search optimization, relationship tracking
- ✅ **Security** - JWT auth, AES-256 encryption, audit logging, rate limiting

---

## 🏛️ Architecture

### Technology Stack

**Backend:**
- **Framework:** FastAPI (Python 3.14)
- **Database:** PostgreSQL (Supabase)
- **AI:** Anthropic Claude Sonnet 4
- **Deployment:** Railway
- **Workers:** Background tasks (payment reminders, email retry)

**Frontend:**
- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** TailwindCSS
- **Deployment:** Vercel
- **PWA:** Installable mobile app

**Integrations:**
- **Stripe:** Payment processing
- **Twilio:** SMS messaging
- **Gmail API:** Email processing
- **Google Calendar:** Scheduling

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ Dashboard │  │ Bookings │  │ Messages │              │
│  └─────┬─────┘  └─────┬────┘  └─────┬────┘              │
└────────┼──────────────┼──────────────┼───────────────────┘
         │              │              │
         └──────────────┼──────────────┘
                        │
         ┌──────────────▼──────────────┐
         │   Backend API (FastAPI)     │
         │  ┌────────────────────────┐  │
         │  │  Email Processor V3   │  │
         │  │  - Acceptance Detect  │  │
         │  │  - Context Reconstruct│  │
         │  │  - Venue Intelligence │  │
         │  └───────────┬────────────┘  │
         │              │               │
         │  ┌───────────▼────────────┐  │
         │  │  Stripe Service       │  │
         │  │  SMS Service          │  │
         │  │  Booking Service      │  │
         │  └───────────┬────────────┘  │
         └──────────────┼───────────────┘
                        │
         ┌──────────────▼──────────────┐
         │   PostgreSQL (Supabase)     │
         │  - Multi-tenant RLS         │
         │  - AES-256 encryption       │
         │  - Audit logging            │
         └─────────────────────────────┘
```

---

## 🔑 Critical Components

### 1. Email Processing Pipeline

**Location:** `backend/app/services/email_processor_v3.py`

**Flow:**
1. Gmail webhook receives email
2. Intelligence modules analyze:
   - Acceptance detection
   - Missing information
   - Venue intelligence
   - Equipment awareness
   - Context reconstruction
3. Claude generates response
4. If acceptance detected → Create Stripe payment link
5. Send draft email (never auto-send)

**Key Methods:**
- `process_email()` - Main processing entry point
- `_extract_booking_details()` - Extract booking info
- `_get_nova_pricing()` - Get pricing from Nova API

### 2. SMS Booking Flow

**Location:** `backend/app/routers/sms.py`, `backend/app/services/booking_service.py`

**State Machine:**
- `initial` → Ask for service type
- `service_selected` → Ask for date
- `date_selected` → Check availability, ask for time
- `time_selected` → Confirm details, create payment link
- `payment_pending` → Wait for payment
- `confirmed` → Booking complete

**Key Methods:**
- `_process_booking_message()` - State machine logic
- `check_availability()` - Calendar availability check
- `create_payment_link_for_booking()` - Stripe integration

### 3. Payment Integration

**Location:** `backend/app/services/stripe_service.py`

**Features:**
- Payment link creation
- Webhook processing
- Payment status tracking
- Automated reminders (Day 3, 7, 14)

**Key Tables:**
- `bookings` - Booking records with payment status
- Reminder columns: `reminder_1_sent`, `reminder_2_sent`, `reminder_3_sent`

### 4. Security Framework

**Components:**
- **JWT Authentication** - `backend/app/routers/auth.py`
- **AES-256 Encryption** - `backend/app/encryption.py`
- **Rate Limiting** - SlowAPI middleware
- **Audit Logging** - `backend/app/services/audit_service.py`
- **Row-Level Security** - PostgreSQL RLS policies

---

## 🗄️ Database Schema

### Key Tables

**clients**
- `id` (UUID, PK)
- `tenant_id` (UUID, FK)
- `email` (encrypted TEXT)
- `email_hash` (TEXT, indexed)
- `name` (TEXT)
- `metadata` (JSONB)

**bookings**
- `id` (UUID, PK)
- `tenant_id` (UUID, FK)
- `booking_id` (TEXT, UNIQUE)
- `client_email` (TEXT)
- `payment_status` (TEXT: pending/paid/failed/refunded)
- `stripe_payment_link_id` (TEXT)
- `reminder_1_sent`, `reminder_2_sent`, `reminder_3_sent` (BOOLEAN)

**conversations**
- `id` (UUID, PK)
- `tenant_id` (UUID, FK)
- `phone_number` (TEXT, UNIQUE)
- `conversation_state` (TEXT)
- `metadata` (JSONB)

**sms_messages**
- `id` (UUID, PK)
- `conversation_id` (UUID, FK)
- `body` (TEXT)
- `direction` (TEXT: inbound/outbound)

### Migrations

All migrations in `backend/migrations/`:
- `001_add_email_hash.sql` - Email search optimization
- `012_add_bookings_table.sql` - Payment integration
- `013_add_reminder_columns.sql` - Payment reminders
- `014_add_conversations_table.sql` - SMS flow

**Apply migrations:**
```bash
cd backend
python apply_bookings_migration.py
python apply_conversations_migration.py
python apply_reminder_migration.py
```

---

## 🚀 Deployment

### Backend (Railway)

1. **Set Environment Variables** (see `backend/ENVIRONMENT_VARIABLES.md`)
2. **Deploy:**
   ```bash
   # Railway auto-deploys on git push
   git push origin main
   ```
3. **Verify:**
   - Health check: `https://your-app.up.railway.app/api/health`
   - Check Railway logs

### Frontend (Vercel)

1. **Connect Repository** to Vercel
2. **Set Environment Variables:**
   - `NEXT_PUBLIC_API_URL` - Backend API URL
3. **Deploy:**
   - Auto-deploys on push to `main`
   - Or manual deploy via Vercel dashboard

### Environment Variables

**Critical Variables:**
- `DATABASE_URL` - PostgreSQL connection string
- `JWT_SECRET_KEY` - JWT signing key (min 32 chars)
- `ENCRYPTION_KEY` - Fernet key for AES-256
- `ANTHROPIC_API_KEY` - Claude API key
- `STRIPE_API_KEY` - Stripe secret key
- `TWILIO_ACCOUNT_SID` - Twilio credentials

**See:** `backend/ENVIRONMENT_VARIABLES.md` for complete list

---

## 🔧 Development Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up .env file
cp .env.example .env  # Edit with your values

# Run migrations
python apply_bookings_migration.py
python apply_conversations_migration.py

# Start server
uvicorn app.main:app --reload
```

### Frontend

```bash
cd omega-frontend
npm install

# Set up .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000

# Start dev server
npm run dev
```

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/
```

**Key Test Files:**
- `test_stripe_integration.py` - Payment flow tests
- `test_intelligence.py` - Email intelligence tests
- `test_calendar.py` - Calendar integration tests

### Frontend Tests

```bash
cd omega-frontend
npm run test
```

---

## 🐛 Common Issues & Solutions

### Issue: Email search not working
**Solution:** Run `fix_email_search.py` to add `email_hash` column and backfill

### Issue: Payment links not generating
**Check:**
- Stripe API key is set correctly
- `STRIPE_WEBHOOK_SECRET` is configured
- Booking record is created in database

### Issue: SMS not receiving
**Check:**
- Twilio webhook URL is set correctly
- `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN` are set
- Phone number is verified in Twilio

### Issue: Database connection errors
**Check:**
- `DATABASE_URL` is correct
- SSL mode matches database requirements
- Network access is allowed

---

## 📚 Key Documentation Files

- `backend/OMEGA_OVERVIEW.md` - Complete system architecture
- `backend/CLAUDE_PROGRESS_LOG.md` - Development history
- `backend/DEPLOYMENT_GUIDE.md` - Deployment instructions
- `MAYA_V3_IMPLEMENTATION_COMPLETE.md` - Implementation summary
- `GITHUB_UPLOAD_REPORT.md` - Repository information

---

## 🔐 Security Checklist

- [ ] All environment variables set
- [ ] JWT secret key is strong (32+ chars)
- [ ] Encryption key is generated securely
- [ ] Database has RLS policies enabled
- [ ] Rate limiting is configured
- [ ] Audit logging is active
- [ ] No secrets in code or git history
- [ ] HTTPS enabled in production

---

## 📞 Support & Contacts

**Repository:**
- GitHub: `https://github.com/skinnymanmusic/maya-mobile`
- Original: `https://github.com/skinnymanmusic/maya-core`

**Documentation:**
- All docs in `/docs` directory
- Backend docs in `/backend` directory

---

## ✅ Handoff Checklist

- [x] Architecture documented
- [x] Database schema documented
- [x] Deployment procedures documented
- [x] Environment variables documented
- [x] Common issues documented
- [x] Security checklist provided
- [x] Code is production-ready
- [x] Tests are passing
- [x] Documentation is complete

---

**Last Updated:** 2025-01-27  
**Maintained By:** Development Team  
**Version:** 3.5.0

