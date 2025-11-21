# 🤝 GILMAN ACCORDS

**Project Standards & Agreements**  
**Version:** 1.0  
**Last Updated:** 2025-01-27

---

## 📋 Purpose

The **Gilman Accords** establish the core principles, standards, and agreements that govern the development, operation, and maintenance of the MAYA/OMEGA system. These accords ensure consistency, quality, and safety across all development work.

---

## 🎯 Core Principles

### 1. Safety First
- **NEVER** auto-send emails to real clients (only test: `channkun@gmail.com`)
- **NEVER** bypass Safe Mode
- **NEVER** hallucinate prices, dates, times, or venues
- **ALWAYS** audit log everything
- **ALWAYS** verify before destructive operations

### 2. Data Integrity
- **NEVER** modify production data without backup
- **ALWAYS** use transactions for multi-step operations
- **ALWAYS** validate input data
- **ALWAYS** encrypt PII (AES-256)

### 3. Code Quality
- **ALWAYS** write tests for new features
- **ALWAYS** document complex logic
- **ALWAYS** follow existing patterns
- **ALWAYS** handle errors gracefully

### 4. Security
- **NEVER** commit secrets to git
- **ALWAYS** use environment variables for config
- **ALWAYS** use parameterized queries
- **ALWAYS** validate user input

---

## 📐 Coding Standards

### Python (Backend)

**Style:**
- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use `snake_case` for functions and variables
- Use `PascalCase` for classes

**Error Handling:**
```python
try:
    result = risky_operation()
except SpecificException as e:
    logger.error(f"Operation failed: {e}")
    raise HTTPException(status_code=500, detail="Operation failed")
```

**Async/Await:**
- Use `async`/`await` for I/O operations
- Use `httpx` for HTTP requests (not `requests`)
- Use `tenacity` for retries

### TypeScript (Frontend)

**Style:**
- Use TypeScript strict mode
- Use `camelCase` for variables and functions
- Use `PascalCase` for components
- Maximum line length: 100 characters

**Components:**
```typescript
'use client'; // For client components

interface ComponentProps {
  prop1: string;
  prop2?: number;
}

export function Component({ prop1, prop2 }: ComponentProps) {
  // Component logic
}
```

---

## 🗄️ Database Standards

### Naming Conventions
- Tables: `snake_case`, plural (e.g., `clients`, `bookings`)
- Columns: `snake_case` (e.g., `client_email`, `payment_status`)
- Indexes: `idx_table_column` (e.g., `idx_clients_email_hash`)
- Foreign Keys: `fk_table_column` (e.g., `fk_bookings_tenant_id`)

### Multi-Tenancy
- **ALWAYS** include `tenant_id` in queries
- **ALWAYS** use Row-Level Security (RLS) policies
- **ALWAYS** filter by `tenant_id` in application code

### Migrations
- **ALWAYS** make migrations idempotent (`IF NOT EXISTS`)
- **ALWAYS** test migrations on staging first
- **ALWAYS** backup database before migrations
- **ALWAYS** document migration purpose

---

## 🔐 Security Standards

### Authentication
- Use JWT tokens (HS256)
- Token expiration: 30 minutes (access), 7 days (refresh)
- **NEVER** store passwords in plain text
- Use bcrypt for password hashing

### Encryption
- Use AES-256 (Fernet) for PII
- **NEVER** log encrypted data
- **ALWAYS** decrypt in memory only
- Rotate encryption keys periodically

### API Security
- **ALWAYS** use HTTPS in production
- **ALWAYS** validate JWT tokens
- **ALWAYS** use rate limiting
- **ALWAYS** sanitize user input

---

## 📝 Documentation Standards

### Code Documentation
- **ALWAYS** document public functions
- **ALWAYS** document complex algorithms
- **ALWAYS** include examples in docstrings
- **ALWAYS** update docs when code changes

### API Documentation
- Use OpenAPI/Swagger for API docs
- Include request/response examples
- Document error codes
- Document rate limits

### Commit Messages
- Format: `type: description`
- Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
- Examples:
  - `feat: add payment reminder worker`
  - `fix: correct email search hash calculation`
  - `docs: update deployment guide`

---

## 🧪 Testing Standards

### Backend Tests
- **ALWAYS** write tests for new features
- Use `pytest` for Python tests
- Aim for 80%+ code coverage
- Test edge cases and error conditions

### Frontend Tests
- Test user interactions
- Test API integration
- Test error states
- Test loading states

### Integration Tests
- Test complete workflows
- Test API endpoints
- Test database operations
- Test external integrations

---

## 🚀 Deployment Standards

### Pre-Deployment
- [ ] All tests passing
- [ ] Environment variables set
- [ ] Database migrations applied
- [ ] Documentation updated
- [ ] Security review completed

### Deployment Process
1. Deploy to staging first
2. Run smoke tests
3. Monitor for errors
4. Deploy to production
5. Verify health checks
6. Monitor for 24 hours

### Rollback Plan
- **ALWAYS** have rollback plan
- **ALWAYS** backup database before deployment
- **ALWAYS** test rollback procedure

---

## 📊 Monitoring Standards

### Logging
- **ALWAYS** log errors with context
- **ALWAYS** use structured logging
- **ALWAYS** include trace IDs
- **NEVER** log sensitive data

### Metrics
- Monitor API response times
- Monitor error rates
- Monitor database performance
- Monitor external API calls

### Alerts
- Set up alerts for errors
- Set up alerts for high latency
- Set up alerts for failed payments
- Set up alerts for system downtime

---

## 🔄 Version Control Standards

### Branch Strategy
- `main` - Production code
- `develop` - Development branch
- `feature/*` - Feature branches
- `fix/*` - Bug fix branches

### Pull Requests
- **ALWAYS** create PR for changes
- **ALWAYS** get code review
- **ALWAYS** run tests before merging
- **ALWAYS** update documentation

### Git Hygiene
- **NEVER** commit secrets
- **NEVER** commit large files
- **ALWAYS** use `.gitignore`
- **ALWAYS** write descriptive commit messages

---

## 🎨 UI/UX Standards

### Accessibility
- **ALWAYS** use semantic HTML
- **ALWAYS** provide alt text for images
- **ALWAYS** ensure keyboard navigation
- **ALWAYS** test with screen readers

### Mobile First
- **ALWAYS** design mobile-first
- **ALWAYS** use 48px touch targets
- **ALWAYS** test on real devices
- **ALWAYS** optimize for performance

### Design System
- Use TailwindCSS for styling
- Follow consistent spacing (4px grid)
- Use consistent colors (see `UX_GUIDELINES.md`)
- Use consistent typography

---

## 🤖 AI Agent Standards

### Safe Mode
- **NEVER** bypass Safe Mode
- **ALWAYS** respect Safe Mode activation
- **ALWAYS** log Safe Mode events
- **ALWAYS** notify admins on activation

### Agent Communication
- **ALWAYS** use audit logging
- **ALWAYS** include trace IDs
- **ALWAYS** handle errors gracefully
- **ALWAYS** respect rate limits

### Claude Integration
- **ALWAYS** use system prompts
- **ALWAYS** sanitize responses
- **ALWAYS** validate AI output
- **ALWAYS** log AI interactions

---

## 📋 Compliance Checklist

Before any production change:

- [ ] Code follows style guide
- [ ] Tests are written and passing
- [ ] Documentation is updated
- [ ] Security review completed
- [ ] Database migrations tested
- [ ] Environment variables documented
- [ ] Rollback plan prepared
- [ ] Monitoring configured
- [ ] Alerts set up

---

## 🔄 Review & Updates

This document should be reviewed and updated:
- Quarterly
- When new standards are established
- When issues are discovered
- When team feedback is received

**Last Review:** 2025-01-27  
**Next Review:** 2025-04-27

---

## 📞 Questions?

If you have questions about these standards:
1. Check existing documentation
2. Ask team lead
3. Update this document if needed

---

**Version:** 1.0  
**Status:** Active  
**Maintained By:** Development Team

