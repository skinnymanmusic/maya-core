# Maya Backend - Dependency Audit

## Summary

- **Total packages in requirements.txt:** 35
- **Used packages:** 14
- **Potentially unused packages:** 21
- **Possibly missing dependencies:** 4

## Used Dependencies ✅

| Package | Version | Status |
|---------|---------|--------|
| anthropic | 0.39.0 | ✅ Used |
| cryptography | 43.0.1 | ✅ Used |
| fastapi | 0.115.0 | ✅ Used |
| google_api_python_client | 2.150.0 | ✅ Used |
| httpx | 0.27.2 | ✅ Used |
| passlib | 1.7.4 | ✅ Used |
| pydantic | 2.9.2 | ✅ Used |
| pydantic_settings | 2.5.2 | ✅ Used |
| pyjwt | 2.9.0 | ✅ Used |
| slowapi | 0.1.9 | ✅ Used |
| sqlalchemy | 2.0.36 | ✅ Used |
| stripe | 7.8.0 | ✅ Used |
| tenacity | 8.2.3 | ✅ Used |
| twilio | 8.10.0 | ✅ Used |

## Potentially Unused Dependencies ⚠️

These packages are in requirements.txt but not directly imported in code.
**NOTE:** They might still be needed as transitive dependencies or for runtime.

| Package | Version | Original Line |
|---------|---------|---------------|
| asyncpg | 0.29.0 | `asyncpg==0.29.0` |
| bcrypt | 4.2.0 | `bcrypt==4.2.0` |
| black | 24.10.0 | `black==24.10.0` |
| email_validator | 2.1.0 | `email-validator==2.1.0` |
| flake8 | 7.1.1 | `flake8==7.1.1` |
| google_auth | 2.34.0 | `google-auth==2.34.0` |
| google_auth_httplib2 | 0.2.0 | `google-auth-httplib2==0.2.0` |
| google_auth_oauthlib | 1.2.1 | `google-auth-oauthlib==1.2.1` |
| mypy | 1.11.2 | `mypy==1.11.2` |
| openai | 1.51.0 | `openai==1.51.0` |
| psycopg2_binary | 2.9.10 | `psycopg2-binary==2.9.10` |
| pytest | 8.3.3 | `pytest==8.3.3` |
| pytest_asyncio | 0.24.0 | `pytest-asyncio==0.24.0` |
| pytest_cov | 6.0.0 | `pytest-cov==6.0.0` |
| python_dateutil | 2.9.0. | `python-dateutil==2.9.0.post0` |
| python_dotenv | 1.0.1 | `python-dotenv==1.0.1` |
| python_jose | 3.3.0 | `python-jose[cryptography]==3.3.0` |
| python_multipart | 0.0.9 | `python-multipart==0.0.9` |
| pytz | 2024.2 | `pytz==2024.2` |
| uvicorn | 0.32.0 | `uvicorn[standard]==0.32.0` |
| uvloop | 0.20.0 | `uvloop==0.20.0` |

## Possibly Missing Dependencies ❌

These are imported in code but not found in requirements.txt:

- `____________`
- `google`
- `psycopg2`
- `starlette`

## Recommendations

### Safe to Remove (After Review)

⚠️ **DO NOT auto-remove** - These might be:
- Transitive dependencies needed at runtime
- Test/dev dependencies
- CLI tools that aren't directly imported

Review each unused package carefully before removal.

### Python 3.11 Compatibility

All dependencies have been verified for Python 3.11 compatibility.
Critical: `asyncpg==0.29.0` REQUIRES Python 3.11 (does not work with 3.13).

