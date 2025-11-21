# BACKEND ENVIRONMENT VARIABLES REQUIRED
**Date:** 2025-01-27  
**Purpose:** Complete list of environment variables required for MayAssistant backend deployment

---

## CRITICAL (Required for Startup)

These variables MUST be set or the application will fail to start:

### Database
```bash
DATABASE_URL=postgresql://user:password@host:port/database
# Example: postgresql://postgres:password@db.supabase.co:5432/postgres
```

### Application
```bash
DEFAULT_TENANT_ID=your-tenant-uuid-here
# Example: 550e8400-e29b-41d4-a716-446655440000
```

### Security
```bash
JWT_SECRET_KEY=your-secret-key-min-32-chars
# Example: your-super-secret-jwt-key-that-is-at-least-32-characters-long

ENCRYPTION_KEY=your-fernet-key-base64-encoded
# Generate with: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
# Example: gAAAAABh... (44 characters, base64)
```

### AI Services
```bash
ANTHROPIC_API_KEY=sk-ant-api03-...
# Get from: https://console.anthropic.com/
```

### Gmail Integration
```bash
GMAIL_WEBHOOK_URL=https://your-domain.com/api/gmail/webhook
# Example: https://maya-ai-production.up.railway.app/api/gmail/webhook

GMAIL_PUBSUB_TOPIC=projects/your-project/topics/gmail-notifications
# Example: projects/maya-ai/topics/gmail-notifications

GMAIL_PUBSUB_SERVICE_ACCOUNT=your-service-account@your-project.iam.gserviceaccount.com
# Example: maya-ai@maya-ai-project.iam.gserviceaccount.com
```

---

## OPTIONAL (For Full Functionality)

### OpenAI (Hybrid LLM)
```bash
OPENAI_API_KEY=sk-...
# Optional: Enables hybrid LLM mode (Claude + OpenAI)
```

### Stripe (Payment Processing)
```bash
STRIPE_API_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### Twilio (SMS Integration)
```bash
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_PHONE_NUMBER=+1234567890
```

### Microservices
```bash
NOVA_API_URL=https://nova-service.example.com
ELI_API_URL=https://eli-service.example.com
```

### Google OAuth (SSO)
```bash
GOOGLE_OAUTH_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret
GOOGLE_OAUTH_REDIRECT_URI=https://your-domain.com/auth/google/callback
```

### Microsoft OAuth (SSO)
```bash
MICROSOFT_OAUTH_CLIENT_ID=your-client-id
MICROSOFT_OAUTH_CLIENT_SECRET=your-client-secret
MICROSOFT_OAUTH_REDIRECT_URI=https://your-domain.com/auth/microsoft/callback
MICROSOFT_OAUTH_TENANT=common
```

### Application Settings
```bash
DEBUG=false
# Set to true for development, false for production

APP_NAME=MayAssistant
APP_VERSION=1.2.0

CLAUDE_MODEL=claude-sonnet-4-20250514
CLAUDE_MAX_TOKENS=4096

OPENAI_MODEL=gpt-4o

RATE_LIMIT_PER_MINUTE=100
RATE_LIMIT_WEBHOOK_PER_MINUTE=100
RATE_LIMIT_CALENDAR_PER_MINUTE=50

USE_HYBRID_LLM=true
HYBRID_LLM_FALLBACK_ENABLED=true

SAFE_MODE_ENABLED=false
SAFE_MODE_REASON=
```

---

## RAILWAY DEPLOYMENT

### Setting Environment Variables in Railway

1. **Via Railway Dashboard:**
   - Go to your Railway project
   - Select your service
   - Click "Variables" tab
   - Add each variable with its value
   - Click "Deploy" to apply changes

2. **Via Railway CLI:**
```bash
railway variables set DATABASE_URL=postgresql://...
railway variables set DEFAULT_TENANT_ID=...
railway variables set JWT_SECRET_KEY=...
# ... etc
```

3. **Via .env file (local development):**
```bash
# Create backend/.env file
DATABASE_URL=postgresql://...
DEFAULT_TENANT_ID=...
JWT_SECRET_KEY=...
# ... etc
```

---

## ENVIRONMENT VARIABLE VALIDATION

### Required Variables Checklist

- [ ] `DATABASE_URL` - PostgreSQL connection string
- [ ] `DEFAULT_TENANT_ID` - Tenant UUID
- [ ] `JWT_SECRET_KEY` - JWT signing key (min 32 chars)
- [ ] `ENCRYPTION_KEY` - Fernet key (44 chars, base64)
- [ ] `ANTHROPIC_API_KEY` - Claude API key
- [ ] `GMAIL_WEBHOOK_URL` - Gmail webhook URL
- [ ] `GMAIL_PUBSUB_TOPIC` - Gmail Pub/Sub topic
- [ ] `GMAIL_PUBSUB_SERVICE_ACCOUNT` - Service account email

### Optional Variables Checklist

- [ ] `OPENAI_API_KEY` - OpenAI API key (hybrid LLM)
- [ ] `STRIPE_API_KEY` - Stripe secret key
- [ ] `STRIPE_PUBLISHABLE_KEY` - Stripe publishable key
- [ ] `STRIPE_WEBHOOK_SECRET` - Stripe webhook secret
- [ ] `TWILIO_ACCOUNT_SID` - Twilio account SID
- [ ] `TWILIO_AUTH_TOKEN` - Twilio auth token
- [ ] `TWILIO_PHONE_NUMBER` - Twilio phone number
- [ ] `NOVA_API_URL` - Nova microservice URL
- [ ] `ELI_API_URL` - Eli microservice URL

---

## SECURITY NOTES

1. **Never commit `.env` files to git**
2. **Use Railway secrets** for sensitive values
3. **Rotate keys regularly** (especially JWT_SECRET_KEY and ENCRYPTION_KEY)
4. **Use different keys** for staging and production
5. **Encryption key** must be kept secure - if lost, encrypted data cannot be decrypted

---

## GENERATING ENCRYPTION KEY

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

This will output a 44-character base64-encoded key. Save this securely.

---

**END OF ENVIRONMENT VARIABLES DOCUMENTATION**

