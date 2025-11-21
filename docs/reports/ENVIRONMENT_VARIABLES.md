# Environment Variables Reference

## Backend Environment Variables

Create a `.env` file in the `backend/` directory with these variables:

```bash
# Application
APP_NAME=OMEGA Core v3.0
APP_VERSION=3.0.0
DEBUG=false

# Database
DATABASE_URL=postgresql://user:password@host:port/dbname
DATABASE_SSL=true

# Default Tenant
DEFAULT_TENANT_ID=your-tenant-uuid-here

# JWT Authentication
JWT_SECRET_KEY=your-secret-key-minimum-32-characters-long
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Encryption (Fernet key - generate with: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
ENCRYPTION_KEY=your-fernet-key-base64-encoded

# Anthropic Claude
ANTHROPIC_API_KEY=sk-ant-api03-...
CLAUDE_MODEL=claude-sonnet-4-20250514
CLAUDE_MAX_TOKENS=4096

# OpenAI (Optional - for Hybrid LLM)
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o

# Google APIs
GMAIL_WEBHOOK_URL=https://your-railway-url.up.railway.app/api/gmail/webhook
GMAIL_PUBSUB_TOPIC=projects/PROJECT/topics/TOPIC
GMAIL_PUBSUB_SERVICE_ACCOUNT=service-account@project.iam.gserviceaccount.com

# Google OAuth (Optional - for SSO)
GOOGLE_OAUTH_CLIENT_ID=
GOOGLE_OAUTH_CLIENT_SECRET=
GOOGLE_OAUTH_REDIRECT_URI=

# Microsoft OAuth (Optional - for SSO)
MICROSOFT_OAUTH_CLIENT_ID=
MICROSOFT_OAUTH_CLIENT_SECRET=
MICROSOFT_OAUTH_REDIRECT_URI=
MICROSOFT_OAUTH_TENANT=common

# Stripe
STRIPE_API_KEY=sk_test_... # Use sk_live_... in production
STRIPE_PUBLISHABLE_KEY=pk_test_... # Use pk_live_... in production
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_BUSINESS_NAME=Skinny Man Entertainment
STRIPE_BUSINESS_SUPPORT_EMAIL=maya@skinnymanmusic.com
STRIPE_BUSINESS_RETURN_URL=https://mayassistant.com/booking-confirmed

# Twilio
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_PHONE_NUMBER=+12345678900

# External APIs (Optional)
NOVA_API_URL=
ELI_API_URL=

# Rate Limiting
RATE_LIMIT_PER_MINUTE=100
RATE_LIMIT_WEBHOOK_PER_MINUTE=100
RATE_LIMIT_CALENDAR_PER_MINUTE=50

# Safe Mode
SAFE_MODE_ENABLED=false
SAFE_MODE_REASON=

# LLM Task Routing
USE_HYBRID_LLM=true
HYBRID_LLM_FALLBACK_ENABLED=true
```

## Frontend Environment Variables

Create a `.env.production` file in the `omega-frontend/` directory:

```bash
# Backend API URL (Railway deployment)
NEXT_PUBLIC_OMEGA_BACKEND=https://your-railway-url.up.railway.app

# Frontend App URL (Vercel deployment)
NEXT_PUBLIC_APP_URL=https://mayassistant.com
```

## Generating Encryption Key

To generate a Fernet encryption key:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

## Security Notes

- **NEVER** commit `.env` files to git
- Use strong, random values for secrets
- JWT_SECRET_KEY should be at least 32 characters
- Use production API keys in production (not test keys)
- Rotate secrets regularly

