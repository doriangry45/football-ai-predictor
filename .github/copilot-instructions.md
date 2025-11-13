[//]: # (Auto-generated concise Copilot instructions tailored for this repo.)
# Copilot AI Instructions

Purpose: Provide immediate, actionable guidance for AI coding agents working on Feature 002 (AI Predictions).

Quick Start (Windows PowerShell):
```powershell
python -m venv .venv; .\.venv\Scripts\Activate; pip install -r services/feature-002-ai-predictor/requirements.txt
python services/feature-002-ai-predictor/app.py
pytest tests/test_predictor.py
```

Key files & flows:
- **Fetcher**: `services/feature-002-ai-predictor/main.py` (RapidAPI client + key rotation)
- **App**: `services/feature-002-ai-predictor/app.py` (Flask routes, `/api/predict` used by `templates/predict.html`)
- **UI**: `templates/predict.html` (fetches `POST /api/predict`, render cards)
- **Tests**: `tests/test_predictor.py` (unit/integration examples)
- **DB/Schema**: `supabase/schema.sql` (persistent cache / tables)

Project-specific conventions:
- Feature directories are prefixed with `feature-###-slug` under `services/` and `plans/`.
- Spec/plans include a `SPECPULSE_METADATA` header—preserve it when editing specs.
- Secrets live in root `.env` (or local env); never commit secrets. Environment vars used: `RAPIDAPI_KEY1`, `RAPIDAPI_KEY2`, `RAPIDAPI_KEY`, `GOOGLE_AI_API_KEY`, `REDIS_URL`, `SUPABASE_URL`, `SUPABASE_KEY`.
- Branch naming: use `feature-002-ai-predictor` / `feature-*` for feature work.

Integration points to check before changes:
- RapidAPI: header `X-RapidAPI-Key` and host `api-football-v1.p.rapidapi.com` (see `specs/` or `spec.yaml` in sibling repo).
- Google Generative AI: key in `GOOGLE_AI_API_KEY` (Gemini integration lives in `app.py`).
- Redis and Supabase: caching layers (fast+persistent). Inspect code for fallback logic in `main.py` and `app.py`.

Agent workflow (required):
- Use `apply_patch` to edit files (preserve style). Do NOT output raw diffs as final — apply edits.
- Track progress with `manage_todo_list` (one item `in-progress` at a time). Mark completed as you finish steps.
- Run unit tests in `tests/` locally after changes. If adding runnable code, include/update `requirements.txt` and a short README in the feature folder.

Testing & debug tips:
- Run `pytest tests/test_predictor.py::test_api_health -v` for targeted checks.
- Use `print`/logging in `services/feature-002-ai-predictor/app.py` to trace incoming `/api/predict` requests; `templates/predict.html` expects JSON { matches: [...] }.

When merging or updating this file:
- Keep the guidance short and concrete. Reference the exact files above for examples.
- Preserve any SPECPULSE metadata blocks in `plans/` and `specs/` files.
- Don't add or expose secrets; reference environment variable names only.

If anything here is unclear or you want this expanded (e.g., CI config or a runnable Dockerfile), tell me which area to expand.