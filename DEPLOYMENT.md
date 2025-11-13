# Deployment guide — Vercel (Docker) / CI

This repository contains a Flask-based feature in `services/feature-002-ai-predictor`.
The project is prepared for containerized deployment using a `Dockerfile` and a
minimal `vercel.json` that instructs Vercel to use the Dockerfile build.

Environment variables (set in Vercel or GitHub Secrets):

- `RAPIDAPI_KEY1`, `RAPIDAPI_KEY2`, `RAPIDAPI_KEY` — RapidAPI keys
- `GOOGLE_AI_API_KEY` — Gemini (optional for production)
- `REDIS_URL` — optional Redis URL
- `SUPABASE_URL`, `SUPABASE_KEY` — optional Supabase
- `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID` — optional (for CI deploy)

Quick local build (Docker):

```powershell
docker build -t football-ai-predictor .
docker run -p 5000:5000 --env-file .env football-ai-predictor
```

Notes about Vercel:
- Vercel can build the Dockerfile when `vercel.json` includes `@vercel/docker`.
- You must add the required environment variables in the Vercel project settings.
- The GitHub Actions workflow `CI` will run tests and will attempt to deploy if
  `VERCEL_TOKEN` is present as a repository secret. To enable automatic deploys
  via CI set `VERCEL_TOKEN`, `VERCEL_ORG_ID`, and `VERCEL_PROJECT_ID`.

If you prefer a platform more tightly integrated with Python web apps (e.g.,
Render, Fly, or Heroku), the provided `Dockerfile` is portable to those hosts.
