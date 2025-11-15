# Project Context

**Project**: football-ai-predictor  
**Current Feature**: 002-ai-predictor  
**Status**: Ready for Deployment (CI/Vercel)  
**Account**: doriangry45 (New Account)
**Last Updated**: 13 Nov 2025 (Session 2)

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
- ✅ Unit Tests (3/3 passing)
- ✅ CI/CD Pipeline (GitHub Actions)
- ✅ Deployment Config (Docker + Vercel)
- ⏳ CI Validation (waiting for main merge)

## Session Updates

- **Session 1 (13 Nov 2025)**: Import errors resolved, stubs added, Docker/Vercel/CI configured, tests passing locally (3/3). Feature branch merged to `main`.
- **Session 2 (13 Nov 2025)**: Fixed `ci-cd.yml` workflow to set up Python and use `python -m pip`, added `SESSION_VARS.md` and `.env.example`, updated `TODO_NEXT_AGENT.md` to remind next assistant to update session vars and `memory/context.md`. Pushed commits and triggered GitHub Actions; monitor Actions for test job result.

 - **Session 3 (15 Nov 2025)**: Local dev fixes and demo mode work
	 - Fixed `.env` formatting problems that caused dotenv parse errors.
	 - Made console output ASCII-safe (removed problematic Unicode icons).
	 - Added `DEMO_MODE` env var and ensured demo/mock responses are returned when external API fetch fails (temporary demo-friendly fallback).
	 - Fixed `TEMPLATE_DIR` path so `predict.html` loads reliably (corrected to point to repo `templates/`). Root UI now returns HTTP 200 and renders `predict.html`.
	 - Disabled Werkzeug reloader by default and added `DEV_MODE=1` to enable reloader when needed.
	 - Committed and pushed changes to `main`.

Note: After every session I update `memory/context.md` and `TODO_NEXT_AGENT.md` with the latest session notes so future assistants can pick up where we left off.

## Session Notes (Action Items Completed)

- Added `.env.example` with required keys (do not store real secrets).
- Created `SESSION_VARS.md` to document env var handling and update steps.
- Reminder: After adding secrets in GitHub, re-run the workflow via Actions UI if necessary.

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
2. ✅ Add CI/CD workflow (GitHub Actions)
3. ✅ Add deployment config (Docker + Vercel)
4. ⏳ Validate CI/CD pipeline (push main, watch Actions)
5. ⏳ Test prod URL endpoint
6. ⏳ Improve AI prompts (accuracy)
7. ⏳ Frontend UX enhancements
8. ⏳ Monitoring & logging setup
