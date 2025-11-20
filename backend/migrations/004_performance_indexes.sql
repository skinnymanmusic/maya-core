-- Migration 004: Add performance indexes
-- Purpose: Optimize common query patterns

-- Email indexes
CREATE INDEX IF NOT EXISTS idx_emails_tenant_processed ON emails(tenant_id, processed, created_at);
CREATE INDEX IF NOT EXISTS idx_emails_tenant_thread ON emails(tenant_id, gmail_thread_id);
CREATE INDEX IF NOT EXISTS idx_emails_gmail_msg_id ON emails(gmail_message_id);

-- Client indexes
CREATE INDEX IF NOT EXISTS idx_clients_tenant_email_hash ON clients(tenant_id, email_hash);
CREATE INDEX IF NOT EXISTS idx_clients_tenant_contact ON clients(tenant_id, last_contact_at);

-- Audit log indexes
CREATE INDEX IF NOT EXISTS idx_audit_log_tenant_time ON audit_log(tenant_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_log_tenant_action ON audit_log(tenant_id, action, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_log_tenant_resource ON audit_log(tenant_id, resource_type, resource_id);

-- Sync log indexes
CREATE INDEX IF NOT EXISTS idx_sync_log_tenant_type ON sync_log(tenant_id, sync_type, created_at);
CREATE INDEX IF NOT EXISTS idx_sync_log_fingerprint ON sync_log(fingerprint);

COMMENT ON INDEX idx_emails_tenant_processed IS 'Optimize unprocessed email queries';
COMMENT ON INDEX idx_audit_log_tenant_time IS 'Optimize audit log time-based queries';

