#!/usr/bin/env python3
"""
Apply fixed schema to Supabase.
Uses new table names to avoid conflicts.
"""

import os
import psycopg2

db_url = 'postgresql://postgres.vmongtwawdphlraijxar:pSRhcw7okkHeSsH1@aws-1-eu-west-1.pooler.supabase.com:6543/postgres'

schema_sql = """
-- Feature 002: AI Predictor Database Schema (Updated)

-- API Cache table
CREATE TABLE IF NOT EXISTS api_cache_v2 (
  id SERIAL PRIMARY KEY,
  key VARCHAR(255) UNIQUE NOT NULL,
  value JSONB NOT NULL,
  expires_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AI Predictions table (new schema for app.py)
CREATE TABLE IF NOT EXISTS ai_predictions (
  id SERIAL PRIMARY KEY,
  league_id INTEGER NOT NULL,
  season INTEGER NOT NULL,
  home_team VARCHAR(255) NOT NULL,
  away_team VARCHAR(255) NOT NULL,
  prediction_type VARCHAR(100),
  prediction VARCHAR(50),
  probability INTEGER,
  reasoning TEXT,
  tweet TEXT,
  prompt_version VARCHAR(20),
  player_snapshot JSONB,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_ai_predictions_league_season 
  ON ai_predictions(league_id, season);
CREATE INDEX IF NOT EXISTS idx_ai_predictions_created_at 
  ON ai_predictions(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_api_cache_v2_expires 
  ON api_cache_v2(expires_at);
"""

try:
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    
    print("Applying schema...")
    cur.execute(schema_sql)
    conn.commit()
    
    # Verify tables
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name IN ('api_cache_v2', 'ai_predictions')
    """)
    created = [row[0] for row in cur.fetchall()]
    
    cur.close()
    conn.close()
    
    print(f"✓ Schema applied successfully!")
    print(f"Created tables: {', '.join(created)}")
    
except Exception as e:
    print(f"ERROR: {e}")
