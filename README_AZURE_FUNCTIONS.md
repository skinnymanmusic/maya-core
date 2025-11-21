# Maya-Core Azure Functions Structure

This directory contains the Azure Functions implementation for OMEGA 4.0 Maya Core.

## Structure

```
api/
  auth/
    login/          # POST /api/auth/login
    refresh/        # POST /api/auth/refresh
    me/             # GET /api/auth/me
  gmail/
    webhook/        # POST /api/gmail/webhook
  calendar/
    events/         # GET, POST /api/calendar/events
    block/          # POST /api/calendar/block
  clients/         # GET, POST /api/clients
  clients/{id}/    # GET, PUT, DELETE /api/clients/{id}
  agents/          # GET, POST /api/agents
  health/          # GET /api/health

shared/
  auth.js          # Authentication utilities
  database.js      # Database connection pool
  gmail.js         # Gmail webhook utilities
  calendar.js      # Calendar operations
  clients.js       # Client CRUD operations
  agents.js        # Agent management
```

## Setup

1. Install dependencies:
```bash
npm install
```

2. Configure `local.settings.json`:
```json
{
  "Values": {
    "DATABASE_URL": "your-postgresql-connection-string",
    "JWT_SECRET_KEY": "your-jwt-secret",
    "GMAIL_WEBHOOK_URL": "https://your-function-app.azurewebsites.net/api/gmail/webhook",
    "GMAIL_PUBSUB_SERVICE_ACCOUNT": "your-service-account-email"
  }
}
```

3. Run locally:
```bash
func start
```

## Endpoints

### Authentication
- `POST /api/auth/login` - Login with email/password
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/me` - Get current user (requires auth)

### Gmail
- `POST /api/gmail/webhook` - Gmail Pub/Sub webhook (requires JWT)

### Calendar
- `GET /api/calendar/events` - List events
- `POST /api/calendar/events` - Create event
- `POST /api/calendar/block` - Auto-block time for confirmed booking

### Clients
- `GET /api/clients` - List clients
- `POST /api/clients` - Create client
- `GET /api/clients/{id}` - Get client
- `PUT /api/clients/{id}` - Update client
- `DELETE /api/clients/{id}` - Delete client

### Agents
- `GET /api/agents` - List agents
- `POST /api/agents` - Create agent

### Health
- `GET /api/health` - Health check

## Notes

- All endpoints (except `/api/health` and `/api/auth/login`, `/api/auth/refresh`) require authentication
- JWT tokens are validated using the `getCurrentUser` function from `shared/auth.js`
- Database connections use connection pooling via `shared/database.js`
- Email hashing uses SHA-256 for deterministic lookups
- All operations are tenant-scoped using `tenant_id` from JWT payload

