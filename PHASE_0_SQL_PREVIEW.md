# PHASE 0: EMAIL SEARCH FIX - SQL PREVIEW
**Date:** 2025-01-27  
**Status:** READY FOR EXECUTION

---

## SQL MIGRATION PREVIEW

### Migration File: `backend/migrations/015_add_clients_email_hash.sql`

```sql
-- Migration 015: Add email_hash column to clients table
-- Purpose: Enable deterministic email search (SHA-256 hash lookup)
-- Related: Migration 001 adds email_hash to emails table
-- Related: Migration 004 creates index on clients(tenant_id, email_hash)

-- Step 1: Add email_hash column to clients table
ALTER TABLE clients 
ADD COLUMN IF NOT EXISTS email_hash TEXT;

-- Step 2: Create index for efficient lookups
CREATE INDEX IF NOT EXISTS idx_clients_tenant_id_email_hash 
ON clients (tenant_id, email_hash);

-- Step 3: Add comment for documentation
COMMENT ON COLUMN clients.email_hash IS 'SHA256 hash of email (lowercase, trimmed) for deterministic lookup';
```

---

## DIFF PREVIEW

### Before (Current State):
```sql
-- clients table structure:
CREATE TABLE clients (
    id UUID PRIMARY KEY,
    tenant_id UUID NOT NULL,
    email TEXT,  -- encrypted with Fernet
    name TEXT,   -- encrypted
    phone TEXT,  -- encrypted
    company TEXT, -- encrypted
    created_at TIMESTAMPTZ,
    last_contact_at TIMESTAMPTZ,
    -- NO email_hash column
    -- NO index on email_hash
);
```

### After (After Migration):
```sql
-- clients table structure:
CREATE TABLE clients (
    id UUID PRIMARY KEY,
    tenant_id UUID NOT NULL,
    email TEXT,      -- encrypted with Fernet (PRESERVED)
    email_hash TEXT, -- NEW: SHA256 hash for lookup
    name TEXT,       -- encrypted
    phone TEXT,      -- encrypted
    company TEXT,    -- encrypted
    created_at TIMESTAMPTZ,
    last_contact_at TIMESTAMPTZ,
    -- NEW INDEX: idx_clients_tenant_id_email_hash (tenant_id, email_hash)
);
```

**Changes:**
- ✅ Added: `email_hash TEXT` column
- ✅ Added: `idx_clients_tenant_id_email_hash` index
- ✅ Preserved: All existing columns and data
- ✅ No data loss or modification

---

## BACKFILL OPERATIONS PREVIEW

### Python Script Operations:

**Step 1: Query clients needing backfill**
```sql
SELECT id, tenant_id, email 
FROM clients 
WHERE email_hash IS NULL AND email IS NOT NULL;
```

**Step 2: For each client (row-by-row):**
```python
# 1. Decrypt email
decrypted_email = decrypt(encrypted_email)

# 2. Hash email
email_hash = hashlib.sha256(decrypted_email.lower().strip().encode()).hexdigest()

# 3. Update client
UPDATE clients 
SET email_hash = %s 
WHERE id = %s AND tenant_id = %s;
```

**Step 3: Verification**
```sql
SELECT COUNT(*) FROM clients 
WHERE email_hash IS NULL AND email IS NOT NULL;
-- Expected: 0
```

---

## EXECUTION SAFETY

✅ **All operations use `IF NOT EXISTS`** - Safe to run multiple times  
✅ **No data deletion** - Only adds column, preserves all data  
✅ **No modification to encrypted email** - Original encrypted email preserved  
✅ **Transaction-safe** - Can rollback if needed  
✅ **Error handling** - Continues on decryption failures  

---

## FIX SCRIPT CORRECTION

**Fixed:** `decrypt_email()` function now correctly imports `decrypt` from `app.encryption`

**Before (broken):**
```python
from app.encryption import get_encryption_service
encryption_service = get_encryption_service()
return encryption_service.decrypt(encrypted_email)
```

**After (fixed):**
```python
from app.encryption import decrypt
return decrypt(encrypted_email)
```

---

**END OF SQL PREVIEW**

**Ready to execute migration and backfill script.**

