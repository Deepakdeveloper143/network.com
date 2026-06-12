-- QuantumShieldAI Database Schema
-- Run this in your Supabase SQL Editor to create all required tables

-- 1. Scan Results Table (stores all types of scans)
CREATE TABLE IF NOT EXISTS scan_results (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    scan_type VARCHAR(50) NOT NULL, -- 'quantum_risk', 'vulnerability_port', 'vulnerability_website', 'prompt_analysis', 'signature_check', 'rsa_encrypt'
    scan_data JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    severity VARCHAR(20)
);

-- 2. Reports Table (stores generated reports)
CREATE TABLE IF NOT EXISTS reports (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    report_type VARCHAR(50) NOT NULL,
    title VARCHAR(255),
    summary TEXT,
    report_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Dashboard Stats Table (stores historical dashboard data for trends)
CREATE TABLE IF NOT EXISTS dashboard_stats (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    total_scans INTEGER DEFAULT 0,
    quantum_risk_score INTEGER,
    active_threats INTEGER DEFAULT 0,
    prompt_attacks_blocked INTEGER DEFAULT 0,
    vulnerabilities_found INTEGER DEFAULT 0,
    compliance_score INTEGER,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security (RLS)
ALTER TABLE scan_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE dashboard_stats ENABLE ROW LEVEL SECURITY;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_scan_results_type ON scan_results(scan_type);
CREATE INDEX IF NOT EXISTS idx_scan_results_created ON scan_results(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_reports_type ON reports(report_type);
CREATE INDEX IF NOT EXISTS idx_reports_created ON reports(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_dashboard_recorded ON dashboard_stats(recorded_at DESC);

-- Insert initial dashboard stats
INSERT INTO dashboard_stats (total_scans, quantum_risk_score, active_threats, prompt_attacks_blocked, vulnerabilities_found, compliance_score)
VALUES (0, 50, 0, 0, 0, 85);
