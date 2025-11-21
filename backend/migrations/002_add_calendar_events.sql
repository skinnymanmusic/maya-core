-- Migration 002: Create calendar_events table
-- Purpose: Store Google Calendar events with tenant isolation

CREATE TABLE IF NOT EXISTS calendar_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    google_event_id TEXT UNIQUE,
    title TEXT NOT NULL,
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ NOT NULL,
    location TEXT,
    description TEXT,
    client_id UUID REFERENCES clients(id) ON DELETE SET NULL,
    color_id INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_calendar_events_tenant_time ON calendar_events(tenant_id, start_time, end_time);
CREATE INDEX IF NOT EXISTS idx_calendar_events_tenant_client ON calendar_events(tenant_id, client_id);
CREATE INDEX IF NOT EXISTS idx_calendar_events_google_id ON calendar_events(google_event_id);

-- RLS Policy
ALTER TABLE calendar_events ENABLE ROW LEVEL SECURITY;

CREATE POLICY calendar_events_tenant_isolation ON calendar_events
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant_id', TRUE)::UUID);

COMMENT ON TABLE calendar_events IS 'Calendar events with tenant isolation and RLS';

