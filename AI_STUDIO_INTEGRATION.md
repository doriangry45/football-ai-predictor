# AI Studio Entegrasyon Rehberi

Bu rehber, Google AI Studio'da geliştirilen prompt'ları `football-ai-predictor` projesine nasıl entegre edeceğini anlatır.

---

## Hızlı Başlangıç (5 dakika)

### 1. Google AI Studio'da Prompt Test Et

```
1. https://aistudio.google.com açmış
2. "+ Create" → "New chat"
3. Şu prompt'ı kopyala ve test et:
```

**Test Prompt:**
```
Futbol analisti olarak, aşağıdaki maçları Over 2.5 tahmini yap.

Maçlar:
[
  {
    "home": "Arsenal",
    "away": "Chelsea",
    "league": "Premier League"
  }
]

Yanıt format:
{
  "matches": [
    {
      "home": "Arsenal",
      "away": "Chelsea",
      "prediction": "OVER",
      "probability": 75,
      "reasoning": "Her iki takımın saldırgan oyunu",
      "tweet": "Tahmin: Over 2.5 🔥"
    }
  ]
}

Yanıt SADECE JSON.
```

**Send** bas → JSON al

---

### 2. app.py'de Prompt'ı Güncelle

Dosya: `services/feature-002-ai-predictor/app.py`

**Şu kısmı bul** (satır ~180 civarında):

```python
def ai_predict(fixtures_data, query="over 2.5"):
    """Analyze fixtures with Gemini."""
    fixtures = fixtures_data.get("response", [])[:10]
    
    if not fixtures:
        return {"matches": [], "error": "No fixtures available"}
    
    fixture_summary = []
    for f in fixtures:
        try:
            h = f.get("teams", {}).get("home", {})
            a = f.get("teams", {}).get("away", {})
            fixture_summary.append({
                "id": f.get("fixture", {}).get("id"),
                "home": h.get("name", "Unknown"),
                "away": a.get("name", "Unknown"),
                "date": f.get("fixture", {}).get("date", ""),
                "status": f.get("fixture", {}).get("status", {}).get("short", "")
            })
        except Exception as e:
            logging.warning(f"Parse fixture error: {e}")
    
    prompt = f"""
    Analyze these upcoming football fixtures for "{query}" predictions:
    {json.dumps(fixture_summary, indent=2)}
    
    For each fixture, provide:
    1. Over 2.5 probability (0-100)
    2. Key analysis reasoning
    3. A short tweet (Turkish)
    
    Return as JSON: {{"matches": [{{"home": "", "away": "", "prediction": "OVER/UNDER", "probability": 0, "reasoning": "", "tweet": ""}}]}}
    """
```

**YENİ PROMPT (AI Studio'dan test edilmiş) ile değiştir:**

```python
def ai_predict(fixtures_data, query="over 2.5"):
    """Analyze fixtures with Gemini."""
    fixtures = fixtures_data.get("response", [])[:10]
    
    if not fixtures:
        return {"matches": [], "error": "No fixtures available"}
    
    fixture_summary = []
    for f in fixtures:
        try:
            h = f.get("teams", {}).get("home", {})
            a = f.get("teams", {}).get("away", {})
            fixture_summary.append({
                "id": f.get("fixture", {}).get("id"),
                "home": h.get("name", "Unknown"),
                "away": a.get("name", "Unknown"),
                "date": f.get("fixture", {}).get("date", ""),
                "status": f.get("fixture", {}).get("status", {}).get("short", "")
            })
        except Exception as e:
            logging.warning(f"Parse fixture error: {e}")
    
    # UPDATED PROMPT (v2 - AI Studio tested)
    prompt = f"""
    Futbol analisti olarak, aşağıdaki maçları "{query}" tahmini yap.

    MAÇLAR:
    {json.dumps(fixture_summary, indent=2)}

    YANIT FORMATI (JSON SADECE):
    {{
      "matches": [
        {{
          "home": "Takım1",
          "away": "Takım2",
          "prediction": "OVER veya UNDER",
          "probability": 0-100 arası sayı,
          "reasoning": "2-3 cümle kısa analiz",
          "tweet": "Maksimum 140 karakterlik Türkçe tweet"
        }}
      ]
    }}

    Analiz faktörleri:
    1. Her iki takımın ortalama gol sayısı
    2. Defans gücü
    3. Ev sahibi/deplasman avantajı
    4. Son form
    
    Yanıt SADECE geçerli JSON olmalı.
    """
```

### 3. Test Et

```powershell
# Terminal'de
pytest tests/test_predictor.py::test_api_predict -v

# Ya da local çalıştır
python services/feature-002-ai-predictor/app.py
# http://localhost:5000 açıp "Tahminleri Getir" basılı
```

---

## Detaylı Kurulum (Production)

### Adım 1: Google AI Studio Hesabı Kur

```
1. https://aistudio.google.com git
2. Sign in (Google hesabı gerekli)
3. Dashboard > "+ Create" > "New chat"
```

### Adım 2: Prompt'ları Versiyonla

`prompts/ai_studio_prompts.md` dosyasında mevcut prompt'lar:
- **Prompt 1**: Over/Under 2.5 (en temel)
- **Prompt 2**: BTTS (Both Teams to Score)
- **Prompt 3**: Result (1X2)
- **Prompt 4**: Advanced (istatistik)
- **Prompt 5**: Form Analysis

**Hangi prompt kullanacağını seç:**

```python
# app.py'de conditional olarak kullan
if query == "over 2.5":
    prompt = get_prompt_over_under_25()  # Prompt 1
elif query == "btts":
    prompt = get_prompt_btts()  # Prompt 2
elif query == "result":
    prompt = get_prompt_result()  # Prompt 3
```

### Adım 3: API Key & Authentication

```python
# app.py'de zaten setup var
import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_AI_API_KEY", ""))
model = genai.GenerativeModel('gemini-2.5-pro')
```

**Gerekli**: `GOOGLE_AI_API_KEY` environment variable set edilmeli.

```powershell
# .env dosyasında
GOOGLE_AI_API_KEY=your_api_key_here
```

### Adım 4: Error Handling

AI Studio prompt'unuzun fail olması durumunda fallback mekanizması:

```python
# app.py'de zaten var (satır ~250)
try:
    response = model.generate_content(prompt)
    text = response.text
    start = text.find("{")
    end = text.rfind("}") + 1
    if start >= 0 and end > start:
        json_str = text[start:end]
        return json.loads(json_str)
except json.JSONDecodeError:
    pass

# Fallback: dummy response
return {
    "matches": [
        {
            "home": f["home"],
            "away": f["away"],
            "prediction": "ANALYZING",
            "probability": 50,
            "reasoning": "Analiz devam ediyor",
            "tweet": "Tahmin yükleniyor..."
        }
        for f in fixture_summary
    ]
}
```

---

## Prompt Geliştirme Workflow

### Iteratif İyileştirme

**Döngü:**
1. Google AI Studio'da prompt'u test et
2. Çıktıyı değerlendir (format, doğruluk, diğer)
3. Prompt'u optimize et
4. app.py'de güncelle
5. Local test et
6. Versel'e push ve prod test et

### Örnek Geliştirme

**v1.0 (Temel):**
```
Predict over/under 2.5 for these matches:
[data]

Return JSON.
```

**Çıktı:** {"matches": [...]}
**Problem:** Reasoning çok kısa, probability biraz random

**v1.1 (İyileştirilmiş):**
```
Futbol analisti: Over/Under 2.5 tahmini yap.

Maçlar: [data]

Analiz yap:
1. Her takımın ortalama gol sayısı
2. Son form (last 5 matches)
3. Defans gücü

Yanıt JSON format:
{
  "matches": [
    {
      "home": "...",
      "away": "...",
      "prediction": "OVER|UNDER",
      "probability": 70,
      "reasoning": "3-5 cümle detaylı analiz",
      "tweet": "140 char Türkçe"
    }
  ]
}
```

**Çıktı:** Daha detaylı reasoning, yüksek probability
**Result:** ✅ Kuruldu

---

## Sorun Giderme

### Problem: "JSON Parse Error"

```
Gemini'nin çıktısı JSON parse edilemiyor.
```

**Çözüm:**
1. Prompt'a ekle: "Yanıt SADECE geçerli JSON olmalı"
2. Örnek JSON ver (few-shot prompting)
3. AI Studio'da test et, çıktıyı doğrula

### Problem: "Reasoning çok kısa"

```
Prediction ama "Iyi maç" gibi 1 cümle.
```

**Çözüm:**
- Prompt'a ekle: "Reasoning: 3-5 cümle detaylı analiz"
- Örnek ver
- Token limit'ini kontrol et (fazla limitli prompt)

### Problem: "Gemini API Error"

```
rate limit exceeded / quota
```

**Çözüm:**
1. Quota check et: https://console.cloud.google.com/apis/dashboard
2. Rate limit'i artır
3. Caching ekle (Redis, Supabase)

### Problem: "Türkçe tweet karakterler yanlış"

```
"çğışüöç" karakterleri kırılıyor.
```

**Çözüm:**
```python
# app.py'de
tweet = response.get("tweet", "")
tweet = tweet.encode('utf-8').decode('utf-8')  # normalize
```

---

## Advanced: Prompt Chaining

Birden fazla prompt zincirleme:

```python
def ai_predict_advanced(fixtures_data):
    """Multi-step prediction."""
    
    # Step 1: Fetch team stats (RapidAPI)
    stats = fetcher.fetch_team_stats(...)
    
    # Step 2: Gemini - Form analysis
    form_analysis = model.generate_content(
        prompt_team_form(stats)
    )
    
    # Step 3: Gemini - Over/Under prediction
    prediction = model.generate_content(
        prompt_over_under(fixtures_data, form_analysis)
    )
    
    # Step 4: Gemini - Generate tweet
    tweet = model.generate_content(
        prompt_tweet(prediction)
    )
    
    return {
        "form": form_analysis,
        "prediction": prediction,
        "tweet": tweet
    }
```

---

## Monitoring & Analytics

### Prediction Accuracy Tracking

```python
# Supabase'e kaydet
def log_prediction(match_id, prediction, actual_result):
    supabase.table('predictions').insert({
        "match_id": match_id,
        "predicted": prediction,
        "actual": actual_result,
        "correct": prediction == actual_result,
        "timestamp": datetime.now()
    }).execute()

# Dashboard
SELECT 
    COUNT(*) as total_predictions,
    SUM(CASE WHEN correct THEN 1 ELSE 0 END) / COUNT(*) as accuracy
FROM predictions
WHERE created_at > NOW() - INTERVAL '7 days'
```

### Prompt Performance

```python
# Hangi prompt'un daha iyi performans gösterdiğini analiz et
SELECT 
    prompt_version,
    AVG(accuracy) as avg_accuracy,
    COUNT(*) as usage_count
FROM predictions
GROUP BY prompt_version
```

---

## Yapılacaklar (TODO)

- [ ] Multi-language prompt'lar (İngilizce, İspanyolca)
- [ ] Real-time pitch data entegrasyonu
- [ ] Injury/suspension data ekleme
- [ ] Head-to-head history analizi
- [ ] Weather factor ekleme
- [ ] Prompt A/B testing dashboard
- [ ] Automatic prompt optimization (feedback loop)

---

**Son Güncelleme:** 13 Nov 2025
**Bakım Eden:** AI Predictions Team
**Versiyon:** 2.0
