# Project Context

**Project**: football-ai-predictor  
**Current Feature**: 002-ai-predictor  
**Status**: In Development  
**Account**: doriangry45 (New Account)

## Active Feature

**Feature 002: AI Predictor**

- **Description**: Gemini 2.5 Pro ile e-football maçlarını tahmin et
- **Stage**: Architecture & Core Implementation
- **Branch**: `feature-002-ai-predictor`
- **Start Date**: 2025-11-13

## Key Technologies

- **AI**: Google Generative AI (Gemini 2.5 Pro)
- **Data**: RapidAPI e-football API
- **Framework**: Flask
- **Cache**: Redis + Supabase
- **Database**: Supabase (PostgreSQL)
- **Testing**: Pytest

## Architecture Pattern

```
Feature Structure:
├── services/feature-002-ai-predictor/
│   ├── main.py          (RapidAPI fetcher)
│   ├── app.py           (Flask + AI logic)
│   ├── requirements.txt  (Dependencies)
│   └── tests/           (Unit tests)
├── templates/           (Web UI)
├── supabase/            (Database)
└── docs/                (Documentation)
```

## Current Implementation Status

- ✅ RapidAPI Fetcher (main.py)
- ✅ Flask Web App (app.py)
- ✅ Error Handling & Fallbacks
- ✅ Rate Limiting (Redis)
- ✅ Caching (Redis + Supabase)
- ✅ AI Integration (Gemini 2.5 Pro)
- ✅ Web Dashboard (predict.html)
- ✅ Database Schema
- ⏳ Unit Tests (in progress)

## Environment Variables Required

```env
RAPIDAPI_KEY1=your_key_1
RAPIDAPI_KEY2=your_key_2
GOOGLE_AI_API_KEY=your_gemini_key
REDIS_URL=redis://localhost:6379
SUPABASE_URL=your_url
SUPABASE_KEY=your_key
```

## Next Steps

1. ✅ Fix failing tests
2. ⏳ Add AI Studio U prompts
3. ⏳ Complete integration tests
4. ⏳ Add CI/CD workflow
5. ⏳ Deploy to production
