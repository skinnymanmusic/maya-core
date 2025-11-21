# PHASE 0: EMAIL SEARCH FIX - EXECUTION PLAN
**Date:** 2025-01-27  
**Mode:** EXECUTION MODE - PHASE 0 (SOLIN v2)  
**Status:** READY FOR EXECUTION - AWAITING FINAL APPROVAL

---

## EXECUTION PLAN

### Step 1: SQL Migration File Created ✅
**File:** `backend/migrations/015_add_clients_email_hash.sql`

**SQL Operations:**
```sql
-- 1. Add email_hash column (IF NOT EXISTS - safe)
ALTER TABLE clients 
ADD COLUMN IF NOT EXISTS email_hash TEXT;

-- 2. Create index for efficient lookups (IF NOT EXISTS - safe)
CREATE INDEX IF NOT EXISTS idx_clients_tenant_id_email_hash 
ON clients (tenant_id, email_hash);

-- 3. Add documentation comment
COMMENT ON COLUMN clients.email_hash IS 'SHA256 hash of email (lowercase, trimmed) for deterministic lookup';
```

**Safety:** All operations use `IF NOT EXISTS` - idempotent and safe to run multiple times.

---

### Step 2: Python Backfill Script Execution

**Script:** `backend/fix_email_search.py`

**Operations:**
1. Connect to database using `DATABASE_URL` environment variable
2. Verify `email_hash` column exists (or create it)
3. Verify index exists (or create it)
4. Query all clients where `email_hash IS NULL AND email IS NOT NULL`
5. For each client:
   - Decrypt `email` using encryption service
   - Hash email: `SHA256(email.lower().strip())`
   - Update `clients.email_hash = <hash>`
6. Verify all clients have `email_hash` populated
7. Report results

**Expected Output:**
```
============================================================
PHASE 0: EMAIL SEARCH FIX
============================================================

Step 1: Adding email_hash column to clients table...
[OK] email_hash column added

Step 2: Creating email_hash index...
[OK] email_hash index created

Step 3: Backfilling email hashes for existing clients...
Found X clients to backfill...
[OK] Backfilled X clients

Step 4: Verifying all clients have email_hash...
[OK] All clients have email_hash

Step 5: Verifying column and index...
[OK] email_hash column exists
[OK] email_hash index exists

============================================================
[SUCCESS] EMAIL SEARCH FIX COMPLETE
============================================================
```

---

### Step 3: Verification Queries

**After backfill, verify:**
```sql
-- Check no clients missing email_hash
SELECT COUNT(*) FROM clients 
WHERE email_hash IS NULL AND email IS NOT NULL;
-- Expected: 0

-- Check column exists
SELECT column_name FROM information_schema.columns 
WHERE table_name = 'clients' AND column_name = 'email_hash';
-- Expected: email_hash

-- Check index exists
SELECT indexname FROM pg_indexes 
WHERE tablename = 'clients' AND indexname = 'idx_clients_tenant_id_email_hash';
-- Expected: idx_clients_tenant_id_email_hash
```

---

## EXECUTION ORDER

1. **First:** Run migration SQL (creates column + index)
2. **Second:** Run Python backfill script (populates email_hash for existing clients)
3. **Third:** Run verification queries (confirm completion)

---

## SAFETY GUARANTEES

✅ **Non-Destructive:**
- Only adds new column (`email_hash`)
- Does NOT modify encrypted `email` column
- Does NOT delete any data
- Preserves all existing client records

✅ **Idempotent:**
- Can run multiple times safely
- `IF NOT EXISTS` prevents duplicate creation
- Backfill only processes NULL values

✅ **Transaction-Safe:**
- Each step can be rolled back if needed
- Backfill processes row-by-row with error handling

✅ **Error Handling:**
- Decryption failures: Skip row, continue to next
- Database errors: Rollback, report error
- Missing encryption key: Report warning, continue

---

## RISK MITIGATION

**Risk:** Decryption failures during backfill
- **Mitigation:** Script handles gracefully, continues to next row
- **Impact:** Some clients may not get backfilled (can re-run script)

**Risk:** Large table backfill performance
- **Mitigation:** Processes row-by-row, can be interrupted and resumed
- **Impact:** Temporary performance impact during backfill

**Risk:** Migration conflicts
- **Mitigation:** Uses `IF NOT EXISTS` - safe if column/index already exists
- **Impact:** None - idempotent operations

---

## PREREQUISITES

**Required Environment Variables:**
- `DATABASE_URL` - PostgreSQL connection string
- `ENCRYPTION_KEY` - Fernet key for decrypting emails

**Required Python Packages:**
- `psycopg2` - PostgreSQL adapter
- `python-dotenv` - Environment variable loading
- `cryptography` - Fernet encryption/decryption

**Required Database Access:**
- ALTER TABLE permission on `clients` table
- CREATE INDEX permission
- SELECT/UPDATE permission on `clients` table

---

## ROLLBACK PLAN

**If migration fails:**
```sql
-- Remove index
DROP INDEX IF EXISTS idx_clients_tenant_id_email_hash;

-- Remove column (only if needed)
ALTER TABLE clients DROP COLUMN IF EXISTS email_hash;
```

**Note:** Rollback is only needed if migration fails. Backfill can be re-run safely.

---

## NEXT STEPS AFTER PHASE 0

1. **Phase 0B:** Run 9/9 basic tests (email search, thread reconstruction, multi-account matching)
2. **Phase 1:** Full backend test suite validation
3. **Phase 2:** Backend deployment readiness

---

**END OF PHASE 0 EXECUTION PLAN**

**Status:** READY FOR EXECUTION  
**Awaiting:** Final approval to execute migration and backfill script

