# Maya Backend - Import Issues Report

**Total Issues Found:** 16

## Missing Symbol (15)

### app.guardians.guardian_daemon
- **Import:** `from app.database import get_async_session`
- **Missing Symbol:** `get_async_session`
- **Target File:** `app\database.py`

### app.main
- **Import:** `from app.routers import gmail`
- **Missing Symbol:** `gmail`
- **Target File:** `app\routers\__init__.py`

### app.main
- **Import:** `from app.routers import calendar`
- **Missing Symbol:** `calendar`
- **Target File:** `app\routers\__init__.py`

### app.main
- **Import:** `from app.routers import health`
- **Missing Symbol:** `health`
- **Target File:** `app\routers\__init__.py`

### app.main
- **Import:** `from app.routers import auth`
- **Missing Symbol:** `auth`
- **Target File:** `app\routers\__init__.py`

### app.main
- **Import:** `from app.routers import clients`
- **Missing Symbol:** `clients`
- **Target File:** `app\routers\__init__.py`

### app.main
- **Import:** `from app.routers import agents`
- **Missing Symbol:** `agents`
- **Target File:** `app\routers\__init__.py`

### app.main
- **Import:** `from app.routers import metrics`
- **Missing Symbol:** `metrics`
- **Target File:** `app\routers\__init__.py`

### app.main
- **Import:** `from app.routers import unsafe_threads`
- **Missing Symbol:** `unsafe_threads`
- **Target File:** `app\routers\__init__.py`

### app.main
- **Import:** `from app.routers import stripe`
- **Missing Symbol:** `stripe`
- **Target File:** `app\routers\__init__.py`

### app.main
- **Import:** `from app.routers import sms`
- **Missing Symbol:** `sms`
- **Target File:** `app\routers\__init__.py`

### app.main
- **Import:** `from app.routers import bookings`
- **Missing Symbol:** `bookings`
- **Target File:** `app\routers\__init__.py`

### app.routers.bookings
- **Import:** `from app.routers.auth import get_current_user`
- **Missing Symbol:** `get_current_user`
- **Target File:** `app\routers\auth.py`

### app.routers.metrics
- **Import:** `from app.database import get_async_session`
- **Missing Symbol:** `get_async_session`
- **Target File:** `app\database.py`

### app.routers.unsafe_threads
- **Import:** `from app.database import get_async_session`
- **Missing Symbol:** `get_async_session`
- **Target File:** `app\database.py`

## Missing Module (1)

### app.routers.clients
- **Import:** `from app.services.encryption import get_encryption_service`

