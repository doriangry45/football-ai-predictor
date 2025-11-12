# Football AI Predictor

Gemini 2.5 Pro ve RapidAPI kullanarak e-football maçlarını tahmin eden AI sistemi.

## 📋 Proje Yapısı

```
football-ai-predictor/
├── services/
│   └── feature-002-ai-predictor/
│       ├── main.py              # RapidAPI Fetcher
│       ├── app.py               # Flask Web App
│       ├── requirements.txt      # Bağımlılıklar
│       └── README.md            # Feature docu
├── templates/
│   └── predict.html             # Web UI
├── supabase/
│   └── schema.sql               # Database
├── tests/
│   └── test_predictor.py        # Unit tests
└── .env.example                 # Env template
```

## 🚀 Hızlı Başlangıç

### 1. Setup

```bash
# Virtual environment
python -m venv .venv
.\.venv\Scripts\Activate  # Windows

# Bağımlılıkları yükle
cd services/feature-002-ai-predictor
pip install -r requirements.txt
```

### 2. Environment

`.env` dosyasını `.env.example` örneğinden oluştur:

```bash
copy .env.example .env
```

Gerekli API anahtarlarını ekle:
- `RAPIDAPI_KEY1` + `RAPIDAPI_KEY2`
- `GOOGLE_AI_API_KEY`

### 3. Çalıştır

```bash
python app.py
```

Dashboard açılır: **http://localhost:5000**

## 🎯 Features

- ✅ **AI Predictions**: Gemini 2.5 Pro ile maç analizi
- ✅ **Rate Limiting**: Redis ile 2 API key döner
- ✅ **Intelligent Caching**: Redis + Supabase yedek
- ✅ **Web Dashboard**: Tahminleri gösteren UI
- ✅ **Error Handling**: Fallback mekanizmaları

## 🔌 API

### POST /api/predict
```json
{
  "league": 39,
  "season": 2025,
  "query": "over 2.5"
}
```

Response:
```json
{
  "matches": [
    {
      "home": "Team A",
      "away": "Team B",
      "prediction": "OVER",
      "probability": 72,
      "reasoning": "...",
      "tweet": "..."
    }
  ]
}
```

### GET /api/health
Sistem durumu kontrolü

### GET /api/leagues
Popüler ligler listesi

## 🧪 Testler

```bash
pytest tests/
```

## 📚 Teknolojiler

- **Framework**: Flask
- **AI**: Google Generative AI (Gemini 2.5 Pro)
- **Data**: RapidAPI (e-football)
- **Cache**: Redis
- **Database**: Supabase (PostgreSQL)
- **Testing**: Pytest

## ⚙️ Configuration

### Environment Variables

```env
# RapidAPI (2 key ile rotation)
RAPIDAPI_KEY1=key1
RAPIDAPI_KEY2=key2

# Google AI
GOOGLE_AI_API_KEY=gemini_key

# Redis (optional)
REDIS_URL=redis://localhost:6379

# Supabase (optional)
SUPABASE_URL=https://...
SUPABASE_KEY=...
```

### Rate Limiting

- **Redis varsa**: Günde 900 çağrı/API key (limit: 1000)
- **Redis yoksa**: Limitsiz (local dev mode)

### Caching

- **L1**: Redis (fast, 1 saat)
- **L2**: Supabase (persistent, 1 saat)

## 🔧 Development

```bash
# Watch mode
python app.py

# CLI fetch
python main.py --league 39 --season 2025 --output fixtures.json
```

## 📝 Notes

- API key rotasyonu otomatik (rate limit sonrası)
- Supabase/Redis down olsa da çalışır
- Tüm errors logglanır
- Response validation yapılır

## 📄 Lisans

MIT