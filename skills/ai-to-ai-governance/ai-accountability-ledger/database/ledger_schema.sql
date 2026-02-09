-- AI Accountability Ledger Database Schema
-- Version: 1.0.0
-- Supports immutable audit trail with chain integrity

-- Main ledger entries table
CREATE TABLE IF NOT EXISTS ledger_entries (
    entry_id VARCHAR(16) PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    entry_type VARCHAR(20) NOT NULL CHECK (entry_type IN ('action', 'decision', 'interaction', 'governance', 'violation', 'correction')),

    -- Actor information
    actor_model_id VARCHAR(100) NOT NULL,
    actor_provider VARCHAR(50) NOT NULL,
    actor_session_id VARCHAR(100) NOT NULL,

    -- Action details
    action_type VARCHAR(100) NOT NULL,
    action_description TEXT NOT NULL,
    action_inputs JSONB DEFAULT '[]',
    action_outputs JSONB DEFAULT '[]',
    action_rationale TEXT,

    -- Context
    context JSONB DEFAULT '{}',

    -- Accountability
    responsibility_chain JSONB NOT NULL DEFAULT '[]',
    human_oversight VARCHAR(20) NOT NULL CHECK (human_oversight IN ('full', 'selective', 'audit', 'minimal')),
    reversibility VARCHAR(20) NOT NULL CHECK (reversibility IN ('reversible', 'irreversible', 'partial')),

    -- Integrity (chain)
    entry_hash CHAR(64) NOT NULL,
    previous_hash CHAR(64) NOT NULL,
    signatures JSONB DEFAULT '[]',

    -- Indexes for common queries
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Indexes for efficient querying
CREATE INDEX idx_ledger_actor ON ledger_entries(actor_model_id);
CREATE INDEX idx_ledger_type ON ledger_entries(entry_type);
CREATE INDEX idx_ledger_timestamp ON ledger_entries(timestamp);
CREATE INDEX idx_ledger_task ON ledger_entries((context->>'task_id'));
CREATE INDEX idx_ledger_chain ON ledger_entries(previous_hash);

-- Violations table (separate for quick access)
CREATE TABLE IF NOT EXISTS violations (
    violation_id VARCHAR(30) PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    severity VARCHAR(20) NOT NULL CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    violator_model_id VARCHAR(100) NOT NULL,
    rule_violated VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    evidence_entries JSONB NOT NULL DEFAULT '[]',
    immediate_action TEXT,
    investigation_status VARCHAR(30) DEFAULT 'pending',
    corrective_action TEXT,
    resolved_at TIMESTAMP WITH TIME ZONE,
    ledger_entry_id VARCHAR(16) REFERENCES ledger_entries(entry_id)
);

CREATE INDEX idx_violations_violator ON violations(violator_model_id);
CREATE INDEX idx_violations_severity ON violations(severity);
CREATE INDEX idx_violations_status ON violations(investigation_status);

-- Audit queries view
CREATE VIEW audit_summary AS
SELECT
    date_trunc('day', timestamp) as day,
    actor_model_id,
    entry_type,
    COUNT(*) as entry_count,
    COUNT(CASE WHEN entry_type = 'violation' THEN 1 END) as violation_count
FROM ledger_entries
GROUP BY date_trunc('day', timestamp), actor_model_id, entry_type
ORDER BY day DESC, actor_model_id;

-- Chain integrity check function
CREATE OR REPLACE FUNCTION verify_chain_integrity()
RETURNS TABLE(entry_id VARCHAR, is_valid BOOLEAN, error_message TEXT) AS $$
DECLARE
    rec RECORD;
    prev_hash CHAR(64) := REPEAT('0', 64);
    expected_hash CHAR(64);
BEGIN
    FOR rec IN SELECT * FROM ledger_entries ORDER BY created_at ASC
    LOOP
        -- Check previous hash link
        IF rec.previous_hash != prev_hash THEN
            RETURN QUERY SELECT rec.entry_id, FALSE, 'Previous hash mismatch';
        ELSE
            RETURN QUERY SELECT rec.entry_id, TRUE, NULL::TEXT;
        END IF;

        prev_hash := rec.entry_hash;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Retention policy function
CREATE OR REPLACE FUNCTION apply_retention_policy()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER := 0;
    retention_days INTEGER;
BEGIN
    -- Action entries: 90 days
    DELETE FROM ledger_entries
    WHERE entry_type = 'action'
    AND timestamp < NOW() - INTERVAL '90 days';
    GET DIAGNOSTICS deleted_count = ROW_COUNT;

    -- Decision entries: 365 days
    DELETE FROM ledger_entries
    WHERE entry_type = 'decision'
    AND timestamp < NOW() - INTERVAL '365 days';
    GET DIAGNOSTICS deleted_count = deleted_count + ROW_COUNT;

    -- Interaction entries: 90 days
    DELETE FROM ledger_entries
    WHERE entry_type = 'interaction'
    AND timestamp < NOW() - INTERVAL '90 days';
    GET DIAGNOSTICS deleted_count = deleted_count + ROW_COUNT;

    -- Note: governance, violation, correction are permanent

    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Responsibility chain query function
CREATE OR REPLACE FUNCTION get_responsibility_chain(p_entry_id VARCHAR)
RETURNS JSONB AS $$
    SELECT responsibility_chain
    FROM ledger_entries
    WHERE entry_id = p_entry_id;
$$ LANGUAGE sql;

-- Task timeline query
CREATE OR REPLACE FUNCTION get_task_timeline(p_task_id VARCHAR)
RETURNS TABLE(
    entry_id VARCHAR,
    timestamp TIMESTAMP WITH TIME ZONE,
    actor_model_id VARCHAR,
    action_type VARCHAR,
    action_description TEXT
) AS $$
    SELECT
        entry_id,
        timestamp,
        actor_model_id,
        action_type,
        action_description
    FROM ledger_entries
    WHERE context->>'task_id' = p_task_id
    ORDER BY timestamp ASC;
$$ LANGUAGE sql;

-- Comments for documentation
COMMENT ON TABLE ledger_entries IS 'Immutable ledger of all AI model actions and decisions';
COMMENT ON TABLE violations IS 'Policy violations with investigation status';
COMMENT ON FUNCTION verify_chain_integrity() IS 'Verify blockchain-style chain integrity';
COMMENT ON FUNCTION apply_retention_policy() IS 'Apply data retention policy (governance/violations are permanent)';
