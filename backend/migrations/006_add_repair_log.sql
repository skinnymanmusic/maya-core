-- Migration 006: Create repair_log table
-- Purpose: Vita repair attempt logging

CREATE TABLE IF NOT EXISTS repair_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    event TEXT NOT NULL,
    action_taken TEXT NOT NULL,
    success BOOLEAN NOT NULL,
    error_message TEXT,
    metadata JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_repair_log_tenant_time ON repair_log(tenant_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_repair_log_tenant_success ON repair_log(tenant_id, success);
CREATE INDEX IF NOT EXISTS idx_repair_log_tenant_event ON repair_log(tenant_id, event);

-- RLS Policy
ALTER TABLE repair_log ENABLE ROW LEVEL SECURITY;

CREATE POLICY repair_log_tenant_isolation ON repair_log
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant_id', TRUE)::UUID);

COMMENT ON TABLE repair_log IS 'Vita repair attempt logs';

