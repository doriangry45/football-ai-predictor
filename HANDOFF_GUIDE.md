# Mevcut Projeye Nasıl Devam Edebileceğiniz — Rehber

## Hızlı Başlangıç (İlk 5 dakika)

```powershell
# 1. Repo'yu clone et ve branch'a git
git clone https://github.com/doriangry45/football-ai-predictor.git
cd football-ai-predictor
git checkout feature-002-ai-predictor

# 2. Environment kurması
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r services/feature-002-ai-predictor/requirements.txt

# 3. Test et (hepsi pass olmalı)
pytest -q
# Output: 3 passed

# 4. Local olarak çalıştır
python services/feature-002-ai-predictor/app.py
# Open http://localhost:5000 in browser
```

---

## Ne Yapıldı? (Geçmiş)

### Session 1 İçinde (13 Nov 2025)

1. **Test Hataları Çözüldü**
   - Import problemi: `google.generativeai` stub oluşturuldu (`google/generativeai.py`)
   - Package import problemi: `services/feature_002_ai_predictor/__init__.py` oluşturuldu
   - Sonuç: Testler 3/3 geçti

2. **Deployment Altyapısı Eklendi**
   - `Dockerfile` — Flask app'i gunicorn ile container'a koydu
   - `vercel.json` — Vercel'e "Docker builder kullan" dedi
   - `.github/workflows/ci.yml` — GitHub Actions: test çalıştır, sonra Vercel'e deploy et (eğer `main` branch ise)

3. **Dokümantasyon Yapıldı**
   - `DEPLOYMENT.md` — Adım adım deployment rehberi
   - `VERCEL_SETUP.md` — Vercel token oluşturma + GitHub secrets ekleme (Türkçe)
   - `.github/copilot-instructions.md` — AI asistan'lar için proje rehberi

4. **GitHub Secrets Eklendi** (sizin tarafınızdan)
   - `VERCEL_TOKEN` ✅
   - `RAPIDAPI_KEY1`, `RAPIDAPI_KEY2`, `RAPIDAPI_KEY` ✅
   - `GOOGLE_AI_API_KEY` ✅
   - `REDIS_URL`, `SUPABASE_URL`, `SUPABASE_KEY` (opsiyonel) ✅

---

## Şimdi Ne Yapılmalı? (Sonraki Adımlar)

### 1️⃣ CI/CD Pipeline'ı Doğrula (En Önemli)

```powershell
# main branch'a merge et
git checkout main
git merge feature-002-ai-predictor
git push origin main
```

**Sonuç**: GitHub Actions otomatik çalışacak:
1. Tests'i run et
2. Eğer pass ise + `VERCEL_TOKEN` var ise → Vercel'e deploy et

**Kontrol et**:
- GitHub > Actions > CI job'un durumunu izle
- Eğer **green** ise: tests pass
- Eğer deploy job çalışırsa: Vercel'de deploy başlayacak
- Vercel dashboardda deployments'ı kontrol et

---

### 2️⃣ Prod URL'i Test Et

Eğer Vercel deploy başarılı ise:
- `https://your-vercel-url/` — Dashboard açılmalı
- `https://your-vercel-url/api/health` — JSON döndürmeli (status: healthy)
- `https://your-vercel-url/api/predict` (POST) — Predictions döndürmeli

**Eğer fail ise**:
- Vercel Dashboard > Deployments > Failed deploy > Build Logs
- Hata mesajını oku (genellikle env var eksik veya import problem)

---

### 3️⃣ AI Accuracy Artır (Next Big Task)

**Dosya**: `services/feature-002-ai-predictor/app.py` (satır ~180 civarında `ai_predict` fonksiyonu)

Şu an Gemini'ye bu prompt gönderiliyor:
```
Analyze these upcoming football fixtures for "over 2.5" predictions:
[fixture data]
...
```

**İyileştirmeler**:
- Fixture data'ya istatistik ekle (team form, goals/game vs)
- Prompt'u daha detaylı yap (Gemini daha iyi analiz yapacak)
- Error handling'i güçlendir (Gemini timeout/fail case'leri)
- Caching'i kontrol et (Redis vs Supabase)

---

### 4️⃣ Frontend UX Geliştirir

**Dosya**: `templates/predict.html`

Şu an:
- Button click → API call → Cards göster
- Basit card design

**Yapılması Gerekenler**:
- Loading spinner ekle (API wait sırasında)
- Error message'lar ekle (API fail ise)
- Daha fazla match info göster (league, date, odds vs)
- Mobile responsive yap
- Dark mode button (zaten dark, light mode option ekle)

---

### 5️⃣ Database & Monitoring Kur

**Supabase Tables** (var mı kontrol et):
- `api_cache` — API responses'ı cache için
- `predictions` — Tüm predictions'ı save et (analytics için)

**Redis** (opsiyonel ama önerilen):
- Local dev için: `redis-server` başlat
- Prod'da: `REDIS_URL` env var set et (ör. Redis Cloud)

**Monitoring**:
- Vercel Analytics'i aç (Dashboard > Analytics)
- Sentry entegrasyonu ekle (errors'ı track et)

---

## Dosya Haritası (Ne Nerede?)

```
football-ai-predictor/
├── services/feature-002-ai-predictor/
│   ├── main.py                    ← RapidAPI client (EFootballFetcher)
│   ├── app.py                     ← Flask app, Gemini logic, routes
│   ├── requirements.txt            ← Python dependencies
│   └── tests/
│       └── test_predictor.py      ← Unit tests (3 tests, all pass)
│
├── templates/
│   └── predict.html               ← Web dashboard UI
│
├── supabase/
│   └── schema.sql                 ← Database tables
│
├── .github/
│   ├── workflows/
│   │   └── ci.yml                 ← CI/CD pipeline (test + deploy)
│   └── copilot-instructions.md    ← AI asistan rehberi
│
├── Dockerfile                      ← Container config
├── vercel.json                     ← Vercel deployment config
├── DEPLOYMENT.md                   ← Deployment guide
├── VERCEL_SETUP.md                ← Vercel setup (Türkçe)
├── TODO_NEXT_AGENT.md             ← Yeni asistan için task list
├── THIS_FILE (HANDOFF.md)         ← Sizin şu an okuduğunuz rehber
│
└── memory/
    └── context.md                 ← Project state (güncellenecek)
```

---

## Common Scenarios & Çözümleri

### Senaryo 1: "Vercel Deploy Failed"
1. Vercel Dashboard > Deployments > Failed
2. "Build Output" tab'ına tıkla
3. Hata mesajını oku (genellikle env var eksik veya Python dependency)
4. GitHub > Settings > Secrets > Check all vars
5. Eksik ise ekle, `main` push'la, Vercel otomatik retry eder

### Senaryo 2: "/api/predict çağırırken 500 error"
1. Local çalışırsa: `python services/feature-002-ai-predictor/app.py`
2. Browser açıp POST test et (curl veya Postman)
3. Eğer local fail ise:
   - `.env` file'ında tüm keys set mi?
   - `GOOGLE_AI_API_KEY` valid mi?
   - `RAPIDAPI_KEY1` valid mi?
4. Logs'u kontrol et (app.py output'unda error backtrace göreceksin)

### Senaryo 3: "Local tests fail ama need to debug"
```powershell
# Verbose mode
pytest tests/test_predictor.py -v

# Specific test
pytest tests/test_predictor.py::test_api_health -v

# Coverage raporu
pytest --cov=services/feature-002-ai-predictor tests/ --cov-report=html
# Açı: htmlcov/index.html
```

### Senaryo 4: "Redis/Supabase bağlantısı başarısız"
- `REDIS_URL` env var olmayabilir (opsiyonel, graceful fallback var)
- Logs'u kontrol et: "Redis connection failed: ..." → OK, devam eder
- Supabase da aynı: optional, fallback logic vardır

---

## Git Workflow (Cleanup için)

```powershell
# Şu anki state
git status
git log --oneline

# Feature test ettikten sonra main'e merge
git checkout main
git merge feature-002-ai-predictor
git push origin main

# Eğer hotfix yapman gerekirse
git checkout -b hotfix/fix-xyz
# ... edit ...
git add .
git commit -m "hotfix: xyz"
git push origin hotfix/fix-xyz
# GitHub'da PR oluştur, main'e merge

# Cleanup: merged branch'ları sil
git branch -d feature-002-ai-predictor
```

---

## Yeni Asistan'a (Session 2+) Mesaj

Eğer yeni asistan bunu okuyorsa:
1. `TODO_NEXT_AGENT.md` oku (detaylı task list)
2. `.github/copilot-instructions.md` oku (project rehberi)
3. `VERCEL_SETUP.md` oku (deployment specifics)
4. `memory/context.md` güncelle (current status)
5. Sonra başlı başına yapılması gerekenler:
   - CI/CD pipeline'ı validate et
   - Prod URL'i test et
   - AI accuracy'i artır
   - Frontend UX geliştirir

---

## İletişim & Notes

**Session 1 Özeti:**
- Import errors fixed ✅
- Tests passing (3/3) ✅
- CI/CD pipeline ready ✅
- Deployment config done ✅
- GitHub secrets added ✅

**Blocked By:**
- Vercel deploy: Secrets doğru ayarlandı, waiting for CI trigger

**Next Priority:**
1. Validate CI/CD (push main, watch Actions)
2. Test prod URL
3. Improve AI prompts

---

**Bu dosya en son güncellendi**: 13 Nov 2025, Session 1 son
