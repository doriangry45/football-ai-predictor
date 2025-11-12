# SPECPULSE_METADATA
- SPEC_ID: 002-spec-001
- FEATURE_ID: 002
- FEATURE_NAME: AI Predictor
- STATUS: In Development
- VERSION: 1.0
- CREATED: 2025-11-13

---

# Feature 002: AI Predictions - Technical Specification

## 📋 Overview

Specification for AI-powered football match predictions using Gemini 2.5 Pro and RapidAPI data.

## 🔌 API Endpoints

### POST /api/predict
**Description**: Get AI predictions for upcoming matches  
**Method**: POST  
**Content-Type**: application/json

#### Request

```json
{
  "league": 39,
  "season": 2025,
  "query": "over 2.5"
}
```

**Parameters**:
- `league` (int, optional): League ID - Default: 39 (Premier League)
- `season` (int, optional): Season year - Default: 2025
- `query` (string, optional): Prediction type - Default: "over 2.5"
  - Values: "over 2.5", "btts", "1x2", "form", "stats"

#### Response (Success - 200)

```json
{
  "matches": [
    {
      "home": "Manchester United",
      "away": "Liverpool",
      "prediction": "OVER",
      "probability": 72,
      "confidence": "HIGH",
      "reasoning": "Statistical analysis shows...",
      "tweet": "Turkish prediction summary",
      "keyFactors": ["Factor 1", "Factor 2"]
    }
  ]
}
```

#### Response (Error - 5XX)

```json
{
  "error": "Error description",
  "code": "ERROR_TYPE"
}
```

---

### GET /api/health
**Description**: Health check endpoint  
**Response**:
```json
{
  "status": "healthy",
  "redis": true,
  "supabase": true,
  "google_ai": true,
  "api_keys": 2
}
```

---

### GET /api/leagues
**Description**: Get list of available leagues  
**Response**:
```json
[
  {"id": 39, "name": "Premier League (England)"},
  {"id": 140, "name": "La Liga (Spain)"},
  {"id": 135, "name": "Serie A (Italy)"},
  {"id": 78, "name": "Bundesliga (Germany)"},
  {"id": 61, "name": "Ligue 1 (France)"}
]
```

---

## 🗄️ Database Schema

### api_cache Table
```sql
CREATE TABLE api_cache (
  id SERIAL PRIMARY KEY,
  key VARCHAR(255) UNIQUE NOT NULL,
  value JSONB NOT NULL,
  expires_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Purpose**: Cache RapidAPI responses (Redis fallback)  
**TTL**: 1 hour  
**Index**: key, expires_at

### predictions Table
```sql
CREATE TABLE predictions (
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
```

**Purpose**: Store AI predictions for history/analytics  
**Index**: league_id, season, created_at

---

## ⚙️ Configuration

### Environment Variables

```env
# RapidAPI (Required for data fetching)
RAPIDAPI_KEY1=your_api_key_1      # Primary key
RAPIDAPI_KEY2=your_api_key_2      # Fallback key
RAPIDAPI_KEY=your_fallback_key    # Secondary fallback

# Google AI (Required for predictions)
GOOGLE_AI_API_KEY=your_gemini_key

# Redis (Optional - for rate limiting and caching)
REDIS_URL=redis://localhost:6379

# Supabase (Optional - for persistent caching and predictions storage)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_key
```

### Rate Limiting

- **Per Key**: 900 requests/day (limit: 1000 from RapidAPI)
- **Rotation**: Automatic fallover when limit reached
- **Storage**: Redis (if available)
- **Fallback**: No limit (local dev mode)

### Caching Strategy

**L1 Cache**: Redis (1 hour TTL)
- Fast access
- Per-request key: `fixtures:{league}:{season}`

**L2 Cache**: Supabase (1 hour TTL)
- Persistent backup
- Survives restarts
- Fallback if Redis down

### AI Model Configuration

- **Model**: gemini-2.5-pro
- **Provider**: Google Generative AI
- **Timeout**: 30 seconds
- **Temperature**: 0.7 (creative but factual)

---

## 🔄 Request Flow

```
1. Client Request
   ↓
2. Validate Input (league, season, query)
   ↓
3. Check Redis Cache
   ├─ Hit? → Return cached data
   └─ Miss? → Continue
   ↓
4. Check Supabase Cache
   ├─ Hit? → Cache in Redis + Return
   └─ Miss? → Continue
   ↓
5. Check Rate Limit (Redis)
   ├─ Exceeded? → Try next API key or error
   └─ OK? → Continue
   ↓
6. Fetch from RapidAPI
   ├─ Success? → Cache + Continue
   └─ Fail? → Try next key or error
   ↓
7. Parse Fixture Data
   ├─ Success? → Continue
   └─ Fail? → Return error
   ↓
8. Send to Gemini AI
   ├─ Success? → Parse JSON + Continue
   └─ Fail? → Return raw response
   ↓
9. Save Predictions to Supabase
   ├─ Optional - doesn't block response
   └─ Log errors only
   ↓
10. Return Predictions to Client
```

---

## 🧪 Testing Requirements

### Unit Tests
- [ ] Test RapidAPI fetcher
- [ ] Test Flask routes
- [ ] Test rate limiting logic
- [ ] Test cache operations
- [ ] Test AI prompt formatting

### Integration Tests
- [ ] End-to-end prediction flow
- [ ] Cache fallback scenarios
- [ ] API key rotation
- [ ] Error recovery

### Edge Cases
- [ ] No fixtures available
- [ ] All API keys rate limited
- [ ] Redis/Supabase down
- [ ] Invalid league/season
- [ ] AI API timeout

---

## 🔒 Security

### API Key Management
- Never commit keys to repository
- Use environment variables only
- Rotate keys periodically
- Monitor usage for anomalies

### Data Validation
- Input validation on all endpoints
- JSON schema validation
- SQL injection prevention (use ORM)
- Rate limiting enabled

### Error Messages
- Don't expose internal errors to client
- Log detailed errors for debugging
- Return generic error messages

---

## 📊 Performance Targets

| Metric | Target | Current |
|--------|--------|---------|
| Response Time | < 2s | ~1.5s |
| Cache Hit Rate | > 80% | TBD |
| API Uptime | > 99% | TBD |
| Error Rate | < 1% | TBD |

---

## 🚀 Deployment Requirements

- Python 3.9+
- Flask 2.3.3+
- redis-server (optional)
- PostgreSQL/Supabase (optional)
- API keys configured

---

## 📚 Related Documents

- [Feature Plan](./plan-001.md)
- [Prompts Library](../../prompts/ai_studio_prompts.md)
- [README](../../services/feature-002-ai-predictor/README.md)
- [Copilot Instructions](./.github/copilot-instructions.md)

---

**Version**: 1.0  
**Last Updated**: 2025-11-13  
**Maintained By**: AI Team
