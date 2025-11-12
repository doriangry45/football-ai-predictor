-- Feature 002: AI Predictor Database Schema

-- API Cache tablosu
CREATE TABLE IF NOT EXISTS api_cache (
  id SERIAL PRIMARY KEY,
  key VARCHAR(255) UNIQUE NOT NULL,
  value JSONB NOT NULL,
  expires_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tahminler tablosu
CREATE TABLE IF NOT EXISTS predictions (
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
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index'ler
CREATE INDEX IF NOT EXISTS idx_predictions_league_season 
  ON predictions(league_id, season);
CREATE INDEX IF NOT EXISTS idx_predictions_created_at 
  ON predictions(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_api_cache_expires 
  ON api_cache(expires_at);