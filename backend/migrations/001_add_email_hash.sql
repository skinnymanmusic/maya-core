-- Migration 001: Add email_hash column to emails table
-- Purpose: Enable hashed email lookups for idempotency

ALTER TABLE emails
ADD COLUMN IF NOT EXISTS email_hash TEXT;

CREATE INDEX IF NOT EXISTS idx_emails_email_hash ON emails(tenant_id, email_hash);

COMMENT ON COLUMN emails.email_hash IS 'SHA256 hash of sender_email for lookup';

