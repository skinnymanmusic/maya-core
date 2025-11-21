-- Migration 014: Add conversations table for SMS booking flow
-- Purpose: Track SMS conversations and booking state

CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    
    -- Conversation Info
    phone_number TEXT NOT NULL,
    conversation_state TEXT DEFAULT 'initial' CHECK (conversation_state IN ('initial', 'service_selected', 'date_selected', 'time_selected', 'confirmed', 'completed', 'cancelled')),
    service_type TEXT,
    event_date DATE,
    event_time TIME,
    duration_hours DECIMAL(4,2),
    
    -- Booking Info
    booking_id TEXT REFERENCES bookings(booking_id),
    client_email TEXT,
    client_name TEXT,
    
    -- Metadata
    last_message_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for fast lookups
CREATE INDEX IF NOT EXISTS idx_conversations_tenant_id ON conversations(tenant_id);
CREATE INDEX IF NOT EXISTS idx_conversations_phone_number ON conversations(tenant_id, phone_number);
CREATE INDEX IF NOT EXISTS idx_conversations_state ON conversations(tenant_id, conversation_state);
CREATE INDEX IF NOT EXISTS idx_conversations_booking_id ON conversations(booking_id);

-- Row Level Security
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS conversations_tenant_isolation ON conversations;
CREATE POLICY conversations_tenant_isolation ON conversations
    FOR ALL
    USING (tenant_id = current_setting('app.tenant_id', true)::UUID);

COMMENT ON TABLE conversations IS 'SMS conversations for booking flow';

-- SMS Messages table
CREATE TABLE IF NOT EXISTS sms_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    
    -- Message Info
    phone_number TEXT NOT NULL,
    message_sid TEXT,
    direction TEXT NOT NULL CHECK (direction IN ('inbound', 'outbound')),
    body TEXT NOT NULL,
    
    -- Metadata
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for fast lookups
CREATE INDEX IF NOT EXISTS idx_sms_messages_tenant_id ON sms_messages(tenant_id);
CREATE INDEX IF NOT EXISTS idx_sms_messages_conversation_id ON sms_messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_sms_messages_phone_number ON sms_messages(tenant_id, phone_number);
CREATE INDEX IF NOT EXISTS idx_sms_messages_created_at ON sms_messages(created_at DESC);

-- Row Level Security
ALTER TABLE sms_messages ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS sms_messages_tenant_isolation ON sms_messages;
CREATE POLICY sms_messages_tenant_isolation ON sms_messages
    FOR ALL
    USING (tenant_id = current_setting('app.tenant_id', true)::UUID);

COMMENT ON TABLE sms_messages IS 'Individual SMS messages in conversations';

