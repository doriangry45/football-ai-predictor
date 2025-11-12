# 🎓 Onboarding Guide

**For New Contributors to football-ai-predictor**

---

## Welcome! 👋

Bu proje Gemini 2.5 Pro kullanarak e-football maçlarını tahmin eden bir AI sistemidir.

## 🚀 5-Minute Quick Start

### 1. Clone & Setup (2 min)

```powershell
git clone https://github.com/doriangry45/football-ai-predictor.git
cd football-ai-predictor
python -m venv .venv
.\.venv\Scripts\Activate
cd services/feature-002-ai-predictor
pip install -r requirements.txt
```

### 2. Configure Environment (1 min)

```powershell
copy ..\..\..\.env.example ..\..\..\.env
# Edit .env - add your API keys
```

### 3. Run App (2 min)

```powershell
python app.py
# Open http://localhost:5000
```

---

## 📁 Project Structure Overview

```
football-ai-predictor/
├── 📁 services/feature-002-ai-predictor/
│   ├── 📄 main.py              ← RapidAPI fetcher
│   ├── 📄 app.py               ← Flask server
│   ├── 📄 requirements.txt
│   └── 📁 tests/               ← Unit tests
├── 📁 templates/
│   └── 📄 predict.html         ← Web UI
├── 📁 supabase/
│   └── 📄 schema.sql           ← Database
├── 📁 memory/
│   └── 📄 context.md           ← Active feature context
├── 📁 plans/
│   └── 📁 002-ai-predictor/    ← Feature plans
├── 📁 specs/
│   └── 📁 002-ai-predictor/    ← Specifications
├── 📄 GUIDE.md                 ← This guide
├── 📄 README.md                ← Project overview
└── 📄 .env.example             ← Environment template
```

---

## 🔑 Key Components

### **main.py** - RapidAPI Fetcher
Footballmaçı verilerini RapidAPI'den çeker.

```python
from main import EFootballFetcher

fetcher = EFootballFetcher(api_key="your_key")
fixtures = fetcher.fetch_fixtures(league=39, season=2025)
```

### **app.py** - Flask Application
Web serveri, AI analizi ve veritabanı işlemleri yapılır.

**Key Functions:**
- `get_fixtures()` - Cache'li veri çekme
- `ai_predict()` - Gemini ile tahmin
- `check_limit()` - Rate limit kontrolü

### **predict.html** - Dashboard
Tahminleri gösteren web arayüzü.

---

## 🧪 Testing

```powershell
# Tüm testleri çalıştır
pytest

# Belirli testi çalıştır
pytest tests/test_predictor.py::test_api_health -v

# Coverage raporu
pytest --cov=services/feature-002-ai-predictor tests/
```

---

## 🔄 Git Workflow

### Branching Strategy

```
main (production)
  ↑
feature-002-ai-predictor (development)
  ↑
feature-xyz (your feature)
```

### Commit Process

```powershell
# 1. Create feature branch
git checkout -b feature/your-feature-name

# 2. Make changes
# ... edit files ...

# 3. Stage changes
git add .

# 4. Commit with message
git commit -m "feat: Add amazing feature"

# 5. Push to remote
git push origin feature/your-feature-name

# 6. Create Pull Request on GitHub
```

### Commit Message Format

```
feat: Add new prediction model
fix: Fix rate limiting bug
docs: Update API documentation
refactor: Improve cache logic
test: Add unit tests for AI module
chore: Update dependencies
```

---

## 🤔 Common Tasks

### How to Add New API Endpoint

1. **Add route in app.py**
```python
@app.route("/api/new-endpoint", methods=["POST"])
def new_endpoint():
    data = request.get_json()
    # Your logic here
    return jsonify(result)
```

2. **Add test in tests/test_predictor.py**
```python
def test_new_endpoint():
    client = app.test_client()
    response = client.post("/api/new-endpoint", json={"param": "value"})
    assert response.status_code == 200
```

3. **Commit and push**
```powershell
git add .
git commit -m "feat: Add new endpoint"
git push origin feature/new-endpoint
```

### How to Debug

```powershell
# Enable Flask debug mode (already enabled in app.py)
python app.py

# Check logs
tail -f app.log

# Debug with Python
python -m pdb app.py
```

### How to Update Dependencies

```powershell
# Add new package
pip install package-name

# Update requirements.txt
pip freeze > services/feature-002-ai-predictor/requirements.txt

# Commit changes
git add requirements.txt
git commit -m "chore: Update dependencies"
```

---

## 🚨 Troubleshooting

### Issue: Tests fail with "ModuleNotFoundError"

**Solution:**
```powershell
# Make sure you're in right directory
cd services/feature-002-ai-predictor

# Reinstall dependencies
pip install -r requirements.txt

# Run tests again
pytest
```

### Issue: "RAPIDAPI_KEY not found"

**Solution:**
```powershell
# Check .env file exists
type .env

# If not, create it
copy .env.example .env

# Add your actual keys to .env
```

### Issue: Redis connection refused

**Solution:**
```powershell
# Redis is optional! App works without it.
# If you want Redis:

# Using Docker
docker run -d -p 6379:6379 redis:latest

# Or install locally
# https://redis.io/download
```

---

## 📚 Learning Resources

### Python
- [Python Official Docs](https://docs.python.org/3/)
- [Real Python Tutorials](https://realpython.com/)

### Flask
- [Flask Official Docs](https://flask.palletsprojects.com/)
- [Miguel Grinberg's Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

### APIs
- [RapidAPI e-Football API](https://rapidapi.com/api-sports/api/api-football)
- [HTTP Methods Guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)

### AI
- [Google Generative AI Documentation](https://ai.google.dev/docs)
- [Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)

---

## ❓ Questions?

1. Check [GUIDE.md](GUIDE.md) for detailed instructions
2. Check [README.md](README.md) for project overview
3. Check existing issues on GitHub
4. Create new issue with detailed description

---

## 🎉 You're All Set!

Başlamaya hazırsın! Herhangi bir sorunda bize ulaş.

**Happy coding! 🚀**
