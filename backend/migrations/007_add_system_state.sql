-- Migration 007: Create system_state table
-- Purpose: Solin MCP Safe Mode and system state storage

CREATE TABLE IF NOT EXISTS system_state (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    state_key TEXT NOT NULL,
    state_value TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(tenant_id, state_key)
);

CREATE INDEX IF NOT EXISTS idx_system_state_tenant_key ON system_state(tenant_id, state_key);

-- RLS Policy
ALTER TABLE system_state ENABLE ROW LEVEL SECURITY;

CREATE POLICY system_state_tenant_isolation ON system_state
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant_id', TRUE)::UUID);

COMMENT ON TABLE system_state IS 'Solin MCP system state (Safe Mode, etc.)';

