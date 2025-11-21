-- Migration 012: Add bookings table for payment tracking
-- Purpose: Track bookings with payment status and Stripe integration

CREATE TABLE IF NOT EXISTS bookings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    
    -- Booking Info
    booking_id TEXT NOT NULL UNIQUE,
    client_email TEXT NOT NULL,
    service_description TEXT NOT NULL,
    event_date TIMESTAMPTZ,
    event_location TEXT,
    
    -- Payment Info
    payment_status TEXT DEFAULT 'pending' CHECK (payment_status IN ('pending', 'paid', 'failed', 'refunded')),
    payment_amount DECIMAL(10,2),
    payment_timestamp TIMESTAMPTZ,
    stripe_payment_link_id TEXT,
    stripe_payment_intent_id TEXT,
    
    -- Metadata
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    created_by UUID REFERENCES users(id)
);

-- Index for fast lookups
CREATE INDEX IF NOT EXISTS idx_bookings_tenant_id ON bookings(tenant_id);
CREATE INDEX IF NOT EXISTS idx_bookings_booking_id ON bookings(booking_id);
CREATE INDEX IF NOT EXISTS idx_bookings_payment_status ON bookings(tenant_id, payment_status);
CREATE INDEX IF NOT EXISTS idx_bookings_client_email ON bookings(tenant_id, client_email);

-- Row Level Security
ALTER TABLE bookings ENABLE ROW LEVEL SECURITY;

CREATE POLICY bookings_tenant_isolation ON bookings
    FOR ALL
    USING (tenant_id = current_setting('app.tenant_id', true)::UUID);

COMMENT ON TABLE bookings IS 'Booking records with payment tracking';

