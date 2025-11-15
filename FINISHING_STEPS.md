Final finishing checklist
=========================

Quick steps to finish and secure the project:

- Run tests: `pytest -q` (from repo root).
- Run the app in demo mode (PowerShell):
  ```powershell
  $env:DEMO_MODE='1'; cd services/feature-002-ai-predictor; python app.py
  ```
- Apply DB schema (if you have a Postgres/Supabase connection):
  ```powershell
  $env:SUPABASE_PG_CONN='postgresql://user:pass@host:5432/dbname'
  Set-Location 'C:\Users\Aria-Thea\football-ai-predictor\scripts'
  .\init_db.ps1
  ```
- Git and secrets (important):
  - Remove any committed secrets from the repository: `git rm --cached .env`
  - Add `.env` to `.gitignore`: `echo ".env" >> .gitignore`
  - Commit the removal: `git commit -m "chore: remove .env from repo and add to .gitignore"`
  - Rotate any leaked API keys immediately (RapidAPI, Google, Supabase, Vercel, Pusher).

- CI / Deploy checklist:
  - Add GitHub repository secrets: `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`, `SUPABASE_URL`, `SUPABASE_KEY`, `GOOGLE_AI_API_KEY`, `RAPIDAPI_KEY1`, `RAPIDAPI_KEY2`, `REDIS_URL`.
  - Re-run GitHub Actions after adding secrets to verify deploy step.

If you want, I can:

- Apply the DB schema for you if you provide `SUPABASE_PG_CONN` (I will run `scripts/init_db.ps1`).
- Remove `.env` from git and help rotate/replace the committed keys.
- Add a CI step to fail the build if `.env` exists in the repo.
