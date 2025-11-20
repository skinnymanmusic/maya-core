-- Migration 003: Add idempotency and retry queue tables
-- Purpose: Global idempotency layer and retry queue for failed processing

-- Processed messages table (idempotency)
CREATE TABLE IF NOT EXISTS processed_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    gmail_message_id TEXT NOT NULL UNIQUE,
    processed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_processed_messages_tenant_msg ON processed_messages(tenant_id, gmail_message_id);
CREATE INDEX IF NOT EXISTS idx_processed_messages_tenant_time ON processed_messages(tenant_id, processed_at DESC);

-- Email retry queue table
CREATE TABLE IF NOT EXISTS email_retry_queue (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    email_id UUID REFERENCES emails(id) ON DELETE CASCADE,
    gmail_message_id TEXT NOT NULL,
    account_email TEXT,
    retry_count INTEGER NOT NULL DEFAULT 0,
    max_retries INTEGER NOT NULL DEFAULT 3,
    status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'completed', 'failed')),
    error_message TEXT,
    error_stack TEXT,
    trace_id TEXT,
    metadata JSONB,
    scheduled_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_retry_queue_tenant_status ON email_retry_queue(tenant_id, status, scheduled_at);
CREATE INDEX IF NOT EXISTS idx_retry_queue_pending ON email_retry_queue(tenant_id, status) WHERE status = 'pending';
CREATE INDEX IF NOT EXISTS idx_retry_queue_gmail_id ON email_retry_queue(gmail_message_id);

-- RLS Policies
ALTER TABLE processed_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE email_retry_queue ENABLE ROW LEVEL SECURITY;

CREATE POLICY processed_messages_tenant_isolation ON processed_messages
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant_id', TRUE)::UUID);

CREATE POLICY retry_queue_tenant_isolation ON email_retry_queue
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant_id', TRUE)::UUID);

COMMENT ON TABLE processed_messages IS 'Global idempotency layer for email processing';
COMMENT ON TABLE email_retry_queue IS 'Retry queue for failed email processing';

