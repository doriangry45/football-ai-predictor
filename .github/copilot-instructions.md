# Copilot AI Instructions

You are building **Feature 002: AI Predictions** for the football-ai-predictor project.

## 🎯 Primary Objectives

1. **Gemini 2.5 Pro Integration** - Use for football match analysis and predictions
2. **RapidAPI with Key Rotation** - 2 keys with automatic failover
3. **Rate Limiting** - Redis-based daily limits (900/key out of 1000)
4. **Multi-Layer Caching** - Redis (fast) + Supabase (persistent)
5. **Error Resilience** - Graceful degradation when services unavailable

## 🏗️ Architecture Pattern

```
Feature Files:
├── services/feature-002-ai-predictor/
│   ├── main.py              (EFootballFetcher class)
│   ├── app.py               (Flask + AI logic)
│   ├── requirements.txt      (Dependencies with versions)
│   └── tests/test_predictor.py
├── templates/predict.html   (Web dashboard)
├── supabase/schema.sql      (Database tables)
└── All docs include SPECPULSE_METADATA headers
```

## 🔧 Technology Stack

- **Framework**: Flask 2.3.3
- **AI**: google-generativeai (Gemini 2.5 Pro)
- **API**: RapidAPI (api-football-v1)
- **Cache**: redis 5.0.0
- **Database**: supabase 2.3.4
- **Testing**: pytest 7.4.2

## 🔑 Configuration & Secrets

**Environment Variables:**
```env
RAPIDAPI_KEY1=your_first_key
RAPIDAPI_KEY2=your_second_key
RAPIDAPI_KEY=fallback_key

GOOGLE_AI_API_KEY=your_gemini_key

REDIS_URL=redis://localhost:6379  (optional)
SUPABASE_URL=https://...          (optional)
SUPABASE_KEY=your_key             (optional)
```

## 📋 Implementation Checklist

### Core Features
- [x] RapidAPI fetcher with error handling
- [x] Gemini 2.5 Pro integration
- [x] Rate limiting with Redis
- [x] Multi-layer caching (Redis + Supabase)
- [x] Web dashboard (Flask + HTML)
- [x] Database schema (PostgreSQL)

### Quality Assurance
- [ ] Unit tests (pytest) - ALL PASSING
- [ ] Integration tests
- [ ] Error scenario testing
- [ ] Performance benchmarking

### Documentation
- [x] GUIDE.md - Comprehensive guide
- [x] ONBOARDING.md - New contributor guide
- [x] README.md - Project overview
- [ ] API documentation
- [ ] Feature specifications

## 🚀 Deployment Pattern

```bash
# Local Development
python app.py

# Production (Docker)
docker build -t football-ai-predictor .
docker run -p 5000:5000 --env-file .env football-ai-predictor
```

## 🧪 Testing Pattern

```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_predictor.py::test_api_health -v

# Generate coverage report
pytest --cov=services/feature-002-ai-predictor tests/
```

## 🔗 Git Workflow

```bash
# Create feature branch
git checkout -b feature-002-improvements

# Make changes
git add .
git commit -m "feat: Improve AI predictions accuracy"

# Push to remote
git push origin feature-002-improvements

# Create Pull Request to main
```

## 📝 Key Files

- **Fetcher**: `services/feature-002-ai-predictor/main.py`
- **App Logic**: `services/feature-002-ai-predictor/app.py`
- **Tests**: `services/feature-002-ai-predictor/tests/test_predictor.py`
- **Database**: `supabase/schema.sql`
- **Context**: `memory/context.md`