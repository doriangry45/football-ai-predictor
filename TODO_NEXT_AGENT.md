# TODO — Yeni Asistan İçin (Session 2+)

## ✅ Tamamlanan (Session 1)

### Test & QA
- ✅ Tüm import hatalarını çözdü (google.generativeai stub, feature_002_ai_predictor package shim)
- ✅ pytest komutları çalışır hale geldi (3/3 test pass)
- ✅ `.github/workflows/ci.yml` oluşturuldu (testler + optional Vercel deploy)

### Deployment
- ✅ `Dockerfile` oluşturuldu (gunicorn + Flask)
- ✅ `vercel.json` yapılandırıldı (@vercel/docker)
- ✅ GitHub Actions CI workflow kuruldu
- ✅ `DEPLOYMENT.md` ve `VERCEL_SETUP.md` yazıldı
- ✅ `.github/copilot-instructions.md` güncellendi (AI agent rehberi)

### Kod Yapısı
- ✅ `services/feature-002-ai-predictor/main.py` — RapidAPI fetcher (EFootballFetcher sınıfı)
- ✅ `services/feature-002-ai-predictor/app.py` — Flask routes (/api/predict, /api/health, /api/leagues)
- ✅ `templates/predict.html` — Web dashboard (POST /api/predict çağırır)
- ✅ `supabase/schema.sql` — Database schema (api_cache, predictions tabloları)

### Secrets & Env (GitHub Actions)
- ✅ `VERCEL_TOKEN` ✅ eklendi
- ✅ `RAPIDAPI_KEY1`, `RAPIDAPI_KEY2`, `RAPIDAPI_KEY` ✅ eklendi
- ✅ `GOOGLE_AI_API_KEY` ✅ eklendi
- ✅ `REDIS_URL`, `SUPABASE_URL`, `SUPABASE_KEY` (opsiyonel) ✅ eklendi

---

## ⏳ Sonraki Adımlar (Session 2+)

### 1. CI/CD Pipeline Validation
- [ ] GitHub Actions workflow'unu test et (push to main veya feature branch)
- [ ] Vercel deployment'ını doğrula (build logs kontrol et)
- [ ] Prod ortamda `/api/predict` endpoint'ini test et
- [ ] Environment variables tümü prod'da mı set kontrol et

### 2. Gemini Integration Validations
- [ ] AI prompt'ını iyileştir (match analysis accuracy artır)
- [ ] Error handling güçlendir (Gemini API failures için retry logic)
- [ ] Rate limiting prodda çalışıyor mu kontrol et
- [ ] Caching (Redis + Supabase) performansını test et

### 3. Frontend Improvements
- [ ] `templates/predict.html` UX iyileştir (loading indicator, error messages)
- [ ] Match cards'a daha fazla bilgi ekle (league, season, fixture date)
- [ ] Turkish language strings'i i18n yapısına taşı
- [ ] Mobile responsiveness test et

### 4. Database & Monitoring
- [ ] Supabase tarafında predictions tablo'sunda queryler test et
- [ ] Redis cache TTL'lerini production load'a göre ayarla
- [ ] Logging'i kurumsal seviyeye çıkar (structured logs, trace IDs)
- [ ] Monitoring dashboard ekle (ör. Vercel Analytics, Sentry)

### 5. Documentation Updates
- [ ] `README.md` içinde local dev setup adımlarını genişlet
- [ ] API endpoint'lerinin OpenAPI/Swagger spec'ini oluştur
- [ ] Database schema'sını diyagram ile görselleştir
- [ ] Troubleshooting section ekle (common errors + solutions)

### 6. Advanced Features (Backlog)
- [ ] Birden fazla AI modeli destekle (Gemini, Claude, OpenAI API)
- [ ] Match statistics'i RapidAPI'den aktar (possession, shots vs)
- [ ] Historical predictions'i track et (accuracy metrics)
- [ ] User authentication ekle (favorites, saved predictions)
- [ ] WebSocket ile real-time predictions gönder

### 7. Testing Coverage
- [ ] Unit tests'e daha fazla test case ekle (error scenarios)
- [ ] Integration tests yaz (RapidAPI + Gemini mock'larla)
- [ ] Load testing yap (concurrent requests)
- [ ] End-to-end (E2E) tests ekle (Selenium/Playwright)

---

## Branching Strategy

- `main` — Production ready, stable
- `feature-002-ai-predictor` — Current dev branch (merge to main when ready)
- `hotfix/*` — Production bugs için
- `feature/*` — Yeni features için

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `services/feature-002-ai-predictor/main.py` | RapidAPI client + fixture fetcher |
| `services/feature-002-ai-predictor/app.py` | Flask app, AI logic, routes |
| `templates/predict.html` | Web UI (POST /api/predict) |
| `supabase/schema.sql` | Database tables (api_cache, predictions) |
| `tests/test_predictor.py` | Unit tests (3 tests, all pass) |
| `.github/workflows/ci.yml` | CI: test + optional Vercel deploy |
| `Dockerfile` | Container for Vercel/other hosts |
| `vercel.json` | Vercel config (uses Docker) |
| `.env` | Local secrets (NEVER commit) |
| `memory/context.md` | Project state (THIS session için güncelle) |

---

## Hızlı Komutlar (Development)

```powershell
# Setup
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r services/feature-002-ai-predictor/requirements.txt

# Run
python services/feature-002-ai-predictor/app.py
# Open http://localhost:5000

# Test
pytest -q
pytest tests/test_predictor.py -v
pytest --cov=services/feature-002-ai-predictor tests/

# Docker (local)
docker build -t football-ai-predictor .
docker run -p 5000:5000 --env-file .env football-ai-predictor

# Git workflow
git checkout feature-002-ai-predictor
git add .
git commit -m "feat: [açıklama]"
git push origin feature-002-ai-predictor
# Create PR to main
```

---

## Sorun Giderme (Troubleshooting)

### "ModuleNotFoundError: google.generativeai"
- Sebep: `google/generativeai.py` stub'ı yüklemediyse
- Çözüm: `pip install google-generativeai` VEYA stub dosyası var mı kontrol et

### "No module named services.feature_002_ai_predictor"
- Sebep: `services/feature_002_ai_predictor/__init__.py` eksik
- Çözüm: Eğer dosya var ise PythonPath'i kur: `export PYTHONPATH=/path/to/repo:$PYTHONPATH`

### Redis connection failed
- Sebep: Redis server çalışmıyor
- Çözüm: Redis'i başlat VEYA `REDIS_URL` env var'ını kaldır (opsiyonel)

### Vercel deploy fails
- Kontrol et:
  - `VERCEL_TOKEN` secret GitHub'da set mi?
  - Tüm env vars Vercel project settings'de var mı?
  - `Dockerfile` ve `vercel.json` dosyaları var mı?
  - Build logs'u oku: Vercel Dashboard > Deployments > Failed deploy > Build Output

---

## Session Notes

**Session 1 (13 Nov 2025)**
- Started: Import errors in tests (google.generativeai, services package)
- Fixed: Added stub modules + package shim
- Added: CI workflow, Dockerfile, Vercel config, deployment docs
- Tests: 3/3 passing
- Deployment: Ready for GitHub secrets -> Vercel CI trigger
- Next: Validate CI/CD pipeline, improve AI prompts, frontend UX

---
