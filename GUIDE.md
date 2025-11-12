# 🚀 Football AI Predictor - Comprehensive Guide

**New Account Setup & Development Guide for AI Predictions Feature**

Repository: https://github.com/doriangry45/football-ai-predictor  
Focus: E-Football AI predictions with Gemini 2.5 Pro

---

## 📋 İçindekiler

1. [GitHub Account Setup](#1-github-account-setup)
2. [Repository Clone](#2-repository-clone)
3. [Local Development Environment](#3-local-development-environment)
4. [Running the Project](#4-running-the-project)
5. [Understanding Architecture](#5-understanding-architecture)
6. [Making Contributions](#6-making-contributions)
7. [Deployment](#7-deployment)

---

## 1. GitHub Account Setup

```powershell
# Git configuration (one time)
git config --global user.name "Your Name"
git config --global user.email "your.email@github.com"

# SSH Key (recommended)
ssh-keygen -t ed25519 -C "your.email@github.com"
```

## 2. Repository Clone

```powershell
# Clone repository
git clone https://github.com/doriangry45/football-ai-predictor.git
cd football-ai-predictor

# Create feature branch
git checkout -b feature-002-ai-predictor
```

## 3. Local Development Environment

### 3.1 Python Virtual Environment

```powershell
# Create venv
python -m venv .venv

# Activate (Windows)
.\.venv\Scripts\Activate

# Verify
python --version  # Should be 3.9+
```

### 3.2 Install Dependencies

```powershell
cd services/feature-002-ai-predictor
pip install -r requirements.txt
```

### 3.3 Environment Variables

```powershell
# Copy template
copy .env.example .env

# Edit .env with your keys:
# - RAPIDAPI_KEY1, RAPIDAPI_KEY2
# - GOOGLE_AI_API_KEY
# - REDIS_URL (optional)
# - SUPABASE_URL, SUPABASE_KEY (optional)
```

## 4. Running the Project

### 4.1 Start Flask App

```powershell
cd services/feature-002-ai-predictor
python app.py

# Output:
# ⚡ E-Football AI Predictor
# ✓ API Keys: 2
# ✓ Redis: True
# ✓ Supabase: True
# ✓ Google AI: True
# 🚀 Running on http://localhost:5000
```

### 4.2 Access Dashboard

Open browser: http://localhost:5000

### 4.3 API Usage

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "league": 39,
    "season": 2025,
    "query": "over 2.5"
  }'
```

### 4.4 Run Tests

```powershell
pytest tests/
```

## 5. Understanding Architecture

### Project Structure

```
football-ai-predictor/
├── .github/
│   ├── copilot-instructions.md
│   └── workflows/
├── services/
│   └── feature-002-ai-predictor/
│       ├── main.py              (RapidAPI Fetcher)
│       ├── app.py               (Flask + AI Logic)
│       ├── requirements.txt
│       ├── README.md
│       └── tests/
├── templates/
│   └── predict.html             (Web UI)
├── supabase/
│   └── schema.sql               (Database)
├── memory/
│   └── context.md               (Feature context)
├── plans/
│   └── 002-ai-predictor/
├── specs/
│   └── 002-ai-predictor/
├── .env.example
├── GUIDE.md
├── README.md
└── ONBOARDING.md
```

### Data Flow

```
User Request
    ↓
Flask API (/api/predict)
    ↓
Check Redis Cache
    ↓
If miss → Fetch RapidAPI (with key rotation)
    ↓
Store in Redis (1hr) + Supabase (backup)
    ↓
Send to Gemini 2.5 Pro
    ↓
AI Analysis & Prediction
    ↓
Save predictions to Supabase
    ↓
Return JSON to Frontend
    ↓
Display on Dashboard
```

### Key Components

**main.py** - RapidAPI Integration
- Fetch fixtures
- Fetch standings
- Fetch statistics

**app.py** - Flask Application
- Rate limiting (Redis)
- Cache management
- AI predictions (Gemini)
- Database operations

**Database Schema**
- `api_cache` - API responses cache
- `predictions` - AI predictions history

## 6. Making Contributions

### Workflow

1. **Create Feature Branch**
   ```powershell
   git checkout -b feature-xyz
   ```

2. **Make Changes**
   - Update code
   - Add tests
   - Update docs

3. **Commit Changes**
   ```powershell
   git add .
   git commit -m "feat: Add new feature"
   ```

4. **Push to Remote**
   ```powershell
   git push origin feature-xyz
   ```

5. **Create Pull Request**
   - Go to GitHub
   - Create PR from feature branch to main
   - Add description
   - Wait for review

### Commit Message Convention

```
feat: Add new feature
fix: Fix bug
docs: Update documentation
refactor: Reorganize code
test: Add tests
```

## 7. Deployment

### Production Checklist

- [ ] All tests pass
- [ ] Code review completed
- [ ] Environment variables set
- [ ] Database migrations done
- [ ] API keys rotated

### Deploy Command

```powershell
# Build Docker image
docker build -t football-ai-predictor .

# Run container
docker run -p 5000:5000 --env-file .env football-ai-predictor
```

---

## 🆘 Troubleshooting

### Tests Failing

```powershell
# Clear cache
rm -r .pytest_cache
pip cache purge

# Reinstall
pip install -r requirements.txt
pytest -v
```

### Redis Connection Error

Redis isteğe bağlı. Olmadan da çalışır ama cache olmaz.

```powershell
# Docker ile Redis
docker run -d -p 6379:6379 redis:latest
```

### API Key Errors

```powershell
# Kontrol et
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('RAPIDAPI_KEY1'))"
```

---

## 📚 Resources

- [RapidAPI Docs](https://rapidapi.com/api-sports/api/api-football)
- [Gemini API](https://ai.google.dev)
- [Flask Docs](https://flask.palletsprojects.com)
- [Supabase Docs](https://supabase.com/docs)
- [Redis Docs](https://redis.io/docs)

---

**Good luck! 🚀**
