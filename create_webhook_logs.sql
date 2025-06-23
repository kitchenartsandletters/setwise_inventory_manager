-- Enable pgcrypto for UUID generation if not already active
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create the webhook_logs table
CREATE TABLE IF NOT EXISTS webhook_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id VARCHAR,
    event_type VARCHAR NOT NULL,
    payload_json JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
