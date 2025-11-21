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

-- Note: Backfill of existing records is handled by fix_email_search.py script
-- This migration only creates the column and index structure

