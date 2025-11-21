# PHASE 0B: BASIC TESTS EXECUTION PLAN
**Date:** 2025-01-27  
**Status:** READY FOR EXECUTION

---

## REQUIRED TESTS: 9/9 BASIC TESTS

### Test Categories:

**1. Email Search Tests (3 tests)**
- Test email hash lookup by email address
- Test client lookup by email hash
- Test email search returns correct client

**2. Thread Reconstruction Tests (3 tests)**
- Test thread reconstruction by thread_id
- Test thread history retrieval
- Test multi-email thread linking

**3. Multi-Account Matching Tests (3 tests)**
- Test client matching across multiple Gmail accounts
- Test email routing to correct account
- Test account-specific behavior (auto-send vs draft)

---

## CURRENT TEST STATUS

**Issue:** Tests require environment variables:
- `GMAIL_WEBHOOK_URL` (required)
- `GMAIL_PUBSUB_TOPIC` (required)
- `GMAIL_PUBSUB_SERVICE_ACCOUNT` (required)
- `DATABASE_URL` (required)
- `ENCRYPTION_KEY` (required)
- `DEFAULT_TENANT_ID` (required)
- `JWT_SECRET_KEY` (required)
- `ANTHROPIC_API_KEY` (required)

**Test Files Found:**
- `test_pipeline.py` - Placeholder tests (4 tests, all `assert True`)
- `test_intelligence.py` - Placeholder tests (3 tests, all `assert True`)
- `test_archivus_service.py` - Has `test_thread_summarization()`
- Other test files exist but are mostly placeholders

**Gap:** The specific 9/9 basic tests for email search, thread reconstruction, and multi-account matching are not yet implemented as real tests.

---

## RECOMMENDATION

**Option 1:** Create the 9 basic tests now (requires environment variables)
**Option 2:** Document test requirements and proceed to Phase 1 (full test suite)
**Option 3:** Skip to Phase 1 if environment variables are not available

---

**END OF PHASE 0B TEST PLAN**

**Status:** AWAITING DECISION - Tests need environment variables or test implementation

