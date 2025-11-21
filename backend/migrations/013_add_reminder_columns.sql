-- Migration 013: Add reminder tracking columns to bookings table
-- Purpose: Track payment reminder emails sent to clients

ALTER TABLE bookings 
ADD COLUMN IF NOT EXISTS reminder_1_sent BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS reminder_1_sent_at TIMESTAMPTZ,
ADD COLUMN IF NOT EXISTS reminder_2_sent BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS reminder_2_sent_at TIMESTAMPTZ,
ADD COLUMN IF NOT EXISTS reminder_3_sent BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS reminder_3_sent_at TIMESTAMPTZ;

COMMENT ON COLUMN bookings.reminder_1_sent IS 'Day 3 friendly reminder sent';
COMMENT ON COLUMN bookings.reminder_2_sent IS 'Day 7 urgent reminder sent';
COMMENT ON COLUMN bookings.reminder_3_sent IS 'Day 14 final notice sent';

