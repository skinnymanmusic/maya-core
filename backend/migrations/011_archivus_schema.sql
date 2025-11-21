-- Migration 011: Create Archivus memory tables
-- Purpose: Long-term memory engine for thread summaries and profiles

-- Archivus threads table
CREATE TABLE IF NOT EXISTS archivus_threads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    gmail_thread_id TEXT NOT NULL,
    summary TEXT,
    key_points JSONB,
    client_context JSONB,
    venue_context JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(tenant_id, gmail_thread_id)
);

CREATE INDEX IF NOT EXISTS idx_archivus_threads_tenant_thread ON archivus_threads(tenant_id, gmail_thread_id);
CREATE INDEX IF NOT EXISTS idx_archivus_threads_tenant_client ON archivus_threads(tenant_id, (key_points->>'client_id'));
CREATE INDEX IF NOT EXISTS idx_archivus_threads_tenant_venue ON archivus_threads(tenant_id, (key_points->>'venue_name'));

-- Archivus memories table
CREATE TABLE IF NOT EXISTS archivus_memories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    memory_type TEXT NOT NULL CHECK (memory_type IN ('client_profile', 'venue_profile', 'thread_summary', 'system_note')),
    key TEXT NOT NULL,
    value JSONB NOT NULL,
    confidence FLOAT NOT NULL DEFAULT 1.0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_archivus_memories_tenant_type ON archivus_memories(tenant_id, memory_type, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_archivus_memories_tenant_key ON archivus_memories(tenant_id, key);

-- RLS Policies
ALTER TABLE archivus_threads ENABLE ROW LEVEL SECURITY;
ALTER TABLE archivus_memories ENABLE ROW LEVEL SECURITY;

CREATE POLICY archivus_threads_tenant_isolation ON archivus_threads
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant_id', TRUE)::UUID);

CREATE POLICY archivus_memories_tenant_isolation ON archivus_memories
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant_id', TRUE)::UUID);

COMMENT ON TABLE archivus_threads IS 'Archivus thread summaries with key points';
COMMENT ON TABLE archivus_memories IS 'Archivus memory storage (client/venue profiles, system notes)';

