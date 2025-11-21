-- Migration 005: Create unsafe_threads table
-- Purpose: Sentra safety tagging for unsafe email threads

CREATE TABLE IF NOT EXISTS unsafe_threads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    thread_id TEXT NOT NULL,
    reason TEXT NOT NULL,
    violation_type TEXT NOT NULL,
    severity TEXT NOT NULL CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    metadata JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(tenant_id, thread_id)
);

CREATE INDEX IF NOT EXISTS idx_unsafe_threads_tenant_thread ON unsafe_threads(tenant_id, thread_id);
CREATE INDEX IF NOT EXISTS idx_unsafe_threads_tenant_severity ON unsafe_threads(tenant_id, severity);
CREATE INDEX IF NOT EXISTS idx_unsafe_threads_tenant_time ON unsafe_threads(tenant_id, created_at DESC);

-- RLS Policy
ALTER TABLE unsafe_threads ENABLE ROW LEVEL SECURITY;

CREATE POLICY unsafe_threads_tenant_isolation ON unsafe_threads
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant_id', TRUE)::UUID);

COMMENT ON TABLE unsafe_threads IS 'Unsafe threads tagged by Sentra Safety AI';

