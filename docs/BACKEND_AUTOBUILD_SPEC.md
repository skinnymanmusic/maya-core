# 🏗️ BACKEND AUTOBUILD SPECIFICATION

**FastAPI Build & Deployment Automation**  
**Version:** 1.0  
**Last Updated:** 2025-01-27

---

## 📋 Overview

This document specifies the automated build, test, and deployment pipeline for the MAYA/OMEGA backend application built with FastAPI (Python 3.14).

---

## 🎯 Build Goals

1. **Fast Builds** - Optimize for speed
2. **Reliable Deployments** - Zero-downtime deployments
3. **Quality Assurance** - Automated testing
4. **Performance** - Optimized runtime
5. **Security** - Dependency scanning

---

## 🏗️ Build Architecture

### Technology Stack

- **Framework:** FastAPI (Python 3.14)
- **Database:** PostgreSQL (Supabase)
- **Package Manager:** pip
- **CI/CD:** GitHub Actions
- **Deployment:** Railway

### Build Process

```
Source Code
    ↓
Lint & Type Check
    ↓
Unit Tests
    ↓
Integration Tests
    ↓
Build (Docker/Nixpacks)
    ↓
Security Scan
    ↓
Deploy (Railway)
    ↓
Health Check
    ↓
Production
```

---

## 📦 Build Configuration

### requirements.txt

```txt
# Core
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0

# Database
psycopg2-binary==2.9.9
sqlalchemy==2.0.23

# Authentication
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# HTTP Client
httpx==0.25.0
tenacity==8.2.3

# AI
anthropic==0.7.0

# Payments
stripe==7.8.0

# SMS
twilio==8.10.0

# Security
cryptography==41.0.7
slowapi==0.1.9

# Monitoring
sentry-sdk==1.38.0
```

### nixpacks.toml (Railway)

```toml
[phases.setup]
nixPkgs = ["python314", "postgresql"]

[phases.install]
cmds = [
  "pip install --upgrade pip",
  "pip install -r requirements.txt"
]

[phases.build]
cmds = [
  "python -m pytest tests/ --cov=app --cov-report=xml"
]

[start]
cmd = "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
```

### Procfile

```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
worker: python -m app.workers.payment_reminder_worker
```

---

## 🔄 GitHub Actions Workflow

### .github/workflows/backend-ci.yml

```yaml
name: Backend CI/CD

on:
  push:
    branches: [main, develop]
    paths:
      - 'backend/**'
      - '.github/workflows/backend-ci.yml'
  pull_request:
    branches: [main, develop]
    paths:
      - 'backend/**'

jobs:
  lint-and-typecheck:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: backend
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.14'
          cache: 'pip'
          cache-dependency-path: backend/requirements.txt
      
      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt
          pip install ruff mypy
      
      - name: Run Ruff (linter)
        run: ruff check app/
      
      - name: Run Ruff (formatter)
        run: ruff format --check app/
      
      - name: Run MyPy (type check)
        run: mypy app/ --ignore-missing-imports

  test:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: backend
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.14'
          cache: 'pip'
          cache-dependency-path: backend/requirements.txt
      
      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-asyncio
      
      - name: Run unit tests
        run: pytest tests/unit/ -v --cov=app --cov-report=xml
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
          JWT_SECRET_KEY: test-secret-key-min-32-characters-long
          ENCRYPTION_KEY: test-encryption-key-base64-encoded-32-chars
      
      - name: Run integration tests
        run: pytest tests/integration/ -v
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
          JWT_SECRET_KEY: test-secret-key-min-32-characters-long
          ENCRYPTION_KEY: test-encryption-key-base64-encoded-32-chars
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./backend/coverage.xml
          flags: backend

  security-scan:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: backend
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.14'
      
      - name: Install safety
        run: pip install safety
      
      - name: Run safety check
        run: safety check --file requirements.txt
      
      - name: Run Bandit (security linter)
        run: |
          pip install bandit
          bandit -r app/ -f json -o bandit-report.json
      
      - name: Upload Bandit report
        uses: actions/upload-artifact@v3
        with:
          name: bandit-report
          path: backend/bandit-report.json

  build:
    runs-on: ubuntu-latest
    needs: [lint-and-typecheck, test]
    defaults:
      run:
        working-directory: backend
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.14'
      
      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: Verify imports
        run: python -c "import app.main; print('✓ Imports successful')"
      
      - name: Check database migrations
        run: |
          python -c "
          import os
          migrations = [f for f in os.listdir('migrations') if f.endswith('.sql')]
          print(f'✓ Found {len(migrations)} migrations')
          "

  deploy:
    runs-on: ubuntu-latest
    needs: [build, security-scan]
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to Railway
        uses: bervProject/railway-deploy@master
        with:
          railway_token: ${{ secrets.RAILWAY_TOKEN }}
          service: maya-backend
          detach: true
```

---

## 🧪 Testing Strategy

### Unit Tests

**Framework:** pytest

**Test Structure:**
```
tests/
  unit/
    test_services/
    test_routers/
    test_utils/
  integration/
    test_api/
    test_workflows/
```

**Example:**
```python
import pytest
from app.services.stripe_service import StripeService

def test_create_payment_link():
    service = StripeService()
    result = service.create_payment_link(
        amount=100.00,
        description="Test booking"
    )
    assert result["payment_link_url"] is not None
```

### Integration Tests

**Database Setup:**
- Use test database
- Run migrations before tests
- Clean up after tests

**Example:**
```python
@pytest.mark.asyncio
async def test_booking_flow():
    # Create booking
    # Verify in database
    # Check payment link created
    # Verify status
```

### Coverage Goals

- **Statements:** 80%+
- **Branches:** 75%+
- **Functions:** 80%+
- **Lines:** 80%+

---

## 📊 Build Optimization

### Dependency Management

- Pin exact versions
- Regular security updates
- Use `pip-tools` for dependency resolution

### Code Optimization

- Use async/await for I/O
- Connection pooling
- Query optimization
- Caching where appropriate

### Performance Targets

- **API Response Time:** < 200ms (p95)
- **Database Query Time:** < 50ms (p95)
- **Memory Usage:** < 512MB
- **CPU Usage:** < 50% average

---

## 🔐 Security

### Dependency Scanning

**Automated:**
- Safety check in CI
- Bandit security linter
- Dependabot alerts

**Manual:**
- Regular dependency updates
- Review security advisories

### Code Security

- No secrets in code
- Environment variables only
- Input validation
- SQL injection prevention (parameterized queries)
- XSS prevention
- CSRF protection

---

## 🚀 Deployment

### Railway Configuration

**railway.json:**
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r requirements.txt"
  },
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/api/health",
    "healthcheckTimeout": 100
  }
}
```

### Deployment Process

1. **Push to main** → Triggers workflow
2. **Run tests** → Lint, type-check, unit tests, integration tests
3. **Build** → Verify imports, check migrations
4. **Security scan** → Safety, Bandit
5. **Deploy** → Railway deployment
6. **Health check** → Verify deployment
7. **Production** → Live API

### Environment Variables

**Required:**
- `DATABASE_URL` - PostgreSQL connection
- `JWT_SECRET_KEY` - JWT signing key
- `ENCRYPTION_KEY` - AES-256 encryption key
- `ANTHROPIC_API_KEY` - Claude API key
- `STRIPE_API_KEY` - Stripe secret key
- `TWILIO_ACCOUNT_SID` - Twilio credentials

**See:** `backend/ENVIRONMENT_VARIABLES.md`

### Rollback Strategy

**Railway:**
- Automatic rollback on health check failure
- Manual rollback via dashboard
- Previous deployments available

**Git:**
- Revert commit
- Push to trigger new deployment

---

## 📈 Monitoring

### Build Metrics

- Build duration
- Test execution time
- Deployment frequency
- Success rate

### Runtime Monitoring

- Railway metrics
- Application logs
- Error tracking (Sentry)
- Performance monitoring

---

## 🐛 Troubleshooting

### Build Failures

**Common Issues:**
- Import errors → Fix imports
- Test failures → Fix failing tests
- Dependency issues → Update requirements.txt
- Migration errors → Check SQL syntax

### Deployment Issues

**Common Issues:**
- Environment variables missing → Check Railway settings
- Database connection errors → Check DATABASE_URL
- Health check failures → Check application logs

---

## ✅ Checklist

Before merging to main:

- [ ] All tests passing
- [ ] No linting errors
- [ ] No type errors
- [ ] Security scan passed
- [ ] Migrations tested
- [ ] Environment variables documented
- [ ] Documentation updated

---

**Version:** 1.0  
**Status:** Active  
**Maintained By:** Backend Team

