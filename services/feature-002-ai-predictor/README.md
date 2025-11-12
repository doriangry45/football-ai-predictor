# Feature 002: AI Predictor

E-Football tahminlerini Gemini 2.5 Pro kullanarak yapan Flask web uygulaması.

## Özellikler

- **RapidAPI Integration**: 2 API key ile dönen erişim
- **AI Analysis**: Gemini 2.5 Pro ile maç analizi
- **Rate Limiting**: Redis ile günlük limit yönetimi
- **Caching**: Redis + Supabase yedekli cache
- **Web Dashboard**: Tahminleri gösteren HTML UI

## Kurulum

```bash
# Venv oluştur
python -m venv .venv
.\.venv\Scripts\Activate  # Windows

# Bağımlılıkları yükle
pip install -r requirements.txt
```

## Ortam Değişkenleri

`.env` dosyasını oluştur:

```env
# RapidAPI Keys (iki key ile döner)
RAPIDAPI_KEY=your_key_1
RAPIDAPI_KEY1=your_key_1
RAPIDAPI_KEY2=your_key_2

# Google AI
GOOGLE_AI_API_KEY=your_gemini_key

# Redis (isteğe bağlı, localhost default)
REDIS_URL=redis://localhost:6379

# Supabase (isteğe bağlı, yedek cache)
SUPABASE_URL=your_url
SUPABASE_KEY=your_key
```

## Çalıştırma

```bash
# Flask app
python app.py

# CLI fetch
python main.py
```

API açılır: `http://localhost:5000`

## API Endpoints

### POST /api/predict
Tahmin al

```json
{
  "league": 39,
  "season": 2025,
  "query": "over 2.5"
}
```

### GET /api/health
Sistem durumu

### GET /api/leagues
Popüler ligler

## Testler

```bash
pytest tests/
```

## Mimarisi

- `main.py`: RapidAPI fetcher sınıfı
- `app.py`: Flask routes + AI logic
- `templates/predict.html`: Web UI
- Tests: `tests/test_predictor.py`

## Rate Limiting

Redis kullanılıyorsa: Günde 900 çağrı/key (1000 limit)
Redis yoksa: Sınır yok (local dev mode)

## Error Handling

- API key eksik/invalid → Error response
- Rate limit aşıldı → 2. key'ye geç
- Supabase/Redis down → Çalışmaya devam et
- AI analiz hata → Raw response döndür
